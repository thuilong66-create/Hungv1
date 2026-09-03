#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIP PRO AI 5.0 — Runner
Hỗ trợ: Render.com, Railway, Heroku, Termux, Local

Deploy Render:
  1. Push code lên GitHub
  2. Vào render.com → New Web Service → Connect repo
  3. Build Command: pip install -r requirements.txt
  4. Start Command: gunicorn app:app
"""
import os, sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    for f in ['algorithms.py','api_client.py','database.py','app.py']:
        if not os.path.exists(f):
            print(f"Thieu file: {f}"); sys.exit(1)
    port = int(os.environ.get('PORT', 5000))
    print(f"VIP PRO AI 5.0 | http://0.0.0.0:{port}")
    from app import app
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

if __name__ == '__main__':
    main()
