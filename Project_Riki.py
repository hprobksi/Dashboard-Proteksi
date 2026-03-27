import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import tempfile
import os
import glob # Tambahkan 'import glob' di bagian paling atas file Anda (bersama import os, pd, dll)

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
        st.button("📖\n\nInstruksi Kerja", type="primary", use_container_width=True, on_click=pindah_halaman, args=('ik',))
    with kolom2:
        st.button("🗺️\n\nWiring", type="primary", use_container_width=True, on_click=pindah_halaman, args=('wiring',))
        st.button("📋\n\nForm Har CL PHT", type="primary", use_container_width=True, on_click=pindah_halaman, args=('cl_pht',))
        st.button("🗄️\n\nData Peralatan", type="primary", use_container_width=True, on_click=pindah_halaman, args=('database',))
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
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "36881926/10/24",
                    "Konfigurasi": [
                        {"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"},
                        {"PIN": "13, 14, 15", "FUNGSI": "PT Tegangan", "AKSI": "Normal"},
                        {"PIN": "21, 22", "FUNGSI": "Trip PMT", "AKSI": "Isolasi"}
                    ],
                    "Catatan Bawaan": "Perhatikan polaritas CT. Pastikan pin trip PMT diisolasi terlebih dahulu sebelum menginjeksi arus."
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
                    "Merk": "Micom", "Tipe": "P546", "No Seri": "34955418/12/19",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "36876504/10/24",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
             "Bay Fajar 2": {
                "Relay Distance": {
                    "Merk": "Micom", "Tipe": "P546", "No Seri": "34955417/12/19",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
             "Bay Jababeka 1": {
                "Relay LCD": {
                    "Merk": "NR", "Tipe": "PCS 931", "No Seri": "NRJB20155116B0250",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
            "Bay Jababeka 2": {
                "Relay LCD": {
                    "Merk": "SIFANG", "Tipe": "CSC 103", "No Seri": "SFJB400004448417000055",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "GE Multilin", "Tipe": "P14D", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
              "Bay Rajapaksi 1": {
                "Relay LCD": {
                    "Merk": "MICOM", "Tipe": "P545", "No Seri": "34486823/06/18",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "MICOM AREVA", "Tipe": "P122", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
             "Bay Rajapaksi 2": {
                "Relay LCD": {
                    "Merk": "MICOM", "Tipe": "P545", "No Seri": "33339701/06/15",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                },
                "Relay OCGF": {
                    "Merk": "SIEMENS", "Tipe": "7SJ62", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                }
            },
              "Bay Trafo 1": {
                "Relay DIFF": {
                    "Merk": "ABB", "Tipe": "RET650", "No Seri": "T1645034",
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
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "36197644/09/22",
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
                    "Merk": "MICOM", "Tipe": "P14D", "No Seri": "34954384/12/19",
                    "Konfigurasi": [{"PIN": "1, 3, 5, 7", "FUNGSI": "CT Arus", "AKSI": "Shorting"}]
                  }
            },
            "Bay Trafo 4": {
                "Relay DIFF": {
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "36197645/09/22",
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
                    "Merk": "MICOM", "Tipe": "P14D", "No Seri": "34954380/12/19",
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
        
        # --- MENAMPILKAN CATATAN BAWAAN ---
        if "Catatan Bawaan" in data and data["Catatan Bawaan"] != "":
            st.warning(f"📌 **Catatan SOP:** {data['Catatan Bawaan']}")
        
        # --- MENAMPILKAN TABEL KONFIGURASI ---
        if len(data["Konfigurasi"]) > 0:
            st.write("**Panduan Test Block:**")
            st.table(pd.DataFrame(data["Konfigurasi"]))
        else:
            st.info("⚠️ Tabel belum diinput.")
            
        st.divider()
        
        # --- FITUR CATATAN TAMBAHAN (INPUT TEKNISI) ---
        st.write("### 📝 Catatan Aktual Lapangan")
        catatan_tambahan = st.text_area(
            "Tambahkan temuan atau anomali saat pengujian (Opsional):", 
            placeholder="Ketik catatan di sini..."
        )
        
        # Tombol aksi (Contoh jika ingin dikembangkan nanti)
        if st.button("💾 Simpan Catatan Tambahan", type="secondary"):
            if catatan_tambahan != "":
                st.success("✅ Catatan berhasil direkam sementara di sesi ini!")
            else:
                st.error("⚠️ Catatan masih kosong.")

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
        "Resetting Relay": "1. Melakukan pengecekan setting yang terpasang\n2. Melakukan Resetting Parameter Relay \n3. Melakukan Pengecekan bersama setting yang terpasang setelah resetting\n4. Melakukan pengujian individu relay pasca resetting\n5. Melakukan pengujian fungsi unjuk kerja relay pasca resetting\n6. Dokumentasi",
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
# ==========================================
# HALAMAN 5: INSTRUKSI KERJA (IK)
# ==========================================
elif st.session_state.halaman == 'ik':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📖 Buku Saku Instruksi Kerja (IK)")
    st.write("Pilih alat uji atau jenis pekerjaan untuk melihat SOP dan langkah kerjanya.")

   # --- DATABASE INSTRUKSI KERJA ---
    # Anda bisa menambahkan alat uji baru di dalam kurung kurawal ini
    db_ik = {
        "Megger TORKEL 900-Series (Discharge Test)": {
            "Fungsi": "Alat ukur untuk menguji kapasitas baterai (discharge test) di gardu induk menggunakan beban arus konstan, daya konstan, atau resistansi konstan.",
            "Persiapan": [
                "Pastikan sirkulasi udara di ruang baterai sangat baik, karena proses pengujian (discharge) dapat menghasilkan gas hidrogen dan memicu ledakan jika ada percikan.",
                "Pastikan jarak bebas di sekitar TORKEL minimal 1.5 meter agar sirkulasi udara kipas pendingin tidak terhalang (jangan letakkan alat saling berdempetan).",
                "Hubungkan TORKEL ke sumber listrik AC (mains) dan nyalakan saklar daya alat."
            ],
            "Langkah Kerja": [
                {
                    "teks": "Pasang kabel arus utama dengan urutan yang benar: Pasang kabel negatif (-) dari TORKEL ke baterai, kemudian pasang kabel positif (+) ke baterai lalu ke terminal TORKEL.",
                    "gambar": "ik_torkel_kabel.jpg" 
                },
                {
                    "teks": "Pasang kabel kecil 'Voltage Sense' langsung ke kutub baterai (jika kabel arus utama cukup panjang). Ini sangat disarankan agar pembacaan tegangan drop di layar lebih akurat.",
                    "gambar": None
                },
                {
                    "teks": "Pada layar sentuh, pilih menu 'TEST', tekan 'Test Method' (pilih 'Constant I' untuk arus konstan), dan masukkan nilai arus pengujian.",
                    "gambar": "ik_torkel_menu.jpg" 
                },
                {
                    "teks": "SANGAT PENTING: Aktifkan batas 'Warning' dan 'Stop Limits' untuk melindungi baterai. Atur batas tegangan bawah (Cut-off voltage), batas waktu maksimum, atau batas kapasitas Ah tercapai.",
                    "gambar": None
                },
                {
                    "teks": "Tunggu hingga tulisan 'Connected ready' muncul di layar informasi bawah, kemudian tekan tombol START (▶) berwarna hijau untuk memulai pengujian.",
                    "gambar": None
                },
                {
                    "teks": "Setelah pengujian selesai dan alat di-STOP, lepaskan kabel dengan urutan kebalikan dari saat memasang. Peringatan: JANGAN PERNAH melepas capit kabel saat pengujian masih berjalan karena akan menimbulkan bunga api!",
                    "gambar": None
                }
            ],
            "Catatan Pengalaman": """
**💡 Catatan Pengalaman Lapangan:**
*(Silakan hapus teks ini dan ketikkan pengalaman Mas Riki di sini. Misalnya: "Perhatikan saat memasang capit buaya ke kepala baterai, pastikan tidak goyang karena arus besar bisa membuat terminal panas/meleleh", atau tips lainnya)*
"""
        }
    }

   # --- TAMPILAN ANTARMUKA ---
    pilihan_alat = st.selectbox("Cari Peralatan Uji:", ["Pilih Alat..."] + list(db_ik.keys()))

    if pilihan_alat != "Pilih Alat...":
        data_ik = db_ik[pilihan_alat]
        st.divider()
        st.markdown(f"### 🛠️ {pilihan_alat}")
        st.info(f"**Fungsi Utama:** {data_ik['Fungsi']}")

        with st.expander("📦 Persiapan", expanded=False):
            for item in data_ik['Persiapan']:
                st.write(f"- {item}")

        st.write("#### 📋 Langkah Kerja & Panduan Visual")
        # Looping pintar: Bisa baca format lama (teks) maupun format baru (teks+gambar)
        for i, item_langkah in enumerate(data_ik['Langkah Kerja']):
            if isinstance(item_langkah, dict):
                # Jika pakai format baru (ada gambar)
                st.write(f"**{i+1}.** {item_langkah['teks']}")
                # Tampilkan gambar jika file-nya ada di GitHub
                if item_langkah.get('gambar') and os.path.exists(item_langkah['gambar']):
                    st.image(item_langkah['gambar'], use_container_width=True)
            else:
                # Jika pakai format lama (teks biasa)
                st.write(f"**{i+1}.** {item_langkah}")

        st.write("---")
        
        # Tampilkan Perhatian (jika ada di database lama)
        if "Perhatian" in data_ik and data_ik["Perhatian"] != "":
            st.warning(data_ik['Perhatian'])
            
        # Tampilkan Catatan Pengalaman (jika ada di database baru)
        if "Catatan Pengalaman" in data_ik and data_ik["Catatan Pengalaman"] != "":
            st.success(data_ik['Catatan Pengalaman'])

# ==========================================
# HALAMAN 6: FORM CHECKLIST PHT
# ==========================================
elif st.session_state.halaman == 'cl_pht':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📋 Generator Form Checklist Penghantar")
    st.write("Isi data di bawah ini, kosongkan (-) jika tidak ada nilai ukur.")

    # --- DATABASE TANDA TANGAN ---
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
        "Riki H": "ttd_riki.png"
    }

    # --- FUNGSI PINTAR UNTUK MENGHEMAT KODE UI ---
    def ui_ukur_fasa(prefix, fasa_list, ada_tegangan=True):
        data = {}
        for fasa in fasa_list:
            c = st.columns(4 if ada_tegangan else 2)
            data[f'{prefix}_i_{fasa}'] = c[0].text_input(f"I-{fasa.upper()} (A)", key=f"in_{prefix}_i_{fasa}")
            data[f'{prefix}_i_{fasa}_sdt'] = c[1].text_input(f"∠ I-{fasa.upper()}", key=f"in_{prefix}_i_{fasa}_sdt")
            if ada_tegangan:
                data[f'{prefix}_v_{fasa}'] = c[2].text_input(f"V-{fasa.upper()} (kV)", key=f"in_{prefix}_v_{fasa}")
                data[f'{prefix}_v_{fasa}_sdt'] = c[3].text_input(f"∠ V-{fasa.upper()}", key=f"in_{prefix}_v_{fasa}_sdt")
        return data

    def ui_ukur_diff(prefix):
        data = {}
        for f in ['r', 's', 't']:
            c = st.columns(2)
            data[f'idiff_{prefix}_{f}'] = c[0].text_input(f"Idiff {f.upper()}", key=f"in_idiff_{prefix}_{f}")
            data[f'irest_{prefix}_{f}'] = c[1].text_input(f"Irest {f.upper()}", key=f"in_irest_{prefix}_{f}")
        return data

    def ui_kontinuitas(prefix):
        data = {}
        for f in ['r', 's', 't']:
            st.caption(f"Fasa {f.upper()}")
            c = st.columns(6)
            data[f'{prefix}_tb1{f}'] = c[0].text_input("TB1", key=f"in_{prefix}_tb1{f}")
            data[f'{prefix}_tb2{f}'] = c[1].text_input("TB2", key=f"in_{prefix}_tb2{f}")
            data[f'{prefix}_tb3{f}'] = c[2].text_input("TB3", key=f"in_{prefix}_tb3{f}")
            data[f'{prefix}_mpu{f}'] = c[3].text_input("MPU", key=f"in_{prefix}_mpu{f}")
            data[f'{prefix}_bpu{f}'] = c[4].text_input("BPU", key=f"in_{prefix}_bpu{f}")
            data[f'{prefix}_mtr{f}'] = c[5].text_input("MTR", key=f"in_{prefix}_mtr{f}")
        return data

    def ui_sistem_dc(prefix):
        data = {}
        c = st.columns(3)
        data[f'pn_{prefix}'] = c[0].text_input("P-N (V)", key=f"in_pn_{prefix}")
        data[f'pg_{prefix}'] = c[1].text_input("P-G (V)", key=f"in_pg_{prefix}")
        data[f'ng_{prefix}'] = c[2].text_input("N-G (V)", key=f"in_ng_{prefix}")
        return data

    # 1. IDENTITAS
    with st.expander("1. Identitas & Pengesahan", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            in_upt = st.text_input("UPT", value="BEKASI")
            in_ultg = st.text_input("ULTG", value="BEKASI")
            in_gi = st.text_input("GI / GITET", value="TAMBUN")
        with c2:
            in_bay = st.text_input("BAY", value="PENGHANTAR HANKOOK 2")
            in_tgl = st.date_input("Tanggal Pekerjaan")
            
        st.divider()
        st.write("**Pejabat Pengesah:**")
        k1, k2, k3 = st.columns(3)
        with k1:
            in_nama_kiri = st.selectbox("Nama Pelaksana", list(db_ttd.keys()), index=1)
        with k2:
            in_nama_tengah = st.selectbox("Pengawas Pekerjaan", list(db_ttd.keys()), index=4)
        with k3:
            in_nama_kanan = st.selectbox("Manager ULTG", list(db_ttd.keys()), index=2)

# 2. CHECKLIST (1 - 29) TIGA TAHAPAN
    cl_vals, cat_vals = {}, {}
    with st.expander("2. Form Checklist Pekerjaan", expanded=True):
        st.write("Pilih (✓) untuk selesai, (✗) jika ada masalah (wajib isi catatan).")
        
        # Membuat 3 Tab di layar aplikasi
        tab_seb, tab_saat, tab_ses = st.tabs(["🟢 SEBELUM", "🟡 SAAT", "🔴 SESUDAH"])
        
        # --- DAFTAR PEKERJAAN SEBELUM (Item 1-8) ---
        seb_list = {
            1: "1. Pengukuran arus & tegangan (Sebelum)",
            2: "2. Cek peralatan tidak bertegangan",
            3: "3. Pasang LOTO & tagging",
            4: "4. Pengukuran DC (Sebelum)",
            5: "5. Blocking & dokumentasi inisiasi CBF",
            6: "6. Amankan input analog ke defense scheme",
            7: "7. Dokumentasi setting/logic awal",
            8: "8. Dokumentasi terminal/wiring awal"
        }
        
        # --- DAFTAR PEKERJAAN SAAT (Item 9-16) ---
        saat_list = {
            9: "1. Pastikan setting relay sesuai dokumen",
            10: "2. Ukur kontinuitas sekunder CT",
            11: "→ Hasil Ukur Kontinuitas Fasa R",
            12: "→ Hasil Ukur Kontinuitas Fasa S",
            13: "→ Hasil Ukur Kontinuitas Fasa T",
            14: "3. Uji individu relay",
            15: "4. Uji fungsi trip/reclose",
            16: "5. Uji fungsi no trip/starting"
        }
        
        # --- DAFTAR PEKERJAAN SESUDAH (Item 17-29) ---
        ses_list = {
            17: "1. Kembalikan wiring/terminal awal",
            18: "2. Cek kekencangan terminal wiring",
            19: "3. Cek kondisi grounding (tidak double)",
            20: "4. Kembalikan setting/logic awal",
            21: "5. Ukur kontinuitas sekunder CT (Penormalan)",
            22: "→ Hasil Ukur Kontinuitas Penormalan",
            23: "6. Pastikan testplug terlepas",
            24: "7. Switch kontrol PMT ke Remote",
            25: "8. Kembalikan input analog defense scheme",
            26: "9. Mengembalikan blocking inisiasi (Part 1)",
            27: "9. Mengembalikan blocking inisiasi (Part 2)",
            28: "10. Ukur DC (Setelah)",
            29: "11. Ukur phasor arus & tegangan (Setelah)"
        }

        # Fungsi pintar pembuat antarmuka Checklist
        def buat_baris_checklist(kamus_pekerjaan):
            for nomor, teks in kamus_pekerjaan.items():
                st.markdown(f"**{teks}**")
                col_cek, col_cat = st.columns([1, 2])
                with col_cek:
                    cl_vals[nomor] = st.radio(
                        f"Item {nomor}", ["✓", "✗", "-"], horizontal=True, key=f"cl_{nomor}", label_visibility="collapsed"
                    )
                with col_cat:
                    if cl_vals[nomor] == "✗":
                        cat_vals[nomor] = st.text_input(f"Cat {nomor}", placeholder="⚠️ Wajib isi alasan...", key=f"cat_{nomor}")
                    else:
                        cat_vals[nomor] = st.text_input(f"Cat {nomor}", placeholder="Opsional...", key=f"cat_{nomor}", label_visibility="collapsed")
                st.write("")

        # Menampilkan antarmuka ke dalam masing-masing Tab
        with tab_seb:
            buat_baris_checklist(seb_list)
        with tab_saat:
            buat_baris_checklist(saat_list)
        with tab_ses:
            buat_baris_checklist(ses_list)

       
    # 3. KONTINUITAS CT
    data_kontinuitas = {}
    with st.expander("3. Nilai Kontinuitas CT", expanded=False):
        st.write("**SEBELUM PEMELIHARAAN**")
        data_kontinuitas.update(ui_kontinuitas("seb"))
        st.divider()
        st.write("**SESUDAH PEMELIHARAAN**")
        data_kontinuitas.update(ui_kontinuitas("set"))

   # 4. FUNGSI PROTEKSI
    fungsi_vals = {}
    with st.expander("4. Form Fungsi Proteksi (Utama, Indikasi, Cadangan)", expanded=True):
        st.write("Tentukan status 20 Item Fungsi Proteksi (Pilih ENABLE/DISABLE).")
        
        # Daftar 20 Fungsi Proteksi yang disesuaikan dengan Template Word
        daftar_fungsi = [
            "1. [UTAMA] RELAY HEALTHY / READY",
            "2. [UTAMA] LINE CURRENT DIFF",
            "3. [UTAMA] DISTANCE",
            "4. [UTAMA] DIRECTIONAL EARTH FAULT",
            "5. [UTAMA] AUTORECLOSE",
            "6. [UTAMA] TOR / SOTF",
            "7. [SINKRON] SETTING SINKRON (Main)",
            "8. [SINKRON] a. Live Bus - Live Line",
            "9. [SINKRON] b. Live Bus - Dead Line",
            "10. [SINKRON] c. Dead Bus - Live Line",
            "11. [SINKRON] d. Dead Bus - Dead Line",
            "12. [INDIKASI] STATUS CB A",
            "13. [INDIKASI] STATUS CB B",
            "14. [INDIKASI] STATUS CB C",
            "15. [INDIKASI] CB READY / HEALTHY / TROUBLE",
            "16. [INDIKASI] STATUS AUTORECLOSE",
            "17. [INDIKASI] COS / CARR. TROUBLE / COM FAIL",
            "18. [CADANGAN] RELAY HEALTHY / READY",
            "19. [CADANGAN] OVER CURRENT",
            "20. [CADANGAN] EARTH FAULT"
        ]

        for i, teks_fungsi in enumerate(daftar_fungsi):
            nomor = i + 1
            # Tampilkan teks fungsi sebagai label judul radio button
            fungsi_vals[nomor] = st.radio(
                teks_fungsi, 
                ["ENABLE", "DISABLE", "-"], 
                horizontal=True, 
                key=f"fungsi_{nomor}"
            )
            st.write("") # Sedikit jarak antar tombol

    # 5. PENGUKURAN
    data_ukur = {}
    with st.expander("5. Pengukuran Arus, Tegangan, Daya", expanded=False):
        tab1, tab2, tab3 = st.tabs(["🔴 Utama", "🟡 Cadangan", "🟢 Metering"])
        with tab1:
            st.write("**SEBELUM**")
            data_ukur.update(ui_ukur_fasa('ut_seb', ['r', 's', 't', 'n'], True))
            st.divider()
            st.write("**SESUDAH**")
            data_ukur.update(ui_ukur_fasa('ut_ses', ['r', 's', 't', 'n'], True))
        with tab2:
            st.write("**SEBELUM**")
            data_ukur.update(ui_ukur_fasa('cd_seb', ['r', 's', 't', 'n'], False))
            st.divider()
            st.write("**SESUDAH**")
            data_ukur.update(ui_ukur_fasa('cd_ses', ['r', 's', 't', 'n'], False))
        with tab3:
            st.write("**SEBELUM**")
            data_ukur.update(ui_ukur_fasa('mt_seb', ['r', 's', 't', 'n'], True))
            st.divider()
            st.write("**SESUDAH**")
            data_ukur.update(ui_ukur_fasa('mt_ses', ['r', 's', 't', 'n'], True))

    # 6. SISTEM DC
    data_dc = {}
    with st.expander("6. Sistem DC & Dokumentasi", expanded=False):
        st.write("**SEBELUM PEMELIHARAAN**")
        data_dc.update(ui_sistem_dc("seb_dc1"))
        data_dc.update(ui_sistem_dc("seb_dc2"))
        st.divider()
        st.write("**SESUDAH PEMELIHARAAN**")
        data_dc.update(ui_sistem_dc("ses_dc1"))
        data_dc.update(ui_sistem_dc("ses_dc2"))
        st.divider()
        in_foto_cl = st.file_uploader("Upload Capture Metering (Opsional)", type=["jpg", "jpeg", "png"], key="foto_cl")

    st.divider()

    # --- TOMBOL GENERATE DOKUMEN CHECKLIST ---
    if st.button("📄 Rakit Dokumen Checklist PHT", type="primary", use_container_width=True):
        with st.spinner("Menyusun ratusan data & tanda tangan... ⏳"):
            try:
                doc = DocxTemplate("template_cl_pht.docx")
                bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                tgl_format = f"{in_tgl.day} {bulan_indo[in_tgl.month - 1]} {in_tgl.year}"
                
                # Context Utama
                context = {
                    'upt': in_upt, 'ultg': in_ultg, 'gi': in_gi, 'bay': in_bay, 'tgl': tgl_format,
                    'nama_pelaksana': f"( {in_nama_kiri} )" if in_nama_kiri and in_nama_kiri != "Kosongkan (Tanda Tangan Basah)" else "",
                    'nama_pengawas': f"( {in_nama_tengah} )" if in_nama_tengah and in_nama_tengah != "Kosongkan (Tanda Tangan Basah)" else "",
                    'nama_manager': f"( {in_nama_kanan} )" if in_nama_kanan and in_nama_kanan != "Kosongkan (Tanda Tangan Basah)" else "",
                    'ttd_pelaksana': '', 'ttd_pengawas': '', 'ttd_manager': '', 'foto_lampiran': ''
                }
                
                def sisipkan_ttd(nama_pejabat):
                    if nama_pejabat in db_ttd and db_ttd[nama_pejabat] != "":
                        file_gambar = db_ttd[nama_pejabat]
                        if os.path.exists(file_gambar): return InlineImage(doc, file_gambar, height=Mm(15))
                    return ''
                
                context['ttd_pelaksana'] = sisipkan_ttd(in_nama_kiri)
                context['ttd_pengawas'] = sisipkan_ttd(in_nama_tengah)
                context['ttd_manager'] = sisipkan_ttd(in_nama_kanan)

                # Looping Otomatis memasukkan 29 item Checklist & Catatan ke Context
                for i in range(1, 30):
                    context[f'cl_{i}'] = cl_vals[i]
                    context[f'cat_{i}'] = cat_vals[i]
                
                # Looping Otomatis memasukkan 20 item Fungsi Enable/Disable
                for i in range(1, 21):
                    if fungsi_vals[i] == "ENABLE":
                        context[f'en_{i}'] = '✓'
                        context[f'dis_{i}'] = ''
                    elif fungsi_vals[i] == "DISABLE":
                        context[f'en_{i}'] = ''
                        context[f'dis_{i}'] = '✓'
                    else:
                        context[f'en_{i}'] = ''
                        context[f'dis_{i}'] = ''

                # Memasukkan semua data tabel yang di-generate otomatis
                context.update(data_kontinuitas)
                context.update(data_ukur)
                context.update(data_dc)

                # Lampiran Foto
                if in_foto_cl:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_foto:
                        tmp_foto.write(in_foto_cl.getvalue())
                        tmp_path = tmp_foto.name
                    context['foto_lampiran'] = InlineImage(doc, tmp_path, width=Mm(150))

                doc.render(context)
                file_output = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                doc.save(file_output.name)
                
                with open(file_output.name, "rb") as f:
                    docx_bytes = f.read()
                
                os.remove(file_output.name)
                if in_foto_cl: os.remove(tmp_path)

                st.success("✅ Form Checklist PHT berhasil dirakit!")
                st.download_button(
                    label="⬇️ Download Form Checklist Siap Cetak (Word .docx)",
                    data=docx_bytes,
                    file_name=f"CL_{in_gi}_{in_bay.replace(' ', '_')}.docx",
                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    type="primary"
                )
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# HALAMAN: DATABASE PERALATAN
# ==========================================
elif st.session_state.halaman == 'database':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🗄️ Mesin Pencari Database Peralatan ULTG Bekasi")
    
  # 1. FUNGSI MEMBACA SEMUA FILE CSV DI HALAMAN DEPAN
    @st.cache_data
    def muat_data_peralatan():
        # Perhatikan tanda bintang (*). Ini artinya "baca SEMUA file csv di sini"
        semua_file = glob.glob("*.csv") 
        list_dataframe = []
        for file in semua_file:
            try:
                # Membaca tiap file dan menggabungkannya
                df = pd.read_csv(file, on_bad_lines='skip')
                list_dataframe.append(df)
            except Exception as e:
                pass
        
        # Gabungkan semua data GI menjadi 1 tabel raksasa
        if list_dataframe:
            df_gabungan = pd.concat(list_dataframe, ignore_index=True)
            # Membersihkan data yang kosong (NaN) agar tampil rapi
            df_gabungan = df_gabungan.fillna("-")
            return df_gabungan
        else:
            return pd.DataFrame() # Return kosong jika file belum diupload

    # Mulai proses pemuatan data
    with st.spinner("Memuat puluhan ribu data peralatan... ⏳"):
        df_master = muat_data_peralatan()
        
        

    if df_master.empty:
        st.error("⚠️ Data belum tersedia. Pastikan Anda sudah membuat folder 'data_peralatan' dan meng-upload file CSV ke GitHub.")
    else:
        st.success(f"✅ Berhasil memuat **{len(df_master)}** unit peralatan dari seluruh GI.")
        
        # 2. FITUR FILTER PENCARIAN CERDAS
        with st.expander("🔍 Filter Pencarian (Klik untuk mencari spesifik)", expanded=True):
            col1, col2 = st.columns(2)
            
            # Filter berdasarkan GI / Penghantar (Kolom GI/Penghantar)
            list_gi = ["Semua GI"] + sorted(df_master['GI/Penghantar'].unique().tolist())
            pilih_gi = col1.selectbox("📍 Lokasi (GI / Penghantar):", list_gi)
            
            # Filter berdasarkan Merk (Kolom Merk)
            list_merk = ["Semua Merk"] + sorted(df_master['Merk'].unique().tolist())
            pilih_merk = col2.selectbox("🏷️ Merk Peralatan:", list_merk)
            
            col3, col4 = st.columns(2)
            # Filter berdasarkan Kategori PST (Kolom PST)
            list_pst = ["Semua Kategori"] + sorted(df_master['PST'].unique().tolist())
            pilih_pst = col3.selectbox("⚙️ Kategori Fungsi (PST):", list_pst)
            
            # Kolom Pencarian Bebas (Type / ID / dll)
            cari_bebas = col4.text_input("⌨️ Kata Kunci Bebas (Misal: PCS-902 / ABB):", "")

        # 3. LOGIKA PENYARINGAN DATA
        df_hasil = df_master.copy()
        
        if pilih_gi != "Semua GI":
            df_hasil = df_hasil[df_hasil['GI/Penghantar'] == pilih_gi]
        if pilih_merk != "Semua Merk":
            df_hasil = df_hasil[df_hasil['Merk'] == pilih_merk]
        if pilih_pst != "Semua Kategori":
            df_hasil = df_hasil[df_hasil['PST'] == pilih_pst]
        if cari_bebas != "":
            # Mencari kata kunci di semua kolom text
            df_hasil = df_hasil[
                df_hasil.astype(str).apply(lambda x: x.str.contains(cari_bebas, case=False, na=False)).any(axis=1)
            ]

        st.divider()
        st.markdown(f"**Menampilkan {len(df_hasil)} peralatan:**")
        
        # 4. MENAMPILKAN TABEL INTERAKTIF
        # st.dataframe memungkinkan user men-scroll, men-sortir kolom, dan memperbesar layar
        st.dataframe(
            df_hasil[['GI/Penghantar', 'PST', 'Merk', 'Type', 'Phasa', 'Volt', 'ID']], 
            use_container_width=True, 
            hide_index=True
        )
# HALAMAN 5: SETTINGS
# ==========================================
elif st.session_state.halaman == 'setting':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("⚙️ Settings")
    st.write("Versi 5.0 - PDF Generator Aktif 📄")
