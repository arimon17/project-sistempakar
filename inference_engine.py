from knowledge_base import load_rules, load_gejala, load_kerusakan


def forward_chaining(gejala_input: list) -> list:
    """
    Implementasi algoritma Forward Chaining.

    Prinsip kerja:
    - Dimulai dari fakta (gejala yang dipilih pengguna)
    - Mencocokkan fakta dengan kondisi IF pada setiap rule
    - Jika semua kondisi IF terpenuhi, rule tersebut AKTIF (fired)
    - Mengumpulkan semua rule yang aktif beserta info CF pakarnya

    Parameter:
        gejala_input : list of str
            Daftar kode gejala yang dipilih pengguna
            Contoh: ["G01", "G02", "G10"]

    Return:
        list of dict — daftar rule yang aktif, masing-masing berisi:
        {
            "kode"      : kode rule (contoh "R01"),
            "diagnosa"  : kode diagnosa (contoh "D01"),
            "gejala"    : list gejala kondisi rule,
            "cf_pakar"  : nilai CF pakar (0.0 – 1.0),
            "deskripsi" : penjelasan rule,
            "gejala_cocok": list gejala yang benar-benar cocok dengan input
        }
    """
    rules = load_rules()
    gejala_set = set(gejala_input)
    rules_aktif = []

    for rule in rules:
        kondisi = set(rule["gejala"])
        # Rule aktif jika SEMUA gejala dalam kondisi IF terpenuhi
        if kondisi.issubset(gejala_set):
            rules_aktif.append({
                "kode"        : rule["kode"],
                "diagnosa"    : rule["diagnosa"],
                "gejala"      : rule["gejala"],
                "cf_pakar"    : rule["cf_pakar"],
                "deskripsi"   : rule["deskripsi"],
                "gejala_cocok": list(kondisi & gejala_set),
            })

    return rules_aktif


def hitung_cf_user(gejala_input: list) -> dict:
    """
    Menghitung nilai CF user untuk setiap gejala yang dipilih.

    Dalam implementasi ini semua gejala yang dipilih pengguna
    dianggap CF_user = 1.0 (pengguna yakin gejala tersebut ada).
    Nilai bisa dikembangkan menjadi slider keyakinan di UI.

    Parameter:
        gejala_input : list of str — kode gejala yang dipilih

    Return:
        dict — { kode_gejala: cf_user }
        Contoh: { "G01": 1.0, "G02": 1.0 }
    """
    return {kode: 1.0 for kode in gejala_input}


def jalankan_inferensi(gejala_input: list) -> dict:
    """
    Fungsi utama yang menggabungkan Forward Chaining dan persiapan
    data untuk perhitungan Certainty Factor.

    Alur:
    1. Jalankan forward chaining → dapatkan rules yang aktif
    2. Kelompokkan rules aktif per diagnosa
    3. Siapkan data CF user per gejala
    4. Bangun jalur inferensi yang bisa ditampilkan di UI

    Parameter:
        gejala_input : list of str — kode gejala yang dipilih pengguna

    Return:
        dict berisi:
        {
            "rules_aktif"     : list semua rule yang fired,
            "per_diagnosa"    : dict rules aktif dikelompokkan per diagnosa,
            "cf_user"         : dict CF user per gejala,
            "jalur_inferensi" : list string penjelasan alur inferensi,
            "ada_hasil"       : bool — True jika ada minimal 1 rule aktif
        }
    """
    if not gejala_input:
        return {
            "rules_aktif"     : [],
            "per_diagnosa"    : {},
            "cf_user"         : {},
            "jalur_inferensi" : [],
            "ada_hasil"       : False,
        }

    rules_aktif   = forward_chaining(gejala_input)
    cf_user       = hitung_cf_user(gejala_input)
    gejala_data   = load_gejala()
    per_diagnosa  = {}
    jalur_inferensi = []

    # Kelompokkan rules aktif per diagnosa
    for rule in rules_aktif:
        kode_d = rule["diagnosa"]
        if kode_d not in per_diagnosa:
            per_diagnosa[kode_d] = []
        per_diagnosa[kode_d].append(rule)

    # Bangun jalur inferensi untuk tampilan UI
    for rule in rules_aktif:
        nama_gejala_list = [
            f"{kode} ({gejala_data[kode]['nama']})"
            for kode in rule["gejala"]
            if kode in gejala_data
        ]
        baris = (
            f"[{rule['kode']}] IF {' AND '.join(nama_gejala_list)} "
            f"→ THEN {rule['diagnosa']} (CF Pakar: {rule['cf_pakar']})"
        )
        jalur_inferensi.append(baris)

    return {
        "rules_aktif"     : rules_aktif,
        "per_diagnosa"    : per_diagnosa,
        "cf_user"         : cf_user,
        "jalur_inferensi" : jalur_inferensi,
        "ada_hasil"       : len(rules_aktif) > 0,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TEST INFERENCE ENGINE — FORWARD CHAINING")
    print("=" * 60)

    # Skenario uji: gejala overheating
    test_gejala = ["G10", "G11", "G13"]
    print(f"\nInput gejala  : {test_gejala}")
    print(f"Keterangan    : cepat panas + kipas bermasalah + mati mendadak")

    hasil = jalankan_inferensi(test_gejala)

    print(f"\nRules aktif   : {len(hasil['rules_aktif'])} rule")
    print(f"Diagnosa ditemukan: {list(hasil['per_diagnosa'].keys())}")

    print("\nJalur inferensi:")
    for jalur in hasil["jalur_inferensi"]:
        print(f"  {jalur}")

    print()

    # Skenario uji 2: gejala HDD rusak
    test_gejala_2 = ["G21", "G06", "G14"]
    print(f"Input gejala  : {test_gejala_2}")
    print(f"Keterangan    : klik-klik + HDD tidak terdeteksi + OS gagal booting")

    hasil2 = jalankan_inferensi(test_gejala_2)
    print(f"\nRules aktif   : {len(hasil2['rules_aktif'])} rule")
    print(f"Diagnosa ditemukan: {list(hasil2['per_diagnosa'].keys())}")
    print("\nJalur inferensi:")
    for jalur in hasil2["jalur_inferensi"]:
        print(f"  {jalur}")

    print()

    # Skenario uji 3: tidak ada gejala cocok
    test_gejala_3 = ["G12"]
    print(f"Input gejala  : {test_gejala_3}")
    print(f"Keterangan    : hanya baterai tidak ngecas (rule butuh kombinasi)")
    hasil3 = jalankan_inferensi(test_gejala_3)
    print(f"Rules aktif   : {len(hasil3['rules_aktif'])} rule")
    print(f"Ada hasil     : {hasil3['ada_hasil']}")
