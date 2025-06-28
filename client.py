

import requests
import threading
import time

# --- Konfigurasi Klien ---
BASE_API_URL = "http://127.0.0.1:5000"

# Data untuk diuji oleh klien: Daftar nama domain yang akan dicek
DOMAIN_UNTUK_DICEK = ["google.com", "startupkeren.com", "belajarpython.com", "idebisnisku.id"]

# ==============================================================================
# SOAL: Implementasi Fungsi untuk Cek Ketersediaan Domain via API
# ==============================================================================
def client_cek_domain_via_api(nama_domain, thread_name):
    """
    TUGAS ANDA:
    Lengkapi fungsi ini untuk mengecek ketersediaan domain dari API
    dan mencetak hasilnya ke konsol.

    Langkah-langkah:
    1. Bentuk URL target: f"{BASE_API_URL}/domain/{nama_domain}/cek"
    2. Cetak pesan ke konsol bahwa thread ini ('thread_name') memulai pengecekan untuk 'nama_domain'.
       Contoh: print(f"[{thread_name}] Mengecek domain: {nama_domain}")
    3. Gunakan blok 'try-except' untuk menangani potensi error saat melakukan permintaan HTTP.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke URL target menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses, berarti domain sudah terdaftar):
                  - Cetak pesan bahwa domain tidak tersedia.
                    Contoh: print(f"[{thread_name}] Domain {nama_domain} TIDAK TERSEDIA.")
              - Jika 404 (tidak ditemukan, berarti domain tersedia):
                  - Cetak pesan bahwa domain tersedia.
                    Contoh: print(f"[{thread_name}] SELAMAT! Domain {nama_domain} TERSEDIA!")
              - Untuk status code lain:
                  - Cetak pesan error umum ke konsol.
       b. Di blok 'except requests.exceptions.Timeout':
          - Cetak pesan bahwa permintaan timeout ke konsol.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Cetak pesan error permintaan umum ke konsol.
    4. Setelah blok try-except, cetak pesan ke konsol bahwa thread ini ('thread_name') selesai memproses 'nama_domain'.
    """
    target_url = f"{BASE_API_URL}/domain/{nama_domain}/cek"
    print(f"[{thread_name}] Mengecek domain: {nama_domain}")

    try:
        response = requests.get(target_url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"[{thread_name}] Domain {nama_domain} TIDAK TERSEDIA.")
        elif response.status_code == 404:
            print(f"[{thread_name}] SELAMAT! Domain {nama_domain} TERSEDIA!")
        else:
            print(f"[{thread_name}] Error API untuk Domain {nama_domain}: Status {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"[{thread_name}] Permintaan ke Domain{nama_domain} timeout.")

    except requests.exceptions.RequestException as e:
        print(f"[{thread_name}] Error saat menghubungi API untuk domain {nama_domain}: {e}")

    print(f"[{thread_name}] Selesai memproses: {nama_domain}")

# --- Bagian Utama Skrip (Tidak Perlu Diubah Peserta) ---
if __name__ == "__main__":
    print(f"Memulai Klien Pengecek untuk {len(DOMAIN_UNTUK_DICEK)} Domain Secara Concurrent.")
    
    threads = []
    start_time = time.time()

    for i, domain_cek in enumerate(DOMAIN_UNTUK_DICEK):
        thread_name_for_task = f"Pencari-{i+1}" 
        thread = threading.Thread(target=client_cek_domain_via_api, args=(domain_cek, thread_name_for_task))
        threads.append(thread)
        thread.start()

    for thread_instance in threads:
        thread_instance.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nSemua pengecekan domain telah selesai diproses dalam {total_time:.2f} detik.")