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
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📝 Generator BA Pemeliharaan")
    st.info("Form ini telah disesuaikan dengan format standar BA UIT JBT ULTG Bekasi.")

    # 1. FORM INPUT DATA (Berdasarkan Template Dokumen Asli)
    with st.expander("1. Identitas Pekerjaan", expanded=True):
        no_ba = st.text_input("Nomor BA", value="001 /BAPS/NWTBN/ULTG-BKSI/III/2026")
        judul_ba = st.text_input("Judul Pekerjaan (Kapital)", value="RESETTING TEGANGAN REFERENSI DAN BANDWITH AVR TRAFO #1 GIS 150KV NEW TAMBUN")
        latar_belakang = st.text_area("Latar Belakang / Dasar Pekerjaan", value="Sebagai tindak lanjut dari surat UP3 terkait permintaan resetting ulang tegangan referensi pada Bay Trafo #1 GIS 150kV New Tambun")
        
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
        kegiatan = st.text_area("Langkah Kegiatan (Gunakan angka 1, 2, 3...)", height=100, value="1. Melakukan pengecekan setting terpasang\n2. Melakukan Resetting Parameter AVR\n3. Pengujian fungsi unjuk kerja")
        col_a, col_b = st.columns(2)
        with col_a:
            anomali = st.text_area("Anomali", value="Nihil")
        with col_b:
            perbaikan = st.text_area("Langkah Perbaikan", value="Nihil")
        tertunda = st.text_input("Pekerjaan Tertunda", value="Nihil")
        kesimpulan = st.text_area("Kesimpulan", value="Telah dilakukan pekerjaan sesuai dengan rekomendasi dengan hasil uji baik.")

    with st.expander("4. Tim Pelaksana & Pengesahan"):
        # Pelaksana lapangan bisa dipilih lebih dari satu
        pelaksana = st.multiselect("Daftar Pelaksana", ["Riki H", "Edward D", "Rizky Wira H", "Teknisi Lainnya"], default=["Edward D", "Rizky Wira H", "Riki H"])
        
        st.write("**Pejabat Pengesah:**")
        k1, k2, k3 = st.columns(3)
        with k1:
            tl_jar = st.text_input("Nama TL Jar", value="M JAENAL M")
        with k2:
            up2d = st.text_input("Nama UP2D", value="ORRY VERNANDA")
        with k3:
            tl_harpromet = st.text_input("Nama TL Harpromet", value="ERVAN JAGI M W")

    st.divider()

    # 2. LOGIKA GENERATOR FPDF (Template Spesifik UIT JBT)
    if st.button("📄 Buat Dokumen BA (PDF)", type="primary", use_container_width=True):
        with st.spinner("Merakit format PDF standar PLN... ⏳"):
            pdf = FPDF()
            pdf.add_page()
            
            # --- MARGIN KIRI KANAN ---
            pdf.set_left_margin(20)
            pdf.set_right_margin(20)
            
            # --- HEADER (KOP SURAT) ---
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 8, txt="BERITA ACARA PEKERJAAN", ln=True, align='C')
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 6, txt=f"No. : {no_ba}", ln=True, align='C')
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 12)
            # Multi_cell untuk judul yang panjang agar turun ke bawah secara rapi
            pdf.multi_cell(0, 6, txt=judul_ba, align='C')
            pdf.ln(8)
            
            # --- PARAGRAF PEMBUKA (Dibuat mengalir) ---
            pdf.set_font("Arial", '', 11)
            teks_pembuka = (f"{latar_belakang}, maka pada hari {hari_ba} pukul {jam_ba.strftime('%H.%M')} WIB, "
                            f"tanggal {tanggal_ba.strftime('%d-%m-%Y')}, PT PLN (Persero) UIT JBT, UPT BEKASI, ULTG BEKASI, "
                            f"Sub-bidang Pemeliharaan Proteksi, Meter dan Otomasi telah melaksanakan pekerjaan {judul_ba}, "
                            f"sesuai dengan rekomendasi serta prosedur dan dinyatakan :")
            pdf.multi_cell(0, 6, txt=teks_pembuka, align='J')
            pdf.ln(4)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 6, txt="TELAH SELESAI DILAKSANAKAN", ln=True, align='C')
            pdf.ln(4)
            
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 6, txt="Demikian Berita Acara ini dibuat dan ditanda tangani dengan sebenar-benarnya.", ln=True)
            pdf.ln(8)
            
            # --- BAGIAN DETAIL TEKNIS ---
            # Fungsi kecil untuk membuat baris detail
            def buat_baris_detail(label, isi):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(50, 6, txt=label, ln=0)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(0, 6, txt=f": {isi}")
                pdf.ln(2)

            buat_baris_detail("PERALATAN TERPASANG", peralatan)
            buat_baris_detail("LANGKAH KEGIATAN", f"\n{kegiatan}") # Di-enter agar rapi ke bawah
            buat_baris_detail("ANOMALI", anomali)
            buat_baris_detail("LANGKAH PERBAIKAN", perbaikan)
            buat_baris_detail("PEKERJAAN TERTUNDA", tertunda)
            buat_baris_detail("KESIMPULAN", kesimpulan)
            pdf.ln(10)
            
            # --- AREA TANDA TANGAN ---
            # Menyusun daftar pelaksana
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 6, txt=f"Bekasi, {tanggal_ba.strftime('%d-%m-%Y')}", ln=True, align='L')
            pdf.cell(30, 6, txt="Pelaksana :", ln=0)
            
            # Loop daftar pelaksana ke bawah
            pos_x_pelaksana = pdf.get_x()
            pos_y_pelaksana = pdf.get_y()
            for orang in pelaksana:
                pdf.set_xy(pos_x_pelaksana, pdf.get_y())
                pdf.cell(50, 6, txt=orang, ln=True)
            
            pdf.ln(15) # Spasi sebelum tabel tanda tangan pengesah
            
            # Matrix 3 Kolom untuk Pengesah (TL Jar, UP2D, TL Harpromet)
            y_awal_ttd = pdf.get_y()
            lebar_kolom = 170 / 3  # Lebar total dibagi 3
            
            pdf.set_font("Arial", '', 10)
            pdf.set_xy(20, y_awal_ttd)
            pdf.cell(lebar_kolom, 5, txt="TL Jar", align='C')
            pdf.set_xy(20 + lebar_kolom, y_awal_ttd)
            pdf.cell(lebar_kolom, 5, txt="UP2D", align='C')
            pdf.set_xy(20 + (lebar_kolom*2), y_awal_ttd)
            pdf.cell(lebar_kolom, 5, txt="TL Harpromet & Otomasi", align='C')
            
            # >>> DI SINI NANTI TEMPAT MENYISIPKAN GAMBAR TANDA TANGAN <<<
            # Contoh: pdf.image("ttd_jaenal.png", x=25, y=pdf.get_y()+5, w=30)
            
            pdf.ln(25) # Ruang kosong vertikal untuk tanda tangan
            
            pdf.set_font("Arial", 'BU', 10) # B = Bold, U = Underline
            pdf.set_xy(20, pdf.get_y())
            pdf.cell(lebar_kolom, 5, txt=f"( {tl_jar} )", align='C')
            pdf.set_xy(20 + lebar_kolom, pdf.get_y())
            pdf.cell(lebar_kolom, 5, txt=f"( {up2d} )", align='C')
            pdf.set_xy(20 + (lebar_kolom*2), pdf.get_y())
            pdf.cell(lebar_kolom, 5, txt=f"( {tl_harpromet} )", align='C')

            # --- EXPORT FILE ---
            import tempfile
            import os
            file_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(file_output.name)
            
            with open(file_output.name, "rb") as f:
                pdf_bytes = f.read()
            os.remove(file_output.name)

        # Tombol Download Tampil Setelah Selesai
        st.success("✅ Dokumen Berita Acara berhasil dirakit!")
        st.download_button(
            label="⬇️ Download BA Format Resmi (PDF)",
            data=pdf_bytes,
            file_name=f"BA_{peralatan.replace(' ', '_')}_{tanggal_ba}.pdf",
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
