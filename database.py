#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 DATABASE MODULE - VIP PRO WEB
Quản lý dữ liệu: Users, Keys, Deposits
Lưu trữ JSON file
"""
import os
import json
import hashlib
import random
import string
from datetime import datetime, timedelta

DATA_FILE = "vip_pro_data.json"

# Bảng giá key
PACKAGES = {
    "buy_1d": {"name": "1 Ngày", "price": 25000, "days": 1},
    "buy_3d": {"name": "3 Ngày", "price": 50000, "days": 3},
    "buy_7d": {"name": "1 Tuần", "price": 80000, "days": 7},
    "buy_30d": {"name": "1 Tháng", "price": 120000, "days": 30},
    "buy_forever": {"name": "Vĩnh Viễn (Update liên tục)", "price": 300000, "days": 9999}
}

# Admin mặc định
ADMIN_USER = "hungdzkk11"
ADMIN_PASS = "hungki98"

# Thông tin ngân hàng
BANK_INFO = {
    "account_number": "32231199999",
    "bank_name": "Mbbank",
    "account_name": "LE THI THAI HIEN",
    "bank_code": "970422",
}

# ═══════════════════════════════════════════════
# HASH & CORE
# ═══════════════════════════════════════════════
def hash_password(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def load_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "users": {
                ADMIN_USER: {
                    "user_id": ADMIN_USER,
                    "username": ADMIN_USER,
                    "password": hash_password(ADMIN_PASS),
                    "full_name": "Administrator",
                    "created_at": datetime.now().isoformat(),
                    "balance": 999999999,
                    "current_key": None,
                    "keys_history": [],
                    "is_admin": True
                }
            },
            "keys": {},
            "deposits": {},
            "settings": {"last_user_id": 1, "last_key_id": 0, "last_deposit_id": 0}
        }
        save_data(data)
        return data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ═══════════════════════════════════════════════
# USER MANAGEMENT
# ═══════════════════════════════════════════════
def register_user(username, password, full_name=""):
    data = load_data()
    ul = username.lower().strip()
    # Check admin username
    if ul == ADMIN_USER.lower():
        return False, "Tên đăng nhập đã tồn tại"
    for uid, u in data["users"].items():
        uname = u.get("username", uid)
        if uname.lower() == ul:
            return False, "Tên đăng nhập đã tồn tại"
    data["settings"]["last_user_id"] += 1
    uid = str(data["settings"]["last_user_id"])
    data["users"][uid] = {
        "user_id": uid,
        "username": username.strip(),
        "password": hash_password(password),
        "full_name": full_name.strip(),
        "created_at": datetime.now().isoformat(),
        "balance": 0,
        "current_key": None,
        "keys_history": [],
        "is_admin": False
    }
    save_data(data)
    return True, "Đăng ký thành công"

def login_user(username, password):
    data = load_data()
    ul = username.lower().strip()
    for uid, u in data["users"].items():
        uname = u.get("username", uid)
        if uname.lower() == ul:
            if u["password"] == hash_password(password):
                return True, {
                    "user_id": uid,
                    "username": uname,
                    "full_name": u.get("full_name", ""),
                    "is_admin": u.get("is_admin", False)
                }
            return False, "Mật khẩu sai"
    return False, "Tên đăng nhập không tồn tại"

def get_user(uid):
    data = load_data()
    u = data["users"].get(str(uid))
    if u:
        info = dict(u)
        info.pop("password", None)
        return info
    return None

def update_balance(uid, amount):
    data = load_data()
    s = str(uid)
    if s in data["users"]:
        data["users"][s]["balance"] = data["users"][s].get("balance", 0) + amount
        save_data(data)
        return True
    return False

def get_all_users():
    data = load_data()
    us = []
    for uid, u in data["users"].items():
        info = dict(u)
        info.pop("password", None)
        info["user_id"] = uid
        us.append(info)
    return us

# ═══════════════════════════════════════════════
# KEY MANAGEMENT
# ═══════════════════════════════════════════════
def create_key(package_type, user_id=None, device_limit=1):
    pkg = PACKAGES.get(package_type)
    if not pkg:
        return None
    days = pkg["days"]
    expires = datetime.now() + timedelta(days=days)
    kv = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    data = load_data()
    data["settings"]["last_key_id"] += 1
    kid = data["settings"]["last_key_id"]
    data["keys"][str(kid)] = {
        "key_id": kid,
        "key_value": kv,
        "package_type": package_type,
        "package_name": pkg["name"],
        "price": pkg["price"],
        "created_at": datetime.now().isoformat(),
        "expires_at": expires.isoformat(),
        "user_id": user_id,
        "is_active": False,
        "activated_at": None,
        "device_limit": device_limit,
        "devices_used": []
    }
    save_data(data)
    return kv, expires.isoformat()

def activate_key(uid, kv):
    data = load_data()
    us = str(uid)
    kvu = kv.strip().upper()
    target = None
    for kid, kd in data["keys"].items():
        if str(kd.get("key_value", "")).strip().upper() == kvu:
            target = (kid, kd)
            break
    if not target:
        return False, "Key không tồn tại"
    kid, kd = target
    if kd.get("is_active"):
        return False, "Key đã được sử dụng"
    exp = datetime.fromisoformat(kd["expires_at"])
    if exp < datetime.now():
        return False, "Key đã hết hạn"
    # Deactivate old key
    for okid, okd in data["keys"].items():
        if str(okd.get("user_id")) == us and okd.get("is_active"):
            okd["is_active"] = False
    kd["user_id"] = uid
    kd["is_active"] = True
    kd["activated_at"] = datetime.now().isoformat()
    if us in data["users"]:
        data["users"][us]["current_key"] = int(kid) if kid.isdigit() else kid
        data["users"][us]["keys_history"].append({
            "key_id": int(kid) if kid.isdigit() else kid,
            "key_value": kvu,
            "activated_at": datetime.now().isoformat(),
            "expires_at": kd["expires_at"],
            "package_type": kd["package_type"],
            "price": kd["price"]
        })
    save_data(data)
    return True, "Kích hoạt thành công"

def check_key(uid):
    data = load_data()
    us = str(uid)
    if us not in data["users"]:
        return None
    ck = data["users"][us].get("current_key")
    if not ck:
        return None
    kd = data["keys"].get(str(ck))
    if not kd or not kd.get("is_active"):
        return None
    if datetime.fromisoformat(kd["expires_at"]) < datetime.now():
        kd["is_active"] = False
        save_data(data)
        return None
    return kd

def get_all_keys():
    return list(load_data()["keys"].values())

# ═══════════════════════════════════════════════
# DEPOSIT MANAGEMENT
# ═══════════════════════════════════════════════
def create_deposit(uid, amount, package_type=None):
    data = load_data()
    data["settings"]["last_deposit_id"] += 1
    did = data["settings"]["last_deposit_id"]
    tc = "VIPPRO" + str(random.randint(10000, 99999))
    data["deposits"][str(did)] = {
        "deposit_id": did,
        "user_id": uid,
        "amount": amount,
        "package_type": package_type,
        "status": "pending",
        "transfer_code": tc,
        "created_at": datetime.now().isoformat()
    }
    save_data(data)
    return did, tc

def get_user_deposits(uid):
    data = load_data()
    ds = []
    for did, d in data["deposits"].items():
        if str(d.get("user_id")) == str(uid):
            ds.append(d)
    return sorted(ds, key=lambda x: x["created_at"], reverse=True)

def get_pending():
    data = load_data()
    return [d for d in data["deposits"].values() if d["status"] == "pending"]

def approve_deposit(did):
    data = load_data()
    ds = str(did)
    if ds not in data["deposits"]:
        return False, "Không tìm thấy"
    d = data["deposits"][ds]
    if d["status"] != "pending":
        return False, "Đã xử lý"
    us = str(d["user_id"])
    amt = d["amount"]
    if us in data["users"]:
        data["users"][us]["balance"] = data["users"][us].get("balance", 0) + amt
    d["status"] = "approved"
    d["processed_at"] = datetime.now().isoformat()
    save_data(data)
    return True, "Đã cộng " + str(amt) + "đ"

def reject_deposit(did):
    data = load_data()
    ds = str(did)
    if ds in data["deposits"]:
        data["deposits"][ds]["status"] = "rejected"
        data["deposits"][ds]["processed_at"] = datetime.now().isoformat()
        save_data(data)
        return True, "Đã từ chối"
    return False, "Không tìm thấy"

def stats():
    data = load_data()
    return {
        "total_users": len(data["users"]),
        "active_keys": sum(1 for k in data["keys"].values() if k.get("is_active")),
        "total_deposits": len(data["deposits"]),
        "pending_deposits": sum(1 for d in data["deposits"].values() if d["status"] == "pending"),
        "approved": sum(1 for d in data["deposits"].values() if d["status"] == "approved"),
        "total_amount": sum(d["amount"] for d in data["deposits"].values() if d["status"] == "approved"),
    }
