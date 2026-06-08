import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_gejala() -> dict:
    """
    Memuat data gejala dari gejala.json.
    Return: dict dengan key = kode gejala, value = dict info gejala
    Contoh: { "G01": { "kode": "G01", "nama": "...", "keterangan": "..." }, ... }
    """
    path = os.path.join(DATA_DIR, "gejala.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {g["kode"]: g for g in data["gejala"]}


def load_kerusakan() -> dict:
    """
    Memuat data diagnosa kerusakan dari kerusakan.json.
    Return: dict dengan key = kode diagnosa, value = dict info diagnosa
    Contoh: { "D01": { "kode": "D01", "nama": "...", "solusi": [...], ... }, ... }
    """
    path = os.path.join(DATA_DIR, "kerusakan.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {k["kode"]: k for k in data["kerusakan"]}


def load_rules() -> list:
    """
    Memuat semua rule IF-THEN dari rules.json.
    Return: list of dict, setiap dict adalah satu rule
    Contoh: [{ "kode": "R01", "diagnosa": "D01", "gejala": ["G07","G04"],
               "cf_pakar": 0.8, "deskripsi": "..." }, ...]
    """
    path = os.path.join(DATA_DIR, "rules.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["rules"]


def get_semua_gejala_list() -> list:
    """
    Mengembalikan list gejala yang sudah diurutkan berdasarkan kode
    untuk keperluan tampilan di UI Streamlit.
    Return: list of dict gejala, diurutkan G01 -> G22
    """
    gejala_dict = load_gejala()
    return sorted(gejala_dict.values(), key=lambda x: x["kode"])


def get_rules_by_diagnosa(kode_diagnosa: str) -> list:
    """
    Mengambil semua rule yang berkaitan dengan satu diagnosa tertentu.
    Parameter: kode_diagnosa — contoh "D01"
    Return: list of rule dict yang diagnosa-nya sesuai
    """
    rules = load_rules()
    return [r for r in rules if r["diagnosa"] == kode_diagnosa]


def get_nama_gejala(kode: str) -> str:
    """
    Mengambil nama gejala berdasarkan kodenya.
    Parameter: kode — contoh "G01"
    Return: string nama gejala, atau kode itu sendiri jika tidak ditemukan
    """
    gejala = load_gejala()
    return gejala.get(kode, {}).get("nama", kode)


def get_nama_kerusakan(kode: str) -> str:
    """
    Mengambil nama diagnosa kerusakan berdasarkan kodenya.
    Parameter: kode — contoh "D01"
    Return: string nama diagnosa, atau kode itu sendiri jika tidak ditemukan
    """
    kerusakan = load_kerusakan()
    return kerusakan.get(kode, {}).get("nama", kode)


def validasi_basis_pengetahuan() -> dict:
    """
    Memvalidasi konsistensi seluruh basis pengetahuan:
    - Semua kode gejala di rules terdaftar di gejala.json
    - Semua kode diagnosa di rules terdaftar di kerusakan.json
    Return: dict berisi status validasi dan list error jika ada
    """
    gejala = load_gejala()
    kerusakan = load_kerusakan()
    rules = load_rules()

    errors = []

    for rule in rules:
        # Cek kode diagnosa
        if rule["diagnosa"] not in kerusakan:
            errors.append(
                f"Rule {rule['kode']}: diagnosa '{rule['diagnosa']}' tidak ditemukan"
            )
        # Cek setiap kode gejala
        for kode_g in rule["gejala"]:
            if kode_g not in gejala:
                errors.append(
                    f"Rule {rule['kode']}: gejala '{kode_g}' tidak ditemukan"
                )

    return {
        "valid": len(errors) == 0,
        "total_gejala": len(gejala),
        "total_kerusakan": len(kerusakan),
        "total_rules": len(rules),
        "errors": errors,
    }


if __name__ == "__main__":
    print("=" * 50)
    print("VALIDASI BASIS PENGETAHUAN")
    print("=" * 50)

    hasil = validasi_basis_pengetahuan()
    print(f"Total gejala    : {hasil['total_gejala']}")
    print(f"Total kerusakan : {hasil['total_kerusakan']}")
    print(f"Total rules     : {hasil['total_rules']}")
    print()

    if hasil["valid"]:
        print("✅ Basis pengetahuan valid — tidak ada inkonsistensi")
    else:
        print("❌ Ditemukan error:")
        for err in hasil["errors"]:
            print(f"   - {err}")

    print()
    print("DAFTAR GEJALA:")
    for g in get_semua_gejala_list():
        print(f"  {g['kode']} | {g['nama']}")
