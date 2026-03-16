import streamlit as st
import pandas as pd

# 1. SETUP HALAMAN UNTUK HP (Centered)
st.set_page_config(page_title="App Proteksi", layout="centered", page_icon="⚡")

# 2. KODE RAHASIA (CSS) UNTUK MEMBUAT TOMBOL JADI KOTAK BESAR
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 120px;
        border-radius: 20px;
        font-size: 16px;
        font-weight: bold;
        background-color: #2c2f33;
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #40444b;
        color: #00d2ff;
        border: 1px solid #00d2ff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Menu Utama")
st.write("Silakan pilih modul pemeliharaan:")

# ==========================================
# MEMBUAT TAMPILAN GRID 2 KOLOM (SEPERTI HP)
# ==========================================
kolom1, kolom2 = st.columns(2)

with kolom1:
    btn_testplug = st.button("🔌\n\nTest Plug", use_container_width=True)
    btn_catatan = st.button("📝\n\nLKP & BA", use_container_width=True)

with kolom2:
    btn_wiring = st.button("🗺️\n\nWiring Diagram", use_container_width=True)
    btn_setting = st.button("⚙️\n\nSettings", use_container_width=True)

st.divider()

# ==========================================
# LOGIKA KETIKA TOMBOL DIPENCET
# ==========================================
if btn_testplug:
    st.subheader("🔌 Konfigurasi Test Plug")
    
    # Masukkan filter GI dan Bay di sini (seperti kode sebelumnya)
    st.info("Pilih GI dan Bay untuk melihat wiring Test Plug.")
    gi = st.selectbox("Gardu Induk", ["Pilih...", "GI Gandamekar", "GI Tambun"])
    if gi == "GI Gandamekar":
        st.success("Menampilkan data untuk Gandamekar...")
        # Lanjutkan logika tabel Test Plug Anda di sini...

elif btn_wiring:
    st.subheader("🗺️ Wiring Diagram Database")
    st.warning("Modul sedang dikembangkan.")

elif btn_catatan:
    st.subheader("📝 Catatan Pemeliharaan")
    st.text_area("Tulis temuan lapangan di sini:")

elif btn_setting:
    st.subheader("⚙️ Pengaturan Aplikasi")
    st.write("Versi 1.0.0")