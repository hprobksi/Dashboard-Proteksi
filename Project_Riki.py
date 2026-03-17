import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os

# 1. SETUP HALAMAN
st.set_page_config(page_title="App Proteksi", layout="centered", page_icon="⚡")

# ==========================================
# SISTEM NAVIGASI
# ==========================================
if 'halaman' not in st.session_state:
    st.session_state.halaman = 'menu'

def pindah_halaman(nama_halaman):
    st.session_state.halaman = nama_halaman
    # ==========================================
# FUNGSI AJAIB: UPLOAD KE GOOGLE DRIVE
# ==========================================
def upload_ke_gdrive(nama_file, byte_data, mime_type):
    try:
        rahasia = json.loads(st.secrets["google_credentials"])
        scopes = ['https://www.googleapis.com/auth/drive.file']
        creds = service_account.Credentials.from_service_account_info(rahasia, scopes=scopes)
        layanan = build('drive', 'v3', credentials=creds)
        
        # 👇👇👇 MASUKKAN ID FOLDER GOOGLE DRIVE ANDA DI BAWAH INI 👇👇👇
        ID_FOLDER = "1gOjfORca3tVLDYJZfhAu0JiHuMKaEoAm" 
        
        metadata_file = {'name': nama_file, 'parents': [ID_FOLDER]}
        media = MediaIoBaseUpload(io.BytesIO(byte_data), mimetype=mime_type, resumable=True)
        layanan.files().create(body=metadata_file, media_body=media, fields='id').execute()
        return True
    except Exception as e:
        st.error(f"Gagal terhubung ke server: {e}")
        return False

# ==========================================
# CSS TEMA & UKURAN IKON
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f4f9f9; }
    button[kind="primary"] {
        height: 140px !important;
        border-radius: 15px !important;
        background-color: #007bb5 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    button[kind="primary"] p {
        font-size: 35px !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
    }
    button[kind="primary"]:hover {
        background-color: #005a87 !important;
        color: #ffcc00 !important;
        border: 2px solid #ffcc00 !important;
    }
    button[kind="secondary"] p { font-size: 16px !important; }
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
        st.title("Dashboard Proteksi")

    st.write("Silakan pilih modul Proteksi:")
    st.divider()

    kolom1, kolom2 = st.columns(2)
    with kolom1:
        st.button("🔌\n\nTest Block", type="primary", use_container_width=True, on_click=pindah_halaman, args=('test_plug',))
        st.button("📝\n\nBA Pekerjaan", type="primary", use_container_width=True, on_click=pindah_halaman, args=('catatan',))
    with kolom2:
        st.button("🗺️\n\nWiring", type="primary", use_container_width=True, on_click=pindah_halaman, args=('wiring',))
        st.button("⚙️\n\nSettings", type="primary", use_container_width=True, on_click=pindah_halaman, args=('setting',))

# ==========================================
# HALAMAN 2: TEST PLUG
# ==========================================
elif st.session_state.halaman == 'test_plug':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🔌 Konfigurasi Test Block")

    # 1. DATABASE (Didefinisikan di awal sebelum dipanggil dropdown)
    database_testplug = {
        "GI Cikarang": {
            "Bay Kopel": {
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"},
                        {"PIN": "13, 14, 15", "FUNGSI": "PT Tegangan", "AKSI": "Normal"},
                        {"PIN": "21, 22", "FUNGSI": "Trip PMT", "AKSI": "Isolasi"}
                    ]
                }
            },
            "Bay Cikarang Listrindo 1": {
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
            "Bay Fajar 1": {
                "Relay Distance": {
                    "Merk": "Micom", "Tipe": "P546", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
             "Bay Fajar 2": {
                "Relay Distance": {
                    "Merk": "Micom", "Tipe": "P546", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
             "Bay Jababeka 1": {
                "Relay LCD": {
                    "Merk": "NR", "Tipe": "PCS 931", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
            "Bay Jababeka 2": {
                "Relay LCD": {
                    "Merk": "SIFANG", "Tipe": "CSC 103", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
              "Bay Rajapaksi 1": {
                "Relay LCD": {
                    "Merk": "MICOM", "Tipe": "P545", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "MICOM AREVA", "Tipe": "P122", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
             "Bay Rajapaksi 2": {
                "Relay LCD": {
                    "Merk": "MICOM", "Tipe": "P545", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "SIEMENS", "Tipe": "7SJ62", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
              "Bay Trafo 1": {
                "Relay DIFF": {
                    "Merk": "ABB", "Tipe": "RET650", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF HV + SBEF": {
                    "Merk": "ABB", "Tipe": "REF615", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                  "Relay OCGF LV": {
                    "Merk": "ABB", "Tipe": "REF615", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  }
            },
            "Bay Trafo 2 KONSUMEN": {
                  "Relay OCGF HV": {
                    "Merk": "ABB", "Tipe": "REF615", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  }
            },
            "Bay Trafo 3": {
                "Relay DIFF": {
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF HV": {
                    "Merk": "MICOM", "Tipe": "P122", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                  "Relay OCGF LV": {
                    "Merk": "MICOM", "Tipe": "P122", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  },
                "Relay SBEF": {
                    "Merk": "MICOM", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  }
            },
            "Bay Trafo 4": {
                "Relay DIFF": {
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF HV": {
                    "Merk": "MICOM", "Tipe": "P122", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                  "Relay OCGF LV": {
                    "Merk": "MICOM", "Tipe": "P122", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  },
                "Relay SBEF": {
                    "Merk": "MICOM", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  }
            },
        },
        "GI Tambun": {
            "Bay Trafo 1": {
                "Relay Differential": {
                    "Merk": "NR", "Tipe": "PCS 978S", "No Seri": "NR-554433",
                    "Konfigurasi": [] 
                }
            }
        }
    }

    # 2. FILTER BERTINGKAT (Semua harus di dalam indentasi ELIF ini)
    kolom_gi, kolom_bay, kolom_relay = st.columns(3)
    
    with kolom_gi:
        daftar_gi = ["Pilih GI..."] + list(database_testplug.keys())
        pilihan_gi = st.selectbox("Gardu Induk", daftar_gi)
        
    with kolom_bay:
        if pilihan_gi != "Pilih GI...":
            daftar_bay = ["Pilih Bay..."] + list(database_testplug[pilihan_gi].keys())
        else:
            daftar_bay = ["Pilih Bay..."]
        pilihan_bay = st.selectbox("Bay / Line", daftar_bay)
        
    with kolom_relay:
        if pilihan_bay != "Pilih Bay...":
            daftar_relay = ["Pilih Relay..."] + list(database_testplug[pilihan_gi][pilihan_bay].keys())
        else:
            daftar_relay = ["Pilih Relay..."]
        pilihan_relay = st.selectbox("Jenis Relay", daftar_relay)

    st.divider()

    # 3. MENAMPILKAN HASIL
    if pilihan_relay != "Pilih Relay...":
        data = database_testplug[pilihan_gi][pilihan_bay][pilihan_relay]
        st.success(f"Lokasi: {pilihan_gi} ➔ {pilihan_bay}")
        st.markdown(f"#### 🏷️ {data['Merk']} {data['Tipe']}")
        st.write(f"**No Seri:** `{data['No Seri']}`")
        
        if len(data["Konfigurasi"]) > 0:
            st.write("**Panduan Test Plug:**")
            st.table(pd.DataFrame(data["Konfigurasi"]))
        else:
            st.info("⚠️ Tabel belum diinput.")

# ==========================================
# HALAMAN 3: WIRING DIAGRAM & DOKUMENTASI
# ==========================================
elif st.session_state.halaman == 'wiring':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🗺️ Database & Dokumentasi Wiring")

    st.info("Pilih lokasi untuk melihat dokumen wiring asli (40GB) atau mengupload foto revisi terbaru.")

    # 1. DATABASE LOKASI & LINK GDRIVE
    # Ganti tulisan "LINK_GDRIVE_XXX" dengan link share asli dari Google Drive Anda
    lokasi_gi = {
        "GI Gandamekar": {
            "Bay Rajapaksi 1": {
                "Relay LCD": "https://drive.google.com/file/d/LINK_GDRIVE_LCD_RAJAPAKSI1/view",
                "Relay OCR": "https://drive.google.com/file/d/LINK_GDRIVE_OCR_RAJAPAKSI1/view"
            },
            "Bay Rajapaksi 2": {
                "Relay LCD": "", # Kosongkan tanda kutip jika link belum ada
                "Relay OCR": ""
            }
        },
        "GI Cikarang": {
            "Bay Kopel": {
                "Relay OCR": "https://drive.google.com/file/d/LINK_GDRIVE_KOPEL_CIKARANG/view"
            },
            "Bay Fajar 1": {
                "Relay Distance": "https://drive.google.com/file/d/LINK_GDRIVE_FAJAR1_DIST/view",
                "Relay OCR": ""
            }
        }
    }

    # 2. FILTER PENCARIAN BERTINGKAT
    k_gi, k_bay, k_relay = st.columns(3)
    with k_gi:
        gi_w = st.selectbox("Gardu Induk", ["Pilih..."] + list(lokasi_gi.keys()), key="w_gi")
    with k_bay:
        if gi_w != "Pilih...":
            bay_w = st.selectbox("Bay / Line", ["Pilih..."] + list(lokasi_gi[gi_w].keys()), key="w_bay")
        else:
            bay_w = st.selectbox("Bay / Line", ["Pilih..."], key="w_bay")
    with k_relay:
        if bay_w != "Pilih...":
            # Mengambil daftar relay dari dalam dictionary
            relay_w = st.selectbox("Jenis Relay", ["Pilih..."] + list(lokasi_gi[gi_w][bay_w].keys()), key="w_relay")
        else:
            relay_w = st.selectbox("Jenis Relay", ["Pilih..."], key="w_relay")

    st.divider()

    # 3. FITUR BACA & TULIS
    if relay_w != "Pilih...":
        st.write(f"**📍 Target Lokasi:** {gi_w} ➔ {bay_w} ➔ {relay_w}")
        
        # Membuat 2 Tab Utama
        tab_lihat, tab_update = st.tabs(["👁️ Lihat Wiring Asli", "📸 Tambah Revisi Baru"])
        
        # --- TAB 1: MEMBUKA FILE 40GB DARI GDRIVE ---
        with tab_lihat:
            st.write("Akses *as-built drawing* asli yang tersimpan di server Google Drive.")
            link_asli = lokasi_gi[gi_w][bay_w][relay_w]
            
            if link_asli != "":
                st.link_button("🚀 Buka PDF Wiring di GDrive", link_asli, type="primary", use_container_width=True)
                st.info("💡 Teknisi akan diarahkan ke aplikasi Google Drive untuk melihat dokumen tanpa menghabiskan memori HP.")
            else:
                st.warning("⚠️ Link file wiring untuk lokasi ini belum diinput ke dalam database.")

        # --- TAB 2: MENGUPLOAD REVISI KE GDRIVE ---
        with tab_update:
            st.write("Gunakan menu ini jika ada perubahan wiring/jumperan baru di lapangan.")
            
            # Sub-Tab untuk memisahkan Kamera dan File
            subtab1, subtab2 = st.tabs(["📸 Kamera", "📂 Upload File"])
            
            with subtab1:
                foto = st.camera_input("Jepret perubahan wiring")
                if foto:
                    with st.spinner('Mengirim ke Google Drive... ⏳'):
                        nama_foto = f"REVISI_WIRING_{gi_w}_{bay_w}_{relay_w}.jpg".replace(" ", "_")
                        sukses = upload_ke_gdrive(nama_foto, foto.getvalue(), "image/jpeg")
                        if sukses:
                            st.success(f"✅ Foto revisi '{nama_foto}' berhasil disimpan permanen ke database!")
                    
            with subtab2:
                file_upload = st.file_uploader("Pilih Dokumen PDF/JPG dari HP", type=["pdf", "jpg", "jpeg", "png"])
                if file_upload:
                    with st.spinner('Mengunggah dokumen revisi... ⏳'):
                        sukses = upload_ke_gdrive(file_upload.name, file_upload.getvalue(), file_upload.type)
                        if sukses:
                            st.success(f"✅ Dokumen revisi '{file_upload.name}' resmi tersimpan di database!")
# ==========================================
# ==========================================
# HALAMAN 4: GENERATOR BERITA ACARA (BA)
# ==========================================
elif st.session_state.halaman == 'catatan':
    from docxtpl import DocxTemplate, InlineImage
    from docx.shared import Mm
    import tempfile
    import os
    
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📝 Generator BA (Otomasi Cerdas)")

    # --- 1. DATABASE TEMPLATE KEGIATAN ---
    db_kegiatan = {
        "Resetting AVR": "1. Melakukan pengecekan setting yang terpasang\n2. Melakukan Resetting Parameter AVR\n3. Melakukan pengecekan bersama setting pasca resetting\n4. Pengujian individu / fungsi unjuk kerja\n5. Dokumentasi",
        "Remote Riding": "1. Persiapan koneksi VPN ke gateway / server\n2. Login ke relay target via remote akses\n3. Unduh data event dan disturbance record\n4. Analisa hasil unduhan record gangguan\n5. Dokumentasi",
        "Resetting Relay": "1.	Melakukan pengecekan setting yang terpasang\n2.	Melakukan Resetting Parameter Relay \n3.	Melakukan Pengecekan bersama setting yang terpasang setelah resetting\n4. Melakukan pengujian individu relay pasca resetting\n5. Melakukan pengujian fungsi unjuk kerja relay pasca resetting\n6. Dokumentasi",
        "Modifikasi Alarm & Trip Bucholz": "1. Pemeriksaan kesesuaian rangkaian eksisting dengan wiring diagram\n2. Melakukan modifikasi rangkaian trip dan alarm relay bucholz\n3. Melakukan pengujian rangkaian baru\n4. Mencatat dan monitor indikasi yang muncul pada saat uji fungsi",
        "Lainnya (Ketik Manual)": ""
    }

    # --- 2. DATABASE FILE TANDA TANGAN ---
    # Sesuaikan "nama_file.png" dengan nama gambar yang Anda upload ke GitHub
    db_ttd = {
        "Kosongkan (Tanda Tangan Basah)": "",
        "M Jaenal M": "ttd_jaenal.png",
        "I Putu Surya A S": "ttd_putu.png",
        "Triawan A P N": "ttd_triawan.png",
        "Fajar Kurniawan": "ttd_fajark.png",
        "Hasanudin": "ttd_hasanudin.png",
        "RD. Jaya Kusuma": "ttd_raden.png",
        "AL Bastomy": "ttd_tomy.png",
        "Saepul Rohmat": "ttd_saepul.png",
        "Khahfi M M": "ttd_khahfi.png",
        "Ervan Jagi M W": "ttd_ervan.png",
        "Fajar R D S": "ttd_fajar.png",
        "Fathoni Diananta": "ttd_fatoni.png",
        "Orry Vernanda": "ttd_orry.png",
        "Riki H": "ttd_riki.png",
    }

    # --- FORM INPUT DATA ---
    with st.expander("1. Identitas Pekerjaan", expanded=True):
        in_no_ba = st.text_input("Nomor BA", value="001 /BAPS/NWTBN/ULTG-BKSI/III/2026")
        in_judul = st.text_area("Judul Pekerjaan (Kapital)", value="RESETTING TEGANGAN REFERENSI DAN BANDWITH AVR TRAFO #1")
        in_latar = st.text_area("Latar Belakang", value="Sebagai tindak lanjut dari surat UP3...")
        
    with st.expander("2. Waktu & Lokasi"):
        c1, c2, c3 = st.columns(3)
        with c1:
            in_hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4)
        with c2:
            in_tgl = st.date_input("Tanggal")
        with c3:
            in_jam = st.time_input("Pukul (WIB)")
            
        in_alat = st.text_input("Peralatan Terpasang", value="AVR Trafo #1 GIS 150kV New Tambun")

    with st.expander("3. Hasil Pekerjaan"):
        # Fitur Otomasi Template Kegiatan
        pilih_template = st.selectbox("Pilih Template Kegiatan", list(db_kegiatan.keys()))
        in_kegiatan = st.text_area("Langkah Kegiatan", value=db_kegiatan[pilih_template], height=130)
        
        col_a, col_b = st.columns(2)
        with col_a:
            in_anomali = st.text_area("Anomali", value="Nihil")
        with col_b:
            in_perbaikan = st.text_area("Langkah Perbaikan", value="Nihil")
        in_tertunda = st.text_input("Pekerjaan Tertunda", value="Nihil")
        in_kesimpulan = st.text_area("Kesimpulan", value="Telah dilakukan pekerjaan sesuai dengan rekomendasi dengan hasil uji baik.")

    with st.expander("4. Tim Pelaksana & Pengesahan"):
        st.write("**Pelaksana Lapangan:**")
        in_p1 = st.text_input("Pelaksana 1", value="Edward D")
        in_p2 = st.text_input("Pelaksana 2", value="Rizky Wira H")
        in_p3 = st.text_input("Pelaksana 3", value="Riki H")
        
        st.divider()
        st.write("**Pejabat Pengesah:**")
        k1, k2, k3 = st.columns(3)
        
        with k1:
            in_jab_kiri = st.text_input("Jabatan (Kiri)", value="TL Jar GIS Tambun")
            in_nama_kiri = st.selectbox("Nama (Kiri)", list(db_ttd.keys()), index=1)
            
        with k2:
            # Fitur Kolom Tengah Opsional
            pakai_tengah = st.checkbox("Aktifkan Pengesah Tengah", value=True)
            if pakai_tengah:
                in_jab_tengah = st.text_input("Jabatan (Tengah)", value="UP2D")
                in_nama_tengah = st.selectbox("Nama (Tengah)", list(db_ttd.keys()), index=2)
            else:
                in_jab_tengah, in_nama_tengah = "", ""
                
        with k3:
            in_jab_kanan = st.text_input("Jabatan (Kanan)", value="TL Harpromet & Otomasi")
            in_nama_kanan = st.selectbox("Nama (Kanan)", list(db_ttd.keys()), index=3)

    st.write("### 📸 Lampiran Dokumentasi")
    in_foto = st.file_uploader("Upload Foto Lapangan (Opsional)", type=["jpg", "jpeg", "png"])

    st.divider()

    # --- LOGIKA PENYUNTIKAN TEMPLATE ---
    if st.button("📄 Buat Dokumen BA", type="primary", use_container_width=True):
        with st.spinner("Merakit BA & Menempelkan Tanda Tangan... ⏳"):
            try:
                doc = DocxTemplate("template_ba.docx")
                
                bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                tgl_format = f"{in_tgl.day} {bulan_indo[in_tgl.month - 1]} {in_tgl.year}"
                
                # Menyiapkan Kamus Data Teks
                context = {
                    'no_ba': in_no_ba, 'judul_ba': in_judul, 'latar_belakang': in_latar,
                    'hari': in_hari, 'tgl': tgl_format, 'jam': in_jam.strftime('%H.%M'),
                    'alat': in_alat, 'kegiatan': in_kegiatan, 'anomali': in_anomali,
                    'perbaikan': in_perbaikan, 'tertunda': in_tertunda, 'kesimpulan': in_kesimpulan,
                    'pelaksana_1': in_p1, 'pelaksana_2': in_p2, 'pelaksana_3': in_p3,
                    
                    # Logika Jabatan & Nama (Tanda kurung dibuat otomatis jika ada isinya)
                    'jab_kiri': in_jab_kiri, 
                    'jab_tengah': in_jab_tengah, 
                    'jab_kanan': in_jab_kanan,
                    'nama_kiri': f"( {in_nama_kiri} )" if in_nama_kiri and in_nama_kiri != "Kosongkan (Tanda Tangan Basah)" else "",
                    'nama_tengah': f"( {in_nama_tengah} )" if in_nama_tengah and in_nama_tengah != "Kosongkan (Tanda Tangan Basah)" else "",
                    'nama_kanan': f"( {in_nama_kanan} )" if in_nama_kanan and in_nama_kanan != "Kosongkan (Tanda Tangan Basah)" else "",
                    
                    'ttd_kiri': '', 'ttd_tengah': '', 'ttd_kanan': '', 'foto_lampiran': ''
                }
                
               # Fungsi cerdas untuk menyisipkan TTD berdasarkan nama
                def sisipkan_ttd(nama_pejabat):
                    if nama_pejabat in db_ttd and db_ttd[nama_pejabat] != "":
                        file_gambar = db_ttd[nama_pejabat]
                        if os.path.exists(file_gambar): 
                            # KUNCI RAHASIANYA DI SINI: Gunakan 'height' (Tinggi), bukan 'width'
                            # Tinggi 15 mm (1.5 cm) adalah ukuran paling ideal dan aman untuk tabel Word
                            return InlineImage(doc, file_gambar, height=Mm(15)) 
                    return '' # Kosongkan jika tidak ketemu gambar

                # Eksekusi Stempel Tanda Tangan
                context['ttd_kiri'] = sisipkan_ttd(in_nama_kiri)
                context['ttd_tengah'] = sisipkan_ttd(in_nama_tengah)
                context['ttd_kanan'] = sisipkan_ttd(in_nama_kanan)
                
                # Eksekusi pemasangan Foto Lampiran (Lebar 13 cm)
                if in_foto:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_foto:
                        tmp_foto.write(in_foto.getvalue())
                        tmp_path = tmp_foto.name
                    context['foto_lampiran'] = InlineImage(doc, tmp_path, width=Mm(130))

                # Render & Simpan
                doc.render(context)
                file_output = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                doc.save(file_output.name)
                
                with open(file_output.name, "rb") as f:
                    docx_bytes = f.read()
                
                os.remove(file_output.name)
                if in_foto:
                    os.remove(tmp_path)

                st.success("✅ Dokumen BA dengan Tanda Tangan berhasil dirakit!")
                st.download_button(
                    label="⬇️ Download BA Siap Cetak (Word .docx)",
                    data=docx_bytes,
                    file_name=f"BA_{in_alat.replace(' ', '_')}.docx",
                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    type="primary"
                )
            except Exception as e:
                st.error(f"Error: Pastikan template_ba.docx & gambar TTD sudah di-upload ke GitHub. Detail: {e}")
# ==========================================
# HALAMAN 5: SETTINGS
# ==========================================
elif st.session_state.halaman == 'setting':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("⚙️ Settings")
    st.write("Versi 5.0 - PDF Generator Aktif 📄")
