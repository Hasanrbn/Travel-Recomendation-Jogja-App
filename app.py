import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from folium.plugins import Fullscreen, MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(
    page_title="SPK Wisata Jogja",
    page_icon="🏛️",
    layout="wide",
)

# ─────────────────────────────────────────────────────────
#  TAMPILAN
#  Warna tema ada di .streamlit/config.toml. CSS di bawah hanya
#  mengatur hal yang tidak bisa diatur lewat tema.
#  Palet: tinta, sogan (cokelat batik), indigo, dan emas hanya
#  untuk peringkat satu.
# ─────────────────────────────────────────────────────────
INK = "#231c16"
SOGAN = "#7a4a2a"
INDIGO = "#27386b"
EMAS = "#b88a2a"
MUTED = "#6f655a"
GARIS = "#e1d9cb"
LATAR = "#faf8f4"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;500;600&display=swap');

html, body, [data-testid="stApp"] { font-family: 'Public Sans', system-ui, sans-serif; }
[data-testid="stMainBlockContainer"] { max-width: 1180px; padding-top: 5rem; }

/* Sidebar */
.brand { font-family: 'Newsreader', Georgia, serif; font-size: 1.45rem; font-weight: 600; line-height: 1.2; }
.brand-sub { font-size: 0.82rem; opacity: 0.72; margin-top: 4px; }
.side-note { font-size: 0.8rem; line-height: 1.6; opacity: 0.72; }

/* Judul halaman */
.page-head { margin: 0 0 1.6rem; padding-bottom: 1.1rem; border-bottom: 1px solid #e1d9cb; }
[data-testid="stMarkdownContainer"] .page-head h1 { font-family: 'Newsreader', Georgia, serif; font-size: 2.1rem; font-weight: 600; margin: 0 0 0.35rem; padding: 0; color: #231c16; line-height: 1.15; }
.page-head p { margin: 0; color: #6f655a; max-width: 62ch; line-height: 1.6; }

/* Judul bagian */
[data-testid="stMarkdownContainer"] h2.sec { font-family: 'Newsreader', Georgia, serif !important; font-size: 1.4rem !important; font-weight: 600 !important; color: #231c16; margin: 2.2rem 0 0.35rem; padding: 0; line-height: 1.25; }
.sec-note { color: #6f655a; font-size: 0.9rem; line-height: 1.6; max-width: 70ch; margin: 0 0 0.9rem; }

/* Hero (Beranda) */
.hero { position: relative; min-height: 300px; border-radius: 4px; overflow: hidden; background: #2b211a; display: flex; align-items: flex-end; margin-bottom: 1.4rem; }
.hero-img { position: absolute; inset: 0; background: url('https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=1400&q=80') center 40% / cover; opacity: 0.55; }
.hero-shade { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(25,18,12,0.92) 0%, rgba(25,18,12,0.35) 70%, rgba(25,18,12,0.1) 100%); }
.hero-body { position: relative; padding: 2rem 2.2rem; max-width: 760px; }
[data-testid="stMarkdownContainer"] .hero-body h1 { font-family: 'Newsreader', Georgia, serif; font-size: 2.4rem; font-weight: 600; color: #fbf6ec; margin: 0 0 0.6rem; padding: 0; line-height: 1.15; }
.hero-body p { color: #e6dccb; margin: 0; line-height: 1.65; }

/* Angka ringkas */
.facts { display: grid; grid-template-columns: repeat(4, 1fr); margin: 0; border-top: 1px solid #e1d9cb; border-bottom: 1px solid #e1d9cb; }
.facts div { padding: 1rem 1.2rem 1rem 0; }
.facts div + div { padding-left: 1.2rem; border-left: 1px solid #e1d9cb; }
.facts dt { color: #6f655a; font-size: 0.85rem; margin: 0 0 2px; }
.facts dd { margin: 0; font-family: 'Newsreader', Georgia, serif; font-size: 1.9rem; font-weight: 600; color: #231c16; font-variant-numeric: tabular-nums; }

/* Langkah SAW */
.steps { margin: 0; padding: 0; list-style: none; counter-reset: s; }
.steps li { counter-increment: s; position: relative; padding: 0 0 0.9rem 2.4rem; line-height: 1.6; color: #231c16; }
.steps li::before { content: counter(s); position: absolute; left: 0; top: -2px; font-family: 'Newsreader', Georgia, serif; font-size: 1.5rem; font-weight: 600; color: #7a4a2a; }
.steps b { font-weight: 600; }

/* Tabel kriteria */
table.plain { width: 100%; border-collapse: collapse; font-size: 0.9rem; border: 0; }
table.plain th, table.plain td { border-left: 0; border-right: 0; border-top: 0; background: transparent; }
table.plain th { text-align: left; font-weight: 600; color: #6f655a; font-size: 0.82rem; padding: 6px 12px 6px 0; border-bottom: 1px solid #231c16; }
table.plain td { padding: 9px 12px 9px 0; border-bottom: 1px solid #e1d9cb; vertical-align: top; line-height: 1.5; }
table.plain td:first-child, table.plain td:last-child { white-space: nowrap; }
table.plain td:first-child { font-weight: 600; }

/* Catatan */
.notes { margin: 0; padding-left: 1.1rem; color: #231c16; line-height: 1.7; max-width: 76ch; }
.notes li { margin-bottom: 0.4rem; }

/* Tiga teratas */
.podium { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.4rem; margin-top: 0.4rem; }
.pod { border-top: 1px solid #231c16; padding-top: 0.7rem; }
.pod.first { border-top: 4px solid #b88a2a; padding-top: 0.55rem; }
.pod .no { font-family: 'Newsreader', Georgia, serif; font-size: 2.4rem; font-weight: 600; line-height: 1; color: #7a4a2a; }
.pod .nm { font-family: 'Newsreader', Georgia, serif; font-size: 1.2rem; font-weight: 600; line-height: 1.25; margin: 0.35rem 0 0.1rem; color: #231c16; }
.pod .jn { color: #6f655a; font-size: 0.85rem; margin-bottom: 0.7rem; }
.pod dl { margin: 0; display: grid; grid-template-columns: auto 1fr; gap: 3px 14px; font-size: 0.88rem; }
.pod dt { color: #6f655a; }
.pod dd { margin: 0; font-variant-numeric: tabular-nums; }

/* Legenda peta */
.legend { display: flex; flex-wrap: wrap; gap: 6px 22px; margin: 0.6rem 0 0; font-size: 0.88rem; }
.legend span { display: inline-flex; align-items: center; gap: 7px; }
.legend i { width: 11px; height: 11px; border-radius: 50%; display: inline-block; }

@media (max-width: 760px) {
  .facts { grid-template-columns: repeat(2, 1fr); }
  .facts div:nth-child(3) { padding-left: 0; border-left: 0; }
  .podium { grid-template-columns: 1fr; }
  .hero-body h1 { font-size: 1.9rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# Gaya grafik
plt.rcParams.update(
    {
        "font.size": 9,
        "axes.edgecolor": GARIS,
        "axes.labelcolor": INK,
        "axes.titlesize": 10,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "text.color": INK,
        "figure.facecolor": LATAR,
        "axes.facecolor": LATAR,
        "figure.dpi": 130,
    }
)


# ─────────────────────────────────────────────────────────
#  FUNGSI BANTU
# ─────────────────────────────────────────────────────────


def fix_lat(val):
    s = str(val).replace(" ", "")
    sign = "-" if s.startswith("-") else ""
    digits = s.replace("-", "").replace(".", "")
    return float(sign + digits[0] + "." + digits[1:])


def fix_lon(val):
    s = str(val).replace(" ", "")
    digits = s.replace("-", "").replace(".", "")
    return float(digits[0:3] + "." + digits[3:])


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    return R * 2 * np.arcsin(np.sqrt(a))


def dec(x, n=1):
    """Angka dengan koma desimal, misalnya 4,7."""
    return f"{x:.{n}f}".replace(".", ",")


def rupiah(x):
    return "Gratis" if x == 0 else "Rp " + f"{x:,.0f}".replace(",", ".")


def page_head(title, lead):
    st.markdown(
        f'<header class="page-head"><h1>{title}</h1><p>{lead}</p></header>',
        unsafe_allow_html=True,
    )


def section(title, note=None):
    html = f'<h2 class="sec">{title}</h2>'
    if note:
        html += f'<p class="sec-note">{note}</p>'
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────────────────

PUSAT_LAT, PUSAT_LON = -7.801363, 110.364787  # titik acuan jarak (pusat kota Yogyakarta)
POPULARITAS_BATAS = [0, 3.9, 4.2, 4.5, 4.7, 5.0]


@st.cache_data
def load_data():
    df = pd.read_csv("tourism_jogja.csv")
    # Baris yang sama persis (selain place_id) hanya dihitung sekali.
    isi = [c for c in df.columns if c != "place_id"]
    df = df.drop_duplicates(subset=isi).reset_index(drop=True)
    df["type"] = df["type"].str.replace(r"\bDan\b", "dan", regex=True)

    df["lat"] = df["latitude"].apply(fix_lat)
    df["lon"] = df["longitude"].apply(fix_lon)
    df["jarak_km"] = haversine(df["lat"], df["lon"], PUSAT_LAT, PUSAT_LON)
    rata_rating = df.groupby("type")["rating"].mean()
    df["kategori"] = df["type"].map(rata_rating).round(3)
    df["popularitas"] = (
        pd.cut(df["rating"], bins=POPULARITAS_BATAS, labels=[1, 2, 3, 4, 5])
        .astype(float)
        .fillna(3)
        .astype(int)
    )
    return df


df_raw = load_data()
N = len(df_raw)

# "min" pada kriteria cost: nilai di bawahnya dihitung sebagai nilai itu.
# Jarak di bawah 1 km dihitung 1 km. Tanpa ini, satu destinasi yang
# berjarak hampir 0 km membuat nilai jarak semua destinasi lain mendekati 0.
KRITERIA = {
    "C1": {"label": "Rating", "col": "rating", "tipe": "benefit"},
    "C2": {"label": "Harga tiket", "col": "htm", "tipe": "cost"},
    "C3": {"label": "Jarak dari pusat kota", "col": "jarak_km", "tipe": "cost", "min": 1.0},
    "C4": {"label": "Kategori wisata", "col": "kategori", "tipe": "benefit"},
    "C5": {"label": "Popularitas", "col": "popularitas", "tipe": "benefit"},
}

# Warna jenis wisata untuk grafik dan peta: enam jenis terbanyak, sisanya satu warna abu-abu.
WARNA_JENIS = {
    "Budaya dan Sejarah": "#27386b",
    "Alam": "#3f6e4f",
    "Agrowisata": "#b88a2a",
    "Buatan": "#8a3f6e",
    "Pantai": "#3a8fb7",
    "Wisata Air": "#2a7f78",
}
WARNA_LAIN = "#8a8279"


# Peta dasar tanpa kunci API.
PETA_DASAR = {
    "OpenStreetMap": {"tiles": "OpenStreetMap"},
    "Abu-abu terang": {
        "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        "attr": "Tiles © Esri, HERE, Garmin, © OpenStreetMap contributors",
    },
}


def warna_jenis(jenis):
    return WARNA_JENIS.get(jenis, WARNA_LAIN)


def hitung_saw(df, bobot):
    """Mengembalikan matriks keputusan, matriks normalisasi, dan skor SAW."""
    matriks = df[[k["col"] for k in KRITERIA.values()]].to_numpy(dtype=float)
    norm = np.zeros_like(matriks)
    for j, k in enumerate(KRITERIA.values()):
        x = matriks[:, j]
        if k["tipe"] == "benefit":
            norm[:, j] = x / x.max() if x.max() > 0 else 0.0
        else:
            x = np.maximum(x, k.get("min", 0.0))
            positif = x[x > 0]
            if len(positif) == 0:
                norm[:, j] = 1.0
            else:
                # Nilai 0 (misalnya tiket gratis) mendapat nilai terbaik, 1.
                norm[:, j] = np.where(x > 0, positif.min() / np.where(x > 0, x, 1.0), 1.0)
    return matriks, norm, norm @ bobot


# ─────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<div class="brand">SPK Wisata Jogja</div>'
        '<div class="brand-sub">Simple Additive Weighting</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    halaman = st.radio(
        "Halaman",
        ["Beranda", "Dataset", "Hitung SPK", "Visualisasi", "Peta"],
        label_visibility="collapsed",
    )
    st.write("")
    st.markdown(
        f'<div class="side-note">{N} destinasi di Daerah Istimewa Yogyakarta, '
        "dibaca dari tourism_jogja.csv.</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────
#  BERANDA
# ─────────────────────────────────────────────────────────

if halaman == "Beranda":
    st.markdown(
        f"""
    <div class="hero">
        <div class="hero-img"></div>
        <div class="hero-shade"></div>
        <div class="hero-body">
            <h1>Pilih wisata Jogja sesuai prioritas Anda</h1>
            <p>Atur seberapa penting rating, harga tiket, jarak, jenis wisata, dan popularitas.
            Aplikasi ini mengurutkan {N} destinasi dengan metode Simple Additive Weighting (SAW).</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    gratis = int((df_raw["htm"] == 0).sum())
    st.markdown(
        f"""
    <dl class="facts">
        <div><dt>Destinasi</dt><dd>{N}</dd></div>
        <div><dt>Jenis wisata</dt><dd>{df_raw["type"].nunique()}</dd></div>
        <div><dt>Rating rata-rata</dt><dd>{dec(df_raw["rating"].mean(), 2)}</dd></div>
        <div><dt>Tiket masuk gratis</dt><dd>{gratis}</dd></div>
    </dl>
    """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([4, 7], gap="large")

    with col_a:
        section("Cara kerja")
        st.markdown(
            """
        <ol class="steps">
            <li><b>Atur bobot.</b> Beri nilai tiap kriteria dengan total 100, lalu pilih filter jenis wisata dan harga tiket maksimum.</li>
            <li><b>Normalisasi.</b> Nilai tiap kriteria diubah ke skala 0 sampai 1 supaya bisa dijumlahkan.</li>
            <li><b>Skor.</b> Setiap nilai dikalikan bobotnya, lalu dijumlahkan menjadi skor SAW.</li>
            <li><b>Peringkat.</b> Destinasi diurutkan dari skor tertinggi.</li>
        </ol>
        """,
            unsafe_allow_html=True,
        )

    with col_b:
        section("Kriteria")
        st.markdown(
            """
        <table class="plain">
            <tr><th>Kode</th><th>Kriteria</th><th>Dinilai dari</th><th>Lebih baik jika</th></tr>
            <tr><td>C1</td><td>Rating</td><td>Rating di dataset</td><td>makin tinggi</td></tr>
            <tr><td>C2</td><td>Harga tiket</td><td>Harga tiket masuk di dataset</td><td>makin murah</td></tr>
            <tr><td>C3</td><td>Jarak dari pusat kota</td><td>Jarak garis lurus dari koordinat destinasi</td><td>makin dekat</td></tr>
            <tr><td>C4</td><td>Kategori wisata</td><td>Rata-rata rating jenis wisatanya</td><td>makin tinggi</td></tr>
            <tr><td>C5</td><td>Popularitas</td><td>Rating dikelompokkan jadi skor 1 sampai 5</td><td>makin tinggi</td></tr>
        </table>
        """,
            unsafe_allow_html=True,
        )



# ─────────────────────────────────────────────────────────
#  DATASET
# ─────────────────────────────────────────────────────────

elif halaman == "Dataset":
    page_head(
        "Dataset",
        "Seluruh destinasi beserta nilai tiap kriteria. Gunakan filter di kiri untuk mempersempit tabel.",
    )

    col1, col2 = st.columns([1, 4], gap="large")
    with col1:
        filter_tipe = st.multiselect(
            "Jenis wisata",
            options=sorted(df_raw["type"].unique()),
            default=[],
            placeholder="Semua jenis",
        )
        min_rating = st.slider("Rating minimum", 2.5, 5.0, 2.5, 0.1)

    df_view = df_raw
    if filter_tipe:
        df_view = df_view[df_view["type"].isin(filter_tipe)]
    df_view = df_view[df_view["rating"] >= min_rating]

    with col2:
        st.caption(f"{len(df_view)} dari {N} destinasi")
        st.dataframe(
            df_view[["place_id", "name", "type", "rating", "htm", "jarak_km", "kategori", "popularitas"]],
            hide_index=True,
            height=430,
            width="stretch",
            column_config={
                "place_id": st.column_config.NumberColumn("ID", format="%d"),
                "name": "Destinasi",
                "type": "Jenis",
                "rating": st.column_config.NumberColumn("Rating", format="%.1f"),
                "htm": st.column_config.NumberColumn("Tiket (Rp)", format="%d"),
                "jarak_km": st.column_config.NumberColumn("Jarak (km)", format="%.1f"),
                "kategori": st.column_config.NumberColumn("Nilai kategori", format="%.2f"),
                "popularitas": st.column_config.NumberColumn("Popularitas", format="%d"),
            },
        )

    section("Statistik ringkas", "Dihitung dari seluruh destinasi, tanpa filter.")
    stat = df_raw[["rating", "htm", "jarak_km", "kategori", "popularitas"]].describe().T
    stat.index = ["Rating", "Tiket (Rp)", "Jarak (km)", "Nilai kategori", "Popularitas"]
    stat.columns = ["Jumlah", "Rata-rata", "Simpangan baku", "Minimum", "Kuartil 1", "Median", "Kuartil 3", "Maksimum"]
    st.dataframe(stat.round(2), width="stretch")


# ─────────────────────────────────────────────────────────
#  HITUNG SPK
# ─────────────────────────────────────────────────────────

elif halaman == "Hitung SPK":
    page_head(
        "Hitung SPK",
        "Atur bobot dan filter, lalu jalankan perhitungan. Tiap tahap perhitungan ikut ditampilkan.",
    )

    section("Bobot kriteria", "Total bobot harus 100. Makin besar bobot, makin kuat pengaruh kriteria itu pada peringkat.")
    cols = st.columns(5)
    awal = [30, 25, 20, 15, 10]
    bobot_pct = [
        c.slider(f"{kode} {k['label']}", 0, 100, awal[i], 5)
        for i, (c, (kode, k)) in enumerate(zip(cols, KRITERIA.items()))
    ]
    total_bobot = sum(bobot_pct)
    if total_bobot == 100:
        st.caption("Total bobot 100.")
    else:
        st.warning(f"Total bobot {total_bobot}. Sesuaikan sampai tepat 100.")

    section("Filter")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_jenis = st.multiselect(
            "Jenis wisata",
            options=sorted(df_raw["type"].unique()),
            default=["Alam", "Budaya dan Sejarah", "Pantai"],
            placeholder="Semua jenis",
        )
    with col_f2:
        max_htm = st.number_input("Harga tiket maksimum (Rp)", 0, 1_500_000, 100_000, 5_000)
    with col_f3:
        top_n = st.selectbox("Jumlah hasil", [10, 20, 30, 50, 100], index=1)

    hitung = st.button("Hitung peringkat", type="primary")

    if hitung:
        if total_bobot != 100:
            st.error("Bobot belum berjumlah 100. Sesuaikan bobot, lalu hitung lagi.")
        else:
            df_calc = df_raw.copy()
            if filter_jenis:
                df_calc = df_calc[df_calc["type"].isin(filter_jenis)]
            df_calc = df_calc[df_calc["htm"] <= max_htm].reset_index(drop=True)

            if len(df_calc) < 2:
                st.error("Destinasi yang lolos filter kurang dari dua. Longgarkan filter jenis wisata atau harga tiket.")
            else:
                bobot = np.array(bobot_pct) / 100
                matriks, norm, skor = hitung_saw(df_calc, bobot)
                kolom_kriteria = [f"{kode} {k['label']}" for kode, k in KRITERIA.items()]

                section("Tahap perhitungan")
                with st.expander("1. Matriks keputusan (10 destinasi pertama)", expanded=True):
                    tabel1 = pd.DataFrame(matriks[:10], columns=kolom_kriteria, index=df_calc["name"].iloc[:10])
                    tabel1.index.name = "Destinasi"
                    st.dataframe(tabel1.round(2), width="stretch")
                with st.expander("2. Matriks normalisasi"):
                    st.caption(
                        "Benefit: nilai dibagi nilai tertinggi. Cost: nilai terendah dibagi nilai. "
                        "Tiket gratis mendapat 1. Jarak di bawah 1 km dihitung 1 km."
                    )
                    tabel2 = pd.DataFrame(norm[:10], columns=kolom_kriteria, index=df_calc["name"].iloc[:10])
                    tabel2.index.name = "Destinasi"
                    st.dataframe(tabel2.round(3), width="stretch")
                with st.expander("3. Bobot yang dipakai"):
                    st.dataframe(
                        pd.DataFrame(
                            {
                                "Kriteria": kolom_kriteria,
                                "Jenis": ["Benefit" if k["tipe"] == "benefit" else "Cost" for k in KRITERIA.values()],
                                "Bobot (%)": bobot_pct,
                            }
                        ),
                        hide_index=True,
                        width="stretch",
                    )

                df_calc["Skor SAW"] = skor
                hasil = (
                    df_calc[["place_id", "name", "type", "rating", "htm", "jarak_km", "kategori", "popularitas", "Skor SAW"]]
                    .sort_values("Skor SAW", ascending=False)
                    .head(top_n)
                    .reset_index(drop=True)
                )
                hasil.index += 1
                hasil.index.name = "Peringkat"
                st.session_state["df_result"] = hasil

                section(
                    f"{len(hasil)} destinasi teratas",
                    f"Dipilih dari {len(df_calc)} destinasi yang lolos filter.",
                )
                tampil = hasil.drop(columns="place_id")[
                    ["name", "type", "Skor SAW", "rating", "htm", "jarak_km", "kategori", "popularitas"]
                ].rename(
                    columns={
                        "name": "Destinasi",
                        "type": "Jenis",
                        "rating": "Rating",
                        "htm": "Tiket",
                        "jarak_km": "Jarak",
                        "kategori": "Kategori",
                        "popularitas": "Popularitas",
                    }
                )

                def tebal_peringkat_satu(row):
                    return ["font-weight:600; background-color:#f3ead6" if row.name == 1 else ""] * len(row)

                st.dataframe(
                    tampil.style.apply(tebal_peringkat_satu, axis=1).format(
                        {
                            "Rating": lambda v: dec(v, 1),
                            "Tiket": rupiah,
                            "Jarak": lambda v: dec(v, 1) + " km",
                            "Kategori": lambda v: dec(v, 2),
                            "Skor SAW": lambda v: dec(v, 4),
                        }
                    ),
                    width="stretch",
                    height=460,
                    column_config={
                        "Destinasi": st.column_config.Column(width=255),
                        "Jenis": st.column_config.Column(width=125),
                        "Skor SAW": st.column_config.Column(width=78),
                        "Rating": st.column_config.Column(width=62),
                        "Tiket": st.column_config.Column(width=72),
                        "Jarak": st.column_config.Column(width=72),
                        "Kategori": st.column_config.Column(width=72),
                        "Popularitas": st.column_config.Column(width=92),
                    },
                )

                section("Tiga teratas")
                podium = '<div class="podium">'
                for no, (_, r) in enumerate(hasil.head(3).iterrows(), start=1):
                    podium += f"""
                    <div class="pod{" first" if no == 1 else ""}">
                        <div class="no">{no}</div>
                        <div class="nm">{r["name"]}</div>
                        <div class="jn">{r["type"]}</div>
                        <dl>
                            <dt>Skor SAW</dt><dd>{dec(r["Skor SAW"], 4)}</dd>
                            <dt>Rating</dt><dd>{dec(r["rating"], 1)}</dd>
                            <dt>Tiket</dt><dd>{rupiah(r["htm"])}</dd>
                            <dt>Jarak</dt><dd>{dec(r["jarak_km"], 1)} km dari pusat kota</dd>
                        </dl>
                    </div>"""
                podium += "</div>"
                st.markdown(podium, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  VISUALISASI
# ─────────────────────────────────────────────────────────

elif halaman == "Visualisasi":
    page_head(
        "Visualisasi",
        "Gambaran isi dataset. Grafik skor SAW muncul setelah perhitungan dijalankan di halaman Hitung SPK.",
    )

    def rapikan(ax, hilangkan=("top", "right", "left")):
        ax.spines[list(hilangkan)].set_visible(False)
        ax.tick_params(length=0)

    # 1. Jumlah destinasi per jenis
    section("Jumlah destinasi per jenis wisata")
    jumlah = df_raw["type"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4))
    barh = ax.barh(jumlah.index, jumlah.values, color=SOGAN, height=0.65)
    ax.bar_label(barh, padding=4, fontsize=8.5)
    ax.set_xlim(0, jumlah.max() * 1.1)
    ax.set_xticks([])
    rapikan(ax, ("top", "right", "left", "bottom"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    col_v1, col_v2 = st.columns(2, gap="large")

    # 2. Rata-rata rating per jenis
    with col_v1:
        section("Rata-rata rating per jenis", "n adalah jumlah destinasi. Jenis dengan n kecil kurang bisa diandalkan.")
        rt = df_raw.groupby("type")["rating"].agg(["mean", "count"]).sort_values("mean")
        fig, ax = plt.subplots(figsize=(5.2, 4.2))
        ax.hlines(rt.index, 3.5, rt["mean"], color=GARIS, linewidth=1)
        ax.scatter(rt["mean"], rt.index, color=INDIGO, s=34, zorder=3)
        for jenis, r in rt.iterrows():
            ax.text(r["mean"] + 0.04, jenis, f"{dec(r['mean'], 2)}  (n={int(r['count'])})", va="center", fontsize=8)
        ax.set_xlim(3.5, 5.6)
        ax.set_xticks([3.5, 4.0, 4.5, 5.0])
        ax.set_xticklabels(["3,5", "4,0", "4,5", "5,0"])
        rapikan(ax)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 3. Sebaran skor popularitas
    with col_v2:
        section("Sebaran skor popularitas", "Skor 1 sampai 5 berasal dari pengelompokan rating.")
        pop = df_raw["popularitas"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
        batas = ["≤ 3,9", "4,0–4,2", "4,3–4,5", "4,6–4,7", "4,8–5,0"]
        fig, ax = plt.subplots(figsize=(5.2, 4.2))
        bars = ax.bar([f"Skor {i}\nrating {b}" for i, b in zip(pop.index, batas)], pop.values, color=SOGAN, width=0.62)
        ax.bar_label(bars, padding=3, fontsize=8.5)
        ax.set_yticks([])
        ax.tick_params(axis="x", labelsize=7.5)
        rapikan(ax, ("top", "right", "left"))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 4. Jarak dan rating
    section(
        "Jarak dari pusat kota dan rating",
        "Satu titik satu destinasi. Enam jenis terbanyak diberi warna, jenis lain berwarna abu-abu.",
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    lain = df_raw[~df_raw["type"].isin(WARNA_JENIS)]
    ax.scatter(lain["jarak_km"], lain["rating"], color=WARNA_LAIN, s=22, alpha=0.7, label="Jenis lain", linewidths=0)
    for jenis, warna in WARNA_JENIS.items():
        sub = df_raw[df_raw["type"] == jenis]
        ax.scatter(sub["jarak_km"], sub["rating"], color=warna, s=22, alpha=0.75, label=jenis, linewidths=0)
    ax.set_xlabel("Jarak dari pusat kota (km)")
    ax.set_ylabel("Rating")
    ax.yaxis.grid(True, color=GARIS, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(ncol=4, fontsize=8, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2))
    rapikan(ax, ("top", "right"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # 5. Skor SAW
    if "df_result" in st.session_state:
        section("Sepuluh destinasi dengan skor SAW tertinggi")
        top10 = st.session_state["df_result"].head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        barh = ax.barh(top10["name"], top10["Skor SAW"], color=INK, height=0.62)
        ax.bar_label(barh, labels=[dec(v, 4) for v in top10["Skor SAW"]], padding=4, fontsize=8.5)
        ax.invert_yaxis()
        ax.set_xlim(0, top10["Skor SAW"].max() * 1.12)
        ax.set_xticks([])
        rapikan(ax, ("top", "right", "left", "bottom"))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Jalankan perhitungan di halaman Hitung SPK untuk melihat grafik skor SAW.")


# ─────────────────────────────────────────────────────────
#  PETA
# ─────────────────────────────────────────────────────────

elif halaman == "Peta":
    page_head(
        "Peta",
        "Letak destinasi di Yogyakarta. Klik titik untuk melihat rating, harga tiket, dan jarak dari pusat kota.",
    )

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        mode_peta = st.selectbox("Tampilkan", ["Semua destinasi", "Hasil perhitungan SAW"])
    with col_c2:
        filter_jenis_peta = st.multiselect(
            "Jenis wisata", sorted(df_raw["type"].unique()), default=[], placeholder="Semua jenis"
        )
    with col_c3:
        tile_style = st.selectbox("Gaya peta", list(PETA_DASAR))

    punya_skor = False
    df_map = df_raw.assign(skor=np.nan)
    if mode_peta == "Hasil perhitungan SAW":
        if "df_result" in st.session_state:
            hasil = st.session_state["df_result"]
            df_map = (
                hasil[["place_id", "Skor SAW"]]
                .merge(df_raw, on="place_id", how="left")
                .rename(columns={"Skor SAW": "skor"})
            )
            punya_skor = True
        else:
            st.warning("Belum ada hasil perhitungan. Jalankan dulu di halaman Hitung SPK.")

    if filter_jenis_peta:
        df_map = df_map[df_map["type"].isin(filter_jenis_peta)]

    st.caption(f"{len(df_map)} destinasi ditampilkan")

    ikon_klaster = (
        "function(c){var n=c.getChildCount();"
        "return L.divIcon({html:'<div style=\"background:#27386b;color:#fff;width:34px;height:34px;"
        "border-radius:50%;display:flex;align-items:center;justify-content:center;"
        "font:600 12px sans-serif;border:2px solid #fff;box-shadow:0 0 0 1px #27386b88\">'+n+'</div>',"
        "className:'',iconSize:[34,34]});}"
    )

    m = folium.Map(location=[PUSAT_LAT, PUSAT_LON], zoom_start=11, **PETA_DASAR[tile_style])
    Fullscreen(position="topright").add_to(m)
    klaster = MarkerCluster(icon_create_function=ikon_klaster).add_to(m)

    folium.CircleMarker(
        [PUSAT_LAT, PUSAT_LON],
        radius=7,
        color="#ffffff",
        weight=2,
        fill=True,
        fill_color=INK,
        fill_opacity=1,
        tooltip="Pusat kota, titik acuan jarak",
    ).add_to(m)

    for _, r in df_map.iterrows():
        baris_skor = f"<br>Skor SAW {dec(r['skor'], 4)}" if punya_skor else ""
        popup = (
            '<div style="font-family:sans-serif;font-size:13px;min-width:180px;line-height:1.5">'
            f'<b style="font-size:14px">{r["name"]}</b><br>'
            f'<span style="color:#6f655a">{r["type"]}</span><br>'
            f'Rating {dec(r["rating"], 1)}<br>'
            f'Tiket {rupiah(r["htm"])}<br>'
            f'{dec(r["jarak_km"], 1)} km dari pusat kota{baris_skor}</div>'
        )
        warna = warna_jenis(r["type"])
        folium.CircleMarker(
            [r["lat"], r["lon"]],
            radius=6,
            color="#ffffff",
            weight=1.5,
            fill=True,
            fill_color=warna,
            fill_opacity=0.95,
            popup=folium.Popup(popup, max_width=260),
            tooltip=f"{r['name']} ({r['type']})",
        ).add_to(klaster)

    st_folium(m, width="100%", height=520, returned_objects=[])

    jumlah_lain = int((~df_raw["type"].isin(WARNA_JENIS)).sum())
    legenda = "".join(
        f'<span><i style="background:{w}"></i>{j} ({int((df_raw["type"] == j).sum())})</span>' for j, w in WARNA_JENIS.items()
    )
    legenda += f'<span><i style="background:{WARNA_LAIN}"></i>Jenis lain ({jumlah_lain})</span>'
    st.markdown(f'<div class="legend">{legenda}</div>', unsafe_allow_html=True)
    st.caption("Angka dalam lingkaran biru adalah jumlah destinasi yang bergabung. Perbesar peta untuk memisahkannya.")
