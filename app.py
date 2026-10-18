import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import folium
from streamlit_folium import st_folium

# ─────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SPK Wisata Jogja – Metode SAW",
    layout="wide",
    page_icon="🏛️",
)

# ─────────────────────────────────────────────────────────
#  GLOBAL STYLE  (Yogyakarta Heritage Theme)
#  Foto background: Unsplash CDN (bebas royalti)
#  Palet: Batik Cokelat Emas + Hijau Tua Keraton
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── RESET & BASE ── */
html, body, [data-testid="stApp"] {
    font-family: 'Inter', sans-serif;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #1a1008 0%, #2d1f0a 55%, #3b2a10 100%);
    border-right: 2px solid #c8922a;
}
[data-testid="stSidebar"] * { color: #f0e6cc !important; }
[data-testid="stSidebar"] .stRadio label { 
    font-size: 0.93rem; 
    padding: 6px 0;
    transition: color 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: #f5c842 !important; }
[data-testid="stSidebar"] hr { border-color: #c8922a55; }

/* ── MAIN BACKGROUND – subtle batik texture via gradient ── */
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"] {
    background: #fdf8f0;
}
section.main > div { padding-top: 0 !important; }

/* ── HERO BANNER ── */
.hero-banner {
    position: relative;
    width: 100%;
    min-height: 360px;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 28px;
    background: linear-gradient(135deg, #1a1008 0%, #3b2a10 100%);
    display: flex;
    align-items: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.28);
}
.hero-bg {
    position: absolute; inset: 0;
    background-image: url('https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=1400&q=80');
    background-size: cover;
    background-position: center 40%;
    opacity: 0.38;
}
.hero-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(90deg, rgba(26,16,8,0.92) 0%, rgba(26,16,8,0.55) 60%, rgba(26,16,8,0.15) 100%);
}
.hero-content {
    position: relative;
    z-index: 2;
    padding: 40px 48px;
    max-width: 620px;
}
.hero-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c8922a;
    margin-bottom: 10px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #fdf5e0;
    line-height: 1.18;
    margin-bottom: 14px;
}
.hero-sub {
    font-size: 0.95rem;
    color: #d4c8b0;
    line-height: 1.65;
    margin-bottom: 22px;
}
.hero-badge {
    display: inline-block;
    background: rgba(200,146,42,0.18);
    border: 1px solid #c8922a;
    color: #f5c842;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 5px 14px;
    border-radius: 20px;
}

/* ── METRIC CARDS ── */
.metric-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 160px;
    background: linear-gradient(145deg, #ffffff, #fdf5e4);
    border-radius: 14px;
    padding: 20px 22px;
    border: 1px solid #e8d8b0;
    border-left: 4px solid #c8922a;
    box-shadow: 0 2px 12px rgba(200,146,42,0.10);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(200,146,42,0.18); }
.metric-icon { font-size: 1.4rem; margin-bottom: 6px; }
.metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem; font-weight: 700; color: #2d1f0a;
}
.metric-lbl { font-size: 0.78rem; color: #8a7055; font-weight: 500; letter-spacing: 0.04em; }

/* ── SECTION HEADERS ── */
.sec-header {
    display: flex; align-items: center; gap: 10px;
    margin: 28px 0 16px;
}
.sec-header-line { flex:1; height: 1px; background: linear-gradient(90deg, #c8922a55, transparent); }
.sec-header-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem; font-weight: 600; color: #2d1f0a;
    white-space: nowrap;
}
.sec-header-dot { color: #c8922a; font-size: 1.1rem; }

/* ── INFO BOX ── */
.info-box {
    background: linear-gradient(135deg, #fffbf0, #fff8e8);
    border: 1px solid #e8d090;
    border-radius: 12px;
    padding: 18px 22px;
    font-size: 0.9rem; color: #4a3520; line-height: 1.7;
    margin-bottom: 20px;
}
.info-box strong { color: #8a5c1a; }

/* ── CRITERIA TABLE WRAPPER ── */
.criteria-grid { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 24px; }
.crit-pill {
    background: #fff;
    border: 1.5px solid #ddd0b0;
    border-radius: 10px;
    padding: 10px 16px;
    flex: 1; min-width: 170px;
}
.crit-pill-code { font-size: 0.7rem; font-weight: 700; color: #c8922a; letter-spacing: 0.1em; }
.crit-pill-name { font-size: 0.88rem; font-weight: 600; color: #2d1f0a; margin: 2px 0; }
.crit-pill-type {
    font-size: 0.72rem; font-weight: 600;
    padding: 2px 8px; border-radius: 8px; display: inline-block;
}
.benefit { background: #e8f5e9; color: #2e7d32; }
.cost    { background: #fce4ec; color: #c62828; }

/* ── SAW FLOW STEPS ── */
.flow-steps { display: flex; gap: 0; margin-bottom: 24px; }
.flow-step {
    flex: 1; background: #fff; padding: 18px 16px 16px;
    border: 1px solid #e0d0b0; text-align: center;
    position: relative;
}
.flow-step:first-child { border-radius: 12px 0 0 12px; }
.flow-step:last-child  { border-radius: 0 12px 12px 0; }
.flow-step::after {
    content: '→';
    position: absolute; right: -12px; top: 50%; transform: translateY(-50%);
    color: #c8922a; font-size: 1.2rem; z-index: 1; background: #fff; padding: 0 2px;
}
.flow-step:last-child::after { display: none; }
.flow-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem; font-weight: 700; color: #c8922a;
}
.flow-title { font-size: 0.8rem; font-weight: 700; color: #2d1f0a; margin: 4px 0 2px; }
.flow-desc  { font-size: 0.72rem; color: #8a7055; line-height: 1.5; }

/* ── PAGE BG IMAGES ── */
.page-bg-bar {
    width: 100%;
    height: 160px;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 24px;
    position: relative;
}
.page-bg-bar img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: center 65%;
    filter: brightness(0.72) saturate(1.1);
}
.page-bg-bar-text {
    position: absolute; bottom: 16px; left: 24px;
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem; font-weight: 700; color: #fff;
    text-shadow: 0 2px 8px rgba(0,0,0,0.55);
}

/* ── RANK CARDS ── */
.rank-cards { display: flex; gap: 14px; margin-top: 20px; }
.rank-card {
    flex: 1; border-radius: 14px; padding: 20px 18px;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.14);
    color: #fff;
}
.rank-card-1 { background: linear-gradient(135deg, #7c5c1a, #c8922a); }
.rank-card-2 { background: linear-gradient(135deg, #4a5568, #718096); }
.rank-card-3 { background: linear-gradient(135deg, #7b4f2e, #a0714d); }
.rank-medal  { font-size: 2rem; margin-bottom: 6px; }
.rank-pos    { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; opacity: 0.8; }
.rank-name   { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; margin: 4px 0 8px; line-height: 1.3; }
.rank-type   { font-size: 0.72rem; opacity: 0.78; margin-bottom: 10px; }
.rank-score  { font-size: 1.3rem; font-weight: 700; }
.rank-score-lbl { font-size: 0.7rem; opacity: 0.75; }
.rank-detail { font-size: 0.78rem; opacity: 0.85; margin-top: 8px; line-height: 1.6; }

/* ── BUTTONS ── */
div.stButton > button {
    background: linear-gradient(135deg, #c8922a, #a06a18) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important; letter-spacing: 0.04em !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 4px 14px rgba(200,146,42,0.35) !important;
    transition: opacity 0.2s !important;
}
div.stButton > button:hover { opacity: 0.88 !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── STREAMLIT WIDGET LABELS ── */
label { color: #2d1f0a !important; font-weight: 500 !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────

def fix_lat(val):
    s = str(val).replace(' ', '')
    sign = '-' if s.startswith('-') else ''
    digits = s.replace('-', '').replace('.', '')
    return float(sign + digits[0] + '.' + digits[1:])

def fix_lon(val):
    s = str(val).replace(' ', '')
    digits = s.replace('-', '').replace('.', '')
    return float(digits[0:3] + '.' + digits[3:])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi    = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def section_header(icon, text):
    st.markdown(f"""
    <div class="sec-header">
        <span class="sec-header-dot">{icon}</span>
        <span class="sec-header-text">{text}</span>
        <div class="sec-header-line"></div>
    </div>""", unsafe_allow_html=True)

def page_banner(img_url, title):
    st.markdown(f"""
    <div class="page-bg-bar">
        <img src="{img_url}" alt="">
        <div class="page-bg-bar-text">{title}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_csv("tourism_jogja.csv")
    df["lat"] = df["latitude"].apply(fix_lat)
    df["lon"] = df["longitude"].apply(fix_lon)
    LAT_PUSAT, LON_PUSAT = -7.801363, 110.364787
    df["jarak_km"] = haversine(df["lat"], df["lon"], LAT_PUSAT, LON_PUSAT)
    avg_rating_per_type = df.groupby("type")["rating"].mean()
    df["kategori"] = df["type"].map(avg_rating_per_type).round(3)
    df["popularitas"] = (
        pd.cut(df["rating"], bins=[0, 3.9, 4.2, 4.5, 4.7, 5.0],
               labels=[1, 2, 3, 4, 5]).astype(float)
    ).fillna(3).astype(int)
    return df

df_raw = load_data()

KRITERIA = {
    "C1": {"label": "Rating Wisatawan",      "col": "rating",      "tipe": "benefit"},
    "C2": {"label": "Harga Tiket (HTM)",     "col": "htm",         "tipe": "cost"},
    "C3": {"label": "Jarak dari Pusat Kota", "col": "jarak_km",    "tipe": "cost"},
    "C4": {"label": "Kategori Wisata",       "col": "kategori",    "tipe": "benefit"},
    "C5": {"label": "Popularitas",           "col": "popularitas", "tipe": "benefit"},
}


# ─────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 18px 0 12px;'>
        <div style='font-size:2.2rem; margin-bottom:4px;'>🏛️</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.15rem; font-weight:700; color:#f5c842; line-height:1.3;'>
            SPK Wisata Jogja
        </div>
        <div style='font-size:0.72rem; color:#c8a86a; letter-spacing:0.12em; margin-top:4px;'>
            METODE SAW
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#c8922a44; margin:0 0 14px'>", unsafe_allow_html=True)

    halaman = st.radio(
        "Navigasi",
        ["🏠  Beranda", "📊  Dataset", "⚖️  Hitung SPK", "📈  Visualisasi", "🗺️  Peta"],
    )

    st.markdown("<hr style='border-color:#c8922a44; margin:14px 0 10px'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#a08060; line-height:1.8; padding:0 4px;'>
        📁 <b>Dataset:</b> Tourism Jogja<br>
        🏷️ <b>Total:</b> 437 destinasi<br>
        📍 <b>Area:</b> DI Yogyakarta<br>
        🔢 <b>Sumber:</b> Kaggle / Data Primer
    </div>
    """, unsafe_allow_html=True)

# strip emoji prefix for comparison
halaman_key = halaman.split("  ", 1)[-1] if "  " in halaman else halaman


# ─────────────────────────────────────────────────────────
#  PAGE 1 – BERANDA
# ─────────────────────────────────────────────────────────

if halaman_key == "Beranda":

    # Hero
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-eyebrow">Sistem Pendukung Keputusan • Yogyakarta</div>
            <div class="hero-title">Temukan Wisata<br>Terbaik di Jogja</div>
            <div class="hero-sub">
                Rekomendasi destinasi wisata Yogyakarta berbasis data menggunakan
                metode <strong style="color:#f5c842">Simple Additive Weighting (SAW)</strong>
                — 437 destinasi, 5 kriteria, hasil objektif.
            </div>
            <span class="hero-badge">🗺️ 437 Destinasi Wisata</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-icon">🏛️</div>
            <div class="metric-val">{len(df_raw):,}</div>
            <div class="metric-lbl">Total Destinasi</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🎭</div>
            <div class="metric-val">{df_raw["type"].nunique()}</div>
            <div class="metric-lbl">Jenis Wisata</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-val">{df_raw["rating"].mean():.2f}</div>
            <div class="metric-lbl">Rata-rata Rating</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-val">Rp {df_raw["htm"].mean():,.0f}</div>
            <div class="metric-lbl">Rata-rata HTM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        section_header("📋", "Tentang Sistem")
        st.markdown("""
        <div class="info-box">
            Sistem ini membantu wisatawan memilih destinasi terbaik di Yogyakarta
            berdasarkan <strong>5 kriteria objektif</strong> menggunakan metode
            <strong>Simple Additive Weighting (SAW)</strong>.
            Seluruh kriteria diturunkan dari data asli dataset — tidak ada penilaian subjektif.
        </div>
        """, unsafe_allow_html=True)

        section_header("🔢", "Kriteria Penilaian")
        crit_data = [
            ("C1", "Rating Wisatawan",      "benefit", "Kolom rating"),
            ("C2", "Harga Tiket (HTM)",     "cost",    "Kolom htm"),
            ("C3", "Jarak dari Pusat Kota", "cost",    "Haversine lat/lon"),
            ("C4", "Kategori Wisata",       "benefit", "Avg rating per type"),
            ("C5", "Popularitas",           "benefit", "Normalisasi rating"),
        ]
        pills_html = '<div class="criteria-grid">'
        for code, name, tipe, src in crit_data:
            tipe_class = "benefit" if tipe == "benefit" else "cost"
            tipe_label = "Benefit" if tipe == "benefit" else "Cost"
            pills_html += f"""
            <div class="crit-pill">
                <div class="crit-pill-code">{code}</div>
                <div class="crit-pill-name">{name}</div>
                <span class="crit-pill-type {tipe_class}">{tipe_label}</span>
                <div style="font-size:0.68rem;color:#8a7055;margin-top:4px;">{src}</div>
            </div>"""
        pills_html += "</div>"
        st.markdown(pills_html, unsafe_allow_html=True)

    with col_b:
        section_header("🔄", "Alur Metode SAW")
        st.markdown("""
        <div class="flow-steps">
            <div class="flow-step">
                <div class="flow-num">01</div>
                <div class="flow-title">Input Data</div>
                <div class="flow-desc">437 destinasi wisata dari dataset Jogja</div>
            </div>
            <div class="flow-step">
                <div class="flow-num">02</div>
                <div class="flow-title">Normalisasi</div>
                <div class="flow-desc">Matriks ternormalisasi benefit / cost</div>
            </div>
            <div class="flow-step">
                <div class="flow-num">03</div>
                <div class="flow-title">Pembobotan</div>
                <div class="flow-desc">Σ(bobot × nilai ternormalisasi)</div>
            </div>
            <div class="flow-step">
                <div class="flow-num">04</div>
                <div class="flow-title">Ranking</div>
                <div class="flow-desc">Urutkan skor dari tertinggi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        section_header("🗂️", "Komposisi Jenis Wisata")
        fig_p, ax_p = plt.subplots(figsize=(5.5, 5.5))
        type_counts = df_raw["type"].value_counts()
        colors_pie = ["#c8922a","#3d6b4f","#7b4f2e","#4a5568","#6d3f1f",
                      "#5f7c68","#8a6030","#9b7040"][:len(type_counts)]
        wedges, texts, autotexts = ax_p.pie(
            type_counts.values,
            labels=None,
            autopct="%1.0f%%",
            startangle=110,
            colors=colors_pie,
            wedgeprops=dict(edgecolor="white", linewidth=1.5),
            pctdistance=0.75,
        )
        for at in autotexts:
            at.set_fontsize(8); at.set_color("white"); at.set_weight("bold")
        ax_p.legend(type_counts.index, loc="lower center",
                    bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=8,
                    frameon=False)
        ax_p.set_facecolor("#fdf8f0"); fig_p.patch.set_facecolor("#fdf8f0")
        plt.tight_layout()
        st.pyplot(fig_p)
        plt.close()


# ─────────────────────────────────────────────────────────
#  PAGE 2 – DATASET
# ─────────────────────────────────────────────────────────

elif halaman_key == "Dataset":
    page_banner(
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1400&q=80",
        "📊 Dataset Destinasi Wisata Jogja"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("<div style='background:#fff;border:1px solid #e0d0b0;border-radius:12px;padding:18px;'>", unsafe_allow_html=True)
        section_header("🔍", "Filter")
        filter_tipe = st.multiselect(
            "Jenis Wisata",
            options=sorted(df_raw["type"].unique()),
            default=[],
            placeholder="Semua jenis",
        )
        min_rating = st.slider("Minimum Rating", 2.5, 5.0, 4.0, 0.1)
        st.markdown("</div>", unsafe_allow_html=True)

    df_view = df_raw.copy()
    if filter_tipe:
        df_view = df_view[df_view["type"].isin(filter_tipe)]
    df_view = df_view[df_view["rating"] >= min_rating]

    with col2:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#fffbf0,#fff5e0);
             border:1px solid #e0c880;border-radius:10px;
             padding:12px 18px;margin-bottom:14px;font-size:0.88rem;color:#5a3a10;'>
            🗺️ Menampilkan <strong>{len(df_view)} destinasi</strong> sesuai filter
            dari total <strong>{len(df_raw)}</strong> destinasi
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            df_view[["place_id","name","type","rating","htm","jarak_km","kategori","popularitas"]].rename(columns={
                "place_id":"ID","name":"Nama Destinasi","type":"Jenis",
                "rating":"Rating","htm":"HTM (Rp)","jarak_km":"Jarak (km)",
                "kategori":"Skor Kategori","popularitas":"Popularitas",
            }),
            width="stretch", height=430,
        )

    section_header("📐", "Statistik Deskriptif")
    st.dataframe(
        df_raw[["rating","htm","jarak_km","kategori","popularitas"]].describe().round(2),
        width="stretch"
    )


# ─────────────────────────────────────────────────────────
#  PAGE 3 – HITUNG SPK
# ─────────────────────────────────────────────────────────

elif halaman_key == "Hitung SPK":
    page_banner(
        "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=1400&q=80",
        "⚖️ Perhitungan SPK – Metode SAW"
    )

    section_header("🎚️", "Bobot Kriteria")
    st.markdown("<p style='color:#6a5040;font-size:0.88rem;margin-bottom:12px;'>Atur bobot setiap kriteria (total harus = 100%). Bobot mencerminkan prioritas Anda.</p>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    w1 = col1.slider("C1 – Rating",      0, 100, 30, 5)
    w2 = col2.slider("C2 – HTM",         0, 100, 25, 5)
    w3 = col3.slider("C3 – Jarak",       0, 100, 20, 5)
    w4 = col4.slider("C4 – Kategori",    0, 100, 15, 5)
    w5 = col5.slider("C5 – Popularitas", 0, 100, 10, 5)

    total_bobot = w1 + w2 + w3 + w4 + w5
    if total_bobot != 100:
        st.warning(f"⚠️ Total bobot = **{total_bobot}** (harus tepat 100)")
    else:
        st.success(f"✅ Total bobot = {total_bobot} – Valid!")

    section_header("🎯", "Filter Preferensi")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_jenis = st.multiselect(
            "Jenis Wisata",
            options=sorted(df_raw["type"].unique()),
            default=["Alam","Budaya Dan Sejarah","Pantai"],
        )
    with col_f2:
        max_htm = st.number_input("Batas Maks HTM (Rp)", 0, 1_500_000, 100_000, 5_000)
    with col_f3:
        top_n = st.selectbox("Tampilkan Top N", [10,20,30,50,100], index=1)

    st.markdown("<div style='margin: 12px 0'>", unsafe_allow_html=True)
    hitung = st.button("▶  Jalankan Perhitungan SAW", width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    if hitung:
        if total_bobot != 100:
            st.error("Harap sesuaikan bobot hingga totalnya tepat 100.")
        else:
            df_calc = df_raw.copy()
            if filter_jenis:
                df_calc = df_calc[df_calc["type"].isin(filter_jenis)]
            df_calc = df_calc[df_calc["htm"] <= max_htm].reset_index(drop=True)

            if len(df_calc) < 2:
                st.error("Data terlalu sedikit setelah filter. Longgarkan filter.")
            else:
                bobot = np.array([w1, w2, w3, w4, w5]) / 100
                cols  = [v["col"]  for v in KRITERIA.values()]
                tipes = [v["tipe"] for v in KRITERIA.values()]
                matriks = df_calc[cols].values.astype(float)

                with st.expander("STEP 1 – Matriks Keputusan (10 baris pertama)", expanded=True):
                    st.dataframe(
                        pd.DataFrame(matriks[:10],
                            columns=[v["label"] for v in KRITERIA.values()],
                            index=df_calc["name"].iloc[:10]).round(4),
                        width="stretch")

                norm = np.zeros_like(matriks)
                for j, tipe in enumerate(tipes):
                    col_vals = matriks[:, j]
                    if tipe == "benefit":
                        denom = col_vals.max()
                        norm[:, j] = col_vals / denom if denom != 0 else 0
                    else:
                        nonzero = col_vals[col_vals > 0]
                        if len(nonzero) > 0:
                            denom = nonzero.min()
                            norm[:, j] = np.where(
                                col_vals == 0, 1.0,
                                denom / np.where(col_vals == 0, 1.0, col_vals),
                            )
                        else:
                            norm[:, j] = 1.0

                with st.expander("STEP 2 – Matriks Normalisasi SAW"):
                    st.dataframe(
                        pd.DataFrame(norm[:10],
                            columns=[v["label"] for v in KRITERIA.values()],
                            index=df_calc["name"].iloc[:10]).round(4),
                        width="stretch")

                with st.expander("STEP 3 – Bobot yang Digunakan"):
                    st.dataframe(pd.DataFrame({
                        "Kriteria": [v["label"] for v in KRITERIA.values()],
                        "Tipe":     [v["tipe"].capitalize() for v in KRITERIA.values()],
                        "Bobot":    bobot,
                        "Bobot (%)": [f"{b*100:.0f}%" for b in bobot],
                    }), width="stretch", hide_index=True)

                skor = np.dot(norm, bobot)
                df_calc["Skor SAW"] = np.round(skor, 4)
                df_result = (
                    df_calc[["name","type","rating","htm","jarak_km",
                              "kategori","popularitas","Skor SAW"]]
                    .sort_values("Skor SAW", ascending=False)
                    .head(top_n).reset_index(drop=True)
                )
                df_result.index += 1
                df_result.index.name = "Peringkat"

                section_header("🏆", f"Top {top_n} Hasil Perangkingan")
                st.markdown(f"<p style='color:#6a5040;font-size:0.85rem;margin-bottom:10px;'>Dari <strong>{len(df_calc)}</strong> destinasi setelah filter</p>", unsafe_allow_html=True)

                def highlight_rows(row):
                    if row.name == 1: return ["background-color:#c8922a22;font-weight:600"] * len(row)
                    if row.name == 2: return ["background-color:#71809622"] * len(row)
                    if row.name == 3: return ["background-color:#a0714d22"] * len(row)
                    return [""] * len(row)

                st.dataframe(
                    df_result.rename(columns={
                        "name":"Nama Destinasi","type":"Jenis","rating":"Rating",
                        "htm":"HTM (Rp)","jarak_km":"Jarak (km)",
                        "kategori":"Skor Kategori","popularitas":"Popularitas"
                    }).style.apply(highlight_rows, axis=1).format({
                        "HTM (Rp)":"Rp {:,.0f}","Jarak (km)":"{:.2f} km","Skor SAW":"{:.4f}"
                    }),
                    width="stretch", height=460,
                )

                st.session_state["df_result"] = df_result
                st.session_state["df_calc"]   = df_calc

                # Top 3 cards
                section_header("🥇", "Top 3 Rekomendasi Terbaik")
                top3 = df_result.head(3)
                medals = ["🥇","🥈","🥉"]
                card_cls = ["rank-card-1","rank-card-2","rank-card-3"]
                pos_labels = ["PERINGKAT 1","PERINGKAT 2","PERINGKAT 3"]
                cards_html = '<div class="rank-cards">'
                for i, (_, row) in enumerate(top3.iterrows()):
                    cards_html += f"""
                    <div class="rank-card {card_cls[i]}">
                        <div class="rank-medal">{medals[i]}</div>
                        <div class="rank-pos">{pos_labels[i]}</div>
                        <div class="rank-name">{row['name']}</div>
                        <div class="rank-type">{row['type']}</div>
                        <div class="rank-score">{row['Skor SAW']:.4f}</div>
                        <div class="rank-score-lbl">Skor SAW</div>
                        <div class="rank-detail">
                            ⭐ {row['rating']} &nbsp;|&nbsp;
                            Rp {row['htm']:,.0f}<br>
                            📍 {row['jarak_km']:.1f} km dari pusat kota
                        </div>
                    </div>"""
                cards_html += "</div>"
                st.markdown(cards_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  PAGE 4 – VISUALISASI
# ─────────────────────────────────────────────────────────

elif halaman_key == "Visualisasi":
    page_banner(
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&q=80",
        "📈 Visualisasi Data Analitik"
    )

    GOLD = "#c8922a"; DARK = "#2d1f0a"; BG = "#fdf8f0"

    # Chart 1
    section_header("🎭", "Distribusi Jenis Wisata")
    type_counts = df_raw["type"].value_counts()
    fig1, ax1 = plt.subplots(figsize=(10, 4.5))
    bar_colors = [GOLD if i < 3 else "#a07840" for i in range(len(type_counts))]
    ax1.bar(type_counts.index, type_counts.values, color=bar_colors, edgecolor="white", linewidth=0.8)
    ax1.set_xlabel("Jenis Wisata", fontsize=10, color=DARK)
    ax1.set_ylabel("Jumlah Destinasi", fontsize=10, color=DARK)
    ax1.tick_params(axis="x", rotation=40, labelsize=8)
    ax1.spines[["top","right","left"]].set_visible(False)
    ax1.set_facecolor(BG); fig1.patch.set_facecolor(BG)
    ax1.yaxis.grid(True, color="#e0d0b022", linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig1); plt.close()

    col_v1, col_v2 = st.columns(2)

    # Chart 2
    with col_v1:
        section_header("⭐", "Rata-rata Rating per Kategori")
        avg_rating = df_raw.groupby("type")["rating"].mean().sort_values(ascending=True)
        fig2, ax2 = plt.subplots(figsize=(6, 4.5))
        cmap = plt.cm.YlOrBr(np.linspace(0.35, 0.9, len(avg_rating)))
        bars2 = ax2.barh(avg_rating.index, avg_rating.values, color=cmap, edgecolor="white", height=0.65)
        ax2.bar_label(bars2, fmt="%.2f", padding=4, fontsize=8, color=DARK)
        ax2.set_xlabel("Rata-rata Rating", fontsize=9, color=DARK)
        ax2.set_xlim(0, 5.6)
        ax2.spines[["top","right","bottom"]].set_visible(False)
        ax2.set_facecolor(BG); fig2.patch.set_facecolor(BG)
        ax2.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig2); plt.close()

    # Chart 3
    with col_v2:
        section_header("📊", "Popularitas Destinasi")
        popularitas_counts = df_raw["popularitas"].value_counts().sort_index()
        labels_pop = ["Tidak Populer","Kurang Populer","Cukup Populer","Populer","Sangat Populer"]
        colors_pop = ["#e8d5b0","#c8a260","#c8922a","#a06a18","#7c4e10"]
        fig4, ax4 = plt.subplots(figsize=(6, 4.5))
        wedges4, _, auto4 = ax4.pie(
            popularitas_counts.values, labels=None, autopct="%1.1f%%",
            startangle=90, colors=colors_pop,
            wedgeprops=dict(edgecolor="white", linewidth=1.8),
            pctdistance=0.75,
        )
        for at in auto4: at.set_fontsize(8); at.set_color("white"); at.set_weight("bold")
        ax4.legend(labels_pop, loc="lower center", bbox_to_anchor=(0.5,-0.18), ncol=2, fontsize=8, frameon=False)
        ax4.set_facecolor(BG); fig4.patch.set_facecolor(BG)
        plt.tight_layout()
        st.pyplot(fig4); plt.close()

    # Chart 4 – Scatter
    section_header("🗺️", "Hubungan Jarak vs Rating")
    jenis_list = df_raw["type"].value_counts().head(6).index.tolist()
    df_scatter = df_raw[df_raw["type"].isin(jenis_list)]
    fig3, ax3 = plt.subplots(figsize=(10, 4.5))
    palette = ["#c8922a","#3d6b4f","#7b4f2e","#4a5568","#6d3f1f","#5f7c68"]
    for i, jenis in enumerate(jenis_list):
        sub = df_scatter[df_scatter["type"] == jenis]
        ax3.scatter(sub["jarak_km"], sub["rating"], label=jenis,
                    color=palette[i], alpha=0.7, s=55,
                    edgecolors="white", linewidths=0.5)
    ax3.set_xlabel("Jarak dari Pusat Kota (km)", fontsize=10, color=DARK)
    ax3.set_ylabel("Rating Wisatawan", fontsize=10, color=DARK)
    ax3.legend(title="Jenis Wisata", fontsize=8, title_fontsize=9,
               bbox_to_anchor=(1.01, 1), frameon=False)
    ax3.spines[["top","right"]].set_visible(False)
    ax3.set_facecolor(BG); fig3.patch.set_facecolor(BG)
    ax3.yaxis.grid(True, color="#e0d0b033", linewidth=0.7)
    plt.tight_layout()
    st.pyplot(fig3); plt.close()

    # Chart 5 – SAW scores
    if "df_result" in st.session_state:
        section_header("🏆", "Top 10 Destinasi – Skor SAW")
        top10 = st.session_state["df_result"].head(10)
        fig5, ax5 = plt.subplots(figsize=(10, 4.5))
        bar_c = plt.cm.YlOrBr_r(np.linspace(0.15, 0.85, len(top10)))
        bars5 = ax5.barh(top10["name"], top10["Skor SAW"], color=bar_c, edgecolor="white", height=0.65)
        ax5.bar_label(bars5, fmt="%.4f", padding=4, fontsize=8, color=DARK)
        ax5.set_xlabel("Skor SAW", fontsize=10, color=DARK)
        ax5.invert_yaxis()
        ax5.spines[["top","right","bottom"]].set_visible(False)
        ax5.set_facecolor(BG); fig5.patch.set_facecolor(BG)
        ax5.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig5); plt.close()
    else:
        st.info("💡 Jalankan perhitungan SAW di halaman **Hitung SPK** untuk melihat grafik skor SAW.")


# ─────────────────────────────────────────────────────────
#  PAGE 5 – PETA
# ─────────────────────────────────────────────────────────

elif halaman_key == "Peta":
    from folium.plugins import MarkerCluster, Fullscreen

    page_banner(
        "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1400&q=80",
        "🗺️ Peta Destinasi Wisata Yogyakarta"
    )

    # Satu warna untuk setiap jenis wisata yang ada di dataset.
    # Nama warna mengikuti pilihan warna ikon folium.
    WARNA_JENIS = {
        "Budaya Dan Sejarah":"orange", "Alam":"green", "Agrowisata":"lightgreen",
        "Buatan":"purple", "Pantai":"blue", "Wisata Air":"lightblue",
        "Museum":"darkpurple", "Religi":"red", "Kuliner":"darkred",
        "Desa Wisata":"beige", "Pendidikan":"cadetblue",
        "Minat Khusus":"pink", "Seni":"darkblue",
    }
    # Warna marker folium (Leaflet.awesome-markers) untuk legenda.
    WARNA_HEX = {
        "orange":"#f69730", "green":"#72af26", "lightgreen":"#bbf970",
        "purple":"#d252b9", "blue":"#38aadd", "lightblue":"#8adaff",
        "darkpurple":"#5b396b", "red":"#d33d2a", "darkred":"#a23336",
        "beige":"#ffcb92", "cadetblue":"#436978", "pink":"#ff91ea",
        "darkblue":"#0067a3", "gray":"#575757",
    }

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        mode_peta = st.selectbox("Tampilkan", ["Semua Destinasi","Hasil Ranking SAW"])
    with col_c2:
        filter_jenis_peta = st.multiselect("Filter Jenis", sorted(df_raw["type"].unique()), default=[], placeholder="Semua jenis")
    with col_c3:
        tile_style = st.selectbox("Gaya Peta", ["OpenStreetMap","CartoDB positron","CartoDB dark_matter"])

    if mode_peta == "Hasil Ranking SAW" and "df_result" in st.session_state:
        df_calc = st.session_state.get("df_calc", df_raw)
        df_map  = df_calc.merge(st.session_state["df_result"][["name","Skor SAW"]], on="name", how="left")
        df_map["Skor SAW"] = df_map["Skor SAW"].fillna(0)
        punya_skor = True
        st.info(f"Menampilkan {len(df_map)} destinasi dari hasil SAW.")
    else:
        df_map = df_raw.copy(); df_map["Skor SAW"] = None; punya_skor = False
        if mode_peta == "Hasil Ranking SAW":
            st.warning("Belum ada hasil SAW. Jalankan Hitung SPK terlebih dahulu.")

    if filter_jenis_peta:
        df_map = df_map[df_map["type"].isin(filter_jenis_peta)]

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#fffbf0,#fff5e0);
         border:1px solid #e0c880;border-radius:10px;padding:10px 18px;
         margin-bottom:14px;font-size:0.86rem;color:#5a3a10;'>
        📍 <strong>{len(df_map)} destinasi</strong> ditampilkan
    </div>""", unsafe_allow_html=True)

    LAT_PUSAT, LON_PUSAT = -7.801363, 110.364787
    m = folium.Map(location=[LAT_PUSAT, LON_PUSAT], zoom_start=11, tiles=tile_style)
    Fullscreen(position="topright").add_to(m)
    cluster = MarkerCluster(name="Destinasi Wisata").add_to(m)

    folium.Marker(
        [LAT_PUSAT, LON_PUSAT],
        popup=folium.Popup("<b>Pusat Kota Yogyakarta</b>", max_width=200),
        tooltip="Pusat Kota Yogyakarta",
        icon=folium.Icon(color="black", icon="home", prefix="fa"),
    ).add_to(m)

    for _, row in df_map.iterrows():
        warna = WARNA_JENIS.get(row["type"], "gray")
        skor_html = f"<br>🏆 Skor SAW: <b>{row['Skor SAW']:.4f}</b>" if punya_skor and row["Skor SAW"] else ""
        popup_html = f"""
        <div style="font-family:sans-serif;font-size:13px;min-width:190px">
            <b style="font-size:14px;color:#2d1f0a">{row['name']}</b><br>
            <span style="color:#8a5c1a;font-size:12px">{row['type']}</span>
            <hr style="margin:5px 0;border-color:#e0d0b0">
            ⭐ {row['rating']} &nbsp;|&nbsp; 💰 Rp {row['htm']:,.0f}<br>
            📍 {row['jarak_km']:.1f} km dari pusat{skor_html}
        </div>"""
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{row['name']} ({row['type']})",
            icon=folium.Icon(color=warna, icon="map-marker", prefix="fa"),
        ).add_to(cluster)

    folium.LayerControl().add_to(m)
    st_folium(m, width="100%", height=520, returned_objects=[])

    section_header("🎨", "Legenda Warna Marker")
    cols_leg = st.columns(4)
    for i, (jenis, warna) in enumerate(WARNA_JENIS.items()):
        hex_c = WARNA_HEX.get(warna, "#888")
        with cols_leg[i % 4]:
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:7px;margin:4px 0'>"
                f"<div style='width:13px;height:13px;border-radius:50%;background:{hex_c};flex-shrink:0'></div>"
                f"<span style='font-size:0.83rem;color:#3a2810'>{jenis}</span></div>",
                unsafe_allow_html=True)

    if punya_skor and "df_result" in st.session_state:
        section_header("🥇", "Top 3 Lokasi (SAW)")
        top3 = st.session_state["df_result"].head(3)
        cols3 = st.columns(3)
        medals = ["🥇","🥈","🥉"]
        for i, (_, row) in enumerate(top3.iterrows()):
            with cols3[i]:
                st.markdown(
                    f"**{medals[i]} {row['name']}**  \n"
                    f"{row['type']}  \n"
                    f"Skor: `{row['Skor SAW']:.4f}` | ⭐{row['rating']}")
