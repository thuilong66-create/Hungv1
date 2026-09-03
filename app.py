#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VIP PRO AI 5.0 — Premium Prediction Web UI (Flask)"""
import os, time
from functools import wraps
from datetime import datetime
from flask import Flask, request, redirect, url_for, session, flash, abort

from database import (PACKAGES, BANK_INFO, register_user, login_user, get_user,
    check_key, activate_key, create_key, create_deposit, get_user_deposits,
    get_pending, approve_deposit, reject_deposit, get_all_users, get_all_keys, stats)
from api_client import (TOOLS_CONFIG, GAME_IMAGES, LOGO_URL, QR_ZALOPAY,
    get_tool_data, get_bcr_data, tools_by_group)
from algorithms import du_doan_tx, du_doan_bcr

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vippro-ai50-secret-2026")
app.config["SESSION_PERMANENT"] = False

# ═══════════════ HELPERS ═══════════════
def login_required(f):
    @wraps(f)
    def w(*a, **kw):
        if 'user_id' not in session: flash('Vui lòng đăng nhập','warning'); return redirect(url_for('login'))
        return f(*a, **kw)
    return w

def admin_required(f):
    @wraps(f)
    def w(*a, **kw):
        if not session.get('is_admin'): abort(403)
        return f(*a, **kw)
    return w

def key_required(f):
    @wraps(f)
    def w(*a, **kw):
        uid = session.get('user_id')
        if not uid: return redirect(url_for('login'))
        k = check_key(uid)
        if not k: flash('Bạn cần kích hoạt key VIP để sử dụng','warning'); return redirect(url_for('payment'))
        return f(*a, **kw)
    return w

def fmoney(v):
    try: return f"{int(v):,}đ".replace(",",".")
    except: return str(v)

def CSS():
    return '''*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:14px;scroll-behavior:smooth}
body{font-family:-apple-system,system-ui,'Inter',sans-serif;background:#030712;color:#e2e8f0;min-height:100vh;line-height:1.6;
background-image:radial-gradient(ellipse at 20% 50%,rgba(99,102,241,.08) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(139,92,246,.06) 0%,transparent 50%),radial-gradient(ellipse at 50% 80%,rgba(244,63,94,.04) 0%,transparent 50%)}
a{color:#818cf8;text-decoration:none}a:hover{color:#a5b4fc}
.mono{font-family:'SF Mono','Fira Code',monospace}
.container{max-width:1200px;margin:0 auto;padding:20px 16px}
.glass{background:rgba(8,8,24,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(99,102,241,.15);border-radius:16px;padding:24px}
.glass:hover{border-color:rgba(99,102,241,.3)}
.btn{display:inline-block;padding:10px 24px;border-radius:12px;border:none;cursor:pointer;font-weight:600;font-size:.95rem;transition:all .3s;text-align:center}
.btn-primary{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;box-shadow:0 4px 15px rgba(99,102,241,.3)}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(99,102,241,.5);color:#fff}
.btn-outline{background:transparent;border:1px solid rgba(99,102,241,.4);color:#a5b4fc}
.btn-outline:hover{background:rgba(99,102,241,.1);border-color:#6366f1}
.btn-danger{background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff}
.btn-success{background:linear-gradient(135deg,#10b981,#059669);color:#fff}
input[type=text],input[type=password],input[type=number],select,textarea{width:100%;padding:12px 16px;background:rgba(15,15,35,.8);border:1px solid rgba(99,102,241,.2);border-radius:12px;color:#e2e8f0;font-size:.95rem;transition:border-color .3s,box-shadow .3s}
input:focus,select:focus,textarea:focus{outline:none;border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.15)}
label{display:block;margin-bottom:6px;color:#94a3b8;font-weight:500;font-size:.85rem}
.grid{display:grid;gap:20px}.grid-2{grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.text-center{text-align:center}.mt-1{margin-top:8px}.mt-2{margin-top:16px}.mt-3{margin-top:24px}.mb-2{margin-bottom:16px}
.flex{display:flex;align-items:center;gap:12px}.flex-between{display:flex;justify-content:space-between;align-items:center}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:600}
.badge-vip{background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#1a1a2e}
.badge-ai{background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff}
.badge-core{background:rgba(99,102,241,.15);color:#818cf8;border:1px solid rgba(99,102,241,.3)}
.badge-rose{background:rgba(244,63,94,.15);color:#fb7185;border:1px solid rgba(244,63,94,.3)}
.badge-blue{background:rgba(59,130,246,.15);color:#60a5fa;border:1px solid rgba(59,130,246,.3)}
.badge-green{background:rgba(16,185,129,.15);color:#34d399;border:1px solid rgba(16,185,129,.3)}
/* NAV */
.nav{background:rgba(8,8,24,.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(99,102,241,.1);padding:12px 0;position:sticky;top:0;z-index:100}
.nav .inner{max-width:1200px;margin:0 auto;padding:0 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
.nav-logo{font-weight:800;font-size:1.15rem;background:linear-gradient(135deg,#6366f1,#8b5cf6,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.nav-links{display:flex;gap:6px;flex-wrap:wrap}.nav-links a{padding:6px 14px;border-radius:8px;color:#94a3b8;font-size:.85rem;transition:all .2s}
.nav-links a:hover,.nav-links a.active{background:rgba(99,102,241,.1);color:#a5b4fc}
/* FLASH */
.flash{padding:12px 20px;border-radius:12px;margin-bottom:16px;font-size:.9rem;border:1px solid}
.flash-success{background:rgba(16,185,129,.1);border-color:rgba(16,185,129,.3);color:#34d399}
.flash-warning{background:rgba(251,191,36,.1);border-color:rgba(251,191,36,.3);color:#fbbf24}
.flash-error,.flash-danger{background:rgba(239,68,68,.1);border-color:rgba(239,68,68,.3);color:#f87171}
/* PREDICTION BALL */
.pred-ball{width:130px;height:130px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2rem;font-weight:900;margin:0 auto;position:relative}
.pred-ball.tai{background:linear-gradient(135deg,#f43f5e,#e11d48);box-shadow:0 0 30px rgba(244,63,94,.4),0 0 60px rgba(244,63,94,.2);animation:pulseRose 2s infinite}
.pred-ball.xiu{background:linear-gradient(135deg,#3b82f6,#2563eb);box-shadow:0 0 30px rgba(59,130,246,.4),0 0 60px rgba(59,130,246,.2);animation:pulseBlue 2s infinite}
.pred-ball.banker{background:linear-gradient(135deg,#f43f5e,#e11d48);box-shadow:0 0 30px rgba(244,63,94,.4),0 0 60px rgba(244,63,94,.2);animation:pulseRose 2s infinite}
.pred-ball.player{background:linear-gradient(135deg,#3b82f6,#2563eb);box-shadow:0 0 30px rgba(59,130,246,.4),0 0 60px rgba(59,130,246,.2);animation:pulseBlue 2s infinite}
@keyframes pulseRose{0%,100%{box-shadow:0 0 30px rgba(244,63,94,.4),0 0 60px rgba(244,63,94,.2)}50%{box-shadow:0 0 40px rgba(244,63,94,.6),0 0 80px rgba(244,63,94,.3)}}
@keyframes pulseBlue{0%,100%{box-shadow:0 0 30px rgba(59,130,246,.4),0 0 60px rgba(59,130,246,.2)}50%{box-shadow:0 0 40px rgba(59,130,246,.6),0 0 80px rgba(59,130,246,.3)}}
/* SMALL BALLS */
.hball{width:30px;height:30px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700;margin:2px}
.hball.t,.hball.b{background:rgba(244,63,94,.2);color:#fb7185;border:1px solid rgba(244,63,94,.4)}
.hball.x,.hball.p{background:rgba(59,130,246,.2);color:#60a5fa;border:1px solid rgba(59,130,246,.4)}
/* CONFIDENCE RING */
.conf-ring{position:relative;width:90px;height:90px;margin:0 auto}
.conf-ring svg{transform:rotate(-90deg)}.conf-ring .val{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:1.1rem;font-weight:800;color:#e2e8f0}
/* SCORE BAR */
.score-bar{height:8px;border-radius:4px;background:rgba(30,30,60,.6);overflow:hidden;margin-top:6px}
.score-fill{height:100%;border-radius:4px;transition:width .6s}
.score-fill.rose{background:linear-gradient(90deg,#f43f5e,#fb7185)}.score-fill.blue{background:linear-gradient(90deg,#3b82f6,#60a5fa)}
/* TABLE */
table{width:100%;border-collapse:collapse}th{text-align:left;padding:10px 12px;color:#94a3b8;font-size:.8rem;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid rgba(99,102,241,.1)}
td{padding:10px 12px;border-bottom:1px solid rgba(99,102,241,.06);font-size:.88rem}
tr:nth-child(even){background:rgba(99,102,241,.03)}tr:hover{background:rgba(99,102,241,.07)}
/* GAME CARD */
.game-card{position:relative;overflow:hidden;transition:transform .3s,box-shadow .3s;cursor:pointer}
.game-card:hover{transform:translateY(-4px);box-shadow:0 8px 30px rgba(99,102,241,.2)}
.game-card img{width:100%;height:140px;object-fit:cover;border-radius:12px 12px 0 0}
.game-card .info{padding:16px}
/* THREE DOT MENU */
.menu-wrap{position:relative;display:inline-block}.menu-btn{background:none;border:none;color:#94a3b8;font-size:1.2rem;cursor:pointer;padding:4px 8px}
.menu-btn:hover{color:#e2e8f0}.menu-drop{display:none;position:absolute;right:0;top:100%;min-width:180px;background:rgba(15,15,35,.95);backdrop-filter:blur(20px);border:1px solid rgba(99,102,241,.2);border-radius:12px;padding:6px;z-index:50;box-shadow:0 8px 30px rgba(0,0,0,.5)}
.menu-drop a{display:block;padding:8px 14px;border-radius:8px;color:#cbd5e1;font-size:.85rem}.menu-drop a:hover{background:rgba(99,102,241,.1);color:#a5b4fc}
.menu-wrap:hover .menu-drop{display:block}
/* GRADIENT BORDER */
.glow-border{position:relative;border:none;padding:2px;background:linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899,#6366f1);background-size:300% 300%;animation:gradBorder 4s ease infinite;border-radius:18px}
.glow-border>.inner{background:rgba(8,8,24,.92);border-radius:16px;padding:24px}
@keyframes gradBorder{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
/* HEADER PARTICLES (pseudo) */
.hero{position:relative;overflow:hidden;padding:60px 20px;text-align:center}
.hero::before,.hero::after{content:'';position:absolute;border-radius:50%;opacity:.15}
.hero::before{width:300px;height:300px;background:radial-gradient(circle,#6366f1,transparent);top:-80px;left:-60px}
.hero::after{width:250px;height:250px;background:radial-gradient(circle,#8b5cf6,transparent);bottom:-60px;right:-40px}
/* STATUS DOT */
.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e;margin-right:6px;animation:statusPulse 2s infinite}
@keyframes statusPulse{0%,100%{box-shadow:0 0 0 0 rgba(34,197,94,.6)}50%{box-shadow:0 0 0 6px rgba(34,197,94,0)}}
/* FADE IN */
.fade-in{animation:fadeIn .6s ease}@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
/* PKG CARD */
.pkg-card{text-align:center;transition:transform .3s}.pkg-card:hover{transform:translateY(-4px)}
.pkg-price{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#fbbf24,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
/* RESPONSIVE */
@media(max-width:640px){.container{padding:12px 10px}.glass{padding:16px}.grid-2{grid-template-columns:1fr}.pred-ball{width:100px;height:100px;font-size:1.6rem}}'''

def nav_html(user=None):
    links = ''
    if user:
        links = f'''<a href="/home">Trang chủ</a><a href="/baccarat">Baccarat</a>
<a href="/payment">Nạp tiền</a><a href="/activate-key">Key</a><a href="/my-keys">Key của tôi</a>'''
        if user.get('is_admin'): links += '<a href="/admin">Admin</a>'
        links += f'<a href="/logout">Đăng xuất</a>'
    else:
        links = '<a href="/login">Đăng nhập</a><a href="/register">Đăng ký</a>'
    return f'<nav class="nav"><div class="inner"><a href="/" class="nav-logo">VIP PRO AI 5.0</a><div class="nav-links">{links}</div></div></nav>'

def flashes():
    h = ''
    msgs = []
    try:
        from flask import get_flashed_messages
        msgs = get_flashed_messages(with_categories=True)
    except: pass
    for cat, msg in msgs:
        c = cat if cat in ('success','warning','error','danger') else 'success'
        h += f'<div class="flash flash-{c}">{msg}</div>'
    return h

def page(title, body, user=None):
    return f'''<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — VIP PRO AI 5.0</title><style>{CSS()}</style></head>
<body>{nav_html(user)}<div class="container fade-in">{flashes()}{body}</div></body></html>'''

def get_sess_user():
    uid = session.get('user_id')
    if not uid: return None
    u = get_user(uid)
    if u: u['is_admin'] = session.get('is_admin', False)
    return u

def conf_ring(val, color='#6366f1'):
    v = min(100, max(0, float(val)))
    circ = 251.2
    off = circ * (1 - v / 100)
    return f'''<div class="conf-ring"><svg width="90" height="90"><circle cx="45" cy="45" r="40" fill="none" stroke="rgba(99,102,241,.15)" stroke-width="6"/>
<circle cx="45" cy="45" r="40" fill="none" stroke="{color}" stroke-width="6" stroke-dasharray="{circ}" stroke-dashoffset="{off}" stroke-linecap="round"/></svg>
<div class="val">{v:.0f}%</div></div>'''

def hist_balls(ls, limit=50, tx=True):
    h = ''
    for c in ls[-limit:]:
        cu = c.upper()
        if tx:
            cls = 't' if cu == 'T' else 'x'
            lbl = 'T' if cu == 'T' else 'X'
        else:
            cls = 'b' if cu == 'B' else 'p'
            lbl = cu
        h += f'<span class="hball {cls}">{lbl}</span>'
    return h

# ═══════════════ ROUTES ═══════════════

# 1. Landing
@app.route('/')
def index():
    body = f'''<div class="hero">
<div style="position:relative;z-index:1">
<div style="font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6,#a78bfa,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px">VIP PRO AI 5.0</div>
<p style="color:#94a3b8;font-size:1.15rem;margin-bottom:32px">Hệ Thống Dự Đoán Trí Tuệ Nhân Tạo</p>
<div class="grid grid-3" style="max-width:700px;margin:0 auto 36px">
<div class="glass text-center" style="padding:20px"><div style="font-size:2rem;font-weight:800;color:#8b5cf6">43</div><div style="color:#94a3b8;font-size:.85rem">BCR Algorithms</div></div>
<div class="glass text-center" style="padding:20px"><div style="font-size:2rem;font-weight:800;color:#6366f1">34</div><div style="color:#94a3b8;font-size:.85rem">TX Algorithms</div></div>
<div class="glass text-center" style="padding:20px"><div style="font-size:2rem;font-weight:800;color:#a78bfa">21</div><div style="color:#94a3b8;font-size:.85rem">Tools</div></div>
</div>
<div class="flex" style="justify-content:center;gap:16px;flex-wrap:wrap">
<a href="/login" class="btn btn-primary" style="min-width:160px">Đăng Nhập</a>
<a href="/register" class="btn btn-outline" style="min-width:160px">Đăng Ký</a>
</div></div></div>'''
    return page('Trang chủ', body)

# 2. Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username','').strip()
        p = request.form.get('password','')
        if not u or not p: flash('Vui lòng nhập đầy đủ','warning'); return redirect(url_for('login'))
        ok, res = login_user(u, p)
        if ok:
            session['user_id'] = res['user_id']; session['username'] = res['username']
            session['is_admin'] = res.get('is_admin', False)
            flash(f'Chào mừng {res["username"]}!','success'); return redirect(url_for('home'))
        flash(res, 'error'); return redirect(url_for('login'))
    body = '''<div style="max-width:420px;margin:60px auto"><div class="glass text-center">
<h2 style="margin-bottom:24px;font-weight:800;font-size:1.5rem">Đăng Nhập</h2>
<form method="post"><div class="mb-2"><label>Tên đăng nhập</label><input type="text" name="username" required></div>
<div class="mb-2"><label>Mật khẩu</label><input type="password" name="password" required></div>
<button type="submit" class="btn btn-primary" style="width:100%;margin-top:8px">Đăng Nhập</button></form>
<p class="mt-2" style="color:#94a3b8;font-size:.85rem">Chưa có tài khoản? <a href="/register">Đăng ký ngay</a></p>
</div></div>'''
    return page('Đăng Nhập', body)

# 3. Register
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username','').strip()
        p = request.form.get('password','')
        fn = request.form.get('full_name','').strip()
        if not u or not p: flash('Vui lòng nhập đầy đủ','warning'); return redirect(url_for('register'))
        if len(u) < 3: flash('Tên đăng nhập ít nhất 3 ký tự','warning'); return redirect(url_for('register'))
        if len(p) < 4: flash('Mật khẩu ít nhất 4 ký tự','warning'); return redirect(url_for('register'))
        ok, msg = register_user(u, p, fn)
        if ok: flash(msg, 'success'); return redirect(url_for('login'))
        flash(msg, 'error'); return redirect(url_for('register'))
    body = '''<div style="max-width:420px;margin:60px auto"><div class="glass text-center">
<h2 style="margin-bottom:24px;font-weight:800;font-size:1.5rem">Đăng Ký Tài Khoản</h2>
<form method="post"><div class="mb-2"><label>Tên đăng nhập</label><input type="text" name="username" required></div>
<div class="mb-2"><label>Họ tên</label><input type="text" name="full_name"></div>
<div class="mb-2"><label>Mật khẩu</label><input type="password" name="password" required></div>
<button type="submit" class="btn btn-primary" style="width:100%;margin-top:8px">Đăng Ký</button></form>
<p class="mt-2" style="color:#94a3b8;font-size:.85rem">Đã có tài khoản? <a href="/login">Đăng nhập</a></p>
</div></div>'''
    return page('Đăng Ký', body)

# 4. Logout
@app.route('/logout')
def logout():
    session.clear(); flash('Đã đăng xuất','success'); return redirect(url_for('index'))

# 5. Home / Dashboard
@app.route('/home')
@login_required
def home():
    user = get_sess_user()
    uname = session.get('username','User')
    uid = session.get('user_id')
    k = check_key(uid)
    groups = tools_by_group()
    # Welcome
    h = f'''<div class="flex-between mb-2" style="flex-wrap:wrap;gap:12px">
<div><h1 style="font-size:1.6rem;font-weight:800">Xin chào, {uname}!</h1>
<p style="color:#94a3b8;font-size:.9rem"><span class="badge badge-ai">AI 5.0</span> <span class="status-dot"></span>ĐANG HOẠT ĐỘNG</p></div></div>'''
    # Key warning
    if not k:
        h += '''<div class="glow-border mt-2 mb-2"><div class="inner" style="text-align:center">
<p style="font-size:1.1rem;font-weight:700;color:#fbbf24;margin-bottom:8px">Chưa có Key VIP</p>
<p style="color:#94a3b8;font-size:.88rem;margin-bottom:12px">Vui lòng nạp tiền và kích hoạt key để sử dụng đầy đủ tính năng</p>
<a href="/payment" class="btn btn-primary">Nạp Tiền Ngay</a></div></div>'''
    # Game cards
    h += '<div class="grid grid-2 mt-3">'
    for nhom, tools in groups.items():
        img = GAME_IMAGES.get(nhom, LOGO_URL)
        first_id = tools[0]['id'] if tools else ''
        menu = ''.join(f'<a href="/tool/{t["id"]}">{t["name"]} <span class="badge badge-core" style="font-size:.65rem">{t["loai"]}</span></a>' for t in tools)
        h += f'''<div class="glass game-card" onclick="location.href='/tool/{first_id}'" style="padding:0">
<img src="{img}" alt="{nhom}" onerror="this.style.display='none'">
<div class="info"><div class="flex-between">
<div><h3 style="font-weight:700;font-size:1.05rem">{nhom}</h3>
<p style="color:#94a3b8;font-size:.8rem">{len(tools)} công cụ AI</p></div>
<div class="menu-wrap" onclick="event.stopPropagation()"><button class="menu-btn">&#8942;</button>
<div class="menu-drop">{menu}</div></div></div></div></div>'''
    # Baccarat card
    h += f'''<div class="glass game-card" onclick="location.href='/baccarat'" style="padding:0">
<img src="{GAME_IMAGES.get('BACCARAT', LOGO_URL)}" alt="Baccarat" onerror="this.style.display='none'">
<div class="info"><h3 style="font-weight:700;font-size:1.05rem">BACCARAT</h3>
<p style="color:#94a3b8;font-size:.8rem">43 Thuật Toán AI</p></div></div>'''
    h += '</div>'
    return page('Dashboard', h, user)

# 6. Tool detail
@app.route('/tool/<tool_id>')
@login_required
@key_required
def tool_detail(tool_id):
    user = get_sess_user()
    if tool_id not in TOOLS_CONFIG: flash('Tool không tồn tại','error'); return redirect(url_for('home'))
    data = get_tool_data(tool_id)
    if not data or not data.get('lich_su'): flash('Không thể lấy dữ liệu','error'); return redirect(url_for('home'))
    dd, cm = du_doan_tx(data['lich_su'])
    if not dd: flash('Chưa đủ dữ liệu để phân tích','warning'); return redirect(url_for('home'))
    pred = dd.get('du_doan','T')
    conf = dd.get('do_tin_cay', 55)
    dt = dd.get('diem_tai', 0); dx = dd.get('diem_xiu', 0)
    st = dd.get('so_thuat_toan_tai', 0); sx = dd.get('so_thuat_toan_xiu', 0)
    vt = dd.get('vip_tai', 0); vx = dd.get('vip_xiu', 0)
    at = dd.get('ai_tai', 0); ax = dd.get('ai_xiu', 0)
    strongest = dd.get('thuat_toan_manh_nhat', {})
    is_tai = pred == 'T'
    pcls = 'tai' if is_tai else 'xiu'
    plbl = 'TÀI' if is_tai else 'XỈU'
    pcolor = '#f43f5e' if is_tai else '#3b82f6'
    total_score = dt + dx if (dt + dx) > 0 else 1
    h = f'''<div class="flex-between mb-2" style="flex-wrap:wrap;gap:12px">
<div><h1 style="font-size:1.4rem;font-weight:800">{data["full_name"]}</h1>
<div class="flex" style="gap:8px;margin-top:4px"><span class="badge badge-ai">{data["nhom"]}</span>
<span class="badge badge-core">{data["loai"]}</span>
<span style="color:#94a3b8;font-size:.8rem">Phiên: <span class="mono">{data.get("phien","N/A")}</span> | {data.get("so_phien",0)} mẫu</span></div></div></div>'''
    # Main prediction
    h += f'''<div class="glow-border mt-2"><div class="inner text-center">
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px"><span class="status-dot"></span>Dự đoán phiên tiếp theo</p>
<div class="pred-ball {pcls}" style="margin-bottom:16px"><span>{plbl}</span></div>
<p style="font-size:1.1rem;font-weight:700;margin-bottom:8px">Độ tin cậy</p>
{conf_ring(conf, pcolor)}
</div></div>'''
    # Scores side by side
    h += '<div class="grid" style="grid-template-columns:1fr 1fr;gap:16px;margin-top:20px">'
    # TAI score
    h += f'''<div class="glass" style="border-color:rgba(244,63,94,.2)"><h3 style="color:#fb7185;font-weight:700;margin-bottom:10px">Điểm TÀI</h3>
<div style="font-size:1.8rem;font-weight:800;color:#fb7185">{dt:.1f}</div>
<p style="color:#94a3b8;font-size:.8rem;margin-top:4px">{st} thuật toán</p>
<div class="score-bar"><div class="score-fill rose" style="width:{dt/total_score*100:.0f}%"></div></div>
<div class="flex mt-1" style="gap:6px">{'<span class="badge badge-vip">VIP '+str(vt)+'</span>' if vt else ''}{'<span class="badge badge-ai">AI '+str(at)+'</span>' if at else ''}</div></div>'''
    # XIU score
    h += f'''<div class="glass" style="border-color:rgba(59,130,246,.2)"><h3 style="color:#60a5fa;font-weight:700;margin-bottom:10px">Điểm XỈU</h3>
<div style="font-size:1.8rem;font-weight:800;color:#60a5fa">{dx:.1f}</div>
<p style="color:#94a3b8;font-size:.8rem;margin-top:4px">{sx} thuật toán</p>
<div class="score-bar"><div class="score-fill blue" style="width:{dx/total_score*100:.0f}%"></div></div>
<div class="flex mt-1" style="gap:6px">{'<span class="badge badge-vip">VIP '+str(vx)+'</span>' if vx else ''}{'<span class="badge badge-ai">AI '+str(ax)+'</span>' if ax else ''}</div></div>'''
    h += '</div>'
    # Strongest
    sname = strongest.get('ten','N/A') if isinstance(strongest, dict) else str(strongest)
    h += f'''<div class="glass mt-2 text-center"><p style="color:#94a3b8;font-size:.85rem">Thuật toán mạnh nhất</p>
<p style="font-size:1.1rem;font-weight:700;color:#fbbf24;margin-top:4px">{sname}</p></div>'''
    # History
    ls = data['lich_su']
    h += f'<div class="glass mt-2"><h3 style="font-weight:700;margin-bottom:12px">Lịch sử ({len(ls)} phiên)</h3><div>{hist_balls(ls, 50)}</div></div>'
    # Algorithm table
    if cm:
        h += '<div class="glass mt-2"><h3 style="font-weight:700;margin-bottom:12px">Chi tiết thuật toán</h3><div style="overflow-x:auto"><table><thead><tr>'
        h += '<th>#</th><th>Tên</th><th>Loại</th><th>Dự đoán</th><th>ĐTC</th><th>Trọng số</th><th>Ưu tiên</th></tr></thead><tbody>'
        for i, m in enumerate(cm[:40], 1):
            ten = m.get('ten','?')
            ktiep = m.get('ket_tiep','?')
            dtc = m.get('do_tin_cay', 0)
            ts = m.get('trong_so', 0)
            ut = m.get('uu_tien', 0)
            is_vip = m.get('la_vip', False)
            is_ai = m.get('la_ai', False)
            badge = '<span class="badge badge-vip">VIP</span>' if is_vip else ('<span class="badge badge-ai">AI</span>' if is_ai else '<span class="badge badge-core">CORE</span>')
            kcls = 'color:#fb7185' if ktiep == 'T' else 'color:#60a5fa'
            klbl = 'TÀI' if ktiep == 'T' else 'XỈU'
            bar_w = min(100, dtc)
            bar_cls = 'rose' if ktiep == 'T' else 'blue'
            h += f'<tr><td>{i}</td><td style="font-weight:600">{ten}</td><td>{badge}</td>'
            h += f'<td style="{kcls};font-weight:700">{klbl}</td>'
            h += f'<td><div class="flex" style="gap:6px"><span class="mono">{dtc}%</span></div><div class="score-bar" style="width:80px"><div class="score-fill {bar_cls}" style="width:{bar_w}%"></div></div></td>'
            h += f'<td class="mono">{ts}</td><td class="mono">{ut}</td></tr>'
        h += '</tbody></table></div></div>'
    h += '<script>setTimeout(()=>location.reload(),8000)</script>'
    return page(data['full_name'], h, user)

# 7. Baccarat list
@app.route('/baccarat')
@login_required
@key_required
def baccarat():
    user = get_sess_user()
    tables = get_bcr_data()
    h = '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:20px">Baccarat Live</h1>'
    if not tables:
        h += '<div class="glass text-center"><p style="color:#94a3b8">Không thể tải dữ liệu Baccarat</p></div>'
    else:
        h += '<div class="grid grid-2">'
        for t in tables:
            ban = t.get('ban','?')
            cau = t.get('cau','')
            hist = t.get('history', [])
            dd, _ = du_doan_bcr(hist)
            pred_lbl = '---'
            pred_cls = ''
            if dd:
                p = dd.get('du_doan','')
                if p == 'B': pred_lbl = 'BANKER'; pred_cls = 'badge-rose'
                elif p == 'P': pred_lbl = 'PLAYER'; pred_cls = 'badge-blue'
            last10 = hist[-10:] if hist else []
            balls = hist_balls(last10, 10, tx=False)
            h += f'''<a href="/baccarat/{ban}" style="text-decoration:none;color:inherit"><div class="glass game-card" style="padding:16px">
<div class="flex-between mb-2"><h3 style="font-weight:700">Bàn {ban}</h3><span class="badge {pred_cls}">{pred_lbl}</span></div>
<p style="color:#94a3b8;font-size:.8rem;margin-bottom:8px">{cau}</p>
<div>{balls}</div></div></a>'''
        h += '</div>'
    h += '<script>setTimeout(()=>location.reload(),10000)</script>'
    return page('Baccarat', h, user)

# 8. Baccarat detail
@app.route('/baccarat/<ban>')
@login_required
@key_required
def baccarat_detail(ban):
    user = get_sess_user()
    tables = get_bcr_data()
    if not tables: flash('Không thể tải dữ liệu','error'); return redirect(url_for('baccarat'))
    tbl = None
    for t in tables:
        if str(t.get('ban','')) == str(ban): tbl = t; break
    if not tbl: flash('Bàn không tồn tại','error'); return redirect(url_for('baccarat'))
    hist = tbl.get('history', [])
    dd, cm = du_doan_bcr(hist)
    h = f'<h1 style="font-size:1.4rem;font-weight:800;margin-bottom:4px">Bàn {ban}</h1>'
    h += f'<p style="color:#94a3b8;font-size:.85rem;margin-bottom:20px">{tbl.get("cau","")} | Phiên: {tbl.get("phien","N/A")} | {tbl.get("so_phien",0)} mẫu</p>'
    if not dd:
        h += '<div class="glass text-center"><p style="color:#94a3b8">Chưa đủ dữ liệu để phân tích</p></div>'
    else:
        pred = dd.get('du_doan','P')
        conf = dd.get('do_tin_cay', 55)
        dp = dd.get('diem_p', 0); db = dd.get('diem_b', 0)
        sp = dd.get('so_p', 0); sb = dd.get('so_b', 0)
        is_banker = pred == 'B'
        pcls = 'banker' if is_banker else 'player'
        plbl = 'BANKER' if is_banker else 'PLAYER'
        pcolor = '#f43f5e' if is_banker else '#3b82f6'
        total_score = dp + db if (dp + db) > 0 else 1
        h += f'''<div class="glow-border"><div class="inner text-center">
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px"><span class="status-dot"></span>Dự đoán phiên tiếp theo</p>
<div class="pred-ball {pcls}" style="margin-bottom:16px"><span>{plbl}</span></div>
{conf_ring(conf, pcolor)}
<p style="font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-top:12px">Phiếu bầu: <span style="color:#60a5fa">P:{sp}</span> | <span style="color:#fb7185">B:{sb}</span></p>
</div></div>'''
        # Score cards
        h += '<div class="grid" style="grid-template-columns:1fr 1fr;gap:16px;margin-top:20px">'
        h += f'''<div class="glass" style="border-color:rgba(59,130,246,.2)"><h3 style="color:#60a5fa;font-weight:700;margin-bottom:10px">Điểm Player</h3>
<div style="font-size:1.8rem;font-weight:800;color:#60a5fa">{dp:.1f}</div>
<p style="color:#94a3b8;font-size:.8rem;margin-top:4px">{sp} thuật toán</p>
<div class="score-bar"><div class="score-fill blue" style="width:{dp/total_score*100:.0f}%"></div></div></div>'''
        h += f'''<div class="glass" style="border-color:rgba(244,63,94,.2)"><h3 style="color:#fb7185;font-weight:700;margin-bottom:10px">Điểm Banker</h3>
<div style="font-size:1.8rem;font-weight:800;color:#fb7185">{db:.1f}</div>
<p style="color:#94a3b8;font-size:.8rem;margin-top:4px">{sb} thuật toán</p>
<div class="score-bar"><div class="score-fill rose" style="width:{db/total_score*100:.0f}%"></div></div></div>'''
        h += '</div>'
    # History
    h += f'<div class="glass mt-2"><h3 style="font-weight:700;margin-bottom:12px">Lịch sử</h3><div>{hist_balls(hist, 50, tx=False)}</div></div>'
    # Algorithm table
    if dd and cm:
        h += '<div class="glass mt-2"><h3 style="font-weight:700;margin-bottom:12px">Chi tiết thuật toán</h3><div style="overflow-x:auto"><table><thead><tr>'
        h += '<th>#</th><th>Tên</th><th>Loại</th><th>Dự đoán</th><th>ĐTC</th><th>Trọng số</th><th>Ưu tiên</th></tr></thead><tbody>'
        for i, m in enumerate(cm[:40], 1):
            ktiep = m.get('ket_tiep','?')
            dtc = m.get('do_tin_cay', 0)
            is_vip = m.get('la_vip', False); is_ai = m.get('la_ai', False)
            badge = '<span class="badge badge-vip">VIP</span>' if is_vip else ('<span class="badge badge-ai">AI</span>' if is_ai else '<span class="badge badge-core">CORE</span>')
            kcls = 'color:#fb7185' if ktiep == 'B' else ('color:#60a5fa' if ktiep == 'P' else 'color:#94a3b8')
            klbl = 'BANKER' if ktiep == 'B' else ('PLAYER' if ktiep == 'P' else ktiep)
            bar_cls = 'rose' if ktiep == 'B' else 'blue'
            h += f'<tr><td>{i}</td><td style="font-weight:600">{m.get("ten","?")}</td><td>{badge}</td>'
            h += f'<td style="{kcls};font-weight:700">{klbl}</td>'
            h += f'<td><span class="mono">{dtc}%</span><div class="score-bar" style="width:80px"><div class="score-fill {bar_cls}" style="width:{min(100,dtc)}%"></div></div></td>'
            h += f'<td class="mono">{m.get("trong_so",0)}</td><td class="mono">{m.get("uu_tien",0)}</td></tr>'
        h += '</tbody></table></div></div>'
    h += '<script>setTimeout(()=>location.reload(),8000)</script>'
    return page(f'Baccarat Bàn {ban}', h, user)

# 9. Payment
@app.route('/payment', methods=['GET','POST'])
@login_required
def payment():
    user = get_sess_user()
    uid = session.get('user_id')
    if request.method == 'POST':
        pkg = request.form.get('package','')
        if pkg not in PACKAGES: flash('Gói không hợp lệ','error'); return redirect(url_for('payment'))
        p = PACKAGES[pkg]
        did, tc = create_deposit(uid, p['price'], pkg)
        flash(f'Tạo yêu cầu nạp {fmoney(p["price"])} thành công! Mã: {tc}','success')
        return redirect(url_for('deposit_qr', did=did))
    # Package cards
    h = '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:20px">Nạp Tiền & Mua Key</h1>'
    h += '<div class="grid grid-3">'
    for pid, pkg in PACKAGES.items():
        h += f'''<div class="glass pkg-card"><h3 style="font-weight:700;margin-bottom:8px">{pkg["name"]}</h3>
<div class="pkg-price">{fmoney(pkg["price"])}</div>
<p style="color:#94a3b8;font-size:.8rem;margin:8px 0">{pkg["days"]} ngày sử dụng</p>
<form method="post"><input type="hidden" name="package" value="{pid}">
<button type="submit" class="btn btn-primary" style="width:100%">Mua Ngay</button></form></div>'''
    h += '</div>'
    # Bank info
    h += f'''<div class="glass mt-3"><h3 style="font-weight:700;margin-bottom:12px">Thông tin chuyển khoản</h3>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">
<div><label>Ngân hàng</label><p style="font-weight:600">{BANK_INFO["bank_name"]}</p></div>
<div><label>Số tài khoản</label><p style="font-weight:600" class="mono">{BANK_INFO["account_number"]}</p></div>
<div><label>Chủ tài khoản</label><p style="font-weight:600">{BANK_INFO["account_name"]}</p></div>
<div><label>QR ZaloPay</label><img src="{QR_ZALOPAY}" style="max-width:150px;border-radius:12px" onerror="this.style.display='none'"></div>
</div></div>'''
    # Deposit history
    deps = get_user_deposits(uid)
    if deps:
        h += '<div class="glass mt-2"><h3 style="font-weight:700;margin-bottom:12px">Lịch sử nạp tiền</h3><div style="overflow-x:auto"><table><thead><tr>'
        h += '<th>Mã</th><th>Số tiền</th><th>Trạng thái</th><th>Thời gian</th></tr></thead><tbody>'
        for d in deps[:20]:
            st = d.get('status','pending')
            st_badge = {'approved':'<span class="badge badge-green">Thành công</span>','rejected':'<span class="badge badge-rose">Từ chối</span>'}.get(st,'<span class="badge badge-core">Chờ duyệt</span>')
            h += f'<tr><td class="mono">{d.get("transfer_code","")}</td><td style="font-weight:600">{fmoney(d.get("amount",0))}</td><td>{st_badge}</td><td style="color:#94a3b8">{d.get("created_at","")[:16]}</td></tr>'
        h += '</tbody></table></div></div>'
    return page('Nạp Tiền', h, user)

# 10. Deposit QR
@app.route('/deposit/<int:did>/qr')
@login_required
def deposit_qr(did):
    user = get_sess_user()
    deps = get_user_deposits(session.get('user_id'))
    dep = None
    for d in deps:
        if d.get('deposit_id') == did: dep = d; break
    if not dep: flash('Không tìm thấy yêu cầu','error'); return redirect(url_for('payment'))
    tc = dep.get('transfer_code','')
    amt = dep.get('amount', 0)
    h = f'''<div style="max-width:500px;margin:40px auto"><div class="glass text-center">
<h2 style="font-weight:800;margin-bottom:16px">Thanh toán</h2>
<img src="{QR_ZALOPAY}" style="max-width:250px;border-radius:16px;margin-bottom:16px" onerror="this.style.display='none'">
<div class="glass" style="background:rgba(99,102,241,.05);margin-bottom:16px">
<p style="color:#94a3b8;font-size:.85rem">Số tiền</p><p style="font-size:1.5rem;font-weight:800;color:#fbbf24">{fmoney(amt)}</p></div>
<div class="glass" style="background:rgba(99,102,241,.05);margin-bottom:16px">
<p style="color:#94a3b8;font-size:.85rem">Nội dung chuyển khoản</p><p style="font-size:1.2rem;font-weight:700" class="mono">{tc}</p></div>
<div style="text-align:left;font-size:.85rem;color:#94a3b8">
<p>Ngân hàng: <strong style="color:#e2e8f0">{BANK_INFO["bank_name"]}</strong></p>
<p>STK: <strong style="color:#e2e8f0" class="mono">{BANK_INFO["account_number"]}</strong></p>
<p>Chủ TK: <strong style="color:#e2e8f0">{BANK_INFO["account_name"]}</strong></p></div>
<a href="/payment" class="btn btn-outline mt-2">Quay lại</a></div></div>'''
    return page('Thanh toán', h, user)

# 11. Activate key
@app.route('/activate-key', methods=['GET','POST'])
@login_required
def activate_key_page():
    user = get_sess_user()
    uid = session.get('user_id')
    if request.method == 'POST':
        kv = request.form.get('key_value','').strip()
        if not kv: flash('Vui lòng nhập key','warning'); return redirect(url_for('activate_key_page'))
        ok, msg = activate_key(uid, kv)
        flash(msg, 'success' if ok else 'error'); return redirect(url_for('activate_key_page'))
    k = check_key(uid)
    h = '<div style="max-width:500px;margin:40px auto"><div class="glass">'
    h += '<h2 style="font-weight:800;margin-bottom:20px;text-align:center">Kích Hoạt Key</h2>'
    if k:
        exp = k.get('expires_at','')[:10]
        h += f'''<div class="glass" style="background:rgba(16,185,129,.05);border-color:rgba(16,185,129,.2);margin-bottom:20px;text-align:center">
<span class="badge badge-green">Đang hoạt động</span>
<p style="font-weight:700;font-size:1.1rem;margin-top:8px">{k.get("package_name","VIP")}</p>
<p style="color:#94a3b8;font-size:.85rem">Key: <span class="mono">{k.get("key_value","")}</span></p>
<p style="color:#94a3b8;font-size:.85rem">Hết hạn: {exp}</p></div>'''
    h += '''<form method="post"><div class="mb-2"><label>Nhập mã key</label><input type="text" name="key_value" placeholder="VD: ABC123" required></div>
<button type="submit" class="btn btn-primary" style="width:100%">Kích Hoạt</button></form></div></div>'''
    return page('Kích hoạt Key', h, user)

# 12. My keys
@app.route('/my-keys')
@login_required
def my_keys():
    user = get_sess_user()
    uid = session.get('user_id')
    u = get_user(uid)
    h = '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:20px">Key của tôi</h1>'
    k = check_key(uid)
    if k:
        exp = k.get('expires_at','')[:10]
        h += f'''<div class="glass mb-2" style="border-color:rgba(16,185,129,.2)"><div class="flex-between">
<div><span class="badge badge-green">Đang hoạt động</span>
<h3 style="font-weight:700;margin-top:6px">{k.get("package_name","VIP")}</h3></div>
<div style="text-align:right"><p class="mono" style="font-size:1.1rem;font-weight:700">{k.get("key_value","")}</p>
<p style="color:#94a3b8;font-size:.8rem">Hết hạn: {exp}</p></div></div></div>'''
    else:
        h += '<div class="glass mb-2 text-center" style="border-color:rgba(251,191,36,.2)"><p style="color:#fbbf24;font-weight:600">Chưa có key hoạt động</p><a href="/payment" class="btn btn-primary mt-1">Mua Key</a></div>'
    # History
    if u and u.get('keys_history'):
        h += '<div class="glass"><h3 style="font-weight:700;margin-bottom:12px">Lịch sử key</h3><div style="overflow-x:auto"><table><thead><tr><th>Key</th><th>Gói</th><th>Kích hoạt</th><th>Hết hạn</th></tr></thead><tbody>'
        for kh in reversed(u['keys_history'][-20:]):
            h += f'<tr><td class="mono">{kh.get("key_value","")}</td><td>{kh.get("package_type","")}</td><td style="color:#94a3b8">{kh.get("activated_at","")[:16]}</td><td style="color:#94a3b8">{kh.get("expires_at","")[:10]}</td></tr>'
        h += '</tbody></table></div></div>'
    return page('Key của tôi', h, user)

# ═══════════════ ADMIN ROUTES ═══════════════

# 13. Admin dashboard
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    user = get_sess_user()
    s = stats()
    pend = get_pending()
    h = '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:20px">Admin Dashboard</h1>'
    h += '<div class="grid grid-3 mb-2">'
    for lbl, val, clr in [('Tổng Users', s.get('total_users',0), '#6366f1'),('Key hoạt động', s.get('active_keys',0), '#10b981'),
        ('Nạp tiền chờ', s.get('pending_deposits',0), '#fbbf24'),('Tổng nạp', s.get('total_deposits',0), '#8b5cf6')]:
        h += f'<div class="glass text-center"><div style="font-size:1.8rem;font-weight:800;color:{clr}">{val}</div><p style="color:#94a3b8;font-size:.85rem">{lbl}</p></div>'
    h += '</div>'
    # Quick links
    h += '''<div class="grid grid-3 mb-2">
<a href="/admin/create-key" class="glass text-center" style="color:#a5b4fc"><span style="font-size:1.5rem">+</span><p>Tạo Key</p></a>
<a href="/admin/users" class="glass text-center" style="color:#a5b4fc"><span style="font-size:1.5rem">&#128100;</span><p>Users</p></a>
<a href="/admin/keys" class="glass text-center" style="color:#a5b4fc"><span style="font-size:1.5rem">&#128273;</span><p>Keys</p></a></div>'''
    # Pending deposits
    if pend:
        h += '<div class="glass"><h3 style="font-weight:700;margin-bottom:12px">Yêu cầu nạp tiền chờ duyệt</h3><div style="overflow-x:auto"><table><thead><tr><th>ID</th><th>User</th><th>Số tiền</th><th>Mã CK</th><th>Thời gian</th><th>Hành động</th></tr></thead><tbody>'
        for d in pend:
            h += f'''<tr><td>{d.get("deposit_id","")}</td><td>{d.get("user_id","")}</td><td style="font-weight:600">{fmoney(d.get("amount",0))}</td>
<td class="mono">{d.get("transfer_code","")}</td><td style="color:#94a3b8">{d.get("created_at","")[:16]}</td>
<td><a href="/admin/approve/{d.get("deposit_id","")}" class="btn btn-success" style="padding:4px 12px;font-size:.8rem;margin-right:4px">Duyệt</a>
<a href="/admin/reject/{d.get("deposit_id","")}" class="btn btn-danger" style="padding:4px 12px;font-size:.8rem">Từ chối</a></td></tr>'''
        h += '</tbody></table></div></div>'
    return page('Admin', h, user)

# 14. Create key
@app.route('/admin/create-key', methods=['GET','POST'])
@login_required
@admin_required
def admin_create_key():
    user = get_sess_user()
    if request.method == 'POST':
        pkg = request.form.get('package','')
        if pkg not in PACKAGES: flash('Gói không hợp lệ','error'); return redirect(url_for('admin_create_key'))
        res = create_key(pkg)
        if res:
            kv, exp = res
            flash(f'Tạo key thành công: {kv} (hết hạn {exp[:10]})','success')
        else: flash('Lỗi tạo key','error')
        return redirect(url_for('admin_create_key'))
    h = '<div style="max-width:500px;margin:40px auto"><div class="glass">'
    h += '<h2 style="font-weight:800;margin-bottom:20px;text-align:center">Tạo Key Mới</h2>'
    h += '<form method="post"><div class="mb-2"><label>Chọn gói</label><select name="package">'
    for pid, pkg in PACKAGES.items():
        h += f'<option value="{pid}">{pkg["name"]} - {fmoney(pkg["price"])}</option>'
    h += '</select></div><button type="submit" class="btn btn-primary" style="width:100%">Tạo Key</button></form></div></div>'
    return page('Tạo Key', h, user)

# 15. Admin users
@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    user = get_sess_user()
    users = get_all_users()
    h = '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:20px">Quản lý Users</h1>'
    h += '<div class="glass"><div style="overflow-x:auto"><table><thead><tr><th>ID</th><th>Username</th><th>Họ tên</th><th>Số dư</th><th>Key</th><th>Admin</th></tr></thead><tbody>'
    for u in users:
        is_a = '<span class="badge badge-vip">Admin</span>' if u.get('is_admin') else ''
        ck = u.get('current_key','')
        h += f'<tr><td>{u.get("user_id","")}</td><td style="font-weight:600">{u.get("username","")}</td><td>{u.get("full_name","")}</td><td class="mono">{fmoney(u.get("balance",0))}</td><td class="mono">{ck or "---"}</td><td>{is_a}</td></tr>'
    h += '</tbody></table></div></div>'
    return page('Users', h, user)

# 16. Admin keys
@app.route('/admin/keys')
@login_required
@admin_required
def admin_keys():
    user = get_sess_user()
    keys = get_all_keys()
    h = '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:20px">Quản lý Keys</h1>'
    h += '<div class="glass"><div style="overflow-x:auto"><table><thead><tr><th>ID</th><th>Key</th><th>Gói</th><th>User</th><th>Trạng thái</th><th>Hết hạn</th></tr></thead><tbody>'
    for k in keys:
        st = '<span class="badge badge-green">Active</span>' if k.get('is_active') else '<span class="badge badge-core">Inactive</span>'
        h += f'<tr><td>{k.get("key_id","")}</td><td class="mono" style="font-weight:600">{k.get("key_value","")}</td><td>{k.get("package_name","")}</td><td>{k.get("user_id","---")}</td><td>{st}</td><td style="color:#94a3b8">{k.get("expires_at","")[:10]}</td></tr>'
    h += '</tbody></table></div></div>'
    return page('Keys', h, user)

# 17. Approve deposit
@app.route('/admin/approve/<int:did>')
@login_required
@admin_required
def admin_approve(did):
    ok, msg = approve_deposit(did)
    flash(msg, 'success' if ok else 'error'); return redirect(url_for('admin_dashboard'))

# 18. Reject deposit
@app.route('/admin/reject/<int:did>')
@login_required
@admin_required
def admin_reject(did):
    ok, msg = reject_deposit(did)
    flash(msg, 'success' if ok else 'error'); return redirect(url_for('admin_dashboard'))

# ═══════════════ ERROR HANDLERS ═══════════════

@app.errorhandler(403)
def err403(e):
    body = '''<div style="text-align:center;margin-top:80px">
<div style="font-size:4rem;font-weight:900;background:linear-gradient(135deg,#f43f5e,#e11d48);-webkit-background-clip:text;-webkit-text-fill-color:transparent">403</div>
<p style="color:#94a3b8;margin:12px 0">Bạn không có quyền truy cập trang này</p>
<a href="/home" class="btn btn-primary">Về trang chủ</a></div>'''
    return page('403', body, get_sess_user()), 403

@app.errorhandler(404)
def err404(e):
    body = '''<div style="text-align:center;margin-top:80px">
<div style="font-size:4rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent">404</div>
<p style="color:#94a3b8;margin:12px 0">Trang bạn tìm không tồn tại</p>
<a href="/home" class="btn btn-primary">Về trang chủ</a></div>'''
    return page('404', body, get_sess_user()), 404

@app.errorhandler(500)
def err500(e):
    body = '''<div style="text-align:center;margin-top:80px">
<div style="font-size:4rem;font-weight:900;background:linear-gradient(135deg,#fbbf24,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent">500</div>
<p style="color:#94a3b8;margin:12px 0">Lỗi hệ thống. Vui lòng thử lại sau</p>
<a href="/home" class="btn btn-primary">Về trang chủ</a></div>'''
    return page('500', body, get_sess_user()), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
