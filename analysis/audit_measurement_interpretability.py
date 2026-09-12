from __future__ import annotations

import argparse, json, math
from pathlib import Path

import numpy as np
import pandas as pd

LOCKED_QATAR = pd.DataFrame([
    ('TOPCon-M2',  0.727,  0.733),
    ('SHJ-M1',    -3.386, -3.423),
    ('TOPCon-M3', -0.661, -0.676),
    ('PERC-M-M4',  0.040,  0.037),
    ('PERC-M3',   -0.409, -0.408),
    ('PERC-C-M4', -0.890, -0.896),
    ('SHJ-M5',    -3.003, -3.016),
], columns=['configuration','signal_pp','ror_pct'])


def parse_vector(x):
    if pd.isna(x): return None
    vals=[]
    for t in str(x).strip().strip('[]').split(','):
        t=t.strip()
        if not t: continue
        try: vals.append(float(t))
        except Exception: return None
    return np.asarray(vals,float) if vals else None


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output-dir',default='results/duramat_best/measurement_audit'); args=ap.parse_args()
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.input); df['measdatetime']=pd.to_datetime(df['measdatetime'],errors='coerce'); df['year']=df['measdatetime'].dt.year

    # 1) Session-span audit: year-level grouping is not automatically a technical replicate group.
    g=(df.dropna(subset=['measdatetime']).groupby(['nrel_id','Side','tracer','year'],dropna=False)
       .agg(n=('measdatetime','size'),first=('measdatetime','min'),last=('measdatetime','max'),
            temp_min=('module_temp_pre','min'),temp_max=('module_temp_pre','max'),
            pmax_min=('tracer_pmax','min'),pmax_max=('tracer_pmax','max'),pmax_median=('tracer_pmax','median')).reset_index())
    g['span_minutes']=(g['last']-g['first']).dt.total_seconds()/60.0
    g['span_days']=g['span_minutes']/1440.0
    g['technical_same_day_candidate']=g['span_minutes'].le(24*60)
    g.to_csv(out/'session_span_audit.csv',index=False)

    # 2) I-V export consistency: sampled max(I*V) versus tracer_pmax. This is not an STC correction.
    iv=[]
    for idx,r in df.iterrows():
        I=parse_vector(r.get('I')); V=parse_vector(r.get('V'))
        sampled=np.nan; rel=np.nan; n=0
        if I is not None and V is not None and len(I)==len(V) and len(I)>0:
            n=len(I); sampled=float(np.nanmax(I*V)); tp=float(r['tracer_pmax']) if pd.notna(r['tracer_pmax']) else np.nan
            if np.isfinite(tp) and tp!=0: rel=100.0*(sampled-tp)/tp
        iv.append({'row':idx,'nrel_id':r.get('nrel_id'),'Side':r.get('Side'),'tracer':r.get('tracer'),'measdatetime':r.get('measdatetime'),
                   'n_iv_samples':n,'sampled_max_iv_w':sampled,'tracer_pmax_w':r.get('tracer_pmax'),'sampled_minus_tracer_pct':rel})
    iv=pd.DataFrame(iv); iv.to_csv(out/'iv_export_consistency_audit.csv',index=False)

    # 3) Conditional interpretability frontier for locked Qatar RoR sensitivity.
    q=LOCKED_QATAR.copy(); q['r_obs_log']=np.log1p(q['ror_pct']/100.0); q['abs_log_signal']=q['r_obs_log'].abs()
    q['equiv_one_sided_pct_change']=100.0*(np.exp(q['abs_log_signal'])-1.0)
    q['interpretation']='If |d_control| + |eta| is bounded strictly below abs_log_signal (plus any separately handled sampling uncertainty), the sign of d_field is preserved under the stated log-ratio measurement model.'
    q.to_csv(out/'measurement_interpretability_frontier.csv',index=False)

    # Worst-case symmetric per-configuration bound that still guarantees SHJ-M1 remains more negative than SHJ-M5.
    m1=float(q.loc[q.configuration.eq('SHJ-M1'),'r_obs_log'].iloc[0]); m5=float(q.loc[q.configuration.eq('SHJ-M5'),'r_obs_log'].iloc[0])
    gap=abs(m1-m5); h=gap/2.0
    ranking={'pair':['SHJ-M1','SHJ-M5'],'observed_log_gap':gap,'max_equal_independent_abs_bound_each_for_guaranteed_order_strictly_less_than':h,
             'equiv_pct_change_each':100.0*(math.exp(h)-1.0),
             'assumption':'Worst-case independent signed combined control-drift plus differential-measurement bound of equal magnitude for each configuration. A common-mode component shared exactly between configurations would cancel differently and is not represented by this worst-case bound.'}
    Path(out/'shj_followup_order_bound.json').write_text(json.dumps(ranking,indent=2))

    summary={
      'source_rows':int(len(df)),
      'corrected_endpoint_populated':int(df['Pmax_VTIF_Corr'].notna().sum()) if 'Pmax_VTIF_Corr' in df else None,
      'correction_factor_populated':int(df['Correction Factor'].notna().sum()) if 'Correction Factor' in df else None,
      'iv_rows_valid':int(iv['sampled_minus_tracer_pct'].notna().sum()),
      'iv_rel_diff_pct_median':float(iv['sampled_minus_tracer_pct'].median()),
      'iv_rel_diff_pct_p95_abs':float(iv['sampled_minus_tracer_pct'].abs().quantile(.95)),
      'iv_rel_diff_pct_max_abs':float(iv['sampled_minus_tracer_pct'].abs().max()),
      'year_instrument_side_groups':int(len(g)),
      'groups_spanning_more_than_one_day':int((g['span_days']>1).sum()),
      'max_group_span_days':float(g['span_days'].max()),
      'claim_boundary':'These audits do not estimate degradation, do not reconstruct Pmax_VTIF_Corr, and do not isolate causal instrument effects. The frontier is conditional sensitivity, not a confidence interval or measured uncertainty budget.'
    }
    Path(out/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2))
    note=f'''# Measurement-Interpretability Audit\n\n- Public DuraMAT rows: **{summary['source_rows']}**.\n- Frozen corrected endpoint populated: **{summary['corrected_endpoint_populated']}/{summary['source_rows']}**.\n- Valid raw I-V exports checked: **{summary['iv_rows_valid']}**; median sampled-max(I×V) minus tracer_pmax = **{summary['iv_rel_diff_pct_median']:.4f}%**, 95th percentile absolute difference = **{summary['iv_rel_diff_pct_p95_abs']:.4f}%**, maximum absolute difference = **{summary['iv_rel_diff_pct_max_abs']:.4f}%**. This is an export-consistency check only.\n- Year/instrument/side groups spanning >1 day: **{summary['groups_spanning_more_than_one_day']}**; maximum span = **{summary['max_group_span_days']:.1f} days**. Such groups must not automatically be called technical replicates.\n- Under the stated log-ratio sensitivity model, the SHJ-M1 versus SHJ-M5 observed log gap is **{gap:.6f}**. If each configuration can have an independent worst-case combined signed bound of equal magnitude, guaranteed preservation of their order requires each bound to be strictly below **{h:.6f}** (about **{ranking['equiv_pct_change_each']:.3f}%** in equivalent multiplicative change). This is conditional sensitivity, not measured uncertainty.\n\nNo Qatar gate, signal, or degradation claim is changed by this audit.\n'''
    Path(out/'MEASUREMENT_INTERPRETABILITY_NOTE.md').write_text(note)
    print(json.dumps(summary,indent=2)); print(json.dumps(ranking,indent=2))

if __name__=='__main__': main()
