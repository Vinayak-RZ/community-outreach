import pandas as pd, numpy as np, json, re, os
SRC='/workspace/library/acads/community-outreach/source/survey/survey-responses.xlsx'
OUT='/workspace/library/acads/community-outreach/analysis-work/out'; os.makedirs(OUT,exist_ok=True)
raw=pd.read_excel(SRC)
cols=list(raw.columns)
short=['timestamp','email','role','experience','problems','reason_place','boundary','aware_ccf_sterilisation','problem_rating','fair_solution']
df=raw.copy(); df.columns=short
df.insert(0,'sheet_row',range(2,len(df)+2))
df['dept']=df.email.str.split('@').str[1].str.replace('.iitr.ac.in','',regex=False)
df.loc[df.dept.isin(['gmail.com','googlemail.com']),'dept']='(personal email)'
df['dept']=df.dept.fillna('(no email)')
PROB=['Dogs entering hostels/buildings','Feeling unsafe or being chased','Noise or dog fights','Hygiene/waste','No significant problems']
toks=df.problems.str.split(', ')
other_tok=sorted(set(t for l in toks for t in l)-set(PROB))
for p in PROB: df['prob: '+p]=toks.apply(lambda l:p in l)
df['n_problems']=toks.apply(lambda l:len([t for t in l if t!='No significant problems']))
BOUND=['Restricted from hostels/buildings','Restricted to designated areas','Allowed only if vaccinated/sterilized','Free movement across campus','Remove from campus']
df['boundary_coded']=df.boundary.where(df.boundary.isin(BOUND),'Other (free text)')
R={}
n=len(df); R['n']=n
R['dates']=df.timestamp.dt.date.astype(str).value_counts().sort_index().to_dict()
R['ts_min']=str(df.timestamp.min()); R['ts_max']=str(df.timestamp.max())
R['email_null']=int(df.email.isna().sum()); R['email_unique']=int(df.email.nunique())
R['dup_answer_patterns']=int(df.duplicated(subset=short[2:]).sum())
R['dup_answer_patterns_excl_text']=int(df.duplicated(subset=short[2:9]).sum())
R['other_problem_tokens']=other_tok
R['none_plus_problem']=int((df['prob: No significant problems']&(df.n_problems>0)).sum())
def vc(s): v=s.value_counts(dropna=False); return {str(k):[int(c),round(100*c/n,1)] for k,c in v.items()}
for c in ['role','experience','reason_place','boundary_coded','aware_ccf_sterilisation','problem_rating','dept']:
    R[c]=vc(df[c])
R['boundary_other_text']=df.loc[df.boundary_coded=='Other (free text)',['sheet_row','boundary']].values.tolist()
R['problems_tokens']={p:[int(df['prob: '+p].sum()),round(100*df['prob: '+p].mean(),1)] for p in PROB}
R['n_problems_dist']={int(k):int(v) for k,v in df.n_problems.value_counts().sort_index().items()}
R['all_four']=int((df.n_problems==4).sum())
R['rating_mean']=round(df.problem_rating.mean(),2); R['rating_median']=float(df.problem_rating.median())
R['rating_4_5']=int((df.problem_rating>=4).sum()); R['rating_1_2']=int((df.problem_rating<=2).sum())
R['reason_place_null_rows']=df.loc[df.reason_place.isna(),'sheet_row'].tolist()
R['fair_solution_n']=int(df.fair_solution.notna().sum())
# crosstabs
def ct(a,b,norm=None):
    t=pd.crosstab(df[a],df[b],margins=True)
    return t
EXP=['Mostly negative','Both positive and negative','Neutral / Rarely interact','Mostly positive']
cts={}
cts['experience_x_boundary']=pd.crosstab(df.experience,df.boundary_coded,margins=True).reindex(EXP+['All'])
cts['experience_x_rating']=pd.crosstab(df.experience,df.problem_rating,margins=True).reindex(EXP+['All'])
cts['experience_x_aware']=pd.crosstab(df.experience,df.aware_ccf_sterilisation,margins=True).reindex(EXP+['All'])
cts['chased_x_boundary']=pd.crosstab(df['prob: Feeling unsafe or being chased'],df.boundary_coded,margins=True)
cts['chased_x_rating']=pd.crosstab(df['prob: Feeling unsafe or being chased'],df.problem_rating,margins=True)
cts['aware_x_rating']=pd.crosstab(df.aware_ccf_sterilisation,df.problem_rating,margins=True)
cts['aware_x_boundary']=pd.crosstab(df.aware_ccf_sterilisation,df.boundary_coded,margins=True)
cts['experience_x_reason']=pd.crosstab(df.experience,df.reason_place,margins=True).reindex(EXP+['All'])
cts['experience_x_problems']=df.groupby('experience')[['prob: '+p for p in PROB]].sum().reindex(EXP)
cts['experience_x_problems']['n']=df.experience.value_counts().reindex(EXP)
R['mean_rating_by_exp']=df.groupby('experience').problem_rating.mean().round(2).reindex(EXP).to_dict()
R['mean_rating_by_chased']={str(k):round(v,2) for k,v in df.groupby('prob: Feeling unsafe or being chased').problem_rating.mean().items()}
R['mean_rating_by_aware']=df.groupby('aware_ccf_sterilisation').problem_rating.mean().round(2).to_dict()
# consensus: any restriction short of removal
R['restrict_not_remove']=int(df.boundary_coded.isin(BOUND[:3]).sum())
R['remove_structured']=int((df.boundary_coded=='Remove from campus').sum())
R['free']=int((df.boundary_coded=='Free movement across campus').sum())
# free text themes (keyword coded, case-insensitive)
TH={
 'Remove dogs from campus (all/most)':r'\bremov|throw them out|kick|nikal|not be allowed inside campus|no dogs|don\'?t allow (stray )?dogs|do not allow them|dont allow dogs at all|outside the campus|out of campus|clear the dogs|shouldn\'?t be present|should not be there',
 'Keep out of hostels/buildings':r'hostel|bhawan|room|mess|canteen|building',
 'Designated areas / shelter / park':r'designated|shelter|separate place|specific area|special area|certain areas|park|sanctuary|zone away|constrained places|proper place|particular',
 'Vaccination':r'vaccin',
 'Sterilisation / neutering':r'steril|neuter|streil',
 'Feeding zones / regular feeding':r'feed|meal|food',
 'Reduce numbers / overpopulation':r'reduce|decrease|too many|too much|number|overpopulat|few number',
 'Remove only aggressive dogs/packs':r'aggress|violent|vicious|groups? (should|really)|disband',
 'Guards / security / hotline':r'guard|watchman|security|hotline|reporting|team ready',
 'Awareness / training / workshop':r'awareness|aware|workshop|training|teach|understand about',
 'Hygiene / waste / garbage':r'hygien|garbage|waste|dustbin|bins|poop|pee|lick|sanitary',
 'Mentions being chased / bitten':r'chase|bitten|bite|biting',
 'Tech (app, collar, tracking)':r'\bapp\b|collar|scan|tracking|dashboard|channeli',
}
ft=df[df.fair_solution.notna()][['sheet_row','fair_solution','experience']].copy()
for k,p in TH.items(): ft[k]=ft.fair_solution.str.contains(p,case=False,regex=True)
R['themes']={k:[int(ft[k].sum()),round(100*ft[k].mean(),1)] for k in TH}
R['theme_rows']={k:ft.loc[ft[k],'sheet_row'].tolist() for k in TH}
R['fair_by_exp']=ft.experience.value_counts().to_dict()
json.dump(R,open(f'{OUT}/stats.json','w'),indent=1,default=str)
with open(f'{OUT}/crosstabs.md','w') as f:
    for k,t in cts.items(): f.write(f'### {k}\n\n'+t.to_markdown()+'\n\n')
df.to_pickle(f'{OUT}/df.pkl'); ft.to_pickle(f'{OUT}/ft.pkl')
print(json.dumps({k:v for k,v in R.items() if k not in('theme_rows','boundary_other_text')},indent=0,default=str))
print(open(f'{OUT}/crosstabs.md').read())
