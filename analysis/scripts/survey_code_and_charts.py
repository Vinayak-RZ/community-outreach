import pandas as pd, json, os, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
W='/workspace/library/acads/community-outreach'; O=W+'/analysis-work/out'
df=pd.read_pickle(O+'/df.pkl'); raw=pd.read_excel(W+'/source/survey/survey-responses.xlsx')
n=len(df)
# hand codes (rows = sheet rows)
REMOVE_SOLE=[12,13,17,25,38,51,57,72,84,93,159,162,193,196,197,210]
REMOVE_OPTION=[20,23,27,58,60,69,143,146,156,186]
REMOVE_AGGR=[31,80,96,127,138]
B_OTHER={51:'Remove from campus (free text)',93:'Remove from campus (free text)',196:'Remove from campus (free text)',197:'Remove from campus (free text)',201:'Remove from campus (free text)',
 13:'Restriction (free text)',37:'Restriction (free text)',125:'Restriction (free text)',80:'Unclear',83:'Unclear',112:'Unclear'}
df['boundary_recoded']=df.boundary_coded
for r,v in B_OTHER.items(): df.loc[df.sheet_row==r,'boundary_recoded']=v
assert (df.boundary_recoded=='Other (free text)').sum()==0
df['text_removal_stance']=''
df.loc[df.sheet_row.isin(REMOVE_SOLE),'text_removal_stance']='remove all/most (sole proposal)'
df.loc[df.sheet_row.isin(REMOVE_OPTION),'text_removal_stance']='remove as one option / ideal'
df.loc[df.sheet_row.isin(REMOVE_AGGR),'text_removal_stance']='remove only aggressive dogs/packs'
df.loc[df.fair_solution.notna()&(df.text_removal_stance==''),'text_removal_stance']='no removal proposed'
S={'boundary_recoded':df.boundary_recoded.value_counts().to_dict(),'text_stance':df.loc[df.fair_solution.notna(),'text_removal_stance'].value_counts().to_dict()}
print(S)
# exports
os.makedirs(W+'/source/survey',exist_ok=True)
full=raw.copy(); full.insert(0,'sheet_row',range(2,n+2)); full.to_csv(W+'/source/survey/survey-responses.csv',index=False)
deid=df[['sheet_row','timestamp','dept','role','experience','problems','reason_place','boundary','aware_ccf_sterilisation','problem_rating','fair_solution','boundary_recoded','text_removal_stance']].copy()
deid.loc[deid.sheet_row==83,'boundary']='[room number redacted]'
deid.columns=['sheet_row','timestamp','dept_from_email','I am a','How would you describe your experience with campus dogs?','What problems have you personally experienced because of campus dogs?','What is the strongest reason you believe dogs have a place in the campus community?','Where should the boundary between dogs and student spaces lie?','Are you aware of any organized sterilization or the CCF committee in campus?','On a scale of 1–5, how much of a problem do you consider campus dogs to currently be?','What would a fair solution look like for both students and dogs?','[coded] boundary_recoded','[coded] text_removal_stance']
os.makedirs(W+'/analysis-work/repo-survey',exist_ok=True)
deid.to_csv(W+'/analysis-work/repo-survey/survey-responses.csv',index=False)
deid.to_excel(W+'/analysis-work/repo-survey/survey-responses.xlsx',index=False)
df.to_pickle(O+'/df2.pkl'); json.dump(S,open(O+'/stats2.json','w'),indent=1)
# ---------- figures ----------
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures')  # poster style: ink + one accent + greys; os.makedirs(F,exist_ok=True)
plt.rcParams.update({'font.size':20,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':26,'axes.titleweight':'normal','text.color':'#1A1A1A','axes.edgecolor':'#9A9A9A','ytick.color':'#1A1A1A'})
SRC=f'Source: group 23 campus-dogs survey, IIT Roorkee, 13–17 Oct 2026 (n = {n})'
INK,ACC,G1,G2,G3='#1A1A1A','#3D7A8C','#4D4D4D','#9A9A9A','#D9D9D9'
RED,GREY,GREEN,AMBER,BLUE=ACC,G3,G2,G2,ACC
def hbar(labels,counts,colors,title,fname,denom=n,sub=None):
    fig,ax=plt.subplots(figsize=(14,1.25*len(labels)+2.4))
    y=range(len(labels))[::-1]
    ax.barh(list(y),counts,color=colors,height=0.65)
    ax.set_yticks(list(y)); ax.set_yticklabels(labels)
    m=max(counts)
    for yi,c in zip(y,counts): ax.text(c+m*0.01,yi,f'{c}  ({100*c/denom:.0f}%)',va='center',fontsize=20)
    ax.set_xlim(0,m*1.28); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
    fig.suptitle(title,x=0.01,ha='left',fontsize=26,fontweight='normal')
    fig.text(0.01,0.01,(sub+'\n' if sub else '')+SRC,fontsize=13,color='#8A8A8A')
    fig.tight_layout(rect=(0,0.06 if sub else 0.04,1,0.95)); fig.savefig(F+'/'+fname,dpi=300); plt.close(fig)
ex=['Mostly negative','Both positive and negative','Neutral / Rarely interact','Mostly positive']
hbar(ex,[int((df.experience==e).sum()) for e in ex],[RED,AMBER,GREY,GREEN],'How would you describe your experience with campus dogs?','fig1_experience.png')
P=['Dogs entering hostels/buildings','Feeling unsafe or being chased','Noise or dog fights','Hygiene/waste','No significant problems']
hbar(P,[int(df['prob: '+p].sum()) for p in P],[RED,RED,RED,RED,GREY],'Problems people have personally experienced','fig2_problems.png',sub='Multiple answers allowed; % of all respondents')
B=['Restricted from hostels/buildings','Restricted to designated areas','Allowed only if vaccinated/sterilized','Free movement across campus','Remove from campus']
bc=[int((df.boundary_recoded==b).sum()) for b in B]
bc[-1]+=int((df.boundary_recoded=='Remove from campus (free text)').sum())
oth=int(df.boundary_recoded.isin(['Restriction (free text)','Unclear']).sum())
hbar(B[:-1]+['Remove from campus (typed)','Other (free text)'],bc+[oth],[BLUE,BLUE,BLUE,G2,G1,GREY],'Where should the boundary between dogs and students lie?','fig3_boundary.png',sub='"Remove from campus" was NOT a listed option: all 7 were typed into "Other". Remaining "Other" = 3 restriction + 3 unclear')
# fig4 rating by chased (100% stacked)
fig,ax=plt.subplots(figsize=(14,5.8))
cols=['#E6E6E6','#CCCCCC','#9A9A9A','#6FA3B2','#3D7A8C']
groups=[('Felt unsafe / chased',True),('Did not report it',False)]
for i,(lab,v) in enumerate(groups):
    sub=df[df['prob: Feeling unsafe or being chased']==v]; left=0
    for k in range(1,6):
        c=int((sub.problem_rating==k).sum()); w=100*c/len(sub)
        ax.barh(i,w,left=left,color=cols[k-1],height=0.6,label=str(k) if i==0 else None)
        if w>=6: ax.text(left+w/2,i,f'{w:.0f}%',ha='center',va='center',fontsize=18,color='white' if k==5 else '#1A1A1A')
        left+=w
    ax.text(101,i,f'n={len(sub)}',va='center',fontsize=18)
ax.set_yticks([0,1]); ax.set_yticklabels([g[0] for g in groups]); ax.invert_yaxis()
ax.set_xlim(0,112); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
fig.suptitle('"How much of a problem are campus dogs?" (rated 1–5)',x=0.01,ha='left',fontsize=26,fontweight='normal')
ax.legend(title='Rating',ncol=5,loc='upper center',bbox_to_anchor=(0.45,-0.02),frameon=False,fontsize=17,title_fontsize=17)
fig.text(0.01,0.01,'Split by whether the respondent ticked "Feeling unsafe or being chased"; 1 = No problem, 5 = Serious problem (form labels)\n'+SRC,fontsize=13,color='#8A8A8A'); fig.tight_layout(rect=(0,0.07,1,0.95)); fig.savefig(F+'/fig4_rating_by_chased.png',dpi=300); plt.close(fig)
# fig5 awareness by experience
fig,ax=plt.subplots(figsize=(14,6.5))
labs=ex+['All respondents']
for i,e in enumerate(labs):
    sub=df if e=='All respondents' else df[df.experience==e]
    y=int((sub.aware_ccf_sterilisation=='Yes').sum()); w=100*y/len(sub)
    ax.barh(i,w,color=BLUE,height=0.6); ax.barh(i,100-w,left=w,color='#E6E6E6',height=0.6)
    ax.text(w+1,i,f'{w:.0f}% aware  ({y}/{len(sub)})',va='center',fontsize=18)
ax.set_yticks(range(len(labs))); ax.set_yticklabels(labs); ax.invert_yaxis(); ax.set_xlim(0,100); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
fig.suptitle('Aware of organised sterilisation or the CCF committee?',x=0.01,ha='left',fontsize=26,fontweight='normal')
fig.text(0.01,0.01,'Grouped by self-described experience with campus dogs\n'+SRC,fontsize=13,color='#8A8A8A'); fig.tight_layout(rect=(0,0.07,1,0.94)); fig.savefig(F+'/fig5_awareness_by_experience.png',dpi=300); plt.close(fig)
R=['They deserve humane treatment','They can coexist with humans','Caring for animals is our responsibility','They are part of campus life','They provide companionship']
hbar(R,[int((df.reason_place==r).sum()) for r in R],[GREEN]*5,'Strongest reason dogs have a place on campus','fig6_reason_place.png',sub='Single choice; 1 blank answer')
print(os.listdir(F))
