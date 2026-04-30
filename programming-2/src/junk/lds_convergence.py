"""Discrete LDS verification for Lingebra"""


def simulate(n_months, alfa_start=5, beta_start=30):
  alpha = alfa_start
  beta = beta_start
  for _ in range(n_months):
    alpha_new = 0.9 * alpha + 0.2 * beta
    beta_new = 0.1 * alpha + 0.8 * beta
    alpha, beta = alpha_new, beta_new
  return alpha, beta


print(f"{'Months':>10} {'Alpha':>12} {'Beta':>12}")
print("-" * 37)

for n in [10, 100, 1000, 10000]:
  alfa, beta = simulate(n)
  print(f"{n:>10} {alfa:>12.8f} {beta:>12.8f}")
