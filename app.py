

import flask
from flask import Flask, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# Database simulasi domain yang sudah terdaftar
domain_db = {
    "google.com": {"status": "Terdaftar", "registrar": "MarkMonitor Inc."},
    "tokopedia.com": {"status": "Terdaftar", "registrar": "Tokopedia"},
    "detik.com": {"status": "Terdaftar", "registrar": "Detikcom"},
    "belajarpython.com": {"status": "Terdaftar", "registrar": "Rumahweb"},
}
db_lock = threading.Lock()

def log_server_activity(message):
    """Fungsi sederhana untuk logging di sisi server (ke konsol)."""
    print(f"[SERVER-DOMAIN] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

@app.route('/domain/<nama_domain>/cek', methods=['GET'])
def cek_domain(nama_domain):
    """Endpoint untuk mengecek ketersediaan domain."""
    log_server_activity(f"Permintaan cek untuk domain: {nama_domain}")
    
    time.sleep(random.uniform(0.2, 0.5)) 
    
    with db_lock:
        domain = domain_db.get(nama_domain.lower())
    
    if domain:
        return jsonify({
            "nama_domain": nama_domain.lower(),
            "status": "Tidak Tersedia (Sudah Terdaftar)"
        }), 200
    else:
        return jsonify({
            "nama_domain": nama_domain.lower(),
            "status": "Tersedia untuk Didaftarkan"
        }), 404 # Menggunakan 404 untuk menandakan "tidak ditemukan di DB", yang berarti "tersedia"

if __name__ == '__main__':
    log_server_activity("API Pengecek Ketersediaan Domain dimulai.")
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False, use_reloader=False)