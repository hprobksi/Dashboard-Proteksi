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
        st.title("Dashboard Proteksi ULTG Bekasi")

    st.write("Silakan pilih modul Proteksi:")
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
    # Tombol kembali ke menu utama
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    
    st.subheader("🔌 Konfigurasi Test Plug")
    
    # 1. DATABASE MINI TEST PLUG (Tempat Anda memasukkan data GI, Bay, dan Relay)
    database_testplug = {
        "GI Cikarang": {
            "Bay Kopel": {
                "Relay OCR": {
                    "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
                },
            "Bay Cikarang Listrindo 1": {
                "Relay OCR": {
                   "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
                },
                 "Bay Cikarang Listrindo 2": {
                "Relay OCR": {
                   "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
                },
            # 1. DATABASE MINI TEST PLUG (Versi Perbaikan Syntax)
    database_testplug = {
        "GI Cikarang": {
            "Bay Kopel": {
                "Relay OCR": {
                    "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
            },
            "Bay Cikarang Listrindo 1": {
                "Relay OCR": {
                    "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
            },
            "Bay Cikarang Listrindo 2": {
                "Relay OCR": {
                    "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
            },
            "Bay Fajar 1": {
                "Relay Distance": {
                    "Merk": "Micom",
                    "Tipe": "P546",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }, # <-- Koma di sini penting
                "Relay OCR": {
                    "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }
            },
            "Bay Fajar 2": {
                "Relay Distance": {
                    "Merk": "Micom",
                    "Tipe": "P546",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
                }, # <-- Koma di sini juga penting
                "Relay OCR": {
                    "Merk": "GE Multilin",
                    "Tipe": "P14D",
                    "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN / TERMINAL": "1, 3, 5, 7", "FUNGSI": "CT Arus Fasa & Netral", "TINDAKAN UJI": "Di-Shorting (Arus Injeksi)"},
                        {"PIN / TERMINAL": "13, 14, 15", "FUNGSI": "PT Tegangan", "TINDAKAN UJI": "Injeksi Tegangan Normal"},
                        {"PIN / TERMINAL": "21, 22", "FUNGSI": "Kontak Trip PMT", "TINDAKAN UJI": "Dilepas / Isolasi"}
                    ]
            
    }
            }
        }
        },
        "GI Tambun": {
            "Bay Trafo 1": {
                "Relay Differential": {
                    "Merk": "NR",
                    "Tipe": "PCS 978S",
                    "No Seri": "NR-554433",
                    "Konfigurasi": [] 
                }
            }
        }
    }

    # 2. MEMBUAT FILTER PENCARIAN BERTINGKAT (3 Kolom Sejajar)
    kolom_gi, kolom_bay, kolom_relay = st.columns(3)
    
    with kolom_gi:
        # Mengambil otomatis nama GI dari database
        daftar_gi = ["Pilih GI..."] + list(database_testplug.keys())
        pilihan_gi = st.selectbox("Gardu Induk", daftar_gi)
        
    with kolom_bay:
        # Logika: Jika GI dipilih, munculkan daftar Bay milik GI tersebut
        if pilihan_gi != "Pilih GI...":
            daftar_bay = ["Pilih Bay..."] + list(database_testplug[pilihan_gi].keys())
        else:
            daftar_bay = ["Pilih Bay..."]
        pilihan_bay = st.selectbox("Bay / Line", daftar_bay)
        
    with kolom_relay:
        # Logika: Jika Bay dipilih, munculkan daftar Relay milik Bay tersebut
        if pilihan_bay != "Pilih Bay...":
            daftar_relay = ["Pilih Relay..."] + list(database_testplug[pilihan_gi][pilihan_bay].keys())
        else:
            daftar_relay = ["Pilih Relay..."]
        pilihan_relay = st.selectbox("Jenis Relay", daftar_relay)

    st.divider()

    # 3. MENAMPILKAN HASIL JIKA RELAY SUDAH DIPILIH SAMPAI AKHIR
    if pilihan_relay != "Pilih Relay...":
        # Menarik spesifik data relay yang dipilih dari database
        data_relay = database_testplug[pilihan_gi][pilihan_bay][pilihan_relay]
        
        st.success(f"Lokasi: {pilihan_gi} ➔ {pilihan_bay}")
        
        # Menampilkan detail Merk, Tipe, dan No Seri
        st.markdown(f"#### 🏷️ {data_relay['Merk']} {data_relay['Tipe']}")
        st.write(f"**No Seri / S/N:** `{data_relay['No Seri']}`")
        
        st.write("") # Spasi
        
        # Menampilkan tabel jika datanya sudah diisi, atau pesan info jika masih kosong
        if len(data_relay["Konfigurasi"]) > 0:
            st.write("**Tabel Panduan Injeksi Test Plug:**")
            df_config = pd.DataFrame(data_relay["Konfigurasi"])
            st.dataframe(df_config, use_container_width=True)
        else:
            st.info("⚠️ Tabel konfigurasi pin Test Plug untuk relay ini belum diinput ke database.")

# (Pastikan kode # HALAMAN 3: WIRING DIAGRAM tetap ada di bawah ini)


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
