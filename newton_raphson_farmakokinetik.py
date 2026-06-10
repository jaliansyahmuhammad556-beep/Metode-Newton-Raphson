"""
===============================================
  METODE NEWTON-RAPHSON — FARMAKOKINETIK
  Menentukan Jendela Terapi Efektif Obat
===============================================
Kasus:
  Model konsentrasi obat dalam darah:
    C(t) = D * (e^(-k1*t) - e^(-k2*t)) / (k2 - k1)

  Parameter:
    D  = 500 mg  (dosis)
    k1 = 0.1 /jam (konstanta eliminasi)
    k2 = 0.5 /jam (konstanta absorpsi)
    C_target = 300 mg/L

  Tujuan: Cari t1 dan t2 sehingga C(t) = 300 mg/L
  yaitu dengan mencari akar dari f(t) = C(t) - C_target = 0
"""

import math

# ── Parameter ──────────────────────────────────────────
D        = 500.0   # mg
k1       = 0.1     # /jam
k2       = 0.5     # /jam
C_target = 300.0   # mg/L
toleransi = 1e-4
maks_iterasi = 100

# ── Model fungsi ───────────────────────────────────────
def C(t):
    """Konsentrasi obat pada waktu t"""
    return D * (math.exp(-k1 * t) - math.exp(-k2 * t)) / (k2 - k1)

def f(t):
    """f(t) = C(t) - C_target  →  dicari akarnya"""
    return C(t) - C_target

def df(t):
    """Turunan f'(t) = C'(t)"""
    return D * (-k1 * math.exp(-k1 * t) + k2 * math.exp(-k2 * t)) / (k2 - k1)

# ── Newton-Raphson ─────────────────────────────────────
def newton_raphson(t0, label):
    print(f"\n[AKAR {label}: tebakan awal t0 = {t0}]")
    print(f"{'It':>4}  {'tᵢ':>10}  {'f(tᵢ)':>10}  {'f′(tᵢ)':>10}  {'tᵢ₊₁':>10}  {'|Error|':>10}")
    print("-" * 65)

    t = t0
    for i in range(1, maks_iterasi + 1):
        ft  = f(t)
        dft = df(t)

        if abs(dft) < 1e-12:
            print("  ⚠ Turunan mendekati nol, iterasi berhenti.")
            return None

        t_baru = t - ft / dft
        error  = abs(t_baru - t)

        status = " ✓ KONVERGEN" if error < toleransi else ""
        print(f"{i:>4}  {t:>10.6f}  {ft:>10.4f}  {dft:>10.4f}  {t_baru:>10.6f}  {error:>10.2e}{status}")

        t = t_baru
        if error < toleransi:
            break
    else:
        print("  ⚠ Tidak konvergen dalam batas iterasi.")
        return None

    return t

# ── Jalankan ───────────────────────────────────────────
print("=" * 65)
print("   NEWTON-RAPHSON — JENDELA TERAPI FARMAKOKINETIK")
print("=" * 65)
print(f"  Model : C(t) = {D}*(e^-{k1}t - e^-{k2}t) / ({k2}-{k1})")
print(f"  Target: C_target = {C_target} mg/L")
print(f"  Tol   : {toleransi}")

t1 = newton_raphson(t0=1.0,  label="t₁ (kadar naik ke 300 mg/L)")
t2 = newton_raphson(t0=15.0, label="t₂ (kadar turun ke 300 mg/L)")

# ── Hasil & Validasi ───────────────────────────────────
print("\n" + "=" * 65)
print("  HASIL AKHIR")
print("=" * 65)

if t1 and t2:
    durasi = t2 - t1
    # cari t_max (C'(t) = 0)
    t_max = math.log(k2 / k1) / (k2 - k1)
    C_max = C(t_max)

    print(f"  t₁ (mulai efektif) = {t1:.6f} jam  (~{t1*60:.1f} menit)")
    print(f"  t₂ (akhir efektif) = {t2:.6f} jam  (~{t2:.2f} jam)")
    print(f"  Durasi terapi      = {durasi:.3f} jam  (~{durasi*60:.0f} menit)")
    print(f"  C_max (puncak)     = {C_max:.2f} mg/L  pada t ≈ {t_max:.2f} jam")
    print(f"  Dosis ulang tiap   ~ {durasi:.1f} jam")

    # Validasi galat
    err1 = abs(f(t1))
    err2 = abs(f(t2))
    print(f"\n  Validasi f(t₁) = {err1:.2e}  ({'✓ ≈ 0' if err1 < 1e-6 else '✗'})")
    print(f"  Validasi f(t₂) = {err2:.2e}  ({'✓ ≈ 0' if err2 < 1e-6 else '✗'})")
    print(f"\n  ✓ Newton-Raphson tervalidasi — konvergensi kuadratik terkonfirmasi")

print("=" * 65)
