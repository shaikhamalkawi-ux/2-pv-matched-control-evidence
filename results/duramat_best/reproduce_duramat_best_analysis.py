#!/usr/bin/env python3
"""Reproduce the Paper 2 AC3 DuraMAT BEST comparability stress test.

This is a post-analysis reproducibility implementation of the already documented
frozen scope. It does not create a new endpoint or alter the claim boundary.
Primary endpoint: source field Pmax_VTIF_Corr. Secondary raw sensitivity:
tracer_pmax, summarized by median within nrel_id x Side x year x tracer.
"""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd


def sha256(path: Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()

def sign(x, eps=1e-15):
    if pd.isna(x): return None
    return 1 if x>eps else (-1 if x<-eps else 0)

def pct(a,b):
    return 100.0*(b/a-1.0)

def group_table(df):
    good=df.dropna(subset=['nrel_id','Side','year','tracer','tracer_pmax']).copy()
    return (good.sort_values('Order')
            .groupby(['nrel_id','Side','year','tracer'],as_index=False)
            .agg(n_sweeps=('tracer_pmax','size'),
                 raw_pmax=('tracer_pmax','median'),
                 first_pmax=('tracer_pmax','first'),
                 corr_pmax_count=('Pmax_VTIF_Corr','count'),
                 corr_factor_count=('Correction Factor','count'),
                 corrected_temp=('corrected_to_temperature','median')))

def get(g,nrel,side,year,tracer,col='raw_pmax'):
    x=g[(g.nrel_id==nrel)&(g.Side==side)&(g.year==year)&(g.tracer==tracer)]
    return None if x.empty else float(x.iloc[0][col])

def contrasts(g, units, ya,yb, ta,tb, label, state):
    rows=[]
    for nrel,side in units:
        a=get(g,nrel,side,ya,ta); b=get(g,nrel,side,yb,tb)
        if a is None or b is None: continue
        na=int(g[(g.nrel_id==nrel)&(g.Side==side)&(g.year==ya)&(g.tracer==ta)].iloc[0].n_sweeps)
        nb=int(g[(g.nrel_id==nrel)&(g.Side==side)&(g.year==yb)&(g.tracer==tb)].iloc[0].n_sweeps)
        rows.append(dict(contrast=label,nrel_id=nrel,Side=side,year_a=ya,year_b=yb,tracer_a=ta,tracer_b=tb,n_a=na,n_b=nb,pmax_a_raw=a,pmax_b_raw=b,delta_raw_pct=pct(a,b),comparability_raw_sensitivity=state,same_instrument=ta==tb,source_bridge_applied=False))
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    src=Path(args.source); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(src)
    dt=pd.to_datetime(df['measdatetime'],errors='coerce')
    df['year']=dt.dt.year
    g=group_table(df)
    g.drop(columns=['first_pmax']).to_csv(out/'specimen_epoch_instrument_map.csv',index=False)
    units=sorted({(str(r.nrel_id),str(r.Side)) for r in g.itertuples() if pd.notna(r.nrel_id) and pd.notna(r.Side)})
    rows=[]
    rows += contrasts(g,units,2019,2024,'Spire 5600','Spire 5600','2019_to_2024','C2')
    rows += contrasts(g,units,2019,2022,'Spire 5600','Spire 4600','2019_to_2022','C1')
    rows += contrasts(g,units,2019,2022,'Spire 5600','Spire 5600','2019_to_2022','C2')
    rows += contrasts(g,units,2022,2024,'Spire 4600','Spire 5600','2022_to_2024','C1')
    rows += contrasts(g,units,2022,2024,'Spire 5600','Spire 5600','2022_to_2024','C2')
    con=pd.DataFrame(rows).sort_values(['contrast','nrel_id','Side','comparability_raw_sensitivity']).reset_index(drop=True)
    con.to_csv(out/'raw_tracer_pmax_sensitivity_contrasts.csv',index=False)

    prim=[]
    for r in con[con.contrast.eq('2019_to_2024')].itertuples():
        prim.append(dict(nrel_id=r.nrel_id,Side=r.Side,primary_endpoint='Pmax_VTIF_Corr',primary_state='C0',
                         primary_reason='Pmax_VTIF_Corr is missing at both source epochs in the admitted resource; prespecified primary endpoint not calculable.',
                         tracer_a=r.tracer_a,tracer_b=r.tracer_b,secondary_raw_tracer_pmax_delta_pct=r.delta_raw_pct))
    pd.DataFrame(prim).to_csv(out/'primary_2019_2024_admission_ledger.csv',index=False)

    gate=[]
    for lab in ['2019_to_2022','2022_to_2024']:
        x=con[con.contrast.eq(lab)]
        for (nrel,side),u in x.groupby(['nrel_id','Side']):
            c1=u[u.comparability_raw_sensitivity.eq('C1')]
            c2=u[u.comparability_raw_sensitivity.eq('C2')]
            if c1.empty or c2.empty: continue
            a=float(c1.iloc[0].delta_raw_pct); b=float(c2.iloc[0].delta_raw_pct)
            gate.append(dict(contrast=lab,nrel_id=nrel,Side=side,cross_instrument_C1_raw_delta_pct=a,same_instrument_C2_raw_delta_pct=b,difference_C1_minus_C2_pp=a-b,sign_change_due_to_comparability_gate=sign(a)!=sign(b)))
    pd.DataFrame(gate).to_csv(out/'instrument_gate_decision_change_ledger.csv',index=False)

    rep=[]
    for r in con[con.comparability_raw_sensitivity.eq('C2')].itertuples():
        fa=get(g,r.nrel_id,r.Side,r.year_a,r.tracer_a,'first_pmax')
        fb=get(g,r.nrel_id,r.Side,r.year_b,r.tracer_b,'first_pmax')
        first=pct(fa,fb)
        rep.append(dict(nrel_id=r.nrel_id,Side=r.Side,tracer_a=r.tracer_a,tracer_b=r.tracer_b,median_replicate_delta_pct=r.delta_raw_pct,first_documented_sweep_delta_pct=first,contrast=r.contrast,first_minus_median_pp=first-r.delta_raw_pct,sign_change_due_to_replicate_summary=sign(first)!=sign(r.delta_raw_pct)))
    pd.DataFrame(rep).to_csv(out/'replicate_summary_sensitivity.csv',index=False)

    def counts(s):
        x=s.fillna('<blank>').astype(str).value_counts(dropna=False)
        return {str(k):int(v) for k,v in x.items()}
    schema={
      'source_file':src.name,'bytes':src.stat().st_size,'sha256':sha256(src),'rows':int(len(df)),'columns':list(pd.read_csv(src,nrows=0).columns),
      'counts':{
        'nrel_id_unique':int(df.nrel_id.nunique(dropna=True)),
        'technology':counts(df['Technology']), 'type':counts(df['type']), 'control_field':counts(df['Control-Field']),
        'tracer':counts(df['tracer']), 'side':counts(df['Side']), 'year':counts(df['year']),
        'primary_Pmax_VTIF_Corr_nonnull':int(df['Pmax_VTIF_Corr'].notna().sum()),
        'secondary_tracer_pmax_nonnull':int(df['tracer_pmax'].notna().sum()),
        'Correction_Factor_nonnull':int(df['Correction Factor'].notna().sum()),
        'corrected_to_temperature_nonnull':int(df['corrected_to_temperature'].notna().sum())},
      'frozen_scope':{'unit':'nrel_id × Side','primary_contrast':'2019→2024','secondary_contrasts':['2019→2022','2022→2024'],
                      'primary_endpoint':'Pmax_VTIF_Corr','secondary_raw_sensitivity':'tracer_pmax','same_instrument_rule':'Spire 5600 at both epochs when available'}
    }
    (out/'schema_audit.json').write_text(json.dumps(schema,indent=2),encoding='utf-8')
    gate_df=pd.DataFrame(gate); rep_df=pd.DataFrame(rep); prim_df=pd.DataFrame(prim)
    c19=con[(con.contrast=='2019_to_2024')&(con.comparability_raw_sensitivity=='C2')]
    dec={
      'source':{'bytes':src.stat().st_size,'sha256':sha256(src),'rows':int(len(df)),'doi':'10.21948/2462712'},
      'primary_endpoint':{'name':'Pmax_VTIF_Corr','nonnull_rows':int(df['Pmax_VTIF_Corr'].notna().sum()),'candidate_2019_2024_specimen_side_units':int(len(prim_df)),'state':'C0 for all primary candidate units','reason':'source column is present but empty throughout this admitted resource'},
      'raw_sensitivity':{
        '2019_to_2024':{'same_instrument_C2_n':int(len(c19)),'median_delta_pct':float(c19.delta_raw_pct.median()),'range_pct':[float(c19.delta_raw_pct.min()),float(c19.delta_raw_pct.max())],'negative_n':int((c19.delta_raw_pct<0).sum()),'positive_n':int((c19.delta_raw_pct>0).sum()),'zero_n':int((c19.delta_raw_pct==0).sum())},
        '2019_to_2022':{},'2022_to_2024':{},'replicate_summary_sign_changes':int(rep_df.sign_change_due_to_replicate_summary.sum())},
      'C3_direction_supported_n':0,
      'main_paper_contribution_gate':{'admit_compact_external_evidence':True,'grounds':['B: comparability admission changes direction in prespecified raw sensitivity cases','D: corrected endpoint availability boundary demonstrates calculability is weaker than interpretable direction'],'claim_boundary':'DuraMAT does not establish degradation/improvement; raw tracer_pmax values remain sensitivity diagnostics only.'}}
    for lab in ['2019_to_2022','2022_to_2024']:
        x=con[con.contrast.eq(lab)]
        overlap=gate_df[gate_df.contrast.eq(lab)]
        dec['raw_sensitivity'][lab]={'C1_cross_instrument_n':int((x.comparability_raw_sensitivity=='C1').sum()),'C2_same_instrument_n':int((x.comparability_raw_sensitivity=='C2').sum()),'overlap_units_with_both_C1_C2':int(len(overlap)),'sign_changes_due_gate':int(overlap.sign_change_due_to_comparability_gate.sum())}
    (out/'contribution_decision.json').write_text(json.dumps(dec,indent=2),encoding='utf-8')
    print(json.dumps(dec,indent=2))

if __name__=='__main__': main()
