# SPK Wisata Jogja — Metode SAW

Aplikasi web untuk merekomendasikan destinasi wisata di Daerah Istimewa Yogyakarta
dengan metode **Simple Additive Weighting (SAW)**. Pengguna mengatur sendiri bobot
kriteria dan filter, lalu aplikasi menghitung dan mengurutkan destinasi dari skor tertinggi.

Proyek ini berawal dari tugas Praktikum Sistem Pendukung Keputusan (SCPK) IF-E
dan dikembangkan lebih lanjut menjadi aplikasi Streamlit dengan tampilan bertema Yogyakarta.

## Fitur

| Halaman | Isi |
| --- | --- |
| Beranda | Ringkasan dataset, cara kerja, daftar kriteria, dan catatan tentang hasilnya |
| Dataset | Tabel destinasi dengan filter jenis wisata dan rating minimum, serta statistik ringkas |
| Hitung SPK | Atur bobot kriteria (total 100) dan filter, lalu lihat matriks keputusan, normalisasi, bobot, tabel peringkat, dan tiga teratas |
| Visualisasi | Jumlah destinasi per jenis, rata-rata rating per jenis, sebaran popularitas, hubungan jarak dan rating, serta sepuluh skor SAW tertinggi (setelah perhitungan dijalankan) |
| Peta | Peta interaktif semua destinasi atau hasil perhitungan SAW, dengan filter jenis wisata dan pilihan peta dasar |

## Kriteria

| Kode | Kriteria | Tipe | Asal nilai |
| --- | --- | --- | --- |
| C1 | Rating Wisatawan | Benefit | Kolom `rating` pada dataset |
| C2 | Harga Tiket (HTM) | Cost | Kolom `htm` pada dataset |
| C3 | Jarak dari Pusat Kota | Cost | Jarak garis lurus (rumus haversine) dari koordinat destinasi ke satu titik pusat kota yang ditetapkan di kode |
| C4 | Kategori Wisata | Benefit | Rata-rata rating dari semua destinasi dengan jenis yang sama |
| C5 | Popularitas | Benefit | Rating dikelompokkan menjadi skor 1–5 |

Semua nilai kriteria diturunkan dari isi dataset. Tidak ada nilai acak.

## Metode SAW

1. **Matriks keputusan** berisi nilai tiap destinasi pada setiap kriteria.
2. **Normalisasi**
   - Benefit: `r = x / max(x)`
   - Cost: `r = min(x) / x`. Jika harga tiket 0 (gratis), nilainya 1. Jarak di bawah 1 km dihitung 1 km.
3. **Skor** `V = Σ (bobot × r)`
4. **Perangkingan** dari skor tertinggi ke terendah.

## Menjalankan di komputer

Butuh Python 3.10 atau lebih baru.

```bash
git clone https://github.com/Hasanrbn/Travel-Recomendation-Jogja-App.git
cd Travel-Recomendation-Jogja-App

python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# macOS / Linux:        source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Aplikasi terbuka di <http://localhost:8501>.

## Struktur

```
app.py                       Aplikasi Streamlit (semua halaman)
tourism_jogja.csv            Dataset destinasi wisata
requirements.txt             Dependensi Python
.streamlit/config.toml       Warna tema aplikasi
Laporan Akhir Prak SCPK.pdf  Laporan praktikum (versi awal aplikasi)
```

## Catatan

- Aplikasi memuat font dari Google Fonts, foto pada Beranda dari Unsplash, dan peta dasar
  dari OpenStreetMap atau Esri. Tanpa internet, aplikasi tetap berjalan tetapi tampil tanpa
  font, foto, dan peta tersebut.
- Koordinat pada `tourism_jogja.csv` tersimpan dengan titik di setiap ribuan
  (misalnya `-7.607.086.854`). `app.py` memperbaikinya menjadi angka desimal yang benar
  saat data dimuat. Berkas CSV tidak diubah.
- Satu baris yang sama persis dengan baris lain (Watu Loncat) hanya dihitung sekali, sehingga
  jumlah destinasi yang tampil di aplikasi 436, bukan 437 baris di CSV. Candi Gebang muncul dua kali
  dengan rating berbeda dan koordinat yang hampir sama. Keduanya masih dihitung sebagai dua destinasi.
- Kriteria C4 dan C5 sama-sama bersumber dari rating, sehingga rating berpengaruh
  lebih besar daripada bobot C1 saja. Ini perlu diingat saat mengatur bobot.
- Jenis wisata yang hanya punya satu atau dua destinasi (misalnya Seni, satu destinasi dengan rating 5,0)
  mendapat nilai Kategori yang tinggi hanya karena sampelnya kecil. Gunakan filter jenis wisata atau
  turunkan bobot C4 jika ini mengganggu hasil.
- Jarak dihitung dalam garis lurus, bukan jarak tempuh di jalan.
- Laporan PDF menjelaskan versi awal aplikasi yang memakai kriteria Fasilitas dan
  Aksesibilitas. Versi sekarang mengganti keduanya dengan Jarak dan Kategori Wisata
  karena nilai Aksesibilitas versi awal dibangkitkan secara acak.
