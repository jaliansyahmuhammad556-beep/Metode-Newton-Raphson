# Newton-Raphson
# Mencari akar persamaan nonlinear
# f(x) = x^3 - x - 2 = 0

def f(x):
    return x**3 - x - 2

def df(x):
    return 3*x**2 - 1

# Tebakan awal
x = 1.5

# Parameter iterasi
tol = 1e-6
max_iter = 100

print("Iterasi\t x_n\t\t f(x_n)")

for i in range(max_iter):
    fx = f(x)
    dfx = df(x)

    print(f"{i}\t\t{x:.10f}\t{fx:.10f}")

    x_new = x - fx/dfx

    error = abs((x_new - x)/x_new) * 100

    if error < tol:
        x = x_new
        break

    x = x_new

print("\n=== HASIL ===")
print(f"Akar aproksimasi = {x:.10f}")
print(f"f(x) = {f(x):.10e}")
print(f"Galat relatif = {error:.10e} %")