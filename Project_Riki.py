import os
import io
import json
import glob
import tempfile
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# ==========================================
# 1. SETUP HALAMAN & FUNGSI GLOBAL
# ==========================================
st.set_page_config(page_title="App Proteksi", layout="centered", page_icon="⚡")

# --- FUNGSI PEMBACA DATABASE PERALATAN ---
@st.cache_data
def muat_data_peralatan():
    # Mencari file CSV di dalam folder data_peralatan ATAU di halaman depan
    semua_file = glob.glob("data_peralatan/*.csv") + glob.glob("*.csv") 
    list_dataframe = []
    for file in semua_file:
        try:
            # FIX: Tambahkan sep=';' karena CSV dari sistem biasanya pakai titik koma
            df = pd.read_csv(file, sep=';', on_bad_lines='skip', dtype=str)
            list_dataframe.append(df)
        except Exception:
            pass
    
    if list_dataframe:
        df_gabungan = pd.concat(list_dataframe, ignore_index=True)
        df_gabungan = df_gabungan.fillna("-")
        return df_gabungan
    else:
        return pd.DataFrame()

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
        st.button("📖\n\nInstruksi Kerja", type="primary", use_container_width=True, on_click=pindah_halaman, args=('ik',))
    with kolom2:
        st.button("🗺️\n\nWiring", type="primary", use_container_width=True, on_click=pindah_halaman, args=('wiring',))
        st.button("📋\n\nForm Har CL PHT", type="primary", use_container_width=True, on_click=pindah_halaman, args=('cl_pht',))
        st.button("🗄️\n\nData Peralatan", type="primary", use_container_width=True, on_click=pindah_halaman, args=('database',))
        st.button("⚙️\n\nSettings", type="primary", use_container_width=True, on_click=pindah_halaman, args=('setting',))

# ==========================================
# ==========================================
# HALAMAN 2: TEST PLUG
# ==========================================
elif st.session_state.halaman == 'test_plug':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🔌 Konfigurasi Test Block")

    # 1. DATABASE BAWAAN (Auto-Migrasi ke JSON)
    DATA_BAWAAN_TESTPLUG = {
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
        "GITET Muaratawar": {
            "Bay IBT 1": {
                "Relay Differential+REF Main A": {
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN": "X21:2, X21:4, X21:6, X21:8", "FUNGSI": "CT Arus HV", "AKSI": "DIFF HV"}, 
                        {"PIN": "X22:2, X22:4", "FUNGSI": "CT Arus Netral", "AKSI": "REF HV"}, 
                        {"PIN": "X22:6, X22:8", "FUNGSI": "CT Arus Netral", "AKSI": "REF LV"}
                    ] 
                },
                "Relay Differential+REF Main B": {
                    "Merk": "GE MULTILIN", "Tipe": "T60", "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN": "X21:2, X21:4, X21:6, X21:8", "FUNGSI": "CT Arus HV", "AKSI": "DIFF HV"}, 
                        {"PIN": "X22:2, X22:4", "FUNGSI": "CT Arus Netral", "AKSI": "REF HV"}, 
                        {"PIN": "X22:6, X22:8", "FUNGSI": "CT Arus Netral", "AKSI": "REF LV"}
                    ] 
                },
                "Relay CCP Main A": {
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN": "X25:22, X25:24, X25:26, X25:28", "FUNGSI": "CT Arus IBT", "AKSI": "CCP"},
                        {"PIN": "X25:2, X25:4, X25:6, X25:8", "FUNGSI": "CT Arus B", "AKSI": "CCP"},
                        {"PIN": "X26:22, X26:24, X26:26, X26:28", "FUNGSI": "CT Arus AB", "AKSI": "CCP"}
                    ] 
                },
                "Relay CCP Main B": {
                    "Merk": "MICOM", "Tipe": "P643", "No Seri": "BLM",
                    "Konfigurasi": [
                        {"PIN": "X24:22, X24:24, X24:26, X24:28", "FUNGSI": "CT Arus IBT", "AKSI": "CCP"}, 
                        {"PIN": "X25:22, X25:24, X25:26, X25:28", "FUNGSI": "CT Arus AB", "AKSI": "CCP"}, 
                        {"PIN": "X24:2, X24:4, X24:6, X24:8", "FUNGSI": "CT Arus IBT", "AKSI": "CCP"}
                    ] 
                },
                "Relay CBF B": {
                    "Merk": "MICOM", "Tipe": "P841", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "X23:2, X23:4, X23:6, X23:8", "FUNGSI": "CT Arus B", "AKSI": "CBF B"}] 
                },
                "Relay CBF AB": {
                    "Merk": "MICOM", "Tipe": "P841", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "X22:2, X22:4, X22:6, X22:8", "FUNGSI": "CT Arus AB", "AKSI": "CBF AB"}] 
                },
                "Relay OCR HV": {
                    "Merk": "SCHNEIDER", "Tipe": "P7", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "X24:2, X24:4, X24:6, X24:8", "FUNGSI": "CT Arus HV", "AKSI": "OCR HV"}] 
                },
                "Relay OCR LV": {
                    "Merk": "SCHNEIDER", "Tipe": "P5", "No Seri": "BLM",
                    "Konfigurasi": [{"PIN": "X26:22, X26:24, X26:26, X26:28", "FUNGSI": "CT Arus LV", "AKSI": "OCR LV"}] 
                }
            }
        }
    }
    
    FILE_DB_TESTPLUG = 'db_testplug.json'

    def simpan_db_testplug(data):
        with open(FILE_DB_TESTPLUG, 'w') as file:
            json.dump(data, file, indent=4)

    def muat_db_testplug():
        if os.path.exists(FILE_DB_TESTPLUG):
            with open(FILE_DB_TESTPLUG, 'r') as file:
                return json.load(file)
        else:
            simpan_db_testplug(DATA_BAWAAN_TESTPLUG)
            return DATA_BAWAAN_TESTPLUG

    database_testplug = muat_db_testplug()

    # 2. FILTER BERTINGKAT
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

    # --- FITUR TAMBAH DATA GI / BAY / RELAY BARU ---
    with st.expander("➕ Klik di sini untuk menambah Gardu Induk, Bay, atau Relay baru ke database"):
        # Kunci (key) form ini diperbarui agar menghindari duplikat
        with st.form("form_tambah_data_baru_unik"):
            st.info("💡 Ketik nama GI yang sudah ada untuk menambahkan Bay di GI tersebut, ATAU ketik nama GI baru untuk membuat daftar baru.")
            
            kol1, kol2, kol3 = st.columns(3)
            with kol1:
                baru_gi = st.text_input("📍 Nama Gardu Induk (Wajib)", placeholder="Contoh: GI Bekasi")
            with kol2:
                baru_bay = st.text_input("🏢 Nama Bay / Line (Wajib)", placeholder="Contoh: Bay Trafo 1")
            with kol3:
                baru_relay = st.text_input("🔌 Jenis Relay (Wajib)", placeholder="Contoh: Relay OCR")
            
            kol4, kol5, kol6 = st.columns(3)
            with kol4:
                baru_merk = st.text_input("🏷️ Merk", placeholder="Contoh: GE Multilin")
            with kol5:
                baru_tipe = st.text_input("⚙️ Tipe", placeholder="Contoh: P14D")
            with kol6:
                baru_seri = st.text_input("🔢 No Seri")
                
            st.write("**Konfigurasi PIN (Opsional, bisa ditambah nanti)**")
            kol7, kol8, kol9 = st.columns(3)
            with kol7:
                baru_pin = st.text_input("PIN Test Block", placeholder="Contoh: 1, 3, 5, 7")
            with kol8:
                baru_fungsi = st.text_input("Fungsi PIN", placeholder="Contoh: CT Arus")
            with kol9:
                baru_aksi = st.selectbox("Aksi Pengamanan", ["Shorting", "Isolasi", "Normal"])
                
            baru_catatan = st.text_area("Catatan Bawaan / SOP (Opsional)")
            
            # --- UPLOAD FOTO ---
            baru_foto = st.file_uploader("📸 Upload Foto Aktual Konfigurasi (Opsional)", type=["jpg", "jpeg", "png"])
            
            tombol_simpan_baru = st.form_submit_button("💾 Simpan Data Baru ke Database", type="primary")
            
            if tombol_simpan_baru:
                if baru_gi and baru_bay and baru_relay:
                    db_sekarang = muat_db_testplug()
                    
                    if baru_gi not in db_sekarang:
                        db_sekarang[baru_gi] = {}
                    if baru_bay not in db_sekarang[baru_gi]:
                        db_sekarang[baru_gi][baru_bay] = {}
                        
                    if baru_relay not in db_sekarang[baru_gi][baru_bay]:
                        db_sekarang[baru_gi][baru_bay][baru_relay] = {
                            "Merk": baru_merk, "Tipe": baru_tipe, "No Seri": baru_seri,
                            "Konfigurasi": [], "Catatan Bawaan": baru_catatan, "Nama Foto": ""
                        }
                    
                    if baru_pin and baru_fungsi:
                        db_sekarang[baru_gi][baru_bay][baru_relay]["Konfigurasi"].append({
                            "PIN": baru_pin, "FUNGSI": baru_fungsi, "AKSI": baru_aksi
                        })

                    if baru_foto:
                        nama_file_aman = f"TESTBLOCK_{baru_gi}_{baru_bay}_{baru_relay}.jpg".replace(" ", "_")
                        with open(nama_file_aman, "wb") as f:
                            f.write(baru_foto.getbuffer())
                        db_sekarang[baru_gi][baru_bay][baru_relay]["Nama Foto"] = nama_file_aman
                        upload_ke_gdrive(nama_file_aman, baru_foto.getvalue(), baru_foto.type)
                        
                    simpan_db_testplug(db_sekarang)
                    st.success(f"✅ Berhasil! {baru_relay} di {baru_gi} - {baru_bay} ditambahkan.")
                    st.rerun() 
                else:
                    st.error("⚠️ Nama Gardu Induk, Bay, dan Jenis Relay tidak boleh kosong!")

    st.divider()

    # 3. MENAMPILKAN HASIL DENGAN FITUR EDIT & HAPUS
    if pilihan_relay != "Pilih Relay...":
        data = database_testplug[pilihan_gi][pilihan_bay][pilihan_relay]
        st.success(f"Lokasi: {pilihan_gi} ➔ {pilihan_bay} ➔ {pilihan_relay}")
        
        # --- MEMBUAT 3 TAB ---
        tab_detail, tab_edit, tab_hapus = st.tabs(["👁️ Detail & Catatan", "✏️ Edit Alat", "🗑️ Hapus Data"])
        
        # TAB 1: TAMPILAN DETAIL
        with tab_detail:
            st.markdown(f"#### 🏷️ {data.get('Merk', '-')} {data.get('Tipe', '-')}")
            st.write(f"**No Seri:** `{data.get('No Seri', '-')}`")
            
            if "Nama Foto" in data and data["Nama Foto"] != "":
                if os.path.exists(data["Nama Foto"]):
                    st.image(data["Nama Foto"], caption=f"Foto Konfigurasi {pilihan_relay}", use_container_width=True)
                else:
                    st.info(f"📸 **Foto Referensi Tersedia di GDrive:** `{data['Nama Foto']}`")
            
            if "Catatan Bawaan" in data and data["Catatan Bawaan"] != "":
                st.warning(f"📌 **Catatan SOP:** {data['Catatan Bawaan']}")
            
            if "Konfigurasi" in data and len(data["Konfigurasi"]) > 0:
                st.write("**Panduan Test Block:**")
                st.table(pd.DataFrame(data["Konfigurasi"]))
                
            st.divider()
            st.write("### 📝 Catatan Aktual Lapangan")
            catatan_tambahan = st.text_area("Tambahkan temuan sementara di sesi ini:", placeholder="Ketik catatan di sini...")
            if st.button("💾 Simpan Catatan Tambahan", type="secondary"):
                if catatan_tambahan != "": st.success("✅ Catatan direkam sementara!")
                else: st.error("⚠️ Catatan masih kosong.")

            st.write("---")
            with st.expander("✏️ Edit Keterangan Database Permanen"):
                with st.form("form_edit_catatan_unik"):
                    catatan_baru = st.text_area("Ubah Catatan Bawaan/SOP:", value=data.get("Catatan Bawaan", ""))
                    if st.form_submit_button("🔄 Update Keterangan Permanen"):
                        db_sekarang = muat_db_testplug()
                        db_sekarang[pilihan_gi][pilihan_bay][pilihan_relay]["Catatan Bawaan"] = catatan_baru
                        simpan_db_testplug(db_sekarang)
                        st.success("✅ Keterangan berhasil di-update!")
                        st.rerun() 

        # TAB 2: EDIT SPESIFIKASI ALAT
        with tab_edit:
            st.write("Ubah spesifikasi alat jika ada kesalahan input.")
            with st.form("form_edit_spesifikasi"):
                edit_merk = st.text_input("Merk", value=data.get("Merk", ""))
                edit_tipe = st.text_input("Tipe", value=data.get("Tipe", ""))
                edit_seri = st.text_input("No Seri", value=data.get("No Seri", ""))
                
                if st.form_submit_button("💾 Simpan Perubahan Alat"):
                    db_sekarang = muat_db_testplug()
                    db_sekarang[pilihan_gi][pilihan_bay][pilihan_relay]["Merk"] = edit_merk
                    db_sekarang[pilihan_gi][pilihan_bay][pilihan_relay]["Tipe"] = edit_tipe
                    db_sekarang[pilihan_gi][pilihan_bay][pilihan_relay]["No Seri"] = edit_seri
                    simpan_db_testplug(db_sekarang)
                    st.success("✅ Spesifikasi berhasil diubah!")
                    st.rerun()

        # TAB 3: HAPUS DATA PERMANEN
        with tab_hapus:
            st.error(f"⚠️ Peringatan! Menghapus **{pilihan_relay}** akan menghilangkan datanya secara permanen dari {pilihan_gi} - {pilihan_bay}.")
            if st.button("🚨 Ya, Hapus Relay Ini", type="primary"):
                db_sekarang = muat_db_testplug()
                
                # Hapus relay
                del db_sekarang[pilihan_gi][pilihan_bay][pilihan_relay]
                
                # Bersihkan Bay jika sudah kosong (tidak ada relay lain)
                if len(db_sekarang[pilihan_gi][pilihan_bay]) == 0:
                    del db_sekarang[pilihan_gi][pilihan_bay]
                    
                # Bersihkan GI jika sudah kosong (tidak ada bay lain)
                if len(db_sekarang[pilihan_gi]) == 0:
                    del db_sekarang[pilihan_gi]
                    
                simpan_db_testplug(db_sekarang)
                st.success("✅ Data berhasil dihapus permanen!")
                st.rerun()
                        
# ==========================================
# HALAMAN 3: WIRING DIAGRAM & DOKUMENTASI
# ==========================================
elif st.session_state.halaman == 'wiring':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🗺️ Database & Dokumentasi Wiring")
    st.info("Pilih lokasi untuk melihat dokumen wiring asli (40GB) atau mengupload foto revisi terbaru.")

    # 1. DATABASE LOKASI & LINK GDRIVE
    lokasi_gi = {
        "GI Gandamekar": {
            "Bay Rajapaksi 1": {
                "Relay LCD": "https://drive.google.com/file/d/LINK_GDRIVE_LCD_RAJAPAKSI1/view",
                "Relay OCR": "https://drive.google.com/file/d/LINK_GDRIVE_OCR_RAJAPAKSI1/view"
            },
            "Bay Rajapaksi 2": {
                "Relay LCD": "", 
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
            relay_w = st.selectbox("Jenis Relay", ["Pilih..."] + list(lokasi_gi[gi_w][bay_w].keys()), key="w_relay")
        else:
            relay_w = st.selectbox("Jenis Relay", ["Pilih..."], key="w_relay")

    st.divider()

    # 3. FITUR BACA & TULIS
    if relay_w != "Pilih...":
        st.write(f"**📍 Target Lokasi:** {gi_w} ➔ {bay_w} ➔ {relay_w}")
        
        tab_lihat, tab_update = st.tabs(["👁️ Lihat Wiring Asli", "📸 Tambah Revisi Baru"])
        
        with tab_lihat:
            st.write("Akses *as-built drawing* asli yang tersimpan di server Google Drive.")
            link_asli = lokasi_gi[gi_w][bay_w][relay_w]
            
            if link_asli != "":
                st.link_button("🚀 Buka PDF Wiring di GDrive", link_asli, type="primary", use_container_width=True)
            else:
                st.warning("⚠️ Link file wiring untuk lokasi ini belum diinput ke dalam database.")

        with tab_update:
            st.write("Gunakan menu ini jika ada perubahan wiring/jumperan baru di lapangan.")
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
# HALAMAN 4: GENERATOR BERITA ACARA (BA)
# ==========================================
elif st.session_state.halaman == 'catatan':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📝 Generator BA (Otomasi Cerdas)")

    db_kegiatan = {
        "Resetting AVR": "1. Melakukan pengecekan setting yang terpasang\n2. Melakukan Resetting Parameter AVR\n3. Melakukan pengecekan bersama setting pasca resetting\n4. Pengujian individu / fungsi unjuk kerja\n5. Dokumentasi",
        "Remote Riding": "1. Persiapan koneksi VPN ke gateway / server\n2. Login ke relay target via remote akses\n3. Unduh data event dan disturbance record\n4. Analisa hasil unduhan record gangguan\n5. Dokumentasi",
        "Resetting Relay": "1. Melakukan pengecekan setting yang terpasang\n2. Melakukan Resetting Parameter Relay \n3. Melakukan Pengecekan bersama setting yang terpasang setelah resetting\n4. Melakukan pengujian individu relay pasca resetting\n5. Melakukan pengujian fungsi unjuk kerja relay pasca resetting\n6. Dokumentasi",
        "Modifikasi Alarm & Trip Bucholz": "1. Pemeriksaan kesesuaian rangkaian eksisting dengan wiring diagram\n2. Melakukan modifikasi rangkaian trip dan alarm relay bucholz\n3. Melakukan pengujian rangkaian baru\n4. Mencatat dan monitor indikasi yang muncul pada saat uji fungsi",
        "Lainnya (Ketik Manual)": ""
    }

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

    if st.button("📄 Buat Dokumen BA", type="primary", use_container_width=True):
        with st.spinner("Merakit BA & Menempelkan Tanda Tangan... ⏳"):
            try:
                doc = DocxTemplate("template_ba.docx")
                bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                tgl_format = f"{in_tgl.day} {bulan_indo[in_tgl.month - 1]} {in_tgl.year}"
                
                context = {
                    'no_ba': in_no_ba, 'judul_ba': in_judul, 'latar_belakang': in_latar,
                    'hari': in_hari, 'tgl': tgl_format, 'jam': in_jam.strftime('%H.%M'),
                    'alat': in_alat, 'kegiatan': in_kegiatan, 'anomali': in_anomali,
                    'perbaikan': in_perbaikan, 'tertunda': in_tertunda, 'kesimpulan': in_kesimpulan,
                    'pelaksana_1': in_p1, 'pelaksana_2': in_p2, 'pelaksana_3': in_p3,
                    
                    'jab_kiri': in_jab_kiri, 
                    'jab_tengah': in_jab_tengah, 
                    'jab_kanan': in_jab_kanan,
                    'nama_kiri': f"( {in_nama_kiri} )" if in_nama_kiri and in_nama_kiri != "Kosongkan (Tanda Tangan Basah)" else "",
                    'nama_tengah': f"( {in_nama_tengah} )" if in_nama_tengah and in_nama_tengah != "Kosongkan (Tanda Tangan Basah)" else "",
                    'nama_kanan': f"( {in_nama_kanan} )" if in_nama_kanan and in_nama_kanan != "Kosongkan (Tanda Tangan Basah)" else "",
                    
                    'ttd_kiri': '', 'ttd_tengah': '', 'ttd_kanan': '', 'foto_lampiran': ''
                }
                
                def sisipkan_ttd(nama_pejabat):
                    if nama_pejabat in db_ttd and db_ttd[nama_pejabat] != "":
                        file_gambar = db_ttd[nama_pejabat]
                        if os.path.exists(file_gambar): 
                            return InlineImage(doc, file_gambar, height=Mm(15)) 
                    return '' 

                context['ttd_kiri'] = sisipkan_ttd(in_nama_kiri)
                context['ttd_tengah'] = sisipkan_ttd(in_nama_tengah)
                context['ttd_kanan'] = sisipkan_ttd(in_nama_kanan)
                
                if in_foto:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_foto:
                        tmp_foto.write(in_foto.getvalue())
                        tmp_path = tmp_foto.name
                    context['foto_lampiran'] = InlineImage(doc, tmp_path, width=Mm(130))

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
# HALAMAN 5: INSTRUKSI KERJA (IK)
# ==========================================
elif st.session_state.halaman == 'ik':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("📖 Buku Saku Instruksi Kerja (IK)")
    st.write("Pilih alat uji atau jenis pekerjaan untuk melihat SOP dan langkah kerjanya.")

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
*(Silakan hapus teks ini dan ketikkan pengalaman Mas Riki di sini)*
"""
        }
    }

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
        for i, item_langkah in enumerate(data_ik['Langkah Kerja']):
            if isinstance(item_langkah, dict):
                st.write(f"**{i+1}.** {item_langkah['teks']}")
                if item_langkah.get('gambar') and os.path.exists(item_langkah['gambar']):
                    st.image(item_langkah['gambar'], use_container_width=True)
            else:
                st.write(f"**{i+1}.** {item_langkah}")

        st.write("---")
        
        if "Perhatian" in data_ik and data_ik["Perhatian"] != "":
            st.warning(data_ik['Perhatian'])
            
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

    # 2. CHECKLIST (1 - 29)
    cl_vals, cat_vals = {}, {}
    with st.expander("2. Form Checklist Pekerjaan", expanded=True):
        st.write("Pilih (✓) untuk selesai, (✗) jika ada masalah (wajib isi catatan).")
        tab_seb, tab_saat, tab_ses = st.tabs(["🟢 SEBELUM", "🟡 SAAT", "🔴 SESUDAH"])
        
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
    with st.expander("4. Form Fungsi Proteksi (Utama, Indikasi, Cadangan)", expanded=False):
        st.write("Tentukan status 20 Item Fungsi Proteksi (Pilih ENABLE/DISABLE).")
        
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
            fungsi_vals[nomor] = st.radio(
                teks_fungsi, 
                ["ENABLE", "DISABLE", "-"], 
                horizontal=True, 
                key=f"fungsi_{nomor}"
            )
            st.write("")

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

                for i in range(1, 30):
                    context[f'cl_{i}'] = cl_vals[i]
                    context[f'cat_{i}'] = cat_vals[i]
                
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

                context.update(data_kontinuitas)
                context.update(data_ukur)
                context.update(data_dc)

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
# HALAMAN 7: DATABASE PERALATAN
# ==========================================
elif st.session_state.halaman == 'database':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("🗄️ Mesin Pencari Database Peralatan ULTG Bekasi")
    
    with st.spinner("Memuat puluhan ribu data peralatan... ⏳"):
        df_master = muat_data_peralatan()

    if df_master.empty:
        st.error("⚠️ Data belum tersedia. Pastikan Anda sudah meng-upload file CSV ke GitHub.")
    else:
        st.success(f"✅ Berhasil memuat **{len(df_master)}** unit peralatan dari seluruh GI.")
        
        with st.expander("🔍 Filter Pencarian (Klik untuk mencari spesifik)", expanded=True):
            col1, col2 = st.columns(2)
            
            # Cek kolom GI/Penghantar
            if 'GI/Penghantar' in df_master.columns:
                list_gi = ["Semua GI"] + sorted(df_master['GI/Penghantar'].astype(str).unique().tolist())
            else:
                list_gi = ["Semua GI"]
            pilih_gi = col1.selectbox("📍 Lokasi (GI / Penghantar):", list_gi)
            
            # Cek kolom Merk
            if 'Merk' in df_master.columns:
                list_merk = ["Semua Merk"] + sorted(df_master['Merk'].astype(str).unique().tolist())
            else:
                list_merk = ["Semua Merk"]
            pilih_merk = col2.selectbox("🏷️ Merk Peralatan:", list_merk)
            
            col3, col4 = st.columns(2)
            # Cek kolom PST
            if 'PST' in df_master.columns:
                list_pst = ["Semua Kategori"] + sorted(df_master['PST'].astype(str).unique().tolist())
            else:
                list_pst = ["Semua Kategori"]
            pilih_pst = col3.selectbox("⚙️ Kategori Fungsi (PST):", list_pst)
            
            cari_bebas = col4.text_input("⌨️ Kata Kunci Bebas (Misal: PCS-902 / ABB):", "")

        df_hasil = df_master.copy()
        
        if pilih_gi != "Semua GI" and 'GI/Penghantar' in df_hasil.columns:
            df_hasil = df_hasil[df_hasil['GI/Penghantar'] == pilih_gi]
        if pilih_merk != "Semua Merk" and 'Merk' in df_hasil.columns:
            df_hasil = df_hasil[df_hasil['Merk'] == pilih_merk]
        if pilih_pst != "Semua Kategori" and 'PST' in df_hasil.columns:
            df_hasil = df_hasil[df_hasil['PST'] == pilih_pst]
        if cari_bebas != "":
            df_hasil = df_hasil[
                df_hasil.astype(str).apply(lambda x: x.str.contains(cari_bebas, case=False, na=False)).any(axis=1)
            ]

        st.divider()
        st.markdown(f"**Menampilkan {len(df_hasil)} peralatan:**")
        
        # --- MENGATUR KOLOM YANG TAMPIL & MENGGANTI NAMA KOLOM BIAR RAPI ---
        # Kita ambil nama kolom dari CSV yang cocok dengan kebutuhanmu
        kolom_tersedia = df_hasil.columns.tolist()
        kolom_target = []
        rename_dict = {}

        # 1. Nama GI
        if 'GI/Penghantar' in kolom_tersedia:
            kolom_target.append('GI/Penghantar')
            rename_dict['GI/Penghantar'] = 'Gardu Induk'
            
        # 2. Nama Bay (Biasanya di CSV SAP namanya Functloc atau Penempatan)
        if 'Functloc' in kolom_tersedia:
            kolom_target.append('Functloc')
            rename_dict['Functloc'] = 'Bay / Lokasi'
            
        # 3. Jenis Peralatan (PST)
        if 'PST' in kolom_tersedia:
            kolom_target.append('PST')
            rename_dict['PST'] = 'Jenis Peralatan'
            
        # 4. Merk
        if 'Merk' in kolom_tersedia:
            kolom_target.append('Merk')
            
        # 5. Type
        if 'Type' in kolom_tersedia:
            kolom_target.append('Type')
            rename_dict['Type'] = 'Tipe'
            
        # 6. No Seri (Bisa ID atau SID)
        if 'ID' in kolom_tersedia:
            kolom_target.append('ID')
            rename_dict['ID'] = 'No Seri'
        elif 'SID' in kolom_tersedia:
            kolom_target.append('SID')
            rename_dict['SID'] = 'No Seri'

        # Eksekusi pemotongan kolom dan tampilkan
        if len(kolom_target) > 0:
            df_tampil = df_hasil[kolom_target].rename(columns=rename_dict)
            st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_hasil, use_container_width=True, hide_index=True)

# ==========================================
# HALAMAN 8: SETTINGS
# ==========================================
elif st.session_state.halaman == 'setting':
    st.button("⬅️ Kembali ke Menu", type="secondary", on_click=pindah_halaman, args=('menu',))
    st.divider()
    st.subheader("⚙️ Settings")
    st.write("Versi 5.1 - Generator & Database Super Aktif ⚡")
