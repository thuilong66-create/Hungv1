#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 API CLIENT MODULE - VIP PRO WEB v4.3
21 Tool Tài Xỉu + Baccarat - API mới nhất
"""
import time
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

# ═══════════════════════════════════════════════
# CẤU HÌNH 21 TOOL TÀI XỈU (từ code_24082026.py)
# ═══════════════════════════════════════════════
TOOLS_CONFIG = {
    '68gb_hu': {'name': '68GB Hũ', 'full_name': '68GB - Tài Xỉu Hũ', 'nhom': '68GB', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/68gamebip/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    '68gb_md5': {'name': '68GB MD5', 'full_name': '68GB - Tài Xỉu MD5', 'nhom': '68GB', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/68gamebip/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'b52_hu': {'name': 'B52 Hũ', 'full_name': 'B52 - Tài Xỉu Hũ', 'nhom': 'B52', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/b52/hu/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'b52_md5': {'name': 'B52 MD5', 'full_name': 'B52 - Tài Xỉu MD5', 'nhom': 'B52', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/b52/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'b52_sicbo': {'name': 'B52 Sicbo', 'full_name': 'B52 - Sicbo Tài Xỉu', 'nhom': 'B52', 'loai': 'SICBO',
        'api_url': 'https://kwinstore.com/b52/sicbo/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore_sicbo'},
    'hit_hu': {'name': 'HitClub Hũ', 'full_name': 'HitClub - Tài Xỉu Hũ', 'nhom': 'HITCLUB', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/hitclub/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'hit_md5': {'name': 'HitClub MD5', 'full_name': 'HitClub - Tài Xỉu MD5', 'nhom': 'HITCLUB', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/hitclub/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'hit_sicbo': {'name': 'HitClub Sicbo', 'full_name': 'HitClub - Sicbo Tài Xỉu', 'nhom': 'HITCLUB', 'loai': 'SICBO',
        'api_url': 'https://kwinstore.com/hitclub/sicbo/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore_sicbo'},
    'max789_hu': {'name': 'Max789 Hũ', 'full_name': 'Max789 - Tài Xỉu Hũ', 'nhom': 'MAX789', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/max789/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'max789_md5': {'name': 'Max789 MD5', 'full_name': 'Max789 - Tài Xỉu MD5', 'nhom': 'MAX789', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/max789/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'rikvip_hu': {'name': 'Rikvip Hũ', 'full_name': 'Rikvip - Tài Xỉu Hũ', 'nhom': 'RIKVIP', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/rikvip/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'rikvip_md5': {'name': 'Rikvip MD5', 'full_name': 'Rikvip - Tài Xỉu MD5', 'nhom': 'RIKVIP', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/rikvip/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'rikvip_sicbo': {'name': 'Rikvip Sicbo', 'full_name': 'Rikvip - Sicbo Tài Xỉu', 'nhom': 'RIKVIP', 'loai': 'SICBO',
        'api_url': 'https://kwinstore.com/rikvip/sicbo/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore_sicbo'},
    'sumclub_hu': {'name': 'SumClub Hũ', 'full_name': 'SumClub - Tài Xỉu Hũ', 'nhom': 'SUMCLUB', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/sumclub/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'sumclub_md5': {'name': 'SumClub MD5', 'full_name': 'SumClub - Tài Xỉu MD5', 'nhom': 'SUMCLUB', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/sumclub/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'sunwin_tx': {'name': 'Sunwin TX', 'full_name': 'Sunwin - Tài Xỉu Thường', 'nhom': 'SUNWIN', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/sunwin/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'sunwin_sicbo': {'name': 'Sunwin Sicbo', 'full_name': 'Sunwin - Sicbo Tài Xỉu', 'nhom': 'SUNWIN', 'loai': 'SICBO',
        'api_url': 'https://kwinstore.com/sunwin/sicbo/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore_sicbo'},
    'lc79_hu': {'name': 'LC79 Hũ', 'full_name': 'LC79 - Tài Xỉu Hũ', 'nhom': 'LC79', 'loai': 'TX',
        'api_url': 'https://kwinstore.com/lc79/tx/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'lc79_md5': {'name': 'LC79 MD5', 'full_name': 'LC79 - Tài Xỉu MD5', 'nhom': 'LC79', 'loai': 'MD5',
        'api_url': 'https://kwinstore.com/lc79/md5/history/fab0615c0d32b17de5c45a5143640c1dbddc01fdf2ca1a29', 'parser': 'kwinstore'},
    'betvip_hu': {'name': 'BETVIP Hũ', 'full_name': 'BETVIP - Tài Xỉu Hũ', 'nhom': 'BETVIP', 'loai': 'TX',
        'api_url': 'https://wtx.macminim6.online/v1/tx/sessions', 'parser': 'tele68'},
    'betvip_md5': {'name': 'BETVIP MD5', 'full_name': 'BETVIP - Tài Xỉu MD5', 'nhom': 'BETVIP', 'loai': 'MD5',
        'api_url': 'https://wtxmd52.macminim6.online/v1/txmd5/sessions', 'parser': 'tele68'},
}

# API Baccarat
BCR_API = "https://bcf-ayt4.onrender.com/sexy/all"

# Ảnh game
GAME_IMAGES = {
    '68GB': 'https://i.ibb.co/S4TPspjJ/IMG-20260826-135222.jpg',
    'B52': 'https://i.ibb.co/BKtFRs37/IMG-20260826-135320.jpg',
    'HITCLUB': 'https://i.ibb.co/vxWppsF4/IMG-20260826-135300.jpg',
    'MAX789': 'https://i.ibb.co/Q7vN703F/IMG-20260826-135405.jpg',
    'RIKVIP': 'https://i.ibb.co/FLtmQzZJ/IMG-20260902-100653.jpg',
    'SUMCLUB': 'https://i.ibb.co/Q7vN703F/IMG-20260826-135405.jpg',
    'SUNWIN': 'https://i.ibb.co/S4TPspjJ/IMG-20260826-135222.jpg',
    'LC79': 'https://i.ibb.co/21g113nY/IMG-20260826-135238.jpg',
    'BETVIP': 'https://i.ibb.co/v68R7XYG/IMG-20260826-135348.jpg',
    'BACCARAT': 'https://i.ibb.co/WWMNJWCj/IMG-20260826-135430.jpg',
}

LOGO_URL = "https://i.postimg.cc/6Qgy45qM/IMG-20260821-091544.jpg"
QR_ZALOPAY = "https://i.postimg.cc/Y0KbjzYx/IMG-20260826-140021.jpg"

NHOM_TOOL = list(dict.fromkeys(cfg['nhom'] for cfg in TOOLS_CONFIG.values()))

# Cache
API_CACHE = {}
CACHE_TTL = 3

# ═══════════════════════════════════════════════
# PARSERS (cải tiến từ code_24082026.py)
# ═══════════════════════════════════════════════
def kq_to_char(r):
    if not r: return ''
    s = str(r).upper()
    if 'TAI' in s or s=='T' or 'TÀI' in s or 'BIG' in s or '大' in s: return 'T'
    if 'XIU' in s or s=='X' or 'XỈU' in s or 'SMALL' in s or '小' in s: return 'X'
    return ''

def find_list(obj):
    for k in ['data','Data','result','Result','list','List','items','Items',
              'history','History','sessions','Sessions','records','Records']:
        if k in obj:
            v=obj[k]
            if isinstance(v, list): return v
            if isinstance(v, dict):
                for k2 in ['list','List','items','Items','data','Data']:
                    if k2 in v and isinstance(v[k2], list): return v[k2]
    if 'data' in obj and isinstance(obj['data'], dict):
        return [obj['data']]
    for v in obj.values():
        if isinstance(v, list): return v
    return None

def parse_kwinstore(raw):
    arr = raw if isinstance(raw, list) else (find_list(raw) or [])
    out = []
    for p in arr:
        if not isinstance(p, dict): continue
        kq = ''
        for k in ['result','Result','kết quả','ket_qua','ketqua','kq','KQ','outcome','Outcome',
                  'type','Type','value','Value','big_small','tai_xiu','resultTruyenThong']:
            if k in p and p[k]:
                val = str(p[k])
                if val.lower() in ('đang chạy','đã có kết quả','pending','running','finished'): continue
                kq = val; break
        if not kq:
            d1=d2=d3=None
            for t1,t2,t3 in [('d1','d2','d3'),('xuc_xac_1','xuc_xac_2','xuc_xac_3'),
                            ('dice1','dice2','dice3'),('Dice1','Dice2','Dice3')]:
                if t1 in p and t2 in p and t3 in p:
                    d1,d2,d3=p.get(t1),p.get(t2),p.get(t3); break
            if d1 is None:
                for k in ['dices','Dices','dice','Dice','results','Results']:
                    if k in p and isinstance(p[k], list) and len(p[k])>=3:
                        d1,d2,d3=p[k][0],p[k][1],p[k][2]; break
            if d1 is not None:
                try:
                    tong=int(d1)+int(d2)+int(d3)
                    kq='TAI' if tong>10 else 'XIU'
                except: pass
        mp=''
        for k in ['session','Session','id','Id','ID','_id','round','Round','phiên','phien',
                  'code','Code','num','Num','number','Number','index','Index','gameNum']:
            if k in p and p[k]: mp=str(p[k]); break
        c=kq_to_char(kq)
        if c in ('T','X'):
            out.append({'ma_phien':mp,'ket_qua':c,'ket_qua_text':str(kq or '')})
    out.reverse()
    return out

def parse_kwinstore_sicbo(raw):
    arr = raw if isinstance(raw, list) else (find_list(raw) or [])
    out = []
    for p in arr:
        if not isinstance(p, dict): continue
        diem=None
        for k in ['score','Score','total','Total','sum','Sum','tong','Tong']:
            if k in p and p[k] is not None:
                try: diem=int(p[k]); break
                except: pass
        kq=''
        if diem is not None:
            if 4<=diem<=10: kq='XIU'
            elif 11<=diem<=17: kq='TAI'
            else: continue
        else:
            for k in ['result','Result','kq','KQ','outcome','Outcome','ket_qua','kết quả']:
                if k in p and p[k]: kq=p[k]; break
            if not kq:
                d1=d2=d3=None
                for t1,t2,t3 in [('d1','d2','d3'),('xuc_xac_1','xuc_xac_2','xuc_xac_3')]:
                    if t1 in p and t2 in p and t3 in p:
                        d1,d2,d3=p.get(t1),p.get(t2),p.get(t3); break
                if d1 is None:
                    for k in ['dices','Dices','faces','Faces','facesList','keyR']:
                        if k in p:
                            v=p[k]
                            if isinstance(v, list) and len(v)>=3:
                                d1,d2,d3=v[0],v[1],v[2]; break
                            if isinstance(v, str) and '-' in v:
                                try:
                                    parts=list(map(int,v.split('-')))
                                    if len(parts)>=3: d1,d2,d3=parts[0],parts[1],parts[2]; break
                                except: pass
                if d1 is not None:
                    try:
                        tong=int(d1)+int(d2)+int(d3)
                        if 4<=tong<=10: kq='XIU'
                        elif 11<=tong<=17: kq='TAI'
                        else: continue
                    except: pass
        mp=''
        for k in ['session','Session','id','Id','ID','round','Round','phiên','phien',
                  'gameNum','GameNum','code','Code']:
            if k in p and p[k]: mp=str(p[k]); break
        if mp.upper().startswith('S'): mp=mp[1:]
        c=kq_to_char(kq)
        if c in ('T','X'):
            ph={'ma_phien':mp,'ket_qua':c,'ket_qua_text':str(kq or '')}
            if diem is not None: ph['diem']=diem
            out.append(ph)
    out.reverse()
    return out

def parse_tele68(raw):
    arr = raw if isinstance(raw, list) else []
    if isinstance(raw, dict):
        if 'sessions' in raw and isinstance(raw['sessions'],list): arr=raw['sessions']
        elif 'data' in raw and isinstance(raw['data'],list): arr=raw['data']
        elif 'list' in raw and isinstance(raw['list'],list): arr=raw['list']
        else: arr=find_list(raw) or []
    out = []
    for p in arr:
        if not isinstance(p, dict): continue
        kq=''
        for k in ['result','big_small','tai_xiu','outcome','value','type','resultTruyenThong']:
            if k in p and p[k] is not None: kq=p[k]; break
        if not kq and 'total' in p and p['total'] is not None:
            try: kq='TAI' if int(p['total'])>10 else 'XIU'
            except: pass
        if not kq and 'dices' in p and isinstance(p['dices'], list) and len(p['dices'])>=3:
            try:
                tong=int(p['dices'][0])+int(p['dices'][1])+int(p['dices'][2])
                kq='TAI' if tong>10 else 'XIU'
            except: pass
        mp=''
        for k in ['id','session','session_id','round','code','number','num','_id']:
            if k in p and p[k] is not None: mp=str(p[k]); break
        c=kq_to_char(kq)
        if c in ('T','X'):
            out.append({'ma_phien':mp,'ket_qua':c,'ket_qua_text':str(kq or '')})
    out.reverse()
    return out

PARSERS = {'kwinstore': parse_kwinstore, 'kwinstore_sicbo': parse_kwinstore_sicbo, 'tele68': parse_tele68}

# ═══════════════════════════════════════════════
# API CALLS
# ═══════════════════════════════════════════════
def call_api(url, timeout=20):
    try:
        h={'Accept':'application/json','Cache-Control':'no-cache',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
           'Origin':'https://kwinstore.com','Referer':'https://kwinstore.com/'}
        r=requests.get(url, timeout=timeout, headers=h, verify=False)
        if r.status_code==200: return r.json()
        return None
    except:
        return None

def get_tool_data(tid):
    if tid not in TOOLS_CONFIG: return None
    cfg=TOOLS_CONFIG[tid]
    now=time.time()
    if tid in API_CACHE and now-API_CACHE[tid]['time']<CACHE_TTL:
        return API_CACHE[tid]['data']
    raw=call_api(cfg['api_url'])
    pf=PARSERS.get(cfg['parser'], parse_kwinstore)
    ph=pf(raw) if raw else []
    ls=[p['ket_qua'] for p in ph]
    pc=ph[-1]['ma_phien'] if ph else ''
    res={'tool_id':tid,'name':cfg['name'],'full_name':cfg['full_name'],
         'nhom':cfg['nhom'],'loai':cfg['loai'],'lich_su':ls,
         'cac_phien':ph,'phien':pc,'so_phien':len(ph)}
    API_CACHE[tid]={'time':now,'data':res}
    return res

def get_bcr_data():
    now=time.time()
    cache_key='_bcr_all'
    if cache_key in API_CACHE and now-API_CACHE[cache_key]['time']<CACHE_TTL:
        return API_CACHE[cache_key]['data']
    try:
        raw=call_api(BCR_API, timeout=15)
        if not raw: return None
        tables=[]
        for item in raw:
            ban=item.get('ban','')
            cau=item.get('cau','')
            kq=item.get('ket_qua','')
            phien=item.get('phien',0)
            gio=item.get('time','')
            history=list(kq.upper())
            if not cau:
                pb=[c for c in history if c in ('P','B')]
                if len(pb)>=5:
                    dao=sum(1 for i in range(1,len(pb)) if pb[i]!=pb[i-1])
                    if dao/(len(pb)-1)>=0.7: cau='Cầu đảo'
                    else: cau='Cầu bình thường'
                else: cau='Chưa rõ'
            tables.append({'ban':ban,'cau':cau,'history':history,'phien':phien,'gio':gio,'so_phien':len(history)})
        def sort_key(b):
            ban=b['ban']
            try:
                if ban.startswith('C'): return (100,int(ban[1:]))
                return (0,int(ban))
            except: return (50,0)
        tables.sort(key=sort_key)
        API_CACHE[cache_key]={'time':now,'data':tables}
        return tables
    except:
        return None

def tools_by_group():
    g={}
    for tid,cfg in TOOLS_CONFIG.items():
        n=cfg['nhom']
        if n not in g: g[n]=[]
        g[n].append({'id':tid,'name':cfg['name'],'full_name':cfg['full_name'],'loai':cfg['loai']})
    return g
