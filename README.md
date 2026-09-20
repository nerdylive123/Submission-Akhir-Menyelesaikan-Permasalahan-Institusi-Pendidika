# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan (Jaya Jaya Institut)

- **Nama:** Jason Clarence
- **Email:** jason_clarence_sab51@dicoding.com
- **ID Dicoding:** jason_clarence_sab51

## Business Understanding

Jaya Jaya Institut adalah institusi pendidikan tinggi yang berdiri sejak tahun 2000 dan telah mencetak banyak lulusan bereputasi baik. Namun, institusi ini menghadapi masalah serius: **tingginya jumlah mahasiswa yang tidak menyelesaikan pendidikannya (dropout)**. Tingkat dropout yang tinggi berdampak pada reputasi, pendapatan, dan efektivitas institusi. Oleh karena itu, Jaya Jaya Institut ingin **mendeteksi sedini mungkin mahasiswa yang berisiko dropout** agar dapat diberikan bimbingan khusus.

### Permasalahan Bisnis

1. Bagaimana karakteristik mahasiswa yang dropout dibandingkan yang lulus/bertahan?
2. Faktor apa saja yang paling berpengaruh terhadap risiko dropout seorang mahasiswa?
3. Bagaimana mendeteksi sedini mungkin mahasiswa yang berisiko dropout agar dapat diberi bimbingan khusus?
4. Bagaimana memonitor performa mahasiswa secara berkala melalui dashboard?

### Cakupan Proyek

1. Analisis data eksploratori (EDA) untuk memahami faktor-faktor pembeda mahasiswa dropout.
2. Membangun model machine learning untuk memprediksi status akhir mahasiswa (Dropout / Enrolled / Graduate).
3. Membuat business dashboard (Metabase) untuk monitoring performa mahasiswa.
4. Membuat prototype sistem prediksi dropout berbasis Streamlit yang dapat dijalankan di cloud.
5. Memberikan rekomendasi action items berdasarkan temuan.

### Persiapan

Sumber data: [Students' Performance — Dicoding Dataset](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance) (berasal dari UCI ML Repository, Realinho et al., 2021). Dataset berisi 4.424 baris × 37 kolom (36 fitur + 1 target), mencakup data pendaftaran (demografi, sosial-ekonomi, jalur akademik) serta performa akademik semester 1 & 2.

Setup environment:

```bash
# 1. Buat virtual environment (opsional namun disarankan)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan notebook (analisis + pelatihan model)
jupyter notebook notebook.ipynb
```

---

## Business Dashboard

Dashboard dibuat menggunakan **Metabase** (dijalankan via Docker) dan berjudul **"Jaya Jaya Institut - Student Dropout Monitoring"**. Dashboard menampilkan faktor-faktor penting untuk memonitor performa mahasiswa dan risiko dropout:

| Visualisasi | Tujuan |
|---|---|
| Total Mahasiswa & Total Dropout (KPI) | Gambaran skala masalah |
| Distribusi Status Mahasiswa (donut) | Proporsi Dropout / Enrolled / Graduate |
| Dropout Rate per Program Studi (bar) | Prodi prioritas intervensi |
| Status berdasarkan Pembayaran Uang Kuliah (stacked) | Dampak finansial terhadap dropout |
| Status berdasarkan Beasiswa (stacked) | Efektivitas dukungan beasiswa |
| Rata-rata SKS Lulus per Status (bar) | Sinyal akademik per status |
| Status berdasarkan Jenis Kelamin (stacked) | Perbedaan demografis |
| Distribusi Usia saat Mendaftar (bar) | Kelompok usia berisiko |

**Kredensial Metabase:**

- Email: `root@mail.com`
- Password: `root123`

Screenshot dashboard: `jason_clarence_sab51-dashboard.jpg` (disertakan dalam submission).

Menjalankan dashboard Metabase secara lokal:

```bash
# Jalankan container Metabase
docker run -d --name metabase -p 3000:3000 metabase/metabase

# Salin database instance yang berisi dashboard & data
docker cp metabase.db.mv.db metabase:/metabase.db/metabase.db.mv.db
docker cp students.mv.db metabase:/metabase.db/students.mv.db

# Restart container lalu buka http://localhost:3000 (login dengan kredensial di atas)
docker restart metabase
```

> Catatan: `metabase.db.mv.db` adalah database instance Metabase (berisi definisi dashboard & koneksi), sedangkan `students.mv.db` adalah database H2 berisi tabel data mahasiswa yang menjadi sumber visualisasi. Keduanya disertakan dalam submission.

---

## Menjalankan Sistem Machine Learning

Prototype sistem prediksi dropout dibangun dengan **Streamlit** (`app.py`). Sistem memuat pipeline model (`model/dropout_model.joblib`) yang sudah mencakup preprocessing (imputasi, one-hot encoding, scaling) + model Random Forest, lalu memprediksi status akhir mahasiswa beserta tingkat risiko dropout-nya.

Menjalankan prototype secara lokal:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Aplikasi akan terbuka di `http://localhost:8501`. Isi data mahasiswa (program studi, nilai, SKS semester, status pembayaran, beasiswa, usia, dll.) lalu tekan **Prediksi** untuk melihat status prediksi (Dropout / Enrolled / Graduate) dan tingkat risiko dropout.

**Akses prototype online (Streamlit Community Cloud):**

```
https://jason-clarence-sab51-submission-akhir.streamlit.app
```

> Prototype di-deploy ke Streamlit Community Cloud dari repository GitHub proyek ini: hubungkan repository ke [share.streamlit.io](https://share.streamlit.io), pilih `app.py` sebagai entry point, dan Streamlit akan menginstal `requirements.txt` lalu menjalankan aplikasi.

---

## Conclusion

1. **Tingkat dropout Jaya Jaya Institut sangat tinggi (~32%)** — hampir 1 dari 3 mahasiswa (1.421 dari 4.424) tidak menyelesaikan studinya.
2. **Sinyal dropout terkuat adalah akademik & finansial.** Berdasarkan EDA dan *feature importance* model, faktor paling menentukan adalah: (a) performa akademik semester 1 & 2 (jumlah SKS lulus & rata-rata nilai) — mahasiswa dropout hanya meluluskan 1–2 SKS per semester; (b) status pembayaran uang kuliah — mahasiswa yang menunggak memiliki dropout rate ~62% vs ~27% yang lunas; (c) kepemilikan beasiswa — penerima beasiswa jauh lebih jarang dropout; (d) usia saat mendaftar — mahasiswa yang lebih tua lebih berisiko.
3. **Dropout rate sangat bervariasi antar program studi** (dari ~15% hingga >60%), sehingga intervensi perlu diprioritaskan per prodi.
4. **Model machine learning efektif sebagai sistem peringatan dini.** Model terbaik (Random Forest) mencapai **akurasi ~75–76%** dan — yang terpenting untuk bisnis — **recall kelas Dropout ~70%**, artinya mayoritas mahasiswa yang benar-benar dropout berhasil terdeteksi dan dapat segera diberi bimbingan khusus.

### Rekomendasi Action Items

- **Bangun sistem peringatan dini (early warning) berbasis model.** Terapkan prototype prediksi ini setiap akhir semester untuk menandai mahasiswa berisiko tinggi, lalu arahkan ke tim bimbingan konseling untuk intervensi sebelum benar-benar dropout.
- **Pantau ketat mahasiswa dengan performa semester awal rendah.** Mahasiswa yang meluluskan ≤2 SKS atau bernilai rendah di semester 1 harus otomatis masuk program bimbingan akademik intensif (tutoring, study group, penyesuaian beban SKS).
- **Perkuat dukungan finansial.** Mahasiswa yang menunggak uang kuliah adalah kelompok paling berisiko — sediakan skema cicilan, penundaan pembayaran, atau perluas kuota beasiswa karena beasiswa terbukti efektif menurunkan dropout.
- **Prioritaskan intervensi pada program studi ber-dropout tinggi.** Evaluasi kurikulum, kualitas pengajaran, dan layanan kemahasiswaan pada prodi dengan dropout rate >40% (mis. Management evening, Informatics Engineering, Journalism).
- **Berikan perhatian khusus pada mahasiswa non-tradisional.** Mahasiswa yang mendaftar pada usia lebih tua (>25 tahun), mahasiswa malam (part-time/evening), dan perantau cenderung lebih berisiko — sediakan jadwal fleksibel, konseling karier, dan dukungan komunitas.
- **Monitor berkala melalui dashboard.** Gunakan dashboard Metabase untuk memantau tren dropout per prodi, status pembayaran, dan beasiswa setiap semester sebagai bahan evaluasi kebijakan.

---

## Struktur Berkas

```
submission/
├── app.py                        # Prototype Streamlit (sistem prediksi dropout)
├── notebook.ipynb                # Analisis lengkap (EDA + modeling), sudah dieksekusi
├── README.md                     # Dokumentasi proyek ini
├── requirements.txt              # Dependensi
├── metabase.db.mv.db             # Database instance Metabase (dashboard)
├── students.mv.db                # Database H2 berisi tabel data mahasiswa
├── jason_clarence_sab51-dashboard.jpg    # Screenshot dashboard
├── VIDEO_DEMO_GUIDE.md           # Panduan merekam video demo (saran #1)
├── model/
│   ├── dropout_model.joblib      # Pipeline preprocessing + model Random Forest
│   ├── label_encoder.joblib      # Encoder label target
│   └── feature_schema.joblib     # Skema fitur
└── data/
    ├── data.csv                  # Dataset asli
    └── dashboard_data.csv        # Dataset + kolom label (untuk Metabase)
```
