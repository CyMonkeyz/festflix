# FESTFLIX (Mini Project 1)

## DESKRIPSI
FestFlix adalah platform lokal untuk kumpulan film festival produksi kreator baru. User bisa menonton gratis 2 film/hari atau unlimited dengan langganan berbayar berbasis waktu. Tersedia fitur chat AI (rekomendasi film), rating & review, serta simulasi payment gateway.

## FITUR
🔑 Login/Register : 
User harus daftar & login untuk mengakses film, review, riwayat, dan fitur lain.
Validasi email wajib @gmail.com.

🏠 Homepage / Dashboard : 
Welcome message untuk user.
Banner status langganan (aktif/tidak aktif, sisa waktu, tombol perpanjang).
Filter kategori genre (Action, Drama, Horror, Sci-fi, Romance, dll).

🎬 Daftar Film (Movie Catalog) : 
List film (poster, judul, genre, tahun, rating, status: tersedia/terkunci).
Detail film: deskripsi, produser, sinopsis, rating, tombol tonton/review.
Tombol “Tonton” hanya aktif jika user sedang berlangganan.
Tombol “Review”/“Beri Rating” muncul setelah menonton.

🔎 Filter & Pencarian : 
Filter genre dengan tombol/dropdown.
Search bar untuk mencari judul/genre (opsional).

⏳ Subscription (Langganan) : 
Pilihan paket (30 detik/1 menit/1 hari dummy).
Setelah pilih paket, langganan langsung aktif (payment gateway simulasi/dummy).
Banner countdown sisa waktu langganan.
User non-subscriber hanya bisa menonton 2 film per hari.

🤖 Festy AI (Chatbot Rekomendasi) : 
Chatbot dengan integrasi Deepseek API/OpenRouter.
User bisa tanya rekomendasi film, info film, bantuan penggunaan, dsb.
Quick chat (preset pertanyaan), respons teks real-time.

🕒 Histori Tontonan : 
Riwayat film yang sudah pernah ditonton user.

⭐ Review & Rating : 
User bisa memberi rating (bintang) & komentar pada film yang sudah ditonton.

🚪 Logout : 
Tombol logout agar user bisa keluar dari aplikasi dengan aman.

Fitur Admin : CRUD data film (tambah, edit, hapus film festival).

## PERSIAPAN
1. Clone repository
   Salin URL dari tombol Code di repo GitHub.
   git clone https://github.com/CyMonkeyz/festflix.git

2. Buat virtual environment
   python -m venv env
   venv adalah modul standar Python untuk virtual environment.

3. Aktifkan virtual environtment
   Windows :
   env\Scripts\activate

   Linux/MacOS :
   source env/bin/activate

4. Install dependencies
   pip install -r requirements.txt
   Menginstall semua paket Python yang dibutuhkan.

5. Setup Tailwind CSS
   cd frontend
   npm install
   npm run build:css
   cd ..

6. Jalankan aplikasi
   python app.py

## STRUKTUR PROYEK
festflix/
├── app.py              # Aplikasi utama Flask
├── models.py           # Koneksi & logic database (users, films, review, history)
├── deepseek.py         # Integrasi chat AI dengan Deepseek/OpenRouter
├── config.py           # Konfigurasi Flask, DB, environment variables
├── templates/          # HTML Jinja2 templates
├── static/             # Asset statis (poster, video, CSS, QR)
├── frontend/           # Setup Tailwind CSS
├── database/
│   └── festflix.db     # SQLite database
├── requirements.txt    # Daftar Python packages
└── .gitignore          # File/folder yang di-ignore Git

## Kontribusi
Silakan fork repo, buat branch fitur, dan ajukan pull request.
Jangan lupa sertakan deskripsi perubahan dan hasil test manual QA.

## Lisensi
MIT License
