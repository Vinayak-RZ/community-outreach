const INK='#1A1A1A',ACC='#3D7A8C',ACCL='#A9C8D1',G1='#4D4D4D',G2='#8A8A8A',G3='#D9D9D9',G4='#EEEEEE';
const P=c=>[figma.util.solidPaint(c)]; const F=s=>({family:'Inter',style:s});
for (const s of ['Regular','Medium','Semi Bold','Bold']) await figma.loadFontAsync(F(s));
const poster=await figma.getNodeByIdAsync('5:1991');
const base=await figma.getNodeByIdAsync('12:2'); figma.currentPage.appendChild(base);
for (const c of [...poster.children]) c.remove();
for (const n of figma.currentPage.children.filter(n=>n.name==='OSM base (© OpenStreetMap contributors)'&&n.parent.type==='PAGE')) n.remove();
const W=3508,M=180,CW=W-2*M,GAP=96; const col=n=>Math.round(n*(CW-11*GAP)/12+(n-1)*GAP);
const T=(s,o={})=>{const t=figma.createText(); t.fontName=F(o.st||'Regular'); t.characters=s; t.fontSize=o.sz||44; t.fills=P(o.c||INK); t.lineHeight={value:o.lh||122,unit:'PERCENT'}; if(o.ls) t.letterSpacing={value:o.ls,unit:'PERCENT'}; if(o.al) t.textAlignHorizontal=o.al; if(o.w){t.resize(o.w,10); t.textAutoResize='HEIGHT';} else t.textAutoResize='WIDTH_AND_HEIGHT'; if(o.x!=null){t.x=o.x;t.y=o.y;} return t;};
const AL=(dir,kids,o={})=>{const f=figma.createFrame(); f.fills=[]; f.layoutMode=dir; f.itemSpacing=o.sp??20; f.clipsContent=false; if(o.w){f.resize(o.w,10); f.counterAxisSizingMode=dir==='VERTICAL'?'FIXED':'AUTO'; f.primaryAxisSizingMode=dir==='VERTICAL'?'AUTO':'FIXED';} else {f.primaryAxisSizingMode='AUTO'; f.counterAxisSizingMode='AUTO';} if(o.ca) f.counterAxisAlignItems=o.ca; if(o.pa) f.primaryAxisAlignItems=o.pa; if(o.name) f.name=o.name; for(const k of kids) f.appendChild(k); return f;};
const V=(k,o)=>AL('VERTICAL',k,o), H=(k,o)=>AL('HORIZONTAL',k,o);
const R=(w,h,c,o={})=>{const r=figma.createRectangle(); r.resize(Math.max(w,0.01),h); r.fills=c?P(c):[]; if(o.x!=null){r.x=o.x;r.y=o.y;} if(o.r) r.cornerRadius=o.r; if(o.stroke){r.strokes=P(o.stroke); r.strokeWeight=o.sw||2;} return r;};
const E=(x,y,d,c,o={})=>{const e=figma.createEllipse(); e.resize(d,d); e.x=x-d/2; e.y=y-d/2; e.fills=c?P(c):[]; if(o.stroke){e.strokes=P(o.stroke); e.strokeWeight=o.sw||3;} if(o.op) e.opacity=o.op; return e;};
const box=(w,h,kids,name)=>{const f=figma.createFrame(); f.resize(w,h); f.fills=[]; f.clipsContent=false; if(name) f.name=name; for(const k of kids) f.appendChild(k); return f;};
const lab=s=>T(s.toUpperCase(),{sz:34,st:'Semi Bold',c:G2,ls:8});
const sec=(title,w,kids,sp=24)=>V([R(w,4,INK),lab(title),...kids],{w,sp});
const cap=(s,w,o={})=>T(s,Object.assign({w,sz:40,c:G1},o));

// HEADER
const header=V([T('EEC 399 Community Outreach  ·  Group 23  ·  Topic 3  ·  Dept. of Electrical Engineering, IIT Roorkee  ·  Autumn 2026',{sz:38,c:G2}),
 T('Campus dogs: two sides of one street',{sz:158,st:'Bold',lh:105,ls:-2}),
 T('Most people we asked want the dogs to stay, as long as they stay out of the hostels.',{sz:76,st:'Medium',c:ACC,lh:120,w:CW})],{w:CW,sp:26});

// FIELDWORK: numbers + timeline
const S=[['211','survey responses'],['36','interviews we recorded'],['37+','people on record'],['6','groups we spoke to'],['3.95','hours of audio and video'],['80','recordings transcribed'],['6','days in the field'],['72','files on our team Drive'],['566','messages in our team chat']];
const stats=H(S.map(([n,l],i)=>V([T(n,{sz:150,st:'Bold',c:i<2?ACC:INK,lh:105,ls:-3}),T(l,{w:250,sz:32,c:G1})],{sp:2})),{w:CW,pa:'SPACE_BETWEEN',sp:24});
const EV=[['16/8','Group formed',0],['23/8','First meetup, first clips',1],['27/8','Survey v1',0],['17/9','CCF volunteer interview',1],['22/9','Survey made anonymous',0],['24/9','Hospital, CCF meet',1],['5/10','CMO permission',0],['13/10','Survey out, CMO met',1],['14/10','Night round, 21 clips',1],['16/10','More interviews',1],['19/10','All media pooled',0],['20/10','Transcribed and coded',0]];
const TH=260,mid=130,step=CW/EV.length,tl=[R(CW,3,G3,{x:0,y:mid-1})];
EV.forEach(([d,t,k],i)=>{const cx=Math.round(step*(i+.5)),up=i%2===0; tl.push(E(cx,mid,26,k?ACC:INK));
 const tx=T(d+'  '+t,{sz:32,w:360,al:'CENTER'}); tx.x=Math.max(0,Math.min(CW-360,cx-180)); tx.y=up?mid-40-tx.height:mid+40; tl.push(tx);});
tl.push(T('Teal dots are field days.',{sz:30,c:G2,x:0,y:TH-36}));
const timeline=box(CW,TH,tl,'Timeline');
const band1=sec('Our fieldwork, 16 Aug to 20 Oct 2026',CW,[stats,timeline],28);

// SURVEY VISUALS
const pw=col(3);
const big=(n,c=ACC)=>T(n,{sz:150,st:'Bold',c,lh:100,ls:-3});
const bar=(w,frac,c=ACC,h=34)=>box(w,h,[R(w,h,G4),R(Math.round(w*frac),h,c)]);
const wcells=[];{const cs=24,g=6; for(let i=0;i<100;i++){const r=9-Math.floor(i/10),cc=i%10; wcells.push(R(cs,cs,i<86?ACC:i<94?INK:G3,{x:cc*(cs+g),y:r*(cs+g)}));}}
const waffle=box(10*30-6,10*30-6,wcells,'Waffle 211');
const p1=V([lab('Survey, 211 replies'),H([waffle,V([big('86%'.replace('','')),cap('want the dogs to stay, with limits (181 of 211)',pw-330,{c:INK}),cap('Dark: free movement, 8% (17)',pw-330,{sz:32,c:G2})],{sp:10})],{sp:28})],{w:pw,sp:20});
const p2=V([lab('In the hostels'),big('68%'),bar(pw,0.68),cap('have had dogs come into their hostel (143 of 211)',pw,{c:INK})],{w:pw,sp:18});
const cb=(l,f,n,c)=>V([H([T(l,{sz:36,st:'Semi Bold'}),T(n,{sz:36,c:G2})],{sp:16}),bar(pw,f,c,48)],{w:pw,sp:8});
const p3=V([lab('Chased vs not chased'),cap('Share who call dogs a serious problem',pw,{c:INK}),cb('Chased: 87%',0.87,'112 of 129',ACC),cb('Not chased: 22%',0.22,'18 of 82',G2)],{w:pw,sp:22});
const p4=V([lab('Knowing CCF'),big('71%',INK),bar(pw,0.71,INK),cap('had not heard of CCF or the sterilisation drives (149 of 211)',pw,{c:INK})],{w:pw,sp:18});
const band2=V([R(CW,4,INK),H([p1,p2,p3,p4],{w:CW,sp:GAP})],{w:CW,sp:28});

// MAP
const D=__DATA__; const MW=D.W, MH=D.H;
const map=figma.createFrame(); map.name='Campus map (native)'; map.resize(MW,MH); map.fills=P('#FFFFFF'); map.clipsContent=true;
base.name='OSM base (© OpenStreetMap contributors)'; map.appendChild(base); base.x=0; base.y=0;
const COL={'chasing':ACC,'bite':ACC,'dogs in hostel':INK};
const SIDE={'MAC':'l','Rajiv Bhawan':'r','Radhakrishnan Bhawan':'r','MNC':'l3','Himalaya Bhawan':'r','Govind Bhawan (towards Chemistry)':'l','Hospital':'l','Kasturba Bhawan':'t','Jawahar Bhawan':'l','Architecture dept':'b','Feeding spot near Mechanical (approx.)':'r','Feeding spot near Kasturba (approx.)':'rb','Mandir':'l','SAC':'l'};
const nm=p=>p.startsWith('Feeding near Kasturba')?'':p.startsWith('Feeding spot near Kasturba')?'feeding\n(approx.)':p.startsWith('Feeding')?'feeding (approx.)':p.replace(' Bhawan','').replace(' (towards Chemistry)','–Chemistry').replace(' dept','');
const labels=[];
for (const q of D.pts.sort((a,b)=>b.n-a.n)) {
  const feed=q.p.startsWith('Feeding'); const r=q.n?(10+8*Math.sqrt(q.n)):0;
  if(feed){const s=R(30,30,'#FFFFFF',{x:q.x-15,y:q.y-15,stroke:ACC,sw:4}); map.appendChild(s);}
  else if(r) map.appendChild(E(q.x,q.y,2*r,COL[q.dom]||'#A3A3A3',{op:0.85}));
  const rr=q.team?Math.max(r,30)+14:r; if(q.team) map.appendChild(E(q.x,q.y,2*rr,null,{stroke:ACC,sw:6}));
  if(q.iv) map.appendChild(E(q.x,q.y,14,'#FFFFFF',{stroke:INK,sw:2}));
  if(!(q.n>=3||q.team||feed)) continue;
  const lines=[]; const main=T(nm(q.p)+(q.n?'  '+q.n:''),{sz:36,st:q.team?'Semi Bold':'Regular',c:feed?ACC:INK}); lines.push(main);
  const sub=[q.approx&&!feed?'approx.':'',q.night?'night: '+q.night:''].filter(Boolean).join(' · '); if(sub) lines.push(T(sub,{sz:30,c:G2}));
  const g=V(lines,{sp:0}); map.appendChild(g); const s=SIDE[q.p]||'r', off=(feed?15:rr)+12;
  if(s==='r'||s==='rb'){g.x=q.x+off; g.y=q.y-main.height/2+(s==='rb'?16:0);} else if(s==='l'||s==='l3'){g.x=q.x-off-g.width; g.y=q.y-main.height/2+(s==='l3'?80:0);} else if(s==='t'){g.x=q.x-g.width/2; g.y=q.y-off-g.height;} else {g.x=q.x-g.width/2; g.y=q.y+off;}
  g.x=Math.max(6,Math.min(MW-g.width-6,g.x));
}
const cr=T('Map data © OpenStreetMap contributors (ODbL)',{sz:26,c:G2}); map.appendChild(cr); cr.x=MW-cr.width-12; cr.y=MH-cr.height-10;
// key + who brought up what, right of map
const RW=CW-MW-GAP;
const keyRow=(shape,s)=>H([shape,T(s,{sz:36,c:G1})],{sp:18,ca:'CENTER'});
const keyc=(c)=>{const e=figma.createEllipse(); e.resize(34,34); e.fills=P(c); e.opacity=0.85; return e;};
const ring=figma.createEllipse(); ring.resize(40,40); ring.fills=[]; ring.strokes=P(ACC); ring.strokeWeight=6;
const sq=R(30,30,'#FFFFFF',{stroke:ACC,sw:4});
const key=V([T('Circle size: how often a place came up in interviews, survey answers and CCF/CMO notes',{w:RW,sz:40}),
 H([keyRow(keyc(ACC),'chasing, bites'),keyRow(keyc(INK),'dogs in hostels'),keyRow(keyc('#A3A3A3'),'other')],{sp:40}),
 keyRow(ring,'spot we saw ourselves, 20 Oct (5)'),keyRow(sq,'feeding spot, position approx.'),
 T('Not placed yet: gate 7 and the wall gaps (11 mentions), mess and canteens (32).',{w:RW,sz:36,c:G2})],{w:RW,sp:18});
const GR=[['In hostels',[9,18],[1,5],[0,4],[0,3]],['Bites',[6,18],[3,5],[2,4],[1,3]],['Chased',[5,18],[3,5],[1,4],[1,3]],['Feeding',[3,18],[2,5],[1,4],[2,3]],['Boundary',[0,18],[2,5],[0,4],[2,3]],['Fewer dogs',[2,18],[1,5],[3,4],[0,3]]];
const GN=['Students (18)','Guards (5)','Staff (4)','CCF (3)'];
const lw=250, cw=Math.floor((RW-lw)/4)-16, bw=cw-20;
const ghead=H([R(lw,1,null),...GN.map(g=>T(g,{w:cw,sz:30,c:G2}))],{sp:16});
const grows=GR.map(([t,...v])=>{const fr=v.map(([a,b])=>a/b), mx=Math.max(...fr); return H([T(t,{w:lw,sz:36}),...v.map(([a,b],j)=>V([box(bw,26,[R(bw,26,G4),R(Math.round(bw*a/b),26,fr[j]===mx&&mx>0?ACC:G2)]),T(a+'/'+b,{sz:28,c:G2})],{sp:4}))],{sp:16,ca:'CENTER'});});
const who=V([T('Who brought up what',{sz:48,st:'Semi Bold'}),ghead,...grows,T('Bar: share of each group\u2019s interviews. Teal: the group that raised it most.',{w:RW,sz:32,c:G2})],{w:RW,sp:16});
const band3=sec('Where it happens',CW,[H([map,V([key,R(RW,2,G3),who],{w:RW,sp:36})],{w:CW,sp:GAP})],24);

// FINDINGS dot matrix
const FW=col(6);
const FND=[['F1','Space is the issue',6],['F2','Dogs get into hostels',4],['F3','Chases cause the fear',4],['F4','Packs and outside dogs',4],['F5','Feeding spots fail',6],['F6','Few know CCF exists',3],['F7','No official numbers',4]];
const MX={0:[0,1,2,3,4,5],1:[0,1,2,3],2:[0,1,2,4],3:[1,2,4,5],4:[0,1,2,3,4,5],5:[0,1,4],6:[1,2,4,6]};
const SRC=['Survey','Students','Guards','Staff','CCF','Feeders, faculty','CMO'];
const fl=620, dc=Math.floor((FW-fl-140)/7);
const dotrow=(i)=>{const k=[]; for(let j=0;j<7;j++){const on=MX[i].includes(j); k.push(E(j*dc+dc/2,24,on?34:12,on?ACC:G3));} return box(7*dc,48,k);};
const fhead=H([R(fl,1,null),...SRC.map(s=>T(s,{w:dc,sz:s==='Students'?23:26,c:G2,al:'CENTER'})),T('sources',{w:140,sz:26,c:G2,al:'RIGHT'})],{sp:0,ca:'MAX'});
const frows=FND.map(([id,t,n],i)=>H([H([T(id,{sz:40,st:'Bold',c:ACC}),T(t,{sz:40,st:'Semi Bold'})],{w:fl,sp:16}),dotrow(i),T(n+' of 7',{w:140,sz:36,c:n>=6?ACC:G1,al:'RIGHT',st:n>=6?'Semi Bold':'Regular'})],{sp:0,ca:'CENTER'}));
const findings=sec('What we found, and who backs it',FW,[fhead,...frows,cap('Big dot: that kind of source supports the finding. 6 of 7 we call strong.',FW,{sz:32,c:G2})],18);

// DISAGREEMENTS
const CF=[['Sterilisation','CCF: about 90 females, all sterilised','Guards: litters keep coming'],['Gate','A gate guard: outside dogs kept out','CCF: gate 7 is broken'],['Shelter','CCF: there is one','Others: no, probably medical cases only'],['Bites','CCF: rare','13 of 36 interviews mention one']];
const hw=Math.floor((FW-40)/2);
const conflicts=sec('Where our sources disagree',FW,[...CF.map(([t,a,b])=>V([T(t,{sz:40,st:'Semi Bold',c:ACC}),H([V([R(hw,3,INK),T(a,{w:hw,sz:38})],{w:hw,sp:8}),V([R(hw,3,G2),T(b,{w:hw,sz:38,c:G1})],{w:hw,sp:8})],{sp:40})],{w:FW,sp:8}))],22);
const band4=H([findings,conflicts],{w:CW,sp:GAP});

// KPI progress + recommendations
const KW=col(6);
const KP=[['Reach','36 interviews, 211 surveyed (target 30 interviews)',1,ACC,'met'],['Depth','3.45 h recorded over 6 days (target 40 person-hours)',null,G2,'in progress'],['Record','2 of 3 datasets (survey, interviews)',2/3,ACC,'2 of 3'],['Output','1 acknowledged note',0,G2,'not yet'],['Change','1 written change',0,G2,'not yet']];
const kb=KW-260-200;
const kpis=sec('KPIs',KW,KP.map(([k,d,f,c,s])=>H([T(k,{w:240,sz:40,st:'Semi Bold'}),V([f===null?box(kb,30,[R(kb,30,null,{stroke:G3,sw:3})]):bar(kb,f,c,30),T(d,{w:kb,sz:32,c:G1})],{w:kb,sp:6}),T(s,{w:180,sz:34,c:f===1?ACC:G2,al:'RIGHT',st:f===1?'Semi Bold':'Regular'})],{sp:20,ca:'CENTER'})),20);
const meth=cap('Method: survey, 36 recorded interviews, all 80 recordings transcribed and translated, 27 codes, checked against 7 kinds of source. Limits: the form had no option to remove dogs, 94% of replies came on one day, the transcripts are machine-made and one of us coded.',KW,{sz:32,c:G2});
const RC=[['Mesh on hostel entrances, lids on bins','Wardens'],['Fewer feeding spots, with clear boards','CCF, feeders'],['Fix gate 7 and the broken walls','Estate, Security'],['Publish sterilisation counts each year','CCF, Security'],['A notice in every hostel on bite care','Hospital'],['One number to report a chasing dog','Security, CCF'],['Teach first-years and feeders','CCF, student council']];
const recs=sec('What we think should change',KW,RC.map(([a,b],i)=>H([T('R'+(i+1),{w:80,sz:40,st:'Bold',c:ACC}),T(a,{w:KW-80-380-40,sz:40}),T(b,{w:380,sz:32,c:G2,al:'RIGHT'})],{sp:20,ca:'CENTER'})),16);
const band5=H([V([kpis,meth],{w:KW,sp:24}),recs],{w:CW,sp:GAP});
const footer=V([R(CW,2,G3),T('Thank you to the guards, mess, canteen and cleaning staff, CCF volunteers, feeders, students, faculty and the institute hospital for talking to us. We have not named anyone we interviewed. Group 23: Vansh Gautam, Vinayak Raizada, Jay D, Vrinda Gupta, Jiya Dubey, Khushi, Nandini.',{w:CW,sz:30,c:G2})],{w:CW,sp:14});
poster.layoutMode='VERTICAL'; poster.itemSpacing=__GAP__; poster.paddingTop=150; poster.paddingBottom=150; poster.paddingLeft=M; poster.paddingRight=M; poster.primaryAxisSizingMode='FIXED'; poster.resize(W,4961); poster.clipsContent=true;
for (const b of [header,band1,band2,band3,band4,band5,footer]) poster.appendChild(b);
const kids=poster.children.map(c=>[c.name,Math.round(c.y),Math.round(c.height)]); const last=poster.children[poster.children.length-1];
return {kids, bottom:Math.round(last.y+last.height), limit:4961-150};
