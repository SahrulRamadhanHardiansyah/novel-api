# NoctuaNovel (Novel API) - Web Scraping API

![image](https://github.com/user-attachments/assets/e567a905-b9ee-47a1-a369-7cab5f43c67a)

Ini adalah backend API yang dibangun dengan **Flask (Python)** untuk proyek NoctuaNovel. API ini bertugas melakukan web scraping secara *real-time* dari situs `bacalightnovel.co` untuk menyediakan data novel, chapter, dan informasi terkait lainnya dalam format JSON.

## 🛠️ Teknologi yang Digunakan

  * **Framework**: [Flask](https://flask.palletsprojects.com/)
  * **Web Scraping**: [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
  * **Permintaan HTTP**: [Requests](https://requests.readthedocs.io/en/latest/)

-----

## 🌐 API Endpoints

Berikut adalah daftar endpoint yang tersedia dan fungsinya. Semua endpoint mengembalikan data dalam format JSON.

| Method | Endpoint                    | Deskripsi                                                |
| :----- | :-------------------------- | :------------------------------------------------------- |
| `GET`  | `/`                         | Menampilkan halaman dokumentasi API dalam format HTML.     |
| `GET`  | `/api/terbaru`              | Mendapatkan daftar novel yang baru dirilis.                |
| `GET`  | `/api/pilihan-editor`       | Mendapatkan daftar novel pilihan editor.                   |
| `GET`  | `/api/rekomendasi`          | Mendapatkan daftar novel yang direkomendasikan.            |
| `GET`  | `/api/search?q=<keyword>`   | Mencari novel berdasarkan kata kunci.                      |
| `GET`  | `/api/novel/<slug>`         | Mendapatkan detail lengkap sebuah novel berdasarkan slug.  |
| `GET`  | `/api/chapter/<slug>`       | Mendapatkan konten teks dari sebuah chapter berdasarkan slug. |

-----

## 🚀 Instalasi & Menjalankan Lokal

Untuk menjalankan API ini di komputer Anda, ikuti langkah-langkah berikut.

### Prasyarat

  * Python (v3.8 atau lebih baru)
  * pip (Package Installer for Python)

### Langkah-langkah

1.  **Clone Repository**

    ```bash
    git clone https://github.com/SahrulRamadhanHardiansyah/novel-api
    ```

2.  **Navigasi ke Folder API**

    ```bash
    cd novel-api 
    ```

3.  **Buat dan Aktifkan Virtual Environment** (Sangat Direkomendasikan)

    ```bash
    # Buat environment
    python -m venv venv

    # Aktifkan di MacOS/Linux
    source venv/bin/activate

    # Aktifkan di Windows
    .\venv\Scripts\activate
    ```

4.  **Instal Dependencies**
    Pastikan Anda memiliki file `requirements.txt`. Jika belum, buat dengan menjalankan `pip freeze > requirements.txt` setelah menginstal library di bawah ini.

    ```bash
    pip install Flask "beautifulsoup4>=4.12.2" "requests>=2.31.0"

    # Atau jika requirements.txt sudah ada
    pip install -r requirements.txt
    ```

5.  **Jalankan Server Flask**

    ```bash
    python app.py
    ```

    API Anda sekarang berjalan di `http://127.0.0.1:5001`.

-----

## ⚠️ Peringatan (Disclaimer)

  * API ini adalah proyek tidak resmi dan sangat bergantung pada struktur HTML dari situs `bacalightnovel.co`.
  * Jika situs sumber mengubah layout mereka, API ini kemungkinan besar akan **berhenti berfungsi** dan memerlukan pembaruan pada kode scraper.
  * Gunakan API ini dengan bijak dan jangan melakukan permintaan secara berlebihan untuk menghormati server sumber.

## 📄 Lisensi

Didistribusikan di bawah Lisensi MIT.
