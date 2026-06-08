from inference_engine import jalankan_inferensi
from knowledge_base import load_kerusakan, get_nama_gejala


def hitung_cf_kombinasi(cf_pakar: float, cf_user: float) -> float:
    """
    Menghitung CF gabungan dari satu rule.

    Rumus:
        CF_kombinasi = CF_pakar × CF_user

    Parameter:
        cf_pakar : float — keyakinan pakar terhadap rule (0.0 – 1.0)
        cf_user  : float — keyakinan pengguna terhadap gejala (0.0 – 1.0)

    Return:
        float — nilai CF gabungan, dibulatkan 4 desimal
    """
    return round(cf_pakar * cf_user, 4)


def hitung_cf_paralel(cf1: float, cf2: float) -> float:
    """
    Menggabungkan dua nilai CF dari dua rule berbeda
    yang mengarah ke diagnosa yang sama (CF paralel).

    Rumus:
        CF_combined = CF1 + CF2 × (1 - CF1)

    Parameter:
        cf1 : float — CF hasil rule pertama
        cf2 : float — CF hasil rule kedua

    Return:
        float — CF gabungan, dibulatkan 4 desimal
    """
    return round(cf1 + cf2 * (1 - cf1), 4)


def hitung_cf_total_diagnosa(rules_aktif_diagnosa: list, cf_user: dict) -> dict:
    """
    Menghitung CF total untuk satu diagnosa dari beberapa rule aktif.

    Alur:
    1. Untuk setiap rule aktif:
       a. Ambil CF_user minimum dari semua gejala dalam rule (operator AND)
       b. Hitung CF_kombinasi = CF_pakar × CF_user_min
    2. Gabungkan semua CF_kombinasi dengan rumus paralel secara berurutan

    Parameter:
        rules_aktif_diagnosa : list of dict — rules aktif untuk satu diagnosa
        cf_user              : dict — { kode_gejala: cf_user }

    Return:
        dict berisi:
        {
            "cf_total"   : float — nilai CF akhir diagnosa,
            "detail"     : list of dict — detail perhitungan tiap rule,
            "persentase" : float — CF total dalam persen (0–100)
        }
    """
    detail = []
    cf_running = 0.0  # Akumulasi CF paralel

    for rule in rules_aktif_diagnosa:
        # Nilai CF_user untuk rule ini = minimum CF_user dari semua gejala
        # (karena kondisi rule menggunakan AND)
        cf_user_values = [cf_user.get(g, 1.0) for g in rule["gejala"]]
        cf_user_min = min(cf_user_values)

        # CF kombinasi untuk rule ini
        cf_komb = hitung_cf_kombinasi(rule["cf_pakar"], cf_user_min)

        # Simpan detail untuk ditampilkan di UI
        detail.append({
            "rule"          : rule["kode"],
            "gejala"        : rule["gejala"],
            "cf_pakar"      : rule["cf_pakar"],
            "cf_user_min"   : cf_user_min,
            "cf_kombinasi"  : cf_komb,
            "deskripsi"     : rule["deskripsi"],
        })

        # Gabungkan dengan CF running menggunakan rumus paralel
        if cf_running == 0.0:
            cf_running = cf_komb
        else:
            cf_running = hitung_cf_paralel(cf_running, cf_komb)

    cf_total = round(cf_running, 4)

    return {
        "cf_total"   : cf_total,
        "detail"     : detail,
        "persentase" : round(cf_total * 100, 2),
    }


def interpretasi_cf(cf: float) -> dict:
    """
    Menginterpretasikan nilai CF menjadi label keyakinan
    yang mudah dipahami pengguna awam.

    Skala interpretasi:
        0.00 – 0.19 : Tidak Yakin
        0.20 – 0.39 : Kemungkinan Kecil
        0.40 – 0.59 : Kemungkinan
        0.60 – 0.79 : Kemungkinan Besar
        0.80 – 1.00 : Sangat Yakin

    Parameter:
        cf : float — nilai CF (0.0 – 1.0)

    Return:
        dict berisi label, warna (untuk UI), dan emoji
    """
    if cf >= 0.80:
        return {"label": "Sangat Yakin",       "warna": "red",    "emoji": "🔴"}
    elif cf >= 0.60:
        return {"label": "Kemungkinan Besar",  "warna": "orange", "emoji": "🟠"}
    elif cf >= 0.40:
        return {"label": "Kemungkinan",        "warna": "yellow", "emoji": "🟡"}
    elif cf >= 0.20:
        return {"label": "Kemungkinan Kecil",  "warna": "blue",   "emoji": "🔵"}
    else:
        return {"label": "Tidak Yakin",        "warna": "gray",   "emoji": "⚪"}


def proses_diagnosa_lengkap(gejala_input: list) -> dict:
    """
    Fungsi utama yang dipanggil oleh app.py.
    Menggabungkan seluruh alur: Forward Chaining → CF → Interpretasi.

    Parameter:
        gejala_input : list of str — kode gejala yang dipilih pengguna

    Return:
        dict berisi:
        {
            "ada_hasil"       : bool,
            "hasil"           : list of dict — diagnosa terurut dari CF tertinggi,
            "rules_aktif"     : list — semua rule yang fired,
            "jalur_inferensi" : list — jalur inferensi untuk ditampilkan,
            "total_rules_aktif": int
        }

        Setiap item dalam "hasil":
        {
            "kode"         : kode diagnosa,
            "nama"         : nama diagnosa,
            "cf_total"     : nilai CF akhir,
            "persentase"   : CF dalam persen,
            "interpretasi" : dict label keyakinan,
            "detail_cf"    : list detail perhitungan CF tiap rule,
            "info"         : dict info lengkap diagnosa (solusi, dll)
        }
    """
    inferensi = jalankan_inferensi(gejala_input)

    if not inferensi["ada_hasil"]:
        return {
            "ada_hasil"        : False,
            "hasil"            : [],
            "rules_aktif"      : [],
            "jalur_inferensi"  : [],
            "total_rules_aktif": 0,
        }

    kerusakan_data = load_kerusakan()
    hasil = []

    for kode_diagnosa, rules_diagnosa in inferensi["per_diagnosa"].items():
        # Hitung CF total untuk diagnosa ini
        cf_result = hitung_cf_total_diagnosa(
            rules_diagnosa,
            inferensi["cf_user"]
        )

        hasil.append({
            "kode"        : kode_diagnosa,
            "nama"        : kerusakan_data[kode_diagnosa]["nama"],
            "cf_total"    : cf_result["cf_total"],
            "persentase"  : cf_result["persentase"],
            "interpretasi": interpretasi_cf(cf_result["cf_total"]),
            "detail_cf"   : cf_result["detail"],
            "info"        : kerusakan_data[kode_diagnosa],
        })

    # Urutkan dari CF tertinggi ke terendah
    hasil.sort(key=lambda x: x["cf_total"], reverse=True)

    return {
        "ada_hasil"        : True,
        "hasil"            : hasil,
        "rules_aktif"      : inferensi["rules_aktif"],
        "jalur_inferensi"  : inferensi["jalur_inferensi"],
        "total_rules_aktif": len(inferensi["rules_aktif"]),
    }


if __name__ == "__main__":
    print("=" * 65)
    print("TEST CERTAINTY FACTOR — PERHITUNGAN NILAI KEYAKINAN")
    print("=" * 65)

    # ── Skenario 1: Overheating ──────────────────────────────────────
    print("\n📌 SKENARIO 1: Overheating Processor")
    print("   Gejala: G10 (cepat panas) + G11 (kipas bermasalah) + G13 (mati mendadak)")
    hasil1 = proses_diagnosa_lengkap(["G10", "G11", "G13"])
    for d in hasil1["hasil"]:
        print(f"\n   Diagnosa : {d['kode']} — {d['nama']}")
        print(f"   CF Total : {d['cf_total']} ({d['persentase']}%)")
        print(f"   Status   : {d['interpretasi']['emoji']} {d['interpretasi']['label']}")

    # ── Skenario 2: HDD rusak — 3 rules paralel ─────────────────────
    print("\n" + "─" * 65)
    print("\n📌 SKENARIO 2: Kerusakan HDD (3 rules aktif paralel)")
    print("   Gejala: G21 (klik-klik) + G06 (HDD tidak terdeteksi) + G14 (OS gagal booting)")
    hasil2 = proses_diagnosa_lengkap(["G21", "G06", "G14"])
    for d in hasil2["hasil"]:
        print(f"\n   Diagnosa : {d['kode']} — {d['nama']}")
        print(f"   CF Total : {d['cf_total']} ({d['persentase']}%)")
        print(f"   Status   : {d['interpretasi']['emoji']} {d['interpretasi']['label']}")
        print(f"   Detail perhitungan CF paralel:")
        cf_run = 0.0
        for i, det in enumerate(d["detail_cf"]):
            print(f"     Step {i+1}: {det['rule']} → CF_komb = {det['cf_pakar']} × {det['cf_user_min']} = {det['cf_kombinasi']}")
            if i == 0:
                cf_run = det["cf_kombinasi"]
            else:
                cf_baru = hitung_cf_paralel(cf_run, det["cf_kombinasi"])
                print(f"             CF_paralel = {cf_run} + {det['cf_kombinasi']} × (1 - {cf_run}) = {cf_baru}")
                cf_run = cf_baru

    # ── Skenario 3: Multi-diagnosa ───────────────────────────────────
    print("\n" + "─" * 65)
    print("\n📌 SKENARIO 3: Gejala ambigu — bisa multi-diagnosa")
    print("   Gejala: G04 (BSOD) + G14 (OS gagal booting) + G07 (beep) + G16 (crash)")
    hasil3 = proses_diagnosa_lengkap(["G04", "G14", "G07", "G16"])
    print(f"\n   Total rules aktif: {hasil3['total_rules_aktif']}")
    for d in hasil3["hasil"]:
        print(f"   {d['interpretasi']['emoji']} {d['kode']} {d['nama']:<35} CF: {d['cf_total']} ({d['persentase']}%)")
