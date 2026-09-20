"""
Prototype Sistem Prediksi Dropout - Jaya Jaya Institut
Jalankan lokal : streamlit run app.py
Model          : model/dropout_model.joblib (pipeline preprocessing + Random Forest)
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------
# Konfigurasi halaman
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Prediksi Dropout - Jaya Jaya Institut",
    page_icon="🎓",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "dropout_model.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.joblib")


@st.cache_resource
def load_artifacts():
    """Muat pipeline model dan label encoder (di-cache agar cepat)."""
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    return model, encoder


try:
    model, le = load_artifacts()
    model_ready = True
except Exception as exc:  # pragma: no cover
    model_ready = False
    load_error = exc

# Pemetaan label program studi (kode -> nama)
COURSE_MAP = {
    33: "Biofuel Production Technologies", 171: "Animation and Multimedia Design",
    8014: "Social Service (evening)", 9003: "Agronomy", 9070: "Communication Design",
    9085: "Veterinary Nursing", 9119: "Informatics Engineering", 9130: "Equinculture",
    9147: "Management", 9238: "Social Service", 9254: "Tourism", 9500: "Nursing",
    9556: "Oral Hygiene", 9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication", 9853: "Basic Education", 9991: "Management (evening)",
}
APPLICATION_MODE_MAP = {
    1: "1st phase - general contingent", 2: "Ordinance No. 612/93",
    5: "1st phase - special contingent (Azores)", 7: "Holders of other higher courses",
    10: "Ordinance No. 854-B/99", 15: "International student (bachelor)",
    16: "1st phase - special contingent (Madeira)", 17: "2nd phase - general contingent",
    18: "3rd phase - general contingent", 26: "Ordinance No. 533-A/99 item b2",
    27: "Ordinance No. 533-A/99 item b3", 39: "Over 23 years old", 42: "Transfer",
    43: "Change of course", 44: "Technological specialization diploma holders",
    51: "Change of institution/course", 53: "Short cycle diploma holders",
    57: "Change of institution/course (International)",
}
PREV_QUAL_MAP = {
    1: "Secondary education", 2: "Higher education - bachelor", 3: "Higher education - degree",
    4: "Higher education - master", 5: "Higher education - doctorate",
    6: "Frequency of higher education", 9: "12th year - not completed",
    10: "11th year - not completed", 12: "Other - 11th year", 14: "10th year",
    15: "10th year - not completed", 19: "Basic education 3rd cycle",
    38: "Basic education 2nd cycle", 39: "Technological specialization course",
    40: "Higher education - degree (1st cycle)", 42: "Professional higher technical course",
    43: "Higher education - master (2nd cycle)",
}
MARITAL_MAP = {1: "Single", 2: "Married", 3: "Widower", 4: "Divorced",
               5: "Facto union", 6: "Legally separated"}

# Kolom input sesuai skema fitur model
ALL_COLUMNS = [
    "Marital_status", "Application_mode", "Application_order", "Course",
    "Daytime_evening_attendance", "Previous_qualification", "Previous_qualification_grade",
    "Nacionality", "Mothers_qualification", "Fathers_qualification", "Mothers_occupation",
    "Fathers_occupation", "Admission_grade", "Displaced", "Educational_special_needs",
    "Debtor", "Tuition_fees_up_to_date", "Gender", "Scholarship_holder",
    "Age_at_enrollment", "International", "Curricular_units_1st_sem_credited",
    "Curricular_units_1st_sem_enrolled", "Curricular_units_1st_sem_evaluations",
    "Curricular_units_1st_sem_approved", "Curricular_units_1st_sem_grade",
    "Curricular_units_1st_sem_without_evaluations", "Curricular_units_2nd_sem_credited",
    "Curricular_units_2nd_sem_enrolled", "Curricular_units_2nd_sem_evaluations",
    "Curricular_units_2nd_sem_approved", "Curricular_units_2nd_sem_grade",
    "Curricular_units_2nd_sem_without_evaluations", "Unemployment_rate",
    "Inflation_rate", "GDP",
]

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.title("🎓 Sistem Prediksi Dropout Mahasiswa")
st.markdown(
    "Prototype ini membantu **Jaya Jaya Institut** mendeteksi sedini mungkin mahasiswa "
    "yang berisiko **dropout** agar dapat diberikan bimbingan khusus. Isi data mahasiswa "
    "pada panel di bawah, lalu tekan **Prediksi**."
)

if not model_ready:
    st.error(f"Model tidak dapat dimuat: {load_error}")
    st.stop()

# ------------------------------------------------------------------
# Form input
# ------------------------------------------------------------------
with st.form("prediction_form"):
    st.subheader("📋 Data Akademik")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        course = st.selectbox("Program Studi", options=list(COURSE_MAP.keys()),
                              format_func=lambda k: COURSE_MAP[k])
        admission_grade = st.number_input("Nilai Admission (0-200)", 0.0, 200.0, 120.0, 0.1)
    with a2:
        application_mode = st.selectbox("Jalur Pendaftaran", options=list(APPLICATION_MODE_MAP.keys()),
                                        format_func=lambda k: APPLICATION_MODE_MAP[k])
        prev_qual_grade = st.number_input("Nilai Kualifikasi Sebelumnya (0-200)", 0.0, 200.0, 120.0, 0.1)
    with a3:
        application_order = st.slider("Urutan Pilihan (0 = pilihan pertama)", 0, 9, 0)
        prev_qual = st.selectbox("Kualifikasi Sebelumnya", options=list(PREV_QUAL_MAP.keys()),
                                 format_func=lambda k: PREV_QUAL_MAP[k])
    with a4:
        daytime = st.selectbox("Waktu Kuliah", options=[1, 0],
                               format_func=lambda k: "Siang" if k == 1 else "Malam")
        age = st.number_input("Usia saat Mendaftar", 17, 70, 20)

    st.subheader("📊 Performa Semester 1 & 2")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        sem1_enrolled = st.number_input("SKS Diambil Sem 1", 0, 30, 6)
        sem2_enrolled = st.number_input("SKS Diambil Sem 2", 0, 30, 6)
    with s2:
        sem1_approved = st.number_input("SKS Lulus Sem 1", 0, 30, 5)
        sem2_approved = st.number_input("SKS Lulus Sem 2", 0, 30, 5)
    with s3:
        sem1_grade = st.number_input("Rata-rata Nilai Sem 1 (0-20)", 0.0, 20.0, 12.0, 0.1)
        sem2_grade = st.number_input("Rata-rata Nilai Sem 2 (0-20)", 0.0, 20.0, 12.0, 0.1)
    with s4:
        sem1_eval = st.number_input("Jumlah Evaluasi Sem 1", 0, 45, 6)
        sem2_eval = st.number_input("Jumlah Evaluasi Sem 2", 0, 45, 6)

    st.subheader("👤 Demografi & Ekonomi")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        gender = st.selectbox("Jenis Kelamin", options=[1, 0],
                              format_func=lambda k: "Laki-laki" if k == 1 else "Perempuan")
        marital = st.selectbox("Status Pernikahan", options=list(MARITAL_MAP.keys()),
                               format_func=lambda k: MARITAL_MAP[k])
    with d2:
        tuition = st.selectbox("Uang Kuliah Lancar?", options=[1, 0],
                               format_func=lambda k: "Lunas / Lancar" if k == 1 else "Menunggak")
        debtor = st.selectbox("Memiliki Hutang?", options=[0, 1],
                              format_func=lambda k: "Ya" if k == 1 else "Tidak")
    with d3:
        scholarship = st.selectbox("Penerima Beasiswa?", options=[0, 1],
                                   format_func=lambda k: "Ya" if k == 1 else "Tidak")
        displaced = st.selectbox("Mahasiswa Perantau (Displaced)?", options=[0, 1],
                                 format_func=lambda k: "Ya" if k == 1 else "Tidak")
    with d4:
        unemployment = st.number_input("Tingkat Pengangguran (%)", 0.0, 20.0, 10.8, 0.1)
        inflation = st.number_input("Tingkat Inflasi (%)", -1.0, 5.0, 1.4, 0.1)
        gdp = st.number_input("GDP", -5.0, 5.0, 1.74, 0.01)

    submitted = st.form_submit_button("🔍 Prediksi", use_container_width=True)

# ------------------------------------------------------------------
# Prediksi
# ------------------------------------------------------------------
if submitted:
    row = {
        "Marital_status": marital, "Application_mode": application_mode,
        "Application_order": application_order, "Course": course,
        "Daytime_evening_attendance": daytime, "Previous_qualification": prev_qual,
        "Previous_qualification_grade": prev_qual_grade, "Nacionality": 1,
        "Mothers_qualification": 1, "Fathers_qualification": 1, "Mothers_occupation": 5,
        "Fathers_occupation": 5, "Admission_grade": admission_grade, "Displaced": displaced,
        "Educational_special_needs": 0, "Debtor": debtor, "Tuition_fees_up_to_date": tuition,
        "Gender": gender, "Scholarship_holder": scholarship, "Age_at_enrollment": age,
        "International": 0, "Curricular_units_1st_sem_credited": 0,
        "Curricular_units_1st_sem_enrolled": sem1_enrolled,
        "Curricular_units_1st_sem_evaluations": sem1_eval,
        "Curricular_units_1st_sem_approved": sem1_approved,
        "Curricular_units_1st_sem_grade": sem1_grade,
        "Curricular_units_1st_sem_without_evaluations": 0,
        "Curricular_units_2nd_sem_credited": 0,
        "Curricular_units_2nd_sem_enrolled": sem2_enrolled,
        "Curricular_units_2nd_sem_evaluations": sem2_eval,
        "Curricular_units_2nd_sem_approved": sem2_approved,
        "Curricular_units_2nd_sem_grade": sem2_grade,
        "Curricular_units_2nd_sem_without_evaluations": 0,
        "Unemployment_rate": unemployment, "Inflation_rate": inflation, "GDP": gdp,
    }
    X_input = pd.DataFrame([row], columns=ALL_COLUMNS)

    pred_enc = model.predict(X_input)[0]
    pred_label = le.inverse_transform([pred_enc])[0]
    proba = model.predict_proba(X_input)[0]
    proba_map = {le.inverse_transform([i])[0]: p for i, p in enumerate(proba)}

    st.markdown("---")
    st.subheader("Hasil Prediksi")

    res_col, chart_col = st.columns([1, 1])
    with res_col:
        if pred_label == "Dropout":
            st.error(f"### ⚠️ Prediksi: **{pred_label}**")
            st.write("Mahasiswa ini **berisiko tinggi dropout**. Segera berikan bimbingan khusus.")
        elif pred_label == "Enrolled":
            st.warning(f"### 🔶 Prediksi: **{pred_label}**")
            st.write("Mahasiswa diprediksi **masih terdaftar** namun belum lulus. Pantau performanya.")
        else:
            st.success(f"### ✅ Prediksi: **{pred_label}**")
            st.write("Mahasiswa diprediksi akan **lulus**. Pertahankan performanya.")

        dropout_risk = proba_map.get("Dropout", 0.0) * 100
        st.metric(label="Tingkat Risiko Dropout", value=f"{dropout_risk:.1f}%")

    with chart_col:
        proba_df = (pd.DataFrame({"Status": list(proba_map.keys()),
                                  "Probabilitas": list(proba_map.values())})
                    .sort_values("Probabilitas"))
        proba_df["Probabilitas (%)"] = (proba_df["Probabilitas"] * 100).round(1)
        st.bar_chart(proba_df.set_index("Status")["Probabilitas (%)"])

    st.caption(
        "Catatan: beberapa fitur kontekstual (kewarganegaraan, kualifikasi & pekerjaan orang tua, "
        "kebutuhan khusus, status internasional, SKS ekuivalensi) diisi nilai umum secara otomatis "
        "demi kemudahan penggunaan."
    )

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.header("Tentang")
    st.write(
        "Prototype machine learning untuk memprediksi status akhir mahasiswa "
        "(Dropout / Enrolled / Graduate) berdasarkan data pendaftaran dan performa "
        "semester 1-2."
    )
    st.write("**Model:** Random Forest Classifier")
    st.write("**Akurasi (data test):** ~75%")
    st.write("**Recall kelas Dropout:** ~70%")
    st.markdown("---")
    st.caption("Proyek Akhir Data Science - Jaya Jaya Institut")
