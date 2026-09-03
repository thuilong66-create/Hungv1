#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALGORITHMS MODULE - VIP PRO WEB
40+ Thuat toan Tai Xiu + Baccarat VIP PRO
"""
import math
from collections import defaultdict

# ================================================================
# THUAT TOAN TAI XIU - 34 PHUONG PHAP
# ================================================================
class TXPatterns:
    # --- CORE PATTERNS ---
    @staticmethod
    def detect_bet(h):
        if len(h)<2: return None
        last=h[-1]; run=1
        for i in range(len(h)-2,-1,-1):
            if h[i]==last: run+=1
            else: break
        if run>=12: return {'id':'cau_bet','ten':f'Cau Bet {run} (BE GAP)','do_tin_cay':98,'ket_tiep':'X' if last=='T' else 'T','trong_so':98,'uu_tien':12}
        if run>=10: return {'id':'cau_bet','ten':f'Cau Bet {run} (BE)','do_tin_cay':95,'ket_tiep':'X' if last=='T' else 'T','trong_so':95,'uu_tien':10}
        if run>=8:  return {'id':'cau_bet','ten':f'Cau Bet {run} (BE)','do_tin_cay':90,'ket_tiep':'X' if last=='T' else 'T','trong_so':88,'uu_tien':8}
        if run>=6:  return {'id':'cau_bet','ten':f'Cau Bet {run}','do_tin_cay':80,'ket_tiep':last,'trong_so':75,'uu_tien':6}
        if run>=4:  return {'id':'cau_bet','ten':f'Cau Bet {run}','do_tin_cay':70,'ket_tiep':last,'trong_so':70,'uu_tien':4}
        if run>=2:  return {'id':'cau_bet','ten':f'Cau Bet {run}','do_tin_cay':58,'ket_tiep':last,'trong_so':60,'uu_tien':2}
        return None

    @staticmethod
    def detect_1_1(h):
        if len(h)>=6 and ''.join(h[-6:]) in ('TXTXTX','XTXTXT'):
            return {'id':'cau_dao_11','ten':'Cau Dao 1-1 (dai)','do_tin_cay':92,'ket_tiep':'X' if h[-1]=='T' else 'T','trong_so':88,'uu_tien':6}
        if len(h)>=4 and ''.join(h[-4:]) in ('TXTX','XTXT'):
            return {'id':'cau_dao_11','ten':'Cau Dao 1-1','do_tin_cay':85,'ket_tiep':'X' if h[-1]=='T' else 'T','trong_so':80,'uu_tien':4}
        return None

    @staticmethod
    def detect_2_2(h):
        if len(h)>=8 and ''.join(h[-8:]) in ('TTXXTTXX','XXTTXXTT'):
            return {'id':'cau_22','ten':'Cau 2-2 (dai)','do_tin_cay':88,'ket_tiep':'X' if h[-1]=='T' else 'T','trong_so':84,'uu_tien':8}
        if len(h)>=4 and ''.join(h[-4:]) in ('TTXX','XXTT'):
            return {'id':'cau_22','ten':'Cau 2-2','do_tin_cay':82,'ket_tiep':'X' if ''.join(h[-4:])=='TTXX' else 'T','trong_so':78,'uu_tien':4}
        return None

    @staticmethod
    def detect_3_3(h):
        if len(h)>=6:
            l6=''.join(h[-6:])
            if l6=='TTTXXX': return {'id':'cau_33','ten':'Cau 3-3','do_tin_cay':80,'ket_tiep':'T','trong_so':76,'uu_tien':6}
            if l6=='XXXTTT': return {'id':'cau_33','ten':'Cau 3-3','do_tin_cay':80,'ket_tiep':'X','trong_so':76,'uu_tien':6}
        return None

    @staticmethod
    def detect_4_4(h):
        if len(h)>=8:
            l8=''.join(h[-8:])
            if l8=='TTTTXXXX': return {'id':'cau_44','ten':'Cau 4-4','do_tin_cay':78,'ket_tiep':'T','trong_so':74,'uu_tien':8}
            if l8=='XXXXTTTT': return {'id':'cau_44','ten':'Cau 4-4','do_tin_cay':78,'ket_tiep':'X','trong_so':74,'uu_tien':8}
        return None

    @staticmethod
    def detect_5_5(h):
        if len(h)>=10:
            l10=''.join(h[-10:])
            if l10=='TTTTTXXXXX': return {'id':'cau_55','ten':'Cau 5-5','do_tin_cay':76,'ket_tiep':'T','trong_so':72,'uu_tien':10}
            if l10=='XXXXXTTTTT': return {'id':'cau_55','ten':'Cau 5-5','do_tin_cay':76,'ket_tiep':'X','trong_so':72,'uu_tien':10}
        return None

    @staticmethod
    def detect_1_2(h):
        p={'TXX':'T','XTT':'X'}
        for k,v in p.items():
            if len(h)>=len(k) and ''.join(h[-len(k):])==k:
                return {'id':'cau_12','ten':f'Cau 1-2 ({k})','do_tin_cay':72,'ket_tiep':v,'trong_so':70,'uu_tien':3}
        return None

    @staticmethod
    def detect_2_1(h):
        p={'TTX':'X','XXT':'T'}
        for k,v in p.items():
            if len(h)>=len(k) and ''.join(h[-len(k):])==k:
                return {'id':'cau_21','ten':f'Cau 2-1 ({k})','do_tin_cay':72,'ket_tiep':v,'trong_so':70,'uu_tien':3}
        return None

    @staticmethod
    def detect_1_2_3(h):
        if len(h)>=6:
            l6=''.join(h[-6:])
            if l6=='TXXTTT': return {'id':'cau_123','ten':'Cau 1-2-3 (T)','do_tin_cay':77,'ket_tiep':'X','trong_so':73,'uu_tien':6}
            if l6=='XTTXXX': return {'id':'cau_123','ten':'Cau 1-2-3 (X)','do_tin_cay':77,'ket_tiep':'T','trong_so':73,'uu_tien':6}
        return None

    @staticmethod
    def detect_3_2_1(h):
        if len(h)>=6:
            l6=''.join(h[-6:])
            if l6=='TTTXXT': return {'id':'cau_321','ten':'Cau 3-2-1 (T)','do_tin_cay':77,'ket_tiep':'X','trong_so':73,'uu_tien':6}
            if l6=='XXXTTX': return {'id':'cau_321','ten':'Cau 3-2-1 (X)','do_tin_cay':77,'ket_tiep':'T','trong_so':73,'uu_tien':6}
        return None

    @staticmethod
    def detect_zigzag(h):
        if len(h)>=7:
            l7=''.join(h[-7:])
            if l7 in ('TXTXTXT','XTXTXTX'): return {'id':'cau_ziczac','ten':'Cau Ziczac (7)','do_tin_cay':88,'ket_tiep':'X' if h[-1]=='T' else 'T','trong_so':84,'uu_tien':7}
        if len(h)>=5:
            l5=''.join(h[-5:])
            if l5 in ('TXTXT','XTXTX'): return {'id':'cau_ziczac','ten':'Cau Ziczac (5)','do_tin_cay':80,'ket_tiep':'X' if h[-1]=='T' else 'T','trong_so':76,'uu_tien':5}
        return None

    @staticmethod
    def detect_dragon(h):
        if len(h)<5: return None
        r=0
        for i in range(len(h)-1,-1,-1):
            if h[i]=='T': r+=1
            else: break
        if r>=8: return {'id':'cau_rong','ten':f'Cau Rong {r} (BE GAP)','do_tin_cay':92,'ket_tiep':'X','trong_so':88,'uu_tien':r}
        if r>=6: return {'id':'cau_rong','ten':f'Cau Rong {r} (BE)','do_tin_cay':85,'ket_tiep':'X','trong_so':80,'uu_tien':r}
        if r>=4: return {'id':'cau_rong','ten':f'Cau Rong {r}','do_tin_cay':72,'ket_tiep':'T','trong_so':68,'uu_tien':r}
        return None

    @staticmethod
    def detect_tiger(h):
        if len(h)<5: return None
        r=0
        for i in range(len(h)-1,-1,-1):
            if h[i]=='X': r+=1
            else: break
        if r>=8: return {'id':'cau_doi','ten':f'Cau Ho {r} (BE GAP)','do_tin_cay':92,'ket_tiep':'T','trong_so':88,'uu_tien':r}
        if r>=6: return {'id':'cau_doi','ten':f'Cau Ho {r} (BE)','do_tin_cay':85,'ket_tiep':'T','trong_so':80,'uu_tien':r}
        if r>=4: return {'id':'cau_doi','ten':f'Cau Ho {r}','do_tin_cay':72,'ket_tiep':'X','trong_so':68,'uu_tien':r}
        return None

    @staticmethod
    def detect_chain(h):
        if len(h)>=9:
            l9=h[-9:]
            if all(l9[i]!=l9[i-1] for i in range(1,len(l9))):
                return {'id':'cau_nhay','ten':'Cau Nhay Coc (9)','do_tin_cay':90,'ket_tiep':'X' if l9[-1]=='T' else 'T','trong_so':85,'uu_tien':9}
        if len(h)>=7:
            l7=h[-7:]
            if all(l7[i]!=l7[i-1] for i in range(1,len(l7))):
                return {'id':'cau_nhay','ten':'Cau Nhay Coc (7)','do_tin_cay':85,'ket_tiep':'X' if l7[-1]=='T' else 'T','trong_so':80,'uu_tien':7}
        return None

    @staticmethod
    def detect_cycle(h):
        for c in range(2,8):
            if len(h)<c*3: continue
            p=''.join(h[-c:])
            m=sum(1 for i in range(1,3) if ''.join(h[-c*(i+1):-c*i])==p)
            if m>=2:
                pos=len(h)%c
                return {'id':'cau_chu_ky','ten':f'Cau Chu Ky {c}','do_tin_cay':82,'ket_tiep':p[pos],'trong_so':76,'uu_tien':c*3}
        return None

    @staticmethod
    def detect_momentum(h):
        if len(h)>=6:
            l6=''.join(h[-6:])
            if l6=='TTTTTT': return {'id':'bien_dong','ten':'Bien dong TANG cuc','do_tin_cay':92,'ket_tiep':'X','trong_so':88,'uu_tien':6}
            if l6=='XXXXXX': return {'id':'bien_dong','ten':'Bien dong GIAM cuc','do_tin_cay':92,'ket_tiep':'T','trong_so':88,'uu_tien':6}
        if len(h)>=5:
            l5=''.join(h[-5:])
            if l5=='TTTTT': return {'id':'bien_dong','ten':'Bien dong TANG','do_tin_cay':85,'ket_tiep':'X','trong_so':80,'uu_tien':5}
            if l5=='XXXXX': return {'id':'bien_dong','ten':'Bien dong GIAM','do_tin_cay':85,'ket_tiep':'T','trong_so':80,'uu_tien':5}
        return None

    @staticmethod
    def detect_balance(h):
        if len(h)<15: return None
        r=h[-15:]; t=sum(1 for c in r if c=='T')
        if abs(t-(15-t))<=3:
            return {'id':'cau_be_cau','ten':'Cau Be Cau','do_tin_cay':78,'ket_tiep':'X' if h[-1]=='T' else 'T','trong_so':72,'uu_tien':15}
        return None

    @staticmethod
    def detect_distribution(h):
        if len(h)<30: return None
        r=h[-30:]; t=sum(1 for c in r if c=='T')/30
        if t>0.68: return {'id':'phan_bo','ten':'Phan bo TAI cao','do_tin_cay':78,'ket_tiep':'X','trong_so':72,'uu_tien':30}
        if t<0.32: return {'id':'phan_bo','ten':'Phan bo XIU cao','do_tin_cay':78,'ket_tiep':'T','trong_so':72,'uu_tien':30}
        return None

    @staticmethod
    def detect_gap(h):
        if len(h)>=6:
            l6=''.join(h[-6:])
            if l6=='TXXTXX': return {'id':'cau_gap','ten':'Cau Gap (TXX)','do_tin_cay':70,'ket_tiep':'X','trong_so':66,'uu_tien':6}
            if l6=='XTTXTT': return {'id':'cau_gap','ten':'Cau Gap (XTT)','do_tin_cay':70,'ket_tiep':'T','trong_so':66,'uu_tien':6}
        return None

    @staticmethod
    def detect_3van1(h):
        if len(h)>=4:
            l4=''.join(h[-4:])
            if l4 in ('TTTX','XXXT'):
                return {'id':'cau_3van1','ten':'Cau 3 Van 1','do_tin_cay':74,'ket_tiep':'X' if l4[-1]=='T' else 'T','trong_so':70,'uu_tien':4}
        return None

    @staticmethod
    def detect_trend(h):
        if len(h)<20: return None
        s=sum(1 for c in h[-5:] if c=='T')/5
        m=sum(1 for c in h[-10:] if c=='T')/10
        l=sum(1 for c in h[-20:] if c=='T')/20
        if s>m>l and s-l>0.2: return {'id':'xu_huong','ten':'Xu huong TAI tang','do_tin_cay':85,'ket_tiep':'T','trong_so':80,'uu_tien':20}
        if l>m>s and l-s>0.2: return {'id':'xu_huong','ten':'Xu huong XIU tang','do_tin_cay':85,'ket_tiep':'X','trong_so':80,'uu_tien':20}
        return None

    # --- MARKOV & STATISTICS ---
    @staticmethod
    def markov1(h):
        if len(h)<5: return None
        last=h[-1]; chuyen=defaultdict(int)
        for i in range(len(h)-1):
            if h[i]==last: chuyen[h[i+1]]+=1
        if chuyen:
            dd=max(chuyen,key=chuyen.get)
            dtc=min(80,50+chuyen[dd]*5)
            return {'id':'markov1','ten':'Markov bac 1','do_tin_cay':round(dtc,1),'ket_tiep':dd,'trong_so':round(50+chuyen[dd]*3),'uu_tien':5}
        return None

    @staticmethod
    def markov2(h):
        if len(h)<8: return None
        l2=''.join(h[-2:]); chuyen=defaultdict(int)
        for i in range(len(h)-2):
            if ''.join(h[i:i+2])==l2: chuyen[h[i+2]]+=1
        if chuyen:
            dd=max(chuyen,key=chuyen.get)
            dtc=min(78,50+chuyen[dd]*5)
            return {'id':'markov2','ten':'Markov bac 2','do_tin_cay':round(dtc,1),'ket_tiep':dd,'trong_so':round(45+chuyen[dd]*4),'uu_tien':6}
        return None

    @staticmethod
    def weighted_frequency(h):
        if len(h)<10: return None
        r=h[-15:]; wt=wx=0
        for i,c in enumerate(reversed(r)):
            w=i+1
            if c=='T': wt+=w
            else: wx+=w
        if abs(wt-wx)>5:
            return {'id':'tan_suat','ten':'Tan suat trong so','do_tin_cay':72,'ket_tiep':'T' if wt>wx else 'X','trong_so':68,'uu_tien':15}
        return None

    @staticmethod
    def rsi_predict(h):
        if len(h)<8: return None
        ky=7; nums=[1 if c=='T' else 0 for c in h[-ky:]]
        tang=giam=0
        for i in range(1,len(nums)):
            ch=nums[i]-nums[i-1]
            if ch>0: tang+=ch
            else: giam+=-ch
        tb_t=tang/ky; tb_g=giam/ky
        rsi=100 if tb_g==0 else 100-(100/(1+tb_t/tb_g))
        if rsi>75: return {'id':'rsi','ten':'RSI Qua mua','do_tin_cay':75,'ket_tiep':'X','trong_so':70,'uu_tien':7}
        if rsi<25: return {'id':'rsi','ten':'RSI Qua ban','do_tin_cay':75,'ket_tiep':'T','trong_so':70,'uu_tien':7}
        return None

    # --- AI NANG CAO ---
    @staticmethod
    def ai_markov_enhanced(h):
        if len(h)<20: return None
        dtn=None; dtcn=0
        for bac in range(2,6):
            if len(h)<bac+5: continue
            chuyen={}
            for i in range(len(h)-bac-1):
                k=''.join(h[i:i+bac]); nv=h[i+bac].lower()
                if k not in chuyen: chuyen[k]={'t':0,'x':0}
                chuyen[k][nv]+=1
            kc=''.join(h[-bac:]); dem=chuyen.get(kc)
            if dem and (dem['t']>0 or dem['x']>0):
                tong=dem['t']+dem['x']; dtc=abs(dem['t']-dem['x'])/tong
                if dtc>dtcn and dtc>0.6:
                    dtcn=dtc; dtn='T' if dem['t']>dem['x'] else 'X'
        if dtn:
            return {'id':'ai_markov','ten':'AI - Markov Nang Cao','do_tin_cay':round(min(85,60+dtcn*30),1),'ket_tiep':dtn,'trong_so':82,'uu_tien':35,'la_ai':True}
        return None

    @staticmethod
    def ai_ngram(h):
        if len(h)<20: return None
        for k in range(3,7):
            if len(h)<k+10: continue
            cuoi=''.join(h[-k:]); dem={'t':0,'x':0}; tong=0
            for i in range(len(h)-k-1):
                if ''.join(h[i:i+k])==cuoi:
                    nv=h[i+k].lower(); dem[nv]+=1; tong+=1
            if tong>=3:
                tl=abs(dem['t']-dem['x'])/tong
                if tl>=0.6:
                    return {'id':'ai_ngram','ten':f'AI - N-gram {k}','do_tin_cay':round(min(85,65+tl*25),1),'ket_tiep':'T' if dem['t']>dem['x'] else 'X','trong_so':80,'uu_tien':33,'la_ai':True}
        return None

    @staticmethod
    def ai_freq_rebalance(h):
        if len(h)<15: return None
        tt=sum(1 for c in h if c=='T'); tx=len(h)-tt
        r10=h[-10:]; rt10=sum(1 for c in r10 if c=='T'); rx10=10-rt10
        if rt10>=7: return {'id':'ai_can_bang','ten':'AI - Can bang tan so 10','do_tin_cay':82,'ket_tiep':'X','trong_so':85,'uu_tien':38,'la_ai':True}
        if rx10>=7: return {'id':'ai_can_bang','ten':'AI - Can bang tan so 10','do_tin_cay':82,'ket_tiep':'T','trong_so':85,'uu_tien':38,'la_ai':True}
        r30=h[-30:] if len(h)>=30 else h; rt30=sum(1 for c in r30 if c=='T'); rx30=len(r30)-rt30
        if tt>tx+8 and rt30>rx30+2: return {'id':'ai_can_bang','ten':'AI - Can bang dai han','do_tin_cay':78,'ket_tiep':'X','trong_so':80,'uu_tien':36,'la_ai':True}
        if tx>tt+8 and rx30>rt30+2: return {'id':'ai_can_bang','ten':'AI - Can bang dai han','do_tin_cay':78,'ket_tiep':'T','trong_so':80,'uu_tien':36,'la_ai':True}
        return None

    @staticmethod
    def ai_super_bridge(h):
        if len(h)<10: return None
        cac_cau=[]; cur=h[0]; rl=1
        for i in range(1,len(h)):
            if h[i]==cur: rl+=1
            else: cac_cau.append({'gia_tri':cur,'chieu_dai':rl}); cur=h[i]; rl=1
        cac_cau.append({'gia_tri':cur,'chieu_dai':rl})
        if len(cac_cau)<2: return None
        cc=cac_cau[-1]
        if cc['chieu_dai']>=4:
            return {'id':'ai_bridge','ten':f'AI - Super Bridge dao {cc["chieu_dai"]}','do_tin_cay':85,'ket_tiep':'X' if cc['gia_tri']=='T' else 'T','trong_so':88,'uu_tien':40,'la_ai':True}
        if cc['chieu_dai']==1 and len(cac_cau)>=2 and cac_cau[-2]['chieu_dai']==1:
            dn=sum(1 for c in cac_cau[-6:] if c['chieu_dai']==1)
            if dn>=4:
                return {'id':'ai_bridge','ten':'AI - Super Bridge nhay','do_tin_cay':80,'ket_tiep':'X' if cc['gia_tri']=='T' else 'T','trong_so':84,'uu_tien':37,'la_ai':True}
        return None

    @staticmethod
    def ai_deep_analysis(h):
        if len(h)<50: return None
        r50=h[-50:]; rt50=sum(1 for c in r50 if c=='T'); rx50=50-rt50
        bc=[]
        if abs(rt50-rx50)>10: bc.append('T' if rt50>rx50 else 'X')
        cac_cau=[]; cur=h[0]; rl=1
        for i in range(1,len(h)):
            if h[i]==cur: rl+=1
            else: cac_cau.append({'gia_tri':cur,'chieu_dai':rl}); cur=h[i]; rl=1
        cac_cau.append({'gia_tri':cur,'chieu_dai':rl})
        if len(cac_cau)>=2:
            cc=cac_cau[-1]
            if cc['chieu_dai']>=4: bc.append('X' if cc['gia_tri']=='T' else 'T')
        c5=''.join(h[-5:]); mp={'TTXTT':'X','TXTXT':'X','XXTXX':'T','XTXTX':'T','TTTTX':'X','XXXXT':'T'}
        if c5 in mp: bc.append(mp[c5])
        if len(bc)==0: return None
        st=sum(1 for v in bc if v=='T'); sx=sum(1 for v in bc if v=='X')
        if st>sx and st>=2: return {'id':'ai_sau','ten':'AI - Phan tich sau','do_tin_cay':83,'ket_tiep':'T','trong_so':86,'uu_tien':42,'la_ai':True}
        if sx>st and sx>=2: return {'id':'ai_sau','ten':'AI - Phan tich sau','do_tin_cay':83,'ket_tiep':'X','trong_so':86,'uu_tien':42,'la_ai':True}
        return None

    # --- VIP PRO ---
    @staticmethod
    def vip_cau_15(h):
        if len(h)<8: return None
        r=h[-15:]; n=len(r); st=sum(1 for c in r if c=='T'); sx=n-st
        cuoi=r[-1]; cd=1
        for i in range(n-2,-1,-1):
            if r[i]==cuoi: cd+=1
            else: break
        sd=n>1 and sum(1 for i in range(1,n) if r[i]!=r[i-1])/(n-1) or 0
        if cd>=5: return {'id':'vip_cau15','ten':f'VIP PRO - Cau dai {cd} lien tiep','do_tin_cay':min(95,70+cd*4),'ket_tiep':'X' if cuoi=='T' else 'T','trong_so':95,'uu_tien':50,'la_vip':True}
        if sd>0.7: return {'id':'vip_cau15','ten':'VIP PRO - Cau dao nhanh','do_tin_cay':88,'ket_tiep':'X' if cuoi=='T' else 'T','trong_so':90,'uu_tien':50,'la_vip':True}
        if n>0 and st/n>=0.65: return {'id':'vip_cau15','ten':f'VIP PRO - TAI ap dao ({st}T-{sx}X)','do_tin_cay':78,'ket_tiep':'X','trong_so':85,'uu_tien':50,'la_vip':True}
        if n>0 and sx/n>=0.65: return {'id':'vip_cau15','ten':f'VIP PRO - XIU ap dao ({st}T-{sx}X)','do_tin_cay':78,'ket_tiep':'T','trong_so':85,'uu_tien':50,'la_vip':True}
        if abs(st-sx)<=2: return {'id':'vip_cau15','ten':f'VIP PRO - Can bang ({st}T-{sx}X)','do_tin_cay':72,'ket_tiep':'X' if cuoi=='T' else 'T','trong_so':80,'uu_tien':50,'la_vip':True}
        return {'id':'vip_cau15','ten':f'VIP PRO - Xu huong ({st}T-{sx}X)','do_tin_cay':68,'ket_tiep':'T' if st>sx else 'X','trong_so':75,'uu_tien':50,'la_vip':True}

    @staticmethod
    def vip_weighted(h):
        if len(h)<10: return None
        r=h[-15:]; wt=wx=0
        for i,c in enumerate(reversed(r)):
            w=math.pow(15-i,1.5)
            if c=='T': wt+=w
            else: wx+=w
        tong=wt+wx
        if tong==0: return None
        ch=abs(wt/tong-wx/tong)
        if ch<0.05: return None
        return {'id':'vip_trong_so','ten':'VIP PRO - Tan suat trong so cao cap','do_tin_cay':round(min(92,55+ch*100),1),'ket_tiep':'T' if wt>wx else 'X','trong_so':88,'uu_tien':45,'la_vip':True}

    @staticmethod
    def vip_context(h):
        if len(h)<15: return None
        l5=h[-5:]; p10=h[-15:-5]
        l5t=sum(1 for c in l5 if c=='T')/5; p10t=sum(1 for c in p10 if c=='T')/10
        if l5t>=0.8 and p10t<=0.5: return {'id':'vip_ngu_canh','ten':'VIP PRO - Chuyen bien TAI (BE)','do_tin_cay':85,'ket_tiep':'X','trong_so':92,'uu_tien':48,'la_vip':True}
        if l5t<=0.2 and p10t>=0.5: return {'id':'vip_ngu_canh','ten':'VIP PRO - Chuyen bien XIU (BE)','do_tin_cay':85,'ket_tiep':'T','trong_so':92,'uu_tien':48,'la_vip':True}
        if sum(1 for c in l5 if c=='T')>=4: return {'id':'vip_ngu_canh','ten':'VIP PRO - TAI thong tri','do_tin_cay':75,'ket_tiep':'X','trong_so':82,'uu_tien':42,'la_vip':True}
        if sum(1 for c in l5 if c=='T')<=1: return {'id':'vip_ngu_canh','ten':'VIP PRO - XIU thong tri','do_tin_cay':75,'ket_tiep':'T','trong_so':82,'uu_tien':42,'la_vip':True}
        return None

    @staticmethod
    def vip_smart(h):
        if len(h)<12: return None
        r=h[-15:]; n=len(r); cuoi=r[n-1]
        l2=r[n-2] if n>1 else None; l3=r[n-3] if n>2 else None
        st=sum(1 for c in r if c=='T'); sx=n-st
        sd=sum(1 for i in range(1,n) if r[i]!=r[i-1])
        cd=1
        for i in range(n-2,-1,-1):
            if r[i]==cuoi: cd+=1
            else: break
        dt=dx=0; ld=[]
        if cd>=6:
            if cuoi=='T': dx+=40; ld.append('Cau TAI dai')
            else: dt+=40; ld.append('Cau XIU dai')
        elif cd>=4:
            if cuoi=='T': dx+=25; ld.append('Cau TAI')
            else: dt+=25; ld.append('Cau XIU')
        if st>n*0.7: dx+=30; ld.append('TAI qua nhieu')
        elif sx>n*0.7: dt+=30; ld.append('XIU qua nhieu')
        if sd>n*0.7:
            if cuoi=='T': dx+=35
            else: dt+=35
            ld.append('Cau dao')
        if l2 and l3:
            l3s=l3+l2+cuoi
            if l3s=='TTX': dx+=15
            elif l3s=='XXT': dt+=15
            elif l3s=='TXX': dt+=15
            elif l3s=='XTT': dx+=15
        if abs(st-sx)<=2 and n>=12:
            if cuoi=='T': dx+=10
            else: dt+=10
        if dt==0 and dx==0: return None
        dd='T' if dt>=dx else 'X'
        dtc=round(min(96,55+(max(dt,dx)-min(dt,dx))*1.2),1)
        return {'id':'vip_smart','ten':'VIP PRO - Du doan thong minh','do_tin_cay':dtc,'ket_tiep':dd,'trong_so':95,'uu_tien':60,'la_vip':True}

    @staticmethod
    def detect_all(h):
        p=[]
        methods=[
            TXPatterns.detect_bet, TXPatterns.detect_1_1, TXPatterns.detect_2_2,
            TXPatterns.detect_3_3, TXPatterns.detect_4_4, TXPatterns.detect_5_5,
            TXPatterns.detect_1_2, TXPatterns.detect_2_1,
            TXPatterns.detect_1_2_3, TXPatterns.detect_3_2_1,
            TXPatterns.detect_zigzag, TXPatterns.detect_dragon, TXPatterns.detect_tiger,
            TXPatterns.detect_chain, TXPatterns.detect_cycle,
            TXPatterns.detect_momentum, TXPatterns.detect_balance,
            TXPatterns.detect_distribution, TXPatterns.detect_gap,
            TXPatterns.detect_3van1, TXPatterns.detect_trend,
            TXPatterns.markov1, TXPatterns.markov2,
            TXPatterns.weighted_frequency, TXPatterns.rsi_predict,
            TXPatterns.ai_markov_enhanced, TXPatterns.ai_ngram,
            TXPatterns.ai_freq_rebalance, TXPatterns.ai_super_bridge,
            TXPatterns.ai_deep_analysis,
            TXPatterns.vip_cau_15, TXPatterns.vip_weighted,
            TXPatterns.vip_context, TXPatterns.vip_smart,
        ]
        for m in methods:
            try:
                kq=m(h)
                if kq: p.append(kq)
            except: pass
        p.sort(key=lambda x:(x.get('uu_tien',0),x.get('trong_so',0)),reverse=True)
        return p

# ================================================================
# THUAT TOAN BACCARAT VIP PRO - NANG CAP TOAN DIEN
# 30+ thuat toan BCR | Da so phieu bau quyet dinh ket qua
# ================================================================
class BCRPatterns:
    @staticmethod
    def normalize(h): return [c for c in h if c in ('P','B')]

    # ─── CAU 1-1: Dao xen ke P-B-P-B ───
    @staticmethod
    def detect_cau_11(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=8:
            l8=''.join(pb[-8:])
            if l8 in ('PBPBPBPB','BPBPBPBP'): return {'id':'bcr_11','ten':'Cau 1-1 (sieu dai 8)','do_tin_cay':95,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':92,'uu_tien':18,'la_vip':True}
        if len(pb)>=6:
            l6=''.join(pb[-6:])
            if l6 in ('PBPBPB','BPBPBP'): return {'id':'bcr_11','ten':'Cau 1-1 (dai 6)','do_tin_cay':90,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':88,'uu_tien':14}
        if len(pb)>=4:
            l4=''.join(pb[-4:])
            if l4 in ('PBPB','BPBP'): return {'id':'bcr_11','ten':'Cau 1-1','do_tin_cay':82,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':78,'uu_tien':8}
        return None

    # ─── CAU 2-2: PP-BB xen ke ───
    @staticmethod
    def detect_cau_22(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=8:
            l8=''.join(pb[-8:])
            if l8 in ('PPBBPPBB','BBPPBBPP'): return {'id':'bcr_22','ten':'Cau 2-2 (dai 8)','do_tin_cay':92,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':88,'uu_tien':18,'la_vip':True}
        if len(pb)>=4:
            l4=''.join(pb[-4:])
            if l4 in ('PPBB','BBPP'): return {'id':'bcr_22','ten':'Cau 2-2','do_tin_cay':80,'ket_tiep':'P' if l4=='PPBB' else 'B','trong_so':76,'uu_tien':8}
        return None

    # ─── CAU 3-3: PPP-BBB xen ke ───
    @staticmethod
    def detect_cau_33(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=12:
            l12=''.join(pb[-12:])
            if l12 in ('PPPBBBPPPBBB','BBBPPPBBBPPP'): return {'id':'bcr_33','ten':'Cau 3-3 (dai 12)','do_tin_cay':92,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':88,'uu_tien':24,'la_vip':True}
        if len(pb)>=6:
            l6=''.join(pb[-6:])
            if l6=='PPPBBB': return {'id':'bcr_33','ten':'Cau 3-3','do_tin_cay':82,'ket_tiep':'P','trong_so':78,'uu_tien':12}
            if l6=='BBBPPP': return {'id':'bcr_33','ten':'Cau 3-3','do_tin_cay':82,'ket_tiep':'B','trong_so':78,'uu_tien':12}
        return None

    # ─── CAU 4-4: PPPP-BBBB xen ke ───
    @staticmethod
    def detect_cau_44(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=8:
            l8=''.join(pb[-8:])
            if l8=='PPPPBBBB': return {'id':'bcr_44','ten':'Cau 4-4','do_tin_cay':80,'ket_tiep':'P','trong_so':76,'uu_tien':16}
            if l8=='BBBBPPPP': return {'id':'bcr_44','ten':'Cau 4-4','do_tin_cay':80,'ket_tiep':'B','trong_so':76,'uu_tien':16}
        return None

    # ─── CAU BE: Cau vua bi be ───
    @staticmethod
    def detect_cau_be(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<4: return None
        last=pb[-1]; break_run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: break_run+=1
            else: break
        prev_side=None; prev_run=0
        for i in range(len(pb)-break_run-1,-1,-1):
            if prev_side is None: prev_side=pb[i]; prev_run=1
            elif pb[i]==prev_side: prev_run+=1
            else: break
        if prev_run>=6 and break_run<=2:
            return {'id':'bcr_be','ten':f'Cau be (be {prev_run}{prev_side})','do_tin_cay':88,'ket_tiep':last,'trong_so':85,'uu_tien':prev_run*2,'la_vip':True}
        if prev_run>=4 and break_run<=2:
            return {'id':'bcr_be','ten':f'Cau be (be {prev_run}{prev_side})','do_tin_cay':78,'ket_tiep':last,'trong_so':74,'uu_tien':prev_run}
        if prev_run>=3 and break_run==1:
            return {'id':'bcr_be','ten':f'Cau be ({prev_run}{prev_side})','do_tin_cay':72,'ket_tiep':last,'trong_so':68,'uu_tien':prev_run}
        return None

    # ─── CAU BET: Cau chay dai 1 ben ───
    @staticmethod
    def detect_cau_bet(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<2: return None
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        opp='P' if last=='B' else 'B'
        if run>=12: return {'id':'bcr_bet','ten':f'Cau bet {run}{last} (SIEU BE)','do_tin_cay':98,'ket_tiep':opp,'trong_so':98,'uu_tien':run*3,'la_vip':True}
        if run>=10: return {'id':'bcr_bet','ten':f'Cau bet {run}{last} (BE GAP)','do_tin_cay':95,'ket_tiep':opp,'trong_so':95,'uu_tien':run*2,'la_vip':True}
        if run>=8:  return {'id':'bcr_bet','ten':f'Cau bet {run}{last} (BE)','do_tin_cay':92,'ket_tiep':opp,'trong_so':90,'uu_tien':run*2,'la_vip':True}
        if run>=6:  return {'id':'bcr_bet','ten':f'Cau bet {run}{last}','do_tin_cay':82,'ket_tiep':last,'trong_so':78,'uu_tien':run}
        if run>=4:  return {'id':'bcr_bet','ten':f'Cau bet {run}{last}','do_tin_cay':72,'ket_tiep':last,'trong_so':70,'uu_tien':run}
        if run>=2:  return {'id':'bcr_bet','ten':f'Cau bet {run}{last}','do_tin_cay':60,'ket_tiep':last,'trong_so':58,'uu_tien':run}
        return None

    # ─── CAU 1-2: PBB hoac BPP ───
    @staticmethod
    def detect_cau_12(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=6:
            l6=''.join(pb[-6:])
            if l6 in ('PBBPBB','BPPBPP'): return {'id':'bcr_12','ten':'Cau 1-2 (dai)','do_tin_cay':85,'ket_tiep':'P' if l6=='PBBPBB' else 'B','trong_so':82,'uu_tien':12}
        if len(pb)>=3:
            l3=''.join(pb[-3:])
            if l3=='PBB': return {'id':'bcr_12','ten':'Cau 1-2 (PBB)','do_tin_cay':74,'ket_tiep':'P','trong_so':70,'uu_tien':6}
            if l3=='BPP': return {'id':'bcr_12','ten':'Cau 1-2 (BPP)','do_tin_cay':74,'ket_tiep':'B','trong_so':70,'uu_tien':6}
        return None

    # ─── CAU 2-1: PPB hoac BBP ───
    @staticmethod
    def detect_cau_21(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=6:
            l6=''.join(pb[-6:])
            if l6 in ('PPBPPB','BBPBBP'): return {'id':'bcr_21','ten':'Cau 2-1 (dai)','do_tin_cay':85,'ket_tiep':'P' if l6=='PPBPPB' else 'B','trong_so':82,'uu_tien':12}
        if len(pb)>=3:
            l3=''.join(pb[-3:])
            if l3=='PPB': return {'id':'bcr_21','ten':'Cau 2-1 (PPB)','do_tin_cay':74,'ket_tiep':'P','trong_so':70,'uu_tien':6}
            if l3=='BBP': return {'id':'bcr_21','ten':'Cau 2-1 (BBP)','do_tin_cay':74,'ket_tiep':'B','trong_so':70,'uu_tien':6}
        return None

    # ─── CAU 3-1: PPPB hoac BBBP ───
    @staticmethod
    def detect_cau_31(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=4:
            l4=''.join(pb[-4:])
            if l4=='PPPB': return {'id':'bcr_31','ten':'Cau 3-1 (PPPB)','do_tin_cay':76,'ket_tiep':'P','trong_so':74,'uu_tien':8}
            if l4=='BBBP': return {'id':'bcr_31','ten':'Cau 3-1 (BBBP)','do_tin_cay':76,'ket_tiep':'B','trong_so':74,'uu_tien':8}
        return None

    # ─── CAU 1-3: PBBB hoac BPPP ───
    @staticmethod
    def detect_cau_13(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=4:
            l4=''.join(pb[-4:])
            if l4=='PBBB': return {'id':'bcr_13','ten':'Cau 1-3 (PBBB)','do_tin_cay':76,'ket_tiep':'P','trong_so':74,'uu_tien':8}
            if l4=='BPPP': return {'id':'bcr_13','ten':'Cau 1-3 (BPPP)','do_tin_cay':76,'ket_tiep':'B','trong_so':74,'uu_tien':8}
        return None

    # ─── CAU 4-1: PPPPB hoac BBBBP ───
    @staticmethod
    def detect_cau_41(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=5:
            l5=''.join(pb[-5:])
            if l5=='PPPPB': return {'id':'bcr_41','ten':'Cau 4-1 (PPPPB)','do_tin_cay':78,'ket_tiep':'P','trong_so':76,'uu_tien':10}
            if l5=='BBBBP': return {'id':'bcr_41','ten':'Cau 4-1 (BBBBP)','do_tin_cay':78,'ket_tiep':'B','trong_so':76,'uu_tien':10}
        return None

    # ─── CAU 1-4: PBBBB hoac BPPPP ───
    @staticmethod
    def detect_cau_14(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)>=5:
            l5=''.join(pb[-5:])
            if l5=='PBBBB': return {'id':'bcr_14','ten':'Cau 1-4 (PBBBB)','do_tin_cay':78,'ket_tiep':'P','trong_so':76,'uu_tien':10}
            if l5=='BPPPP': return {'id':'bcr_14','ten':'Cau 1-4 (BPPPP)','do_tin_cay':78,'ket_tiep':'B','trong_so':76,'uu_tien':10}
        return None

    # ─── THUAT TOAN GOC: Cau dai (long run) ───
    @staticmethod
    def detect_long_run(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<2: return None
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        if run>=8: return {'id':'bcr_dai','ten':f'Cau dai {run}{last} (DAO)','do_tin_cay':95,'ket_tiep':'P' if last=='B' else 'B','trong_so':95,'uu_tien':run*2,'la_vip':True}
        if run>=6: return {'id':'bcr_dai','ten':f'Cau dai {run}{last} (DAO)','do_tin_cay':88,'ket_tiep':'P' if last=='B' else 'B','trong_so':85,'uu_tien':run*2}
        if run>=4: return {'id':'bcr_dai','ten':f'Cau dai {run}{last}','do_tin_cay':75,'ket_tiep':last,'trong_so':70,'uu_tien':run}
        if run>=2: return {'id':'bcr_ngan','ten':f'Cau ngan {run}{last}','do_tin_cay':60,'ket_tiep':last,'trong_so':55,'uu_tien':run}
        return None

    # ─── Sau Tie -> Banker ───
    @staticmethod
    def detect_after_tie(h):
        if len(h)>=1 and h[-1]=='T':
            return {'id':'bcr_tie','ten':'Sau Tie->Banker','do_tin_cay':68,'ket_tiep':'B','trong_so':62,'uu_tien':10}
        return None

    # ─── Banker/Player thong tri ───
    @staticmethod
    def detect_bank_dom(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<15: return None
        recent=pb[-20:] if len(pb)>=20 else pb
        b=recent.count('B'); p=recent.count('P'); br=b/len(recent)
        if br>=0.70: return {'id':'bcr_dom','ten':f'Banker thong tri MANH ({b}B-{p}P)','do_tin_cay':88,'ket_tiep':'B','trong_so':85,'uu_tien':22,'la_vip':True}
        if br>=0.60: return {'id':'bcr_dom','ten':f'Banker thong tri ({b}B-{p}P)','do_tin_cay':78,'ket_tiep':'B','trong_so':74,'uu_tien':18}
        if br<=0.30: return {'id':'bcr_dom','ten':f'Player thong tri MANH ({p}P-{b}B)','do_tin_cay':88,'ket_tiep':'P','trong_so':85,'uu_tien':22,'la_vip':True}
        if br<=0.40: return {'id':'bcr_dom','ten':f'Player thong tri ({p}P-{b}B)','do_tin_cay':78,'ket_tiep':'P','trong_so':74,'uu_tien':18}
        return None

    # ─── Phan bo thong ke ───
    @staticmethod
    def detect_dist(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<20: return None
        recent=pb[-40:] if len(pb)>=40 else pb
        b=recent.count('B'); p=recent.count('P'); total=b+p
        if total==0: return None
        br=b/total
        if br>0.62: return {'id':'bcr_dist','ten':f'Phan bo B cao ({br:.0%})','do_tin_cay':80,'ket_tiep':'P','trong_so':75,'uu_tien':25}
        if br<0.38: return {'id':'bcr_dist','ten':f'Phan bo P cao ({1-br:.0%})','do_tin_cay':80,'ket_tiep':'B','trong_so':75,'uu_tien':25}
        return None

    # ─── Tan suat trong so ───
    @staticmethod
    def detect_freq_w(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<10: return None
        recent=pb[-20:]; wp=wb=0
        for i,c in enumerate(reversed(recent)):
            w=(i+1)**1.3
            if c=='P': wp+=w
            else: wb+=w
        if abs(wp-wb)>10:
            return {'id':'bcr_freq','ten':'Tan suat trong so','do_tin_cay':74,'ket_tiep':'P' if wp>wb else 'B','trong_so':70,'uu_tien':15}
        return None

    # ─── Markov bac 1 ───
    @staticmethod
    def markov1(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<5: return None
        last=pb[-1]; tr=defaultdict(int)
        for i in range(len(pb)-1):
            if pb[i]==last: tr[pb[i+1]]+=1
        if tr:
            pred=max(tr,key=tr.get); total=sum(tr.values())
            conf=min(82,50+(tr[pred]/total)*42)
            return {'id':'bcr_mk1','ten':'Markov bac 1','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':round(conf*0.85),'uu_tien':10}
        return None

    # ─── Markov bac 2 ───
    @staticmethod
    def markov2(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        last2=''.join(pb[-2:]); tr=defaultdict(int)
        for i in range(len(pb)-2):
            if ''.join(pb[i:i+2])==last2: tr[pb[i+2]]+=1
        if tr:
            pred=max(tr,key=tr.get); total=sum(tr.values())
            conf=min(80,48+(tr[pred]/total)*42)
            return {'id':'bcr_mk2','ten':'Markov bac 2','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':round(conf*0.8),'uu_tien':12}
        return None

    # ─── Markov bac 3 (MOI) ───
    @staticmethod
    def markov3(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<12: return None
        last3=''.join(pb[-3:]); tr=defaultdict(int)
        for i in range(len(pb)-3):
            if ''.join(pb[i:i+3])==last3: tr[pb[i+3]]+=1
        if tr and sum(tr.values())>=2:
            pred=max(tr,key=tr.get); total=sum(tr.values())
            conf=min(82,50+(tr[pred]/total)*42)
            return {'id':'bcr_mk3','ten':'Markov bac 3','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':round(conf*0.85),'uu_tien':14,'la_ai':True}
        return None

    # ─── AI Nhan dang mau ───
    @staticmethod
    def ai_pattern(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<12: return None
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        sp=sb=0
        if run>=5:
            if last=='B': sp+=35
            else: sb+=35
        elif run>=3:
            if last=='B': sb+=18
            else: sp+=18
        elif run==1:
            if last=='B': sb+=8
            else: sp+=8
        sb+=5
        if abs(sp-sb)>=10:
            pred='P' if sp>sb else 'B'
            conf=min(88,58+abs(sp-sb)*0.8)
            return {'id':'bcr_ai','ten':'AI Nhan dang mau','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':84,'uu_tien':30,'la_ai':True}
        return None

    # ─── AI N-gram (MOI) ───
    @staticmethod
    def ai_ngram(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<15: return None
        for n in range(3,6):
            if len(pb)<n+8: continue
            pat=''.join(pb[-n:]); occ={'P':0,'B':0}
            for i in range(len(pb)-n-1):
                if ''.join(pb[i:i+n])==pat: occ[pb[i+n]]+=1
            total=occ['P']+occ['B']
            if total>=3:
                ratio=abs(occ['P']-occ['B'])/total
                if ratio>=0.5:
                    pred='P' if occ['P']>occ['B'] else 'B'
                    conf=min(88,62+ratio*30)
                    return {'id':'bcr_ngram','ten':f'AI N-gram {n}','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':82,'uu_tien':28,'la_ai':True}
        return None

    # ─── AI Can bang tan so (MOI) ───
    @staticmethod
    def ai_freq_balance(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<12: return None
        r10=pb[-10:]; b10=r10.count('B'); p10=r10.count('P')
        if b10>=8: return {'id':'bcr_balance','ten':'AI Can bang (B qua nhieu)','do_tin_cay':84,'ket_tiep':'P','trong_so':82,'uu_tien':32,'la_ai':True}
        if p10>=8: return {'id':'bcr_balance','ten':'AI Can bang (P qua nhieu)','do_tin_cay':84,'ket_tiep':'B','trong_so':82,'uu_tien':32,'la_ai':True}
        if b10>=7: return {'id':'bcr_balance','ten':'AI Can bang tan so','do_tin_cay':78,'ket_tiep':'P','trong_so':76,'uu_tien':26,'la_ai':True}
        if p10>=7: return {'id':'bcr_balance','ten':'AI Can bang tan so','do_tin_cay':78,'ket_tiep':'B','trong_so':76,'uu_tien':26,'la_ai':True}
        return None

    # ─── AI Momentum (MOI) ───
    @staticmethod
    def ai_momentum(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<15: return None
        r5=pb[-5:]; r10=pb[-15:-5]
        rb5=r5.count('B')/5; rb10=r10.count('B')/10
        diff=rb5-rb10
        if diff>0.35: return {'id':'bcr_momentum','ten':'AI Momentum B tang','do_tin_cay':80,'ket_tiep':'B','trong_so':78,'uu_tien':24,'la_ai':True}
        if diff<-0.35: return {'id':'bcr_momentum','ten':'AI Momentum P tang','do_tin_cay':80,'ket_tiep':'P','trong_so':78,'uu_tien':24,'la_ai':True}
        return None

    # ─── VIP PRO - Baccarat Master ───
    @staticmethod
    def vip_master(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        sp=0.0; sb=0.0; reasons=[]
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        if run>=6:
            pred='P' if last=='B' else 'B'; w=run*3.5
            if pred=='P': sp+=w
            else: sb+=w
            reasons.append(f"Cau dai {run}{last}->DAO{pred}")
        elif run>=3:
            w=run*1.5
            if last=='P': sp+=w
            else: sb+=w
            reasons.append(f"Cau {run}{last}->THEO")
        for window,weight in [(5,2.5),(10,2.0),(20,1.5),(30,1.0)]:
            if len(pb)>=window:
                seg=pb[-window:]; b=seg.count('B'); p=seg.count('P'); total=b+p
                if total>0:
                    br=b/total
                    if br>=0.65: sp+=10*weight
                    elif br<=0.35: sb+=10*weight
        sb+=3; reasons.append("Loi the Banker +3")
        if len(h)>=1 and h[-1]=='T': sb+=8; reasons.append("Sau Tie->B +8")
        total=sp+sb
        if total==0: return None
        pred='P' if sp>=sb else 'B'
        ratio=max(sp,sb)/total
        conf=min(95,max(60,55+ratio*45))
        return {'id':'bcr_vip','ten':'VIP Master','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':95,'uu_tien':60,'la_vip':True,'diem_p':round(sp,1),'diem_b':round(sb,1),'ly_do':reasons[:4]}

    # ─── DU DOAN CHUAN - Tong hop da chieu ───
    @staticmethod
    def detect_du_doan_chuan(h):
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        sp=0.0; sb=0.0; signals=0
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        if run>=6:
            if last=='P': sb+=run*3.0
            else: sp+=run*3.0
            signals+=1
        elif run>=3:
            if last=='P': sp+=run*2.0
            else: sb+=run*2.0
            signals+=1
        elif run==1:
            if last=='P': sp+=3.0
            else: sb+=3.0
            signals+=1
        for window,weight in [(5,3.0),(10,2.0),(20,1.5)]:
            if len(pb)>=window:
                seg=pb[-window:]; bc=seg.count('B'); pc=seg.count('P')
                if bc+pc>0:
                    br=bc/(bc+pc)
                    if br>=0.65: sp+=8*weight; signals+=1
                    elif br<=0.35: sb+=8*weight; signals+=1
        if len(pb)>=15:
            r5=pb[-5:]; r10=pb[-15:-5]
            m=r5.count('B')/5-r10.count('B')/10
            if m>0.3: sb+=12; signals+=1
            elif m<-0.3: sp+=12; signals+=1
        runs=[]; cur=pb[0]; rl=1
        for i in range(1,len(pb)):
            if pb[i]==cur: rl+=1
            else: runs.append((cur,rl)); cur=pb[i]; rl=1
        runs.append((cur,rl))
        if len(runs)>=3:
            lens=[r[1] for r in runs[-5:]]
            if len(lens)>=3:
                if lens[-1]>lens[-2]>lens[-3]:
                    if runs[-1][0]=='P': sp+=8
                    else: sb+=8
                    signals+=1
                elif lens[-1]<lens[-2]<lens[-3]:
                    if runs[-1][0]=='P': sb+=6
                    else: sp+=6
                    signals+=1
        sb+=2
        if signals<1: return None
        total_score=sp+sb
        if total_score==0: return None
        pred='P' if sp>sb else 'B'
        ratio=max(sp,sb)/total_score
        conf=min(94,max(62,55+ratio*40+signals*2))
        return {'id':'bcr_chuan','ten':'Du doan chuan','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':94,'uu_tien':58,'la_vip':True,'la_ai':True}

    # ═══════════════════════════════════════════════════════════
    # 18 CÔNG THỨC BCR NÂNG CẤP (từ công thức bcr.txt)
    # Adapt từ phân tích tài chính sang dự đoán Baccarat
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def bcr_vip_plus(h):
        """BCR VIP+: Trọng số giảm dần theo thời gian - phiên gần đây quan trọng hơn"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<6: return None
        sp=sb=0.0
        n=min(len(pb),20)
        for i in range(n):
            w=1.5-i*0.05 if i<10 else 1.0
            idx=len(pb)-n+i
            if pb[idx]=='P': sp+=w
            else: sb+=w
        total=sp+sb
        if total==0 or abs(sp-sb)<1: return None
        pred='P' if sp>sb else 'B'
        conf=min(85,60+abs(sp-sb)/total*30)
        return {'id':'bcr_vip_plus','ten':'BCR VIP+ Trong so','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':78,'uu_tien':20}

    @staticmethod
    def bcr_omega(h):
        """BCR Omega: Đo lường tỷ lệ thắng/thua vượt ngưỡng"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<10: return None
        mar=0.5; wins_p=wins_b=0
        for i in range(len(pb)-1):
            seg=pb[max(0,i-4):i+1]; pr=seg.count('P')/len(seg)
            if pr>mar: wins_p+=pr-mar
            else: wins_b+=mar-pr
        if wins_b==0 and wins_p==0: return None
        if wins_p>wins_b*1.3:
            return {'id':'bcr_omega','ten':'BCR Omega->P','do_tin_cay':75,'ket_tiep':'P','trong_so':72,'uu_tien':18}
        if wins_b>wins_p*1.3:
            return {'id':'bcr_omega','ten':'BCR Omega->B','do_tin_cay':75,'ket_tiep':'B','trong_so':72,'uu_tien':18}
        return None

    @staticmethod
    def bcr_chuan_hoa_score(h):
        """BCR Chuẩn hóa: So sánh P/B ratio ở nhiều window"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<12: return None
        ratios=[]
        for w in [5,8,12,16,20]:
            if len(pb)>=w:
                seg=pb[-w:]
                r=seg.count('P')/w
                ratios.append(r)
        if not ratios: return None
        mn=min(ratios); mx=max(ratios)
        if mx==mn: return None
        norm=[(r-mn)/(mx-mn) for r in ratios]
        avg=sum(norm)/len(norm)
        if avg>0.65:
            return {'id':'bcr_chuan_hoa','ten':'BCR Chuan hoa->P','do_tin_cay':76,'ket_tiep':'P','trong_so':73,'uu_tien':16}
        if avg<0.35:
            return {'id':'bcr_chuan_hoa','ten':'BCR Chuan hoa->B','do_tin_cay':76,'ket_tiep':'B','trong_so':73,'uu_tien':16}
        return None

    @staticmethod
    def bcr_tong_sigma(h):
        """BCR Tổng Sigma: Phân tích đa chiều - chia history thành hàng/cột"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<12: return None
        sp=sb=0.0
        chunk_size=4
        n_chunks=min(len(pb)//chunk_size,5)
        for i in range(n_chunks):
            start=len(pb)-chunk_size*(n_chunks-i)
            seg=pb[start:start+chunk_size]
            w=1.0+i*0.3
            p_count=seg.count('P'); b_count=seg.count('B')
            sp+=p_count*w; sb+=b_count*w
        total=sp+sb
        if total==0 or abs(sp-sb)<2: return None
        pred='P' if sp>sb else 'B'
        conf=min(82,58+abs(sp-sb)/total*28)
        return {'id':'bcr_sigma','ten':'BCR Tong Sigma','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':76,'uu_tien':19}

    @staticmethod
    def bcr_ptpbt(h):
        """BCR PTPBT: Phân tích theo thời gian - BCR tích lũy"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        cum_p=cum_b=0; trend=[]
        for c in pb[-20:]:
            if c=='P': cum_p+=1
            else: cum_b+=1
            ratio=cum_p/(cum_p+cum_b) if (cum_p+cum_b)>0 else 0.5
            trend.append(ratio)
        if len(trend)<5: return None
        recent=sum(trend[-3:])/3; early=sum(trend[:3])/3
        if recent>early+0.1 and recent>0.55:
            return {'id':'bcr_ptpbt','ten':'BCR PTPBT xu huong P','do_tin_cay':77,'ket_tiep':'P','trong_so':74,'uu_tien':17}
        if recent<early-0.1 and recent<0.45:
            return {'id':'bcr_ptpbt','ten':'BCR PTPBT xu huong B','do_tin_cay':77,'ket_tiep':'B','trong_so':74,'uu_tien':17}
        return None

    @staticmethod
    def bcr_doi_xung(h):
        """BCR Đối xứng: Phân tích tính đối xứng của chuỗi"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<10: return None
        n=min(len(pb),20)
        recent=pb[-n:]
        half=n//2
        first=''.join(recent[:half]); second=''.join(recent[half:])
        fp=first.count('P'); sp2=second.count('P')
        if fp>sp2+2:
            return {'id':'bcr_dx','ten':'BCR Doi xung->B','do_tin_cay':74,'ket_tiep':'B','trong_so':70,'uu_tien':15}
        if sp2>fp+2:
            return {'id':'bcr_dx','ten':'BCR Doi xung->P','do_tin_cay':74,'ket_tiep':'P','trong_so':70,'uu_tien':15}
        return None

    @staticmethod
    def bcr_chu_ky(h):
        """BCR Chu kỳ: Phát hiện chu kỳ lặp lại"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        for cycle_len in range(2,6):
            if len(pb)<cycle_len*3: continue
            pattern=''.join(pb[-cycle_len:])
            matches=0
            for i in range(1,3):
                start=-cycle_len*(i+1); end=-cycle_len*i
                if ''.join(pb[start:end])==pattern: matches+=1
            if matches>=2:
                next_pos=len(pb)%cycle_len
                pred=pattern[next_pos] if next_pos<len(pattern) else pattern[0]
                if pred in ('P','B'):
                    return {'id':'bcr_chuky','ten':f'BCR Chu ky {cycle_len}','do_tin_cay':82,'ket_tiep':pred,'trong_so':80,'uu_tien':22}
        return None

    @staticmethod
    def bcr_boi_so(h):
        """BCR Bội số: Tích lũy nhân - phiên liên tiếp cùng bên tăng trọng số"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<6: return None
        tp=tb=1.0
        for i in range(max(0,len(pb)-10),len(pb)):
            w=1.0+(i-max(0,len(pb)-10))*0.1
            if pb[i]=='P': tp*=w
            else: tb*=w
        if tp==tb: return None
        pred='P' if tp>tb else 'B'
        ratio=max(tp,tb)/min(tp,tb) if min(tp,tb)>0 else 2
        if ratio<1.3: return None
        conf=min(80,60+ratio*5)
        return {'id':'bcr_boiso','ten':'BCR Boi so','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':74,'uu_tien':16}

    @staticmethod
    def bcr_pb_ratio(h):
        """BCR P/B Ratio: Tỷ lệ P/B giống P/B ratio tài chính"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<10: return None
        r5=pb[-5:]; r10=pb[-10:]
        p5=r5.count('P')/5; p10=r10.count('P')/10
        b5=1-p5; b10=1-p10
        pb_r=p5/b5 if b5>0 else 3
        if pb_r>1.8:
            return {'id':'bcr_pb_r','ten':'BCR PB Ratio P cao','do_tin_cay':78,'ket_tiep':'B','trong_so':74,'uu_tien':17}
        if pb_r<0.55:
            return {'id':'bcr_pb_r','ten':'BCR PB Ratio B cao','do_tin_cay':78,'ket_tiep':'P','trong_so':74,'uu_tien':17}
        return None

    @staticmethod
    def bcr_tong_hop_multi(h):
        """BCR Tổng hợp: Kết hợp nhiều tín hiệu nhỏ"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        votes_p=votes_b=0
        # Signal 1: Last 5
        r5=pb[-5:]
        if r5.count('P')>=4: votes_b+=1
        elif r5.count('B')>=4: votes_p+=1
        # Signal 2: Last 10
        if len(pb)>=10:
            r10=pb[-10:]
            if r10.count('P')>=7: votes_b+=1
            elif r10.count('B')>=7: votes_p+=1
        # Signal 3: Alternation
        if len(pb)>=4:
            alt=sum(1 for i in range(len(pb)-3,len(pb)) if pb[i]!=pb[i-1])
            if alt>=2:
                if pb[-1]=='P': votes_b+=1
                else: votes_p+=1
        # Signal 4: Last result
        if pb[-1]=='P': votes_p+=1
        else: votes_b+=1
        if votes_p==votes_b: return None
        pred='P' if votes_p>votes_b else 'B'
        conf=min(82,60+abs(votes_p-votes_b)*6)
        return {'id':'bcr_tonghop','ten':'BCR Tong hop da tin hieu','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':80,'uu_tien':25,'la_vip':True}

    @staticmethod
    def bcr_neural_simple(h):
        """BCR AI Neural: Mạng neural đơn giản dự đoán"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<10: return None
        # Feature extraction
        n=min(len(pb),20)
        recent=pb[-n:]
        f1=recent.count('P')/n  # P ratio
        f2=sum(1 for i in range(1,len(recent)) if recent[i]!=recent[i-1])/(n-1)  # Alternation rate
        last=recent[-1]; run=1
        for i in range(len(recent)-2,-1,-1):
            if recent[i]==last: run+=1
            else: break
        f3=run/n  # Run ratio
        f4=recent[-5:].count('P')/5 if len(recent)>=5 else 0.5  # Recent P ratio
        # Simple neural computation
        w=[0.3,-0.5,0.4,-0.2]; b=0.1
        score=sum(w[i]*[f1,f2,f3,f4][i] for i in range(4))+b
        # Sigmoid
        import math
        try: sig=1/(1+math.exp(-score*3))
        except: sig=0.5
        if sig>0.6:
            return {'id':'bcr_neural','ten':'BCR AI Neural->P','do_tin_cay':round(55+sig*30,1),'ket_tiep':'P','trong_so':82,'uu_tien':28,'la_ai':True}
        if sig<0.4:
            return {'id':'bcr_neural','ten':'BCR AI Neural->B','do_tin_cay':round(55+(1-sig)*30,1),'ket_tiep':'B','trong_so':82,'uu_tien':28,'la_ai':True}
        return None

    @staticmethod
    def bcr_nang_cao(h):
        """BCR Nâng cao: Điều chỉnh rủi ro + phát triển"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<12: return None
        sp=sb=0.0
        n=min(len(pb),20)
        for i in range(n):
            idx=len(pb)-n+i
            rui_ro=1-(0.05*i/n)  # Risk decreases over time
            phat_trien=1+(0.03*i)  # Development increases
            if pb[idx]=='P': sp+=rui_ro*phat_trien
            else: sb+=rui_ro*phat_trien
        total=sp+sb
        if total==0 or abs(sp-sb)/total<0.1: return None
        pred='P' if sp>sb else 'B'
        conf=min(82,60+abs(sp-sb)/total*25)
        return {'id':'bcr_nangcao','ten':'BCR Nang cao','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':78,'uu_tien':20}

    @staticmethod
    def bcr_pro_mc(h):
        """BCR Pro Monte Carlo: Mô phỏng nhiều kịch bản"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<8: return None
        import random as rng
        rng.seed(sum(1 if c=='P' else 0 for c in pb[-10:]))
        p_wins=b_wins=0
        n=min(len(pb),15)
        base_p=pb[-n:].count('P')/n
        for _ in range(100):
            noise=rng.uniform(-0.1,0.1)
            prob=base_p+noise
            if rng.random()<prob: p_wins+=1
            else: b_wins+=1
        if abs(p_wins-b_wins)<15: return None
        pred='P' if p_wins>b_wins else 'B'
        conf=min(85,55+abs(p_wins-b_wins)*0.3)
        return {'id':'bcr_pro_mc','ten':'BCR Pro Monte Carlo','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':82,'uu_tien':26,'la_ai':True}

    @staticmethod
    def bcr_gemini_local(h):
        """BCR AI Gemini Local: Phân tích đa tiêu chí"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<10: return None
        diem=0; pred_signals=[]
        # Tiêu chí 1: Xu hướng
        n=min(len(pb),20); recent=pb[-n:]
        if recent[-1]!=recent[0]:
            if recent.count('P')>recent.count('B'):
                diem+=15; pred_signals.append('P')
            else:
                diem+=15; pred_signals.append('B')
        # Tiêu chí 2: Ổn định
        r5=pb[-5:]
        if r5.count('P')>=4 or r5.count('B')>=4:
            diem+=20
            pred_signals.append('B' if r5.count('P')>=4 else 'P')
        # Tiêu chí 3: Cầu hiện tại
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        if run>=3:
            diem+=15
            pred_signals.append('B' if last=='P' else 'P')
        if diem<15 or not pred_signals: return None
        from collections import Counter
        mc=Counter(pred_signals).most_common(1)[0]
        pred=mc[0]; votes=mc[1]
        conf=min(85,55+diem*0.4)
        return {'id':'bcr_gemini_local','ten':'BCR Gemini Local','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':84,'uu_tien':30,'la_ai':True,'la_vip':True}

    @staticmethod
    def bcr_vo_han(h):
        """BCR Vô hạn: Phân tích xu hướng dài hạn không giới hạn"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<15: return None
        total_p=pb.count('P'); total_b=pb.count('B')
        total=total_p+total_b
        if total==0: return None
        long_ratio=total_p/total
        r10=pb[-10:]
        short_ratio=r10.count('P')/10
        if short_ratio>long_ratio+0.15 and short_ratio>0.6:
            return {'id':'bcr_vohan','ten':'BCR Vo han->B (P qua nhieu)','do_tin_cay':76,'ket_tiep':'B','trong_so':72,'uu_tien':18}
        if short_ratio<long_ratio-0.15 and short_ratio<0.4:
            return {'id':'bcr_vohan','ten':'BCR Vo han->P (B qua nhieu)','do_tin_cay':76,'ket_tiep':'P','trong_so':72,'uu_tien':18}
        return None

    @staticmethod
    def bcr_nguyen_to_an(h):
        """BCR Nguyên tố ẩn: Phát hiện pattern ẩn qua prime numbers"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<7: return None
        primes=[2,3,5,7,11,13]
        sp=sb=0
        for p in primes:
            if p<=len(pb):
                if pb[-p]=='P': sp+=1
                else: sb+=1
        if sp==sb: return None
        pred='P' if sp>sb else 'B'
        conf=min(78,58+abs(sp-sb)*5)
        return {'id':'bcr_nta','ten':'BCR Nguyen to an','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':72,'uu_tien':14}

    @staticmethod
    def bcr_pbpb_pattern(h):
        """BCR PBPB: Phân tích theo tỷ lệ phân bổ từng đoạn"""
        pb=BCRPatterns.normalize(h)
        if len(pb)<9: return None
        chunks=[]
        cs=3
        for i in range(0,min(len(pb),15),cs):
            seg=pb[-(i+cs):-i] if i>0 else pb[-cs:]
            if len(seg)==cs:
                chunks.append(seg.count('P')/cs)
        if len(chunks)<2: return None
        if chunks[0]>0.66 and chunks[1]<0.5:
            return {'id':'bcr_pbpb','ten':'BCR PBPB->B','do_tin_cay':74,'ket_tiep':'B','trong_so':70,'uu_tien':15}
        if chunks[0]<0.33 and chunks[1]>0.5:
            return {'id':'bcr_pbpb','ten':'BCR PBPB->P','do_tin_cay':74,'ket_tiep':'P','trong_so':70,'uu_tien':15}
        return None

    # ═══════════════════════════════════════════════════════════
    # 6 THUẬT TOÁN VIP PRO (từ code_02092026.py)
    # PhanTichCauBaccaratVIP - Phân tích cầu + Quản lý vốn
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def vip_thong_ke_cau(h):
        """VIP PRO 1: Phân tích cầu thống kê — tần suất + chuỗi + độ lệch lý thuyết"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<10: return None
        from collections import Counter
        ts=Counter(pb); n=len(pb)
        # Tỷ lệ lý thuyết: B=0.4587, P=0.4463
        p_ratio=ts.get('P',0)/n; b_ratio=ts.get('B',0)/n
        p_lech=p_ratio-0.4463; b_lech=b_ratio-0.4587
        # Nếu P xuất hiện quá nhiều so với lý thuyết → predict B (hồi quy trung bình)
        if p_lech>0.08:
            return {'id':'vip_tk','ten':'VIP Thong ke (P lech +)','do_tin_cay':80,'ket_tiep':'B','trong_so':82,'uu_tien':32,'la_vip':True}
        if b_lech>0.08:
            return {'id':'vip_tk','ten':'VIP Thong ke (B lech +)','do_tin_cay':80,'ket_tiep':'P','trong_so':82,'uu_tien':32,'la_vip':True}
        return None

    @staticmethod
    def vip_du_doan_ket_hop(h):
        """VIP PRO 2: Dự đoán kết hợp 3 phương pháp — tần suất + chuỗi + Markov"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<8: return None
        from collections import Counter
        votes={'P':0,'B':0}
        # PP1: Tần suất gần đây (10 phiên cuối)
        r10=pb[-10:] if len(pb)>=10 else pb
        ts=Counter(r10)
        dd_ts=max(ts,key=ts.get)
        votes[dd_ts]+=ts[dd_ts]/len(r10)
        # PP2: Chuỗi 3 phiên cuối — tìm lại trong lịch sử
        if len(pb)>=6:
            chuoi=''.join(pb[-3:])
            hits={'P':0,'B':0}
            for i in range(len(pb)-3):
                if ''.join(pb[i:i+3])==chuoi and i+3<len(pb):
                    hits[pb[i+3]]+=1
            total_hits=hits['P']+hits['B']
            if total_hits>=2:
                dd_c=max(hits,key=hits.get)
                votes[dd_c]+=hits[dd_c]/total_hits*0.8
        # PP3: Markov bậc 1
        last=pb[-1]; tr={'P':0,'B':0}
        for i in range(len(pb)-1):
            if pb[i]==last: tr[pb[i+1]]+=1
        total_tr=tr['P']+tr['B']
        if total_tr>0:
            dd_m=max(tr,key=tr.get)
            votes[dd_m]+=tr[dd_m]/total_tr*0.7
        total_v=votes['P']+votes['B']
        if total_v==0 or abs(votes['P']-votes['B'])<0.1: return None
        pred='P' if votes['P']>votes['B'] else 'B'
        conf=min(90,60+abs(votes['P']-votes['B'])/total_v*35)
        return {'id':'vip_kethop','ten':'VIP Ket hop 3PP','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':88,'uu_tien':45,'la_vip':True,'la_ai':True}

    @staticmethod
    def vip_kelly_signal(h):
        """VIP PRO 3: Tín hiệu Kelly — chỉ đặt khi xác suất đủ lớn"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<15: return None
        from collections import Counter
        ts=Counter(pb); n=len(pb)
        for side in ['P','B']:
            p=ts.get(side,0)/n
            b=0.95 if side=='B' else 1.0  # Hệ số trả thưởng
            q=1-p
            f_kelly=(p*b-q)/b if b>0 else 0
            if f_kelly>0.05:  # Kelly > 5% = tín hiệu mạnh
                conf=min(88,65+f_kelly*100)
                return {'id':'vip_kelly','ten':f'VIP Kelly->{side}','do_tin_cay':round(conf,1),'ket_tiep':side,'trong_so':84,'uu_tien':35,'la_vip':True}
        return None

    @staticmethod
    def vip_rui_ro(h):
        """VIP PRO 4: Đánh giá rủi ro — biến động cầu quyết định hướng đi"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<12: return None
        # Tính biến động
        n=len(pb); bien_dong=sum(1 for i in range(1,n) if pb[i]!=pb[i-1])
        ty_le_bd=bien_dong/(n-1)
        # Tìm chuỗi dài nhất
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        # Biến động cao (>65%) + chuỗi ngắn → cầu đảo → theo đảo
        if ty_le_bd>0.65 and run<=2:
            pred='B' if last=='P' else 'P'
            return {'id':'vip_ruiro','ten':'VIP Rui ro (BD cao->dao)','do_tin_cay':78,'ket_tiep':pred,'trong_so':76,'uu_tien':28,'la_vip':True}
        # Biến động thấp (<35%) + chuỗi dài → cầu bệt → theo cầu
        if ty_le_bd<0.35 and run>=3:
            return {'id':'vip_ruiro','ten':'VIP Rui ro (BD thap->theo)','do_tin_cay':80,'ket_tiep':last,'trong_so':78,'uu_tien':30,'la_vip':True}
        return None

    @staticmethod
    def vip_mo_phong(h):
        """VIP PRO 5: Mô phỏng nhanh — chạy 50 scenario dựa trên tỷ lệ hiện tại"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<10: return None
        import random as rng
        n=min(len(pb),20); recent=pb[-n:]
        base_p=recent.count('P')/n
        rng.seed(hash(tuple(recent[-5:])))
        p_wins=b_wins=0
        for _ in range(50):
            if rng.random()<base_p+rng.uniform(-0.05,0.05): p_wins+=1
            else: b_wins+=1
        if abs(p_wins-b_wins)<8: return None
        pred='P' if p_wins>b_wins else 'B'
        conf=min(82,55+abs(p_wins-b_wins)*0.5)
        return {'id':'vip_mophong','ten':'VIP Mo phong','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':78,'uu_tien':24,'la_ai':True}

    @staticmethod
    def vip_bao_cao(h):
        """VIP PRO 6: Báo cáo tổng hợp — kết hợp tất cả VIP signals"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<10: return None
        from collections import Counter
        signals={'P':0,'B':0}
        # Signal 1: Tần suất gần đây
        r8=pb[-8:]; ts=Counter(r8)
        if ts.get('P',0)>ts.get('B',0)+2: signals['B']+=1
        elif ts.get('B',0)>ts.get('P',0)+2: signals['P']+=1
        # Signal 2: Xu hướng
        if len(pb)>=15:
            r5=pb[-5:]; r10=pb[-15:-5]
            p5=r5.count('P')/5; p10=r10.count('P')/10
            if p5>p10+0.2: signals['B']+=1  # P đang tăng → có thể quay lại
            elif p5<p10-0.2: signals['P']+=1
        # Signal 3: Chuỗi hiện tại
        last=pb[-1]; run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        if run>=4:
            signals['P' if last=='B' else 'B']+=1  # Chuỗi dài → đảo
        elif run<=1:
            signals[last]+=1  # Vừa đổi → tiếp tục
        # Signal 4: Banker edge
        signals['B']+=0.5
        total=signals['P']+signals['B']
        if total<1.5 or abs(signals['P']-signals['B'])<0.5: return None
        pred='P' if signals['P']>signals['B'] else 'B'
        conf=min(90,58+abs(signals['P']-signals['B'])/total*35)
        return {'id':'vip_baocao','ten':'VIP Bao cao tong hop','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':90,'uu_tien':50,'la_vip':True,'la_ai':True}

    # ═══════════════════════════════════════════════════════════
    # CẦU PHỔ BIẾN BACCARAT — Nâng cấp VIP PRO
    # Các cầu phổ biến nhất trong Baccarat thực tế
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def cau_rong_P(h):
        """Cầu Rồng Player: P liên tục dài"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<4: return None
        run=0
        for c in reversed(pb):
            if c=='P': run+=1
            else: break
        if run>=7: return {'id':'rong_p','ten':f'Cau Rong P ({run}) -> BE','do_tin_cay':92,'ket_tiep':'B','trong_so':90,'uu_tien':run*3,'la_vip':True}
        if run>=5: return {'id':'rong_p','ten':f'Cau Rong P ({run})','do_tin_cay':82,'ket_tiep':'P','trong_so':78,'uu_tien':run*2}
        if run>=3: return {'id':'rong_p','ten':f'Cau P lien ({run})','do_tin_cay':70,'ket_tiep':'P','trong_so':66,'uu_tien':run}
        return None

    @staticmethod
    def cau_rong_B(h):
        """Cầu Rồng Banker: B liên tục dài"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<4: return None
        run=0
        for c in reversed(pb):
            if c=='B': run+=1
            else: break
        if run>=7: return {'id':'rong_b','ten':f'Cau Rong B ({run}) -> BE','do_tin_cay':92,'ket_tiep':'P','trong_so':90,'uu_tien':run*3,'la_vip':True}
        if run>=5: return {'id':'rong_b','ten':f'Cau Rong B ({run})','do_tin_cay':82,'ket_tiep':'B','trong_so':78,'uu_tien':run*2}
        if run>=3: return {'id':'rong_b','ten':f'Cau B lien ({run})','do_tin_cay':70,'ket_tiep':'B','trong_so':66,'uu_tien':run}
        return None

    @staticmethod
    def cau_mat_bead(h):
        """Cầu Mắt (Big Eye Boy): So sánh cột hiện tại với cột trước"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<6: return None
        # Chia thành các cột (runs)
        runs=[]; cur=pb[0]; rl=1
        for i in range(1,len(pb)):
            if pb[i]==cur: rl+=1
            else: runs.append((cur,rl)); cur=pb[i]; rl=1
        runs.append((cur,rl))
        if len(runs)<3: return None
        # So sánh cột cuối vs cột trước
        last_run=runs[-1]; prev_run=runs[-2]
        if last_run[1]==prev_run[1]:
            # Cùng độ dài → "đỏ" → cầu theo (tiếp tục cùng loại)
            return {'id':'mat_bead','ten':'Cau Mat (cung do dai) -> THEO','do_tin_cay':76,'ket_tiep':last_run[0],'trong_so':74,'uu_tien':20}
        else:
            # Khác độ dài → "xanh" → cầu đảo
            opp='P' if last_run[0]=='B' else 'B'
            return {'id':'mat_bead','ten':'Cau Mat (khac do dai) -> DAO','do_tin_cay':74,'ket_tiep':opp,'trong_so':72,'uu_tien':18}

    @staticmethod
    def cau_gian_doan(h):
        """Cầu Gián đoạn (Cockroach Road): So sánh với 2 cột trước"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<8: return None
        runs=[]; cur=pb[0]; rl=1
        for i in range(1,len(pb)):
            if pb[i]==cur: rl+=1
            else: runs.append((cur,rl)); cur=pb[i]; rl=1
        runs.append((cur,rl))
        if len(runs)<4: return None
        last=runs[-1]; two_back=runs[-3]
        if last[1]==two_back[1]:
            return {'id':'gian_doan','ten':'Cau Gian doan -> THEO','do_tin_cay':75,'ket_tiep':last[0],'trong_so':72,'uu_tien':18}
        else:
            opp='P' if last[0]=='B' else 'B'
            return {'id':'gian_doan','ten':'Cau Gian doan -> DAO','do_tin_cay':73,'ket_tiep':opp,'trong_so':70,'uu_tien':16}

    @staticmethod
    def cau_nhay_co(h):
        """Cầu Nhảy Cóc: P-B xen kẽ liên tục nhiều phiên"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<6: return None
        alt=0
        for i in range(len(pb)-1,max(len(pb)-8,0),-1):
            if pb[i]!=pb[i-1]: alt+=1
            else: break
        if alt>=6:
            return {'id':'nhay_co','ten':f'Cau Nhay Co ({alt}) -> TIEP','do_tin_cay':88,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':86,'uu_tien':alt*2,'la_vip':True}
        if alt>=4:
            return {'id':'nhay_co','ten':f'Cau Nhay Co ({alt})','do_tin_cay':80,'ket_tiep':'P' if pb[-1]=='B' else 'B','trong_so':78,'uu_tien':alt}
        return None

    @staticmethod
    def cau_xuyen(h):
        """Cầu Xuyên: Một bên thắng áp đảo rồi đột ngột đổi chiều"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<10: return None
        r10=pb[-10:]; r3=pb[-3:]
        p10=r10.count('P'); b10=r10.count('B')
        p3=r3.count('P'); b3=r3.count('B')
        # P áp đảo 10 phiên nhưng 3 phiên gần đây B lấy lại
        if p10>=7 and b3>=2:
            return {'id':'xuyen','ten':'Cau Xuyen (P->B)','do_tin_cay':82,'ket_tiep':'B','trong_so':80,'uu_tien':25,'la_vip':True}
        if b10>=7 and p3>=2:
            return {'id':'xuyen','ten':'Cau Xuyen (B->P)','do_tin_cay':82,'ket_tiep':'P','trong_so':80,'uu_tien':25,'la_vip':True}
        return None

    @staticmethod
    def cau_doi_ben(h):
        """Cầu Đôi Bên: Cân bằng P/B → dự đoán theo bên vừa thắng"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<12: return None
        r12=pb[-12:]
        p=r12.count('P'); b=r12.count('B')
        if abs(p-b)<=2:  # Rất cân bằng
            last=pb[-1]
            return {'id':'doi_ben','ten':'Cau Doi Ben (can bang)','do_tin_cay':72,'ket_tiep':last,'trong_so':68,'uu_tien':14}
        return None

    @staticmethod
    def cau_3_3_repeat(h):
        """Cầu 3-3 lặp: PPP BBB PPP BBB pattern"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<9: return None
        l9=''.join(pb[-9:])
        if l9 in ('PPPBBBPPP','BBBPPPBBB'):
            opp='B' if l9[-1]=='P' else 'P'
            return {'id':'cau33r','ten':'Cau 3-3 lap','do_tin_cay':86,'ket_tiep':opp,'trong_so':84,'uu_tien':22,'la_vip':True}
        l6=''.join(pb[-6:])
        if l6 in ('PPPBBB','BBBPPP'):
            return {'id':'cau33r','ten':'Cau 3-3','do_tin_cay':78,'ket_tiep':'P' if l6[-1]=='B' else 'B','trong_so':76,'uu_tien':14}
        return None

    @staticmethod
    def cau_tang_dan(h):
        """Cầu Tăng Dần: Chuỗi 1-2-3 hoặc 3-2-1"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<6: return None
        runs=[]; cur=pb[0]; rl=1
        for i in range(1,len(pb)):
            if pb[i]==cur: rl+=1
            else: runs.append(rl); cur=pb[i]; rl=1
        runs.append(rl)
        if len(runs)>=3:
            last3=runs[-3:]
            if last3[0]<last3[1]<last3[2]:  # 1,2,3 tăng dần
                return {'id':'tang_dan','ten':'Cau Tang Dan','do_tin_cay':78,'ket_tiep':pb[-1],'trong_so':76,'uu_tien':18}
            if last3[0]>last3[1]>last3[2]:  # 3,2,1 giảm dần
                opp='P' if pb[-1]=='B' else 'B'
                return {'id':'tang_dan','ten':'Cau Giam Dan','do_tin_cay':76,'ket_tiep':opp,'trong_so':74,'uu_tien':16}
        return None

    @staticmethod
    def cau_ping_pong(h):
        """Cầu Ping Pong: PPBB PPBB lặp lại"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<8: return None
        l8=''.join(pb[-8:])
        if l8 in ('PPBBPPBB','BBPPBBPP'):
            opp='P' if pb[-1]=='B' else 'B'
            return {'id':'ping_pong','ten':'Cau Ping Pong','do_tin_cay':85,'ket_tiep':opp,'trong_so':82,'uu_tien':22,'la_vip':True}
        l4=''.join(pb[-4:])
        if l4 in ('PPBB','BBPP'):
            return {'id':'ping_pong','ten':'Cau Ping Pong (4)','do_tin_cay':76,'ket_tiep':'P' if l4=='PPBB' else 'B','trong_so':74,'uu_tien':12}
        return None

    @staticmethod
    def du_doan_sieu_chuan(h):
        """DỰ ĐOÁN SIÊU CHUẨN: Tổng hợp tất cả tín hiệu với trọng số thông minh"""
        pb=[c for c in h if c in ('P','B')]
        if len(pb)<8: return None
        sp=sb=0.0; sig=0
        last=pb[-1]
        # 1. Chuỗi hiện tại (trọng số cao nhất)
        run=1
        for i in range(len(pb)-2,-1,-1):
            if pb[i]==last: run+=1
            else: break
        if run>=6: w=run*4; (sb if last=='P' else sp).__class__  # break predict
        if run>=6:
            if last=='P': sb+=run*4
            else: sp+=run*4
            sig+=2
        elif run>=3:
            if last=='P': sp+=run*2.5
            else: sb+=run*2.5
            sig+=1
        elif run==1:
            if last=='P': sp+=3
            else: sb+=3
            sig+=1
        # 2. Multi-window phân bố (5/10/15/20)
        for w,wt in [(5,4),(10,3),(15,2),(20,1.5)]:
            if len(pb)>=w:
                seg=pb[-w:]; pc=seg.count('P'); bc=seg.count('B')
                if pc+bc>0:
                    ratio=pc/(pc+bc)
                    if ratio>=0.7: sb+=8*wt; sig+=1
                    elif ratio<=0.3: sp+=8*wt; sig+=1
                    elif ratio>=0.6: sb+=4*wt; sig+=1
                    elif ratio<=0.4: sp+=4*wt; sig+=1
        # 3. Momentum (5 gần vs 10 xa)
        if len(pb)>=15:
            r5=pb[-5:]; r10=pb[-15:-5]
            m=r5.count('B')/5 - r10.count('B')/10
            if m>0.25: sb+=15; sig+=1
            elif m<-0.25: sp+=15; sig+=1
        # 4. Run length trend
        runs=[]; cur=pb[0]; rl=1
        for i in range(1,len(pb)):
            if pb[i]==cur: rl+=1
            else: runs.append((cur,rl)); cur=pb[i]; rl=1
        runs.append((cur,rl))
        if len(runs)>=3:
            lens=[r[1] for r in runs[-4:]]
            if len(lens)>=3:
                if lens[-1]>lens[-2]: sp+=6 if runs[-1][0]=='P' else 0; sb+=6 if runs[-1][0]=='B' else 0; sig+=1
                elif lens[-1]<lens[-2]: opp='B' if runs[-1][0]=='P' else 'P'; (sb if opp=='B' else sp).__class__; sig+=1
                if lens[-1]<lens[-2]:
                    if runs[-1][0]=='P': sb+=5
                    else: sp+=5
        # 5. Alternation rate
        if len(pb)>=6:
            alt_count=sum(1 for i in range(max(0,len(pb)-6),len(pb)-1) if pb[i]!=pb[i+1])
            if alt_count>=4:
                if last=='P': sb+=8
                else: sp+=8
                sig+=1
        # 6. Banker edge
        sb+=3
        # Final
        if sig<2: return None
        total=sp+sb
        if total==0: return None
        pred='P' if sp>sb else 'B'
        ratio=max(sp,sb)/total
        conf=min(96,max(65,55+ratio*42+sig*2))
        return {'id':'sieu_chuan','ten':'DU DOAN SIEU CHUAN','do_tin_cay':round(conf,1),'ket_tiep':pred,'trong_so':98,'uu_tien':70,'la_vip':True,'la_ai':True}

    # ─── DETECT ALL (NÂNG CẤP FULL VIP PRO) ───
    @staticmethod
    def detect_all(h):
        results=[]
        methods=[
            BCRPatterns.detect_cau_11, BCRPatterns.detect_cau_22,
            BCRPatterns.detect_cau_33, BCRPatterns.detect_cau_44,
            BCRPatterns.detect_cau_be, BCRPatterns.detect_cau_bet,
            BCRPatterns.detect_cau_12, BCRPatterns.detect_cau_21,
            BCRPatterns.detect_cau_31, BCRPatterns.detect_cau_13,
            BCRPatterns.detect_cau_41, BCRPatterns.detect_cau_14,
            BCRPatterns.detect_long_run, BCRPatterns.detect_after_tie,
            BCRPatterns.detect_bank_dom, BCRPatterns.detect_dist,
            BCRPatterns.detect_freq_w,
            BCRPatterns.markov1, BCRPatterns.markov2, BCRPatterns.markov3,
            BCRPatterns.ai_pattern, BCRPatterns.ai_ngram,
            BCRPatterns.ai_freq_balance, BCRPatterns.ai_momentum,
            BCRPatterns.vip_master, BCRPatterns.detect_du_doan_chuan,
            # 17 công thức BCR
            BCRPatterns.bcr_vip_plus, BCRPatterns.bcr_omega,
            BCRPatterns.bcr_chuan_hoa_score, BCRPatterns.bcr_tong_sigma,
            BCRPatterns.bcr_ptpbt, BCRPatterns.bcr_doi_xung,
            BCRPatterns.bcr_chu_ky, BCRPatterns.bcr_boi_so,
            BCRPatterns.bcr_pb_ratio, BCRPatterns.bcr_tong_hop_multi,
            BCRPatterns.bcr_neural_simple, BCRPatterns.bcr_nang_cao,
            BCRPatterns.bcr_pro_mc, BCRPatterns.bcr_gemini_local,
            BCRPatterns.bcr_vo_han, BCRPatterns.bcr_nguyen_to_an,
            BCRPatterns.bcr_pbpb_pattern,
            # 6 VIP PRO
            BCRPatterns.vip_thong_ke_cau, BCRPatterns.vip_du_doan_ket_hop,
            BCRPatterns.vip_kelly_signal, BCRPatterns.vip_rui_ro,
            BCRPatterns.vip_mo_phong, BCRPatterns.vip_bao_cao,
            # CẦU PHỔ BIẾN + DỰ ĐOÁN SIÊU CHUẨN
            BCRPatterns.cau_rong_P, BCRPatterns.cau_rong_B,
            BCRPatterns.cau_mat_bead, BCRPatterns.cau_gian_doan,
            BCRPatterns.cau_nhay_co, BCRPatterns.cau_xuyen,
            BCRPatterns.cau_doi_ben, BCRPatterns.cau_3_3_repeat,
            BCRPatterns.cau_tang_dan, BCRPatterns.cau_ping_pong,
            BCRPatterns.du_doan_sieu_chuan,
        ]
        for m in methods:
            try:
                r=m(h)
                if r: results.append(r)
            except: pass
        results.sort(key=lambda x:(x.get('uu_tien',0),x.get('trong_so',0)),reverse=True)
        return results

# ================================================================
# TONG HOP DU DOAN
# ================================================================
def tong_hop_tx(cac_mau):
    if not cac_mau: return None
    dt=dx=0; st=sx=0; vt=vx=0; at=ax=0; mm=cac_mau[0]
    for m in cac_mau:
        dcb=(m.get('trong_so',0)*m.get('do_tin_cay',0))/100
        hs=1.0
        if m.get('la_vip'): hs=max(hs,2.5)
        elif m.get('la_ai'): hs=max(hs,2.0)
        ten=m.get('ten','')
        if any(kw in ten for kw in ['Bet','Dao','Rong','Ho','Bien dong','Bridge','sau']):
            hs=max(hs,1.3)
        dc=dcb*hs
        if m.get('ket_tiep')=='T':
            dt+=dc; st+=1
            if m.get('la_vip'): vt+=1
            if m.get('la_ai'): at+=1
        elif m.get('ket_tiep')=='X':
            dx+=dc; sx+=1
            if m.get('la_vip'): vx+=1
            if m.get('la_ai'): ax+=1
    if vt>vx: dt*=1.15
    elif vx>vt: dx*=1.15
    if at>ax: dt*=1.1
    elif ax>at: dx*=1.1
    tong=dt+dx; dd='T' if dt>=dx else 'X'
    if tong>0:
        tl=max(dt,dx)/tong
        if vt>0 and vx==0 and dd=='T': dtc=min(98,75+tl*20)
        elif vx>0 and vt==0 and dd=='X': dtc=min(98,75+tl*20)
        else: dtc=min(96,max(55,50+tl*45))
    else: dtc=55
    return {'du_doan':dd,'do_tin_cay':round(dtc,1),'diem_tai':round(dt,1),'diem_xiu':round(dx,1),
            'so_thuat_toan_tai':st,'so_thuat_toan_xiu':sx,'vip_tai':vt,'vip_xiu':vx,
            'ai_tai':at,'ai_xiu':ax,'thuat_toan_manh_nhat':mm,'tong_mau':len(cac_mau),
            'la_vip':mm.get('la_vip',False),'la_ai':mm.get('la_ai',False)}

def tong_hop_bcr(patterns):
    """Tong hop BCR: DA SO PHIEU BAU quyet dinh ket qua.
    Ben nao co nhieu thuat toan du doan hon -> chon ben do.
    Trong so va do tin cay chi dung de tinh do chinh xac cuoi cung."""
    if not patterns: return None
    scores={'P':0.0,'B':0.0,'T':0.0}; counts={'P':0,'B':0,'T':0}
    vip={'P':0,'B':0,'T':0}; ai={'P':0,'B':0,'T':0}; strongest=patterns[0]
    for m in patterns:
        base=(m.get('trong_so',0)*m.get('do_tin_cay',0))/100
        hs=1.0
        if m.get('la_vip'): hs=max(hs,2.5)
        elif m.get('la_ai'): hs=max(hs,2.0)
        final=base*hs; kt=m.get('ket_tiep')
        if kt in scores:
            scores[kt]+=final; counts[kt]+=1
            if m.get('la_vip'): vip[kt]+=1
            if m.get('la_ai'): ai[kt]+=1
    total_votes=counts['P']+counts['B']
    if total_votes==0: return None
    # DA SO PHIEU BAU: ben nao nhieu thuat toan hon -> chon
    if counts['P']>counts['B']:
        pred='P'
    elif counts['B']>counts['P']:
        pred='B'
    else:
        # Hoa phieu -> dung diem so quyet dinh
        pred=max(scores,key=scores.get)
    # Tinh do tin cay dua tren ty le phieu + diem so
    vote_ratio=counts[pred]/total_votes if total_votes>0 else 0.5
    score_total=scores['P']+scores['B']
    score_ratio=scores[pred]/score_total if score_total>0 else 0.5
    # Ket hop ty le phieu (60%) + ty le diem (40%)
    combined=vote_ratio*0.6+score_ratio*0.4
    conf=min(96,max(55,48+combined*48))
    # Bonus neu VIP dong thuan
    if vip[pred]>=2: conf=min(98,conf+4)
    elif vip[pred]>=1 and vip.get('P' if pred=='B' else 'B',0)==0: conf=min(97,conf+3)
    if ai[pred]>=2: conf=min(97,conf+2)
    return {'du_doan':pred,'do_tin_cay':round(conf,1),
            'diem_p':round(scores['P'],1),'diem_b':round(scores['B'],1),
            'diem_t':round(scores['T'],1),
            'so_p':counts['P'],'so_b':counts['B'],'so_t':counts['T'],
            'vip_p':vip['P'],'vip_b':vip['B'],'ai_p':ai['P'],'ai_b':ai['B'],
            'thuat_toan_manh_nhat':strongest,'tong_mau':len(patterns),
            'la_vip':strongest.get('la_vip',False),'la_ai':strongest.get('la_ai',False)}

def du_doan_tx(ls):
    if not ls or len(ls)<3: return None, []
    cm = TXPatterns.detect_all(ls)
    dd = tong_hop_tx(cm)
    return dd, cm

def du_doan_bcr(h):
    if not h or len([c for c in h if c in ('P','B')])<3: return None, []
    patterns = BCRPatterns.detect_all(h)
    main = tong_hop_bcr(patterns)
    return main, patterns
