#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bilibili Video Data Analyzer v1.0"""
import sys, re, json, urllib.request
from datetime import datetime

class C:
    R=chr(27)+"[0m"; B=chr(27)+"[1m"; D=chr(27)+"[2m"
    RED=chr(27)+"[91m"; GRN=chr(27)+"[92m"; YEL=chr(27)+"[93m"
    BLU=chr(27)+"[94m"; MAG=chr(27)+"[95m"; CYN=chr(27)+"[96m"
    WHT=chr(27)+"[97m"; BGB=chr(27)+"[44m"

def fmt(n):
    if n is None: return "N/A"
    if n>=1e8: return f"{n/1e8:.1f}"+chr(20108)
    if n>=1e4: return f"{n/1e4:.1f}"+chr(19975)
    return str(n)

def barchart(val, mx, w=30, fill=None, empty=None):
    if mx==0: return (empty or chr(9617))*w
    f=int(min(val/mx,1.0)*w)
    return (fill or chr(9608))*f+(empty or chr(9617))*(w-f)

def parse_bvid(s):
    m=re.search(r"(BV[A-Za-z0-9]+)", s.strip())
    return m.group(1) if m else None

def fetch(bvid):
    url=f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    hdr={"User-Agent":"Mozilla/5.0","Referer":"https://www.bilibili.com"}
    with urllib.request.urlopen(urllib.request.Request(url,headers=hdr),timeout=15) as r:
        data=json.loads(r.read().decode("utf-8"))
    if data.get("code")!=0:
        raise Exception(f"API err: {data.get(chr(109)+chr(101)+chr(115)+chr(115)+chr(97)+chr(103)+chr(101),chr(63))}")
    return data["data"]

def analyze(bvid):
    R=C.R; B_=C.B; D_=C.D
    print(C.CYN+B_)
    print("="*52)
    print("  Bilibili Video Analyzer v1.0")
    print("="*52+R)
    print(D_+"Fetching: "+bvid+" ..."+R)
    try:
        info=fetch(bvid)
    except Exception as e:
        print(C.RED+"Failed: "+str(e)+R)
        return
    t=info.get("title","?")
    owner=info.get("owner",{}).get("name","?")
    mid=info.get("owner",{}).get("mid","")
    desc=info.get("desc","")
    dur=info.get("duration",0)
    pub=datetime.fromtimestamp(info.get("pubdate",0)).strftime("%Y-%m-%d %H:%M")
    tn=info.get("tname","?")
    s=info.get("stat",{})
    vi=s.get("view",0); dm=s.get("danmaku",0); rp=s.get("reply",0)
    fav=s.get("favorite",0); coin=s.get("coin",0); sh=s.get("share",0); lk=s.get("like",0)
    eng=((lk+coin*2+fav+sh)/vi*100) if vi>0 else 0
    dm_r=(dm/vi*100) if vi>0 else 0
    cv_r=(coin/vi) if vi>0 else 0
    lv_r=(lk/vi*100) if vi>0 else 0
    print()
    print("  "+B_+"--- Video Info ---"+R)
    print("  Title:    "+t)
    print("  UP:       "+owner+" (UID:"+str(mid)+")")
    print("  Zone:     "+tn)
    print("  Duration: "+str(dur//60)+"m"+str(dur%60)+"s")
    print("  PubDate:  "+pub)
    mx=max(vi,lk,coin,fav,dm,rp,sh,1)
    metrics=[(chr(9654)+" Views",vi,C.GRN),(chr(128077)+" Likes",lk,C.RED),
             (chr(129689)+" Coins",coin,C.YEL),(chr(11088)+" Favs",fav,C.MAG),
             ("Reply",rp,C.BLU),("Danmaku",dm,C.CYN),("Share",sh,C.WHT)]
    print()
    print("  "+B_+C.BGB+" Core Data Dashboard "+R)
    print("  "+D_+"-"*48+R)
    for lb,v,cl in metrics:
        print("  "+B_+f"{lb:12s}"+R+" "+cl+barchart(v,mx,28)+R+" "+B_+f"{fmt(v):>10s}"+R)
    print()
    if eng>=15: eg,ec="S-Tier Viral",C.RED
    elif eng>=8: eg,ec="A-Tier Good",C.YEL
    elif eng>=4: eg,ec="B-Tier OK",C.GRN
    elif eng>=2: eg,ec="C-Tier Avg",C.CYN
    else: eg,ec="D-Tier Low",D_
    print("  "+B_+C.BGB+" Quality Metrics "+R)
    print("  "+D_+"-"*48+R)
    print("  Engagement:  "+B_+f"{eng:.2f}%"+R+" "+ec+"["+eg+"]"+R)
    print("  Like Rate:   "+B_+f"{lv_r:.2f}%"+R)
    print("  Danmaku Rate:"+B_+f"{dm_r:.2f}%"+R)
    print("  Coin/View:   "+B_+f"{cv_r:.4f}"+R)
    sc=min(min(vi/1e4,25)+min(eng*2,25)+min(dm_r*10,25)+min(cv_r*100,25),100)
    if sc>=80: sg,scl="Viral!",C.RED
    elif sc>=60: sg,scl="Quality",C.GRN
    elif sc>=40: sg,scl="Average",C.YEL
    else: sg,scl="Needs Work",D_
    print()
    print("  "+B_+C.BGB+" Score "+R)
    print("  "+D_+"-"*48+R)
    bar_sc=barchart(sc,100,40,chr(9619),chr(9617))
    print("  "+scl+bar_sc+R+" "+B_+f"{sc:.0f}/100"+R+" "+scl+sg+R)
    print()
    print("  "+B_+C.BGB+" Optimization Tips "+R)
    print("  "+D_+"-"*48+R)
    tips=[]
    if lv_r<3: tips.append("- Like rate low, add CTA at end")
    if dm_r<1: tips.append("- Few danmaku, add interaction points")
    if cv_r<0.01: tips.append("- Low coins, ask for sanlian")
    if eng<4: tips.append("- Low engagement, improve title/cover")
    if vi>1e4 and fav<vi*0.02: tips.append("- High views low favs, add save-worthy content")
    if not tips: tips.append("- Great performance, keep it up!")
    for tip in tips: print("  "+tip)
    if desc:
        print()
        print("  "+D_+"-"*48+R)
        print("  "+B_+C.CYN+"Description:"+R)
        d=desc[:200]+("..." if len(desc)>200 else "")
        print("  "+D_+d+R)
    print()
    print("  "+B_+"="*52+R)
    print("  "+D_+"Done @ "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+R)
    print()

if __name__=="__main__":
    if len(sys.argv)<2:
        R=C.R; print(C.RED+"Usage: python bilibili_analyzer.py <BV or URL>"+R)
        print(C.D+"Example: python bilibili_analyzer.py BV1GJ411x7h7"+R)
        sys.exit(1)
    bvid=parse_bvid(" ".join(sys.argv[1:]))
    if not bvid: print(C.RED+"Cannot parse BV ID"+R); sys.exit(1)
    analyze(bvid)