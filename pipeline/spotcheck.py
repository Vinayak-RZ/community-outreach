import json, re, sys, difflib, statistics, time
from faster_whisper import WhisperModel
RAW="/workspace/library/acads/community-outreach/media/raw/"
TR="/workspace/repos/Illusion/transcripts/"
OUT="/workspace/library/acads/community-outreach/media/logs/spotcheck/"
m=WhisperModel("small", device="cpu", compute_type="float32", cpu_threads=3)
norm=lambda t:re.sub(r"[^\w']","",t.lower())
for f in sys.argv[1:]:
    stem=f.rsplit(".",1)[0]
    d=json.load(open(f"{TR}{stem}/{stem}.json"))
    t0=time.time()
    import subprocess
    wav=OUT+stem+".wav"
    subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-i",RAW+f,"-vn","-ac","1","-ar","16000","-c:a","pcm_s16le",wav],check=True)
    segs,info=m.transcribe(wav, task="transcribe", language=d["language"], beam_size=5, temperature=[0.0,0.4], best_of=2,
        repetition_penalty=1.1, vad_filter=False, word_timestamps=True,
        condition_on_previous_text=False, no_speech_threshold=None)
    segs=list(segs)
    S=[norm(w.word) for s in segs for w in (s.words or [])]; S=[w for w in S if w]
    MW=[(w["start"],w["end"],norm(w["word"]),w["prob"]) for s in d["segments"] for w in (s.get("words") or []) if norm(w["word"])]
    A=[w[2] for w in MW]
    sm=difflib.SequenceMatcher(None,A,S,autojunk=False)
    matched=[False]*len(A)
    for b in sm.get_matching_blocks():
        for i in range(b.a,b.a+b.size): matched[i]=True
    win=30; wins={}
    for (st,en,w,p),ok in zip(MW,matched):
        k=int(st//win); x=wins.setdefault(k,{"n":0,"ok":0,"p":[]}); x["n"]+=1; x["ok"]+=ok; x["p"].append(p)
    W=[{"start":k*win,"words":v["n"],"agree":round(v["ok"]/v["n"],2),"prob":round(statistics.mean(v["p"]),2),
        "low":sum(q<0.5 for q in v["p"])} for k,v in sorted(wins.items())]
    segrep=[{"start":s["start"],"end":s["end"],"text":s["text"].strip(),"avg_logprob":s["avg_logprob"],"no_speech_prob":s["no_speech_prob"]} for s in d["segments"]]
    gaps=[(a["end"],b["start"]) for a,b in zip(d["segments"],d["segments"][1:]) if b["start"]-a["end"]>8]
    res={"file":f,"language":d["language"],"duration_s":d["duration_s"],"small_s":round(time.time()-t0,1),
         "overall_agree":round(sum(matched)/len(A),3),"word_prob_mean":round(statistics.mean(w[3] for w in MW),3),
         "low_word_share":round(sum(w[3]<0.5 for w in MW)/len(MW),3),"words":len(A),"small_words":len(S),
         "windows":W,"gaps":gaps,"low_words":[(round(w[0],1),w[2],w[3]) for w in MW if w[3]<0.3],
         "small_text":" ".join(s.text.strip() for s in segs),"segments":segrep}
    json.dump(res,open(OUT+stem+".json","w"),ensure_ascii=False,indent=1)
    print(f,res["overall_agree"],res["word_prob_mean"],res["low_word_share"],len(A),len(S),res["small_s"],flush=True)
print("SPOTCHECK DONE")
