import streamlit as st
import pandas as pd

# 1. BIKIN LAYOUT JADI LEBAR (FULL SCREEN) ALA DASHBOARD
st.set_page_config(page_title="Dashboard Proteksi", layout="wide", page_icon="⚡")

# ==========================================
# BAGIAN KIRI: SIDEBAR (MENU NAVIGASI)
# ==========================================
with st.sidebar:
    st.title("⚡ PROTEKSI ULTG BEKASI")
    st.write("Modul Pendukung Pemeliharaan")
    st.divider()
    
    # Membuat tombol pilihan menu
    menu_pilihan = st.radio(
        "PILIH MENU UTAMA:",
        ["🔌 Konfigurasi Test Plug", "🗺️ Wiring Diagram", "📝 Catatan & Berita Acara"]
    )

# ==========================================
# BAGIAN TENGAH/KANAN: KONTEN UTAMA
# ==========================================
st.title(menu_pilihan)
st.divider()

# --- HALAMAN 1: TEST PLUG ---
if menu_pilihan == "🔌 Konfigurasi Test Plug":
    st.write("Pilih Lokasi dan Jenis Relay untuk melihat panduan wiring Test Plug.")
    
    # Membuat filter pencarian di atas tabel (mirip web TRION)
    # ==========================================
    # DATABASE MINI ASET GARDU INDUK
    # ==========================================
    # Format: { "Nama GI": { "Nama Bay": ["Relay 1", "Relay 2"] } }
    database_aset = {
        "GI Gandamekar": {
            "Line Rajapaksi 1": ["LCD (MiCOM P545)", "OCR Backup"],
            "Bay Trafo 1": ["Differential Trafo (NR PCS 978S)", "OCR / GFR"]
        },
        "GI New Tambun": {
            "Line Muaratawar": ["LCD Main A (Siemens 7SL87)"],
            "Line Jatiwaringin 1": ["LCD (Siemens 7SL87)", "OCR (Siemens 7SJ82)"],
            "Kopel AB": ["OCR (Siemens 7SJ82)"]
        },
        "GI Poncol Baru": {
            "Line Tambun 1": ["LCD (MiCOM P546)", "OCR Backup"]
        }
    }

   
    # Membuat filter pencarian di atas tabel (Dropdown Bertingkat)
    kolom1, kolom2, kolom3 = st.columns(3)
    
    with kolom1:
        # Mengambil daftar GI otomatis dari database_aset
        daftar_gi = ["Pilih GI..."] + list(database_aset.keys())
        pilihan_gi = st.selectbox("Gardu Induk", daftar_gi)
        
    with kolom2:
        # Logika If: Jika GI sudah dipilih, tampilkan Bay yang ada di GI tersebut
        if pilihan_gi != "Pilih GI...":
            daftar_bay = ["Pilih Bay..."] + list(database_aset[pilihan_gi].keys())
        else:
            daftar_bay = ["Pilih Bay..."] # Kosong jika GI belum dipilih
            
        pilihan_bay = st.selectbox("Bay / Line", daftar_bay)
        
    with kolom3:
        # Logika If: Jika Bay sudah dipilih, tampilkan Relay yang ada di Bay tersebut
        if pilihan_bay != "Pilih Bay...":
            daftar_relay = ["Pilih Relay..."] + database_aset[pilihan_gi][pilihan_bay]
        else:
            daftar_relay = ["Pilih Relay..."] # Kosong jika Bay belum dipilih
            
        pilihan_relay = st.selectbox("Nama / Fungsi Relay", daftar_relay)

    st.write("") # Spasi kosong
    st.divider()

    # ==========================================
    # MENAMPILKAN TABEL TEST PLUG SESUAI RELAY
    # ==========================================
    # Kita buat logikanya membaca kata kunci merk dari pilihan_relay
    if "MiCOM" in pilihan_relay:
        st.subheader(f"Konfigurasi Pin Test Plug: {pilihan_relay}")
        
        data_pin = [
            {"TERMINAL": "Pin 1, 3, 5, 7", "FUNGSI": "CT Fasa & Netral", "STATUS UJI": "Di-Shorting (Injeksi Arus)"},
            {"TERMINAL": "Pin 13, 14, 15", "FUNGSI": "PT Tegangan", "STATUS UJI": "Injeksi Tegangan Normal"},
            {"TERMINAL": "Pin 21, 22", "FUNGSI": "Kontak Trip ke PMT", "STATUS UJI": "Dilepas / Isolasi"}
        ]
        
        df_pin = pd.DataFrame(data_pin)
        st.dataframe(df_pin, use_container_width=True)
        st.warning("⚠️ PENTING: Jangan lupa ubah setting menjadi Out of Service untuk loopback testing!")

    elif "Siemens" in pilihan_relay or "NR" in pilihan_relay:
        st.info(f"Database konfigurasi Test Plug untuk {pilihan_relay} sedang disusun...")


# --- HALAMAN 2: WIRING DIAGRAM ---
elif menu_pilihan == "🗺️ Wiring Diagram":
    st.info("Nantinya, Anda bisa mengunggah dan menampilkan foto As-Built Drawing (PDF/JPG) di halaman ini per Bay.")

# --- HALAMAN 3: CATATAN ---
elif menu_pilihan == "📝 Catatan & Berita Acara":
    st.info("Form untuk menginput data pengujian (LKP) dan mencetak Berita Acara PDF akan dibuat di sini.")
    
