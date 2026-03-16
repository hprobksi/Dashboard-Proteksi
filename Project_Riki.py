import streamlit as st
import pandas as pd

# 1. SETUP HALAMAN
st.set_page_config(page_title="App Proteksi", layout="centered", page_icon="⚡")

# ==========================================
# SISTEM NAVIGASI (DAYA INGAT APLIKASI)
# ==========================================
# Jika baru pertama kali dibuka, set ke halaman utama ('menu')
if 'halaman' not in st.session_state:
    st.session_state.halaman = 'menu'

# Fungsi ajaib untuk mengganti halaman
def pindah_halaman(nama_halaman):
    st.session_state.halaman = nama_halaman

# ==========================================
# KODE RAHASIA (CSS) UNTUK TEMA & UKURAN IKON
# ==========================================
# ==========================================
# KODE RAHASIA (CSS) UNTUK TEMA & UKURAN IKON
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f9f9;
    }
    
    /* 1. MENGATUR KOTAK TOMBOLNYA */
    button[kind="primary"] {
        height: 140px !important;
        border-radius: 15px !important;
        background-color: #007bb5 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* 2. INI KUNCI RAHASIANYA: MENGATUR UKURAN IKON & TEKS DI DALAM KOTAK */
    button[kind="primary"] p {
        font-size: 35px !important; /* Ganti angka 35px ini jika ingin lebih raksasa lagi */
        font-weight: bold !important;
        line-height: 1.2 !important; /* Mengatur jarak atas-bawah antara ikon dan teks */
    }
    
    /* 3. EFEK SAAT TOMBOL DISENTUH */
    button[kind="primary"]:hover {
        background-color: #005a87 !important;
        color: #ffcc00 !important;
        border: 2px solid #ffcc00 !important;
    }
    button[kind="primary"]:hover p {
        color: #ffcc00 !important; /* Memastikan teks juga ikut kuning saat disentuh */
    }
    
    /* 4. TOMBOL KEMBALI AGAR TETAP KECIL */
    button[kind="secondary"] p {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HALAMAN 1: MENU UTAMA
# ==========================================
if st.session_state.halaman == 'menu':
    col_logo, col_judul = st.columns([1, 4])
    with col_logo:
        st.image("https://upload.wikimedia.org/wikipedia/commons/9/97/Logo_PLN.png", width=60)
    with col_judul:
        st.title("Menu Utama")

    st.write("Silakan pilih modul pemeliharaan Gardu Induk:")
    st.divider()

    kolom1, kolom2 = st.columns(2)

    # Tambahkan parameter type="primary" agar tombol ini membesar mengikuti CSS
    with kolom1:
        st.button("🔌\n\nTest Plug", type="primary", use_container_width=True, on_click=pindah_halaman, args=('test_plug',))
        st.button("📝\n\nLKP & BA", type="primary", use_container_width=True, on_click=pindah_halaman, args=('catatan',))

    with kolom2:
        st.button("🗺️\n\nWiring", type="primary", use_container_width=True, on_click=pindah_halaman, args=('wiring',))
        st.button("⚙️\n\nSettings", type="primary", use_container_width=True, on_click=pindah_halaman, args=('setting',))


# ==========================================
# HALAMAN 2: TEST PLUG
# ==========================================
elif st.session_state.halaman == 'test_plug':
    # Tombol kembali ke menu utama (type="secondary" agar ukurannya kecil)
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    
    st.subheader("🔌 Konfigurasi Test Plug")
    st.info("Pilih GI dan Bay untuk melihat wiring Test Plug.")
    
    gi = st.selectbox("Gardu Induk", ["Pilih...", "GI Gandamekar", "GI Tambun"])
    if gi == "GI Gandamekar":
        st.success("Menampilkan data untuk Gandamekar...")
        # Nanti tambahkan database tabel Test Plug di sini


# ==========================================
# HALAMAN 3: WIRING DIAGRAM
# ==========================================
elif st.session_state.halaman == 'wiring':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🗺️ Wiring Diagram Database")
    st.warning("Modul sedang dikembangkan.")


# ==========================================
# HALAMAN 4: CATATAN (LKP)
# ==========================================
elif st.session_state.halaman == 'catatan':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📝 Catatan Pemeliharaan")
    st.text_area("Tulis temuan lapangan di sini:")


# ==========================================
# HALAMAN 5: SETTINGS
# ==========================================
elif st.session_state.halaman == 'setting':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("⚙️ Pengaturan Aplikasi")
    st.write("Versi 2.0.0 - Navigasi Multi-Halaman")
