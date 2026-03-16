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
        st.button("📝\n\nLKP & BA", type="primary", use_container_width=True, on_click=pindah_halaman, args=('catatan',))
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
    from fpdf import FPDF
    import tempfile
    import os
    from datetime import datetime
    
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📝 Generator BA (Presisi Microsoft Word)")

    # --- KELAS KHUSUS: KOP SURAT PRESISI MILIMETER ---
    class PDF_BA(FPDF):
        def header(self):
            start_x = 10.8
            y_start = 20 
            
            # 1. BORDERS TABEL
            self.rect(start_x, y_start, 28.4, 16) 
            self.rect(start_x + 28.4, y_start, 35, 8) 
            self.rect(start_x + 63.4, y_start, 65, 8) 
            self.rect(start_x + 128.4, y_start, 25, 8) 
            self.rect(start_x + 153.4, y_start, 35, 8) 
            
            self.rect(start_x + 28.4, y_start + 8, 35, 8) 
            self.rect(start_x + 63.4, y_start + 8, 65, 8) 
            self.rect(start_x + 128.4, y_start + 8, 25, 8) 
            self.rect(start_x + 153.4, y_start + 8, 35, 8) 
            
            self.rect(start_x, y_start + 16, 188.4, 12) 
            
            # 2. TEKS KOP SURAT (Di-adjust vertikalnya agar lebih ke tengah kotak)
            self.set_font('Arial', 'B', 14)
            self.set_xy(start_x, y_start + 3)
            self.cell(28.4, 5, 'LEVEL', align='C')
            self.set_font('Arial', 'B', 18)
            self.set_xy(start_x, y_start + 9)
            self.cell(28.4, 5, '5', align='C')
            
            self.set_font('Arial', '', 9)
            self.set_xy(start_x + 29.4, y_start + 1.5)
            self.multi_cell(33, 3.5, 'No. Informasi\nTerdokumentasi')
            self.set_xy(start_x + 64.4, y_start + 2.5)
            self.cell(63, 4, '0003.DOK/BA/HAR/UITJBT/2024')
            self.set_xy(start_x + 129.4, y_start + 1.5)
            self.multi_cell(23, 3.5, 'Berlaku\nEfektif')
            self.set_xy(start_x + 154.4, y_start + 2.5)
            self.cell(33, 4, '05 Maret 2024')
            
            self.set_xy(start_x + 29.4, y_start + 10.5)
            self.cell(33, 4, 'Status')
            self.set_xy(start_x + 64.4, y_start + 10.5)
            self.cell(63, 4, 'Edisi : 01 / Revisi : 00')
            self.set_xy(start_x + 129.4, y_start + 10.5)
            self.cell(23, 4, 'Halaman')
            self.set_xy(start_x + 154.4, y_start + 10.5)
            self.cell(33, 4, f'{self.page_no()} dari {{nb}}')
            
            self.set_font('Arial', 'B', 11)
            self.set_xy(start_x, y_start + 17.5)
            self.cell(188.4, 4.5, 'BERITA ACARA PEMELIHARAAN ALAT UJI / ALAT KERJA', align='C')
            self.set_font('Arial', 'B', 10)
            self.set_xy(start_x, y_start + 22)
            self.cell(188.4, 4.5, 'PT PLN (PERSERO) UNIT INDUK TRANSMISI JAWA BAGIAN TENGAH', align='C')
            
            self.set_y(y_start + 35)

    # 1. FORM INPUT DATA
    with st.expander("1. Identitas Pekerjaan", expanded=True):
        no_ba = st.text_input("Nomor BA", value="001 /BAPS/NWTBN/ULTG-BKSI/III/2026")
        judul_ba = st.text_area("Judul Pekerjaan (Kapital)", value="RESETTING TEGANGAN REFERENSI DAN BANDWITH AVR TRAFO #1 GIS 150KV NEW TAMBUN")
        latar_belakang = st.text_area("Latar Belakang", value="Sebagai tindak lanjut dari surat UP3 terkait permintaan resetting ulang tegangan referensi pada Bay Trafo #1 GIS 150kV New Tambun")
        
    with st.expander("2. Waktu & Lokasi"):
        c1, c2, c3 = st.columns(3)
        with c1:
            hari_ba = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4)
        with c2:
            tanggal_ba = st.date_input("Tanggal Pelaksanaan")
        with c3:
            jam_ba = st.time_input("Pukul (WIB)")
            
        peralatan = st.text_input("Peralatan Terpasang", value="AVR Trafo #1 GIS 150kV New Tambun")

    with st.expander("3. Hasil Pekerjaan"):
        kegiatan = st.text_area("Langkah Kegiatan", height=120, value="1. Melakukan pengecekan setting yang terpasang\n2. Melakukan Resetting Parameter AVR\n3. Melakukan Pengecekan bersama setting yang terpasang setelah resetting\n4. Melakukan pengujian individu pasca resetting (jika offline)\n5. Melakukan pengujian fungsi unjuk kerja AVR pasca resetting\n6. Dokumentasi")
        col_a, col_b = st.columns(2)
        with col_a:
            anomali = st.text_area("Anomali", value="Nihil")
        with col_b:
            perbaikan = st.text_area("Langkah Perbaikan", value="Nihil")
        tertunda = st.text_input("Pekerjaan Tertunda", value="Nihil")
        kesimpulan = st.text_area("Kesimpulan", value="Telah dilakukan pekerjaan Resetting Tegangan Referensi dan Bandwith Trafo #1 GIS 150kV New Tambun sesuai dengan rekomendasi dengan hasil uji baik.")

    with st.expander("4. Tim Pelaksana & Pengesahan"):
        pelaksana = st.multiselect("Daftar Pelaksana", ["Edward D", "Rizky Wira H", "Riki H", "Teknisi Lainnya"], default=["Edward D", "Rizky Wira H", "Riki H"])
        k1, k2, k3 = st.columns(3)
        with k1:
            tl_jar = st.text_input("TL Jar", value="M JAENAL M")
        with k2:
            up2d = st.text_input("UP2D", value="ORRY VERNANDA")
        with k3:
            tl_harpromet = st.text_input("TL Harpromet", value="ERVAN JAGI M W")

    st.write("### 📸 Lampiran Dokumentasi")
    foto_lapangan = st.file_uploader("Upload Foto Sebelum & Sesudah (Opsional)", type=["jpg", "jpeg", "png"])

    st.divider()

    # 2. LOGIKA GENERATOR FPDF
    if st.button("📄 Buat Dokumen BA (PDF)", type="primary", use_container_width=True):
        with st.spinner("Merakit format presisi Microsoft Word... ⏳"):
            pdf = PDF_BA(orientation='P', unit='mm', format='A4')
            pdf.set_margins(left=25, top=20, right=12.5)
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.alias_nb_pages()
            
            w_aktif = 172.5 
            
            # --- KAMUS TRANSLATE BULAN INDONESIA ---
            bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            tgl_indo = f"{tanggal_ba.day} {bulan_indo[tanggal_ba.month - 1]} {tanggal_ba.year}"
            
            # ================= HALAMAN 1 =================
            pdf.add_page()
            
            pdf.set_font("Times", 'B', 12)
            pdf.cell(w_aktif, 6, txt="BERITA ACARA PEKERJAAN", ln=True, align='C')
            pdf.set_font("Times", 'B', 11)
            pdf.cell(w_aktif, 6, txt=f"No. : {no_ba}", ln=True, align='C')
            pdf.ln(3)
            
            pdf.set_font("Times", 'B', 16)
            pdf.multi_cell(w_aktif, 6, txt=judul_ba, align='C')
            pdf.ln(5)
            
            # --- PARAGRAF DENGAN FITUR MARKDOWN BOLD (fpdf2) ---
            pdf.set_left_margin(34.4) 
            pdf.set_right_margin(17.5) 
            pdf.set_font("Times", '', 11)
            
            # Perhatikan penggunaan bintang ganda (**) untuk mencetak tebal
            teks_pembuka = (f"    {latar_belakang}, maka pada hari **{hari_ba}** pukul **{jam_ba.strftime('%H.%M')} WIB**, "
                            f"tanggal **{tgl_indo}**, **PT PLN (Persero) UIT JBT, UPT BEKASI, ULTG BEKASI, "
                            f"Sub-bidang Pemeliharaan Proteksi, Meter dan Otomasi** telah melaksanakan **{judul_ba}**, "
                            f"sesuai dengan rekomendasi serta prosedur dan dinyatakan :")
            
            # markdown=True mengaktifkan fitur bold
            pdf.multi_cell(0, 7, txt=teks_pembuka, align='J', markdown=True) 
            pdf.ln(4)
            
            pdf.set_left_margin(25)
            pdf.set_right_margin(12.5)
            
            pdf.set_font("Times", 'B', 12)
            pdf.cell(w_aktif, 6, txt='"TELAH SELESAI DILAKSANAKAN"', ln=True, align='C')
            pdf.ln(4)
            
            pdf.set_font("Times", '', 11)
            pdf.cell(w_aktif, 6, txt="Demikian Berita Acara ini dibuat dan ditanda tangani dengan sebenar-benarnya.", ln=True)
            pdf.ln(10)
            
            # --- TANDA TANGAN PELAKSANA DI KANAN ---
            pdf.set_font("Times", '', 12)
            posisi_kanan = 120 # Koordinat X untuk menggeser ke kanan
            
            pdf.set_x(posisi_kanan)
            pdf.cell(50, 6, txt=f"Bekasi, {tgl_indo}", ln=True)
            pdf.set_x(posisi_kanan)
            pdf.cell(50, 6, txt="Pelaksana :", ln=True)
            for i, orang in enumerate(pelaksana):
                pdf.set_x(posisi_kanan)
                pdf.cell(50, 6, txt=f"{i+1}. {orang}", ln=True)
            
            pdf.ln(15) 
            
            # --- MATRIX PENGESAH DI BAWAH ---
            y_awal_ttd = pdf.get_y()
            lebar_kolom = w_aktif / 3
            
            pdf.set_font("Times", '', 12)
            pdf.set_xy(25, y_awal_ttd)
            pdf.cell(lebar_kolom, 5, txt="TL Jar", align='C')
            pdf.set_xy(25 + lebar_kolom, y_awal_ttd)
            pdf.cell(lebar_kolom, 5, txt="UP2D", align='C')
            pdf.set_xy(25 + (lebar_kolom*2), y_awal_ttd)
            pdf.cell(lebar_kolom, 5, txt="TL Harpromet & Otomasi", align='C')
            
            pdf.ln(25)
            
            y_nama = pdf.get_y()
            pdf.set_font("Times", 'B', 12)
            pdf.set_xy(25, y_nama)
            pdf.cell(lebar_kolom, 5, txt=f"( {tl_jar} )", align='C')
            pdf.set_xy(25 + lebar_kolom, y_nama)
            pdf.cell(lebar_kolom, 5, txt=f"( {up2d} )", align='C')
            pdf.set_xy(25 + (lebar_kolom*2), y_nama)
            pdf.cell(lebar_kolom, 5, txt=f"( {tl_harpromet} )", align='C')

            # ================= HALAMAN 2 =================
            pdf.add_page()
            
            def tulis_poin(huruf, judul, isi):
                pdf.set_font("Times", 'B', 12)
                pdf.cell(w_aktif, 7, txt=f"{huruf}. {judul}", ln=True)
                pdf.set_font("Times", '', 12)
                pdf.set_x(30) 
                pdf.multi_cell(w_aktif - 5, 7, txt=isi)
                pdf.ln(3)

            tulis_poin("A", "PERALATAN TERPASANG", peralatan)
            tulis_poin("B", "LANGKAH KEGIATAN", kegiatan)
            tulis_poin("C", "ANOMALI", anomali)
            tulis_poin("D", "LANGKAH PERBAIKAN :", perbaikan)
            tulis_poin("E", "PEKERJAAN TERTUNDA :", tertunda)
            tulis_poin("F", "KESIMPULAN", kesimpulan)

            # ================= HALAMAN 3 =================
            if foto_lapangan is not None:
                pdf.add_page()
                pdf.set_font("Times", 'B', 12)
                pdf.cell(w_aktif, 8, txt="LAMPIRAN DOKUMENTASI", ln=True, align='C')
                pdf.ln(5)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_foto:
                    tmp_foto.write(foto_lapangan.getvalue())
                    tmp_foto_path = tmp_foto.name
                
                # Agar gambar selalu center di kertas A4 (Lebar 210mm)
                # Jika lebar gambar 130mm, maka posisi X = (210 - 130) / 2 = 40mm
                pdf.image(tmp_foto_path, x=40, w=130)
                os.remove(tmp_foto_path)

            # --- EXPORT ---
            file_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(file_output.name)
            
            with open(file_output.name, "rb") as f:
                pdf_bytes = f.read()
            os.remove(file_output.name)

        st.success("✅ Dokumen BA presisi tinggi berhasil dirakit!")
        st.download_button(
            label="⬇️ Download BA Format Asli (PDF)",
            data=pdf_bytes,
            file_name=f"BA_{peralatan.replace(' ', '_')}.pdf",
            mime='application/pdf',
            type="primary"
        )
# ==========================================
# HALAMAN 5: SETTINGS
# ==========================================
elif st.session_state.halaman == 'setting':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("⚙️ Settings")
    st.write("Versi 5.0 - PDF Generator Aktif 📄")
