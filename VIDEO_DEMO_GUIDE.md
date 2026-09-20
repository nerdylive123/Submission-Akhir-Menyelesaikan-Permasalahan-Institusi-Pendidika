# Panduan Video Demo (maks. 5 menit)

Rekam layar sambil menjelaskan tiap poin. Satu aksi per langkah, satu penjelasan per aksi.

## 1. Pembukaan (~20 detik)
- **Aksi:** Tampilkan judul proyek / README.
- **Jelaskan:** Proyek ini menyelesaikan masalah dropout Jaya Jaya Institut — tingkat dropout ~32%, dan solusinya adalah model ML + dashboard monitoring.

## 2. Solusi Machine Learning (~90 detik)
- **Aksi:** Buka `notebook.ipynb`, scroll cepat bagian Modeling & Evaluation.
- **Jelaskan:** Model yang digunakan adalah **Random Forest Classifier** yang memprediksi status akhir mahasiswa (Dropout / Enrolled / Graduate).
- **Aksi:** Tunjukkan hasil classification report & confusion matrix.
- **Jelaskan:** Akurasi ~75%, dan yang terpenting **recall kelas Dropout ~70%** — mayoritas mahasiswa berisiko berhasil terdeteksi.
- **Aksi:** Tunjukkan grafik feature importance.
- **Jelaskan:** Faktor terpenting: performa semester 1 & 2, status pembayaran uang kuliah, beasiswa, dan usia saat mendaftar.

## 3. Dashboard (~90 detik)
- **Aksi:** Buka Metabase, tampilkan dashboard "Jaya Jaya Institut - Student Dropout Monitoring".
- **Jelaskan:** Dashboard untuk memonitor performa mahasiswa dan faktor risiko dropout.
- **Aksi:** Tunjuk KPI Total Mahasiswa & Total Dropout, lalu donut distribusi status.
- **Jelaskan:** 1.421 dari 4.424 mahasiswa dropout (32,1%).
- **Aksi:** Tunjuk bar "Dropout Rate per Program Studi".
- **Jelaskan:** Dropout sangat bervariasi antar prodi — prodi tertentu perlu prioritas intervensi.
- **Aksi:** Tunjuk chart status per pembayaran & beasiswa.
- **Jelaskan:** Mahasiswa yang menunggak jauh lebih berisiko; penerima beasiswa jauh lebih aman.

## 4. Prototype Prediksi (~60 detik)
- **Aksi:** Buka aplikasi Streamlit (`streamlit run app.py` atau link cloud), isi contoh data mahasiswa berisiko.
- **Jelaskan:** Tim bimbingan cukup memasukkan data mahasiswa untuk mendapat prediksi.
- **Aksi:** Tekan tombol Prediksi, tunjukkan hasil status & tingkat risiko.
- **Jelaskan:** Sistem menampilkan prediksi status dan persentase risiko dropout sehingga mahasiswa berisiko bisa segera dibimbing.

## 5. Kesimpulan (~40 detik)
- **Aksi:** Kembali ke README bagian Conclusion / Rekomendasi.
- **Jelaskan:** Kesimpulan — dropout dipicu terutama oleh performa akademik awal yang rendah dan tekanan finansial; model ML efektif sebagai early warning. Rekomendasi: sistem peringatan dini, bimbingan untuk SKS rendah, perkuat beasiswa, fokus pada prodi ber-dropout tinggi.
