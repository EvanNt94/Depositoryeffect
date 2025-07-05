#include "option.h"
#include <stdio.h>
#include <time.h>

int main() {
  double S = 203.27;
  double K = 205.00;
  double T = 6.0 / 252.0;
  double r = 0.0409;
  double sigma = 0.32;
  char flag = 'c';

  clock_t start = clock();
  double iv = implied_volatility('c', 203.27, 205.00, 6.0 / 252.0, 0.0409, 3.35);
  double price, delta, gamma, vega, theta, rho;
  int N = 1000000;
  for (int i = 0; i < N; i++) {
    option_all_greeks(flag, S, K, T, r, sigma, &price, &delta, &gamma, &vega,
                      &theta, &rho);
  }
  clock_t end = clock();
  double seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Implied Volatility: %.6f\n", iv);
  printf("Ergebnisse eines Durchlaufs:\n");
  printf("Preis:  %.4f\n", price);
  printf("Delta:  %.4f\n", delta);
  printf("Gamma:  %.6f\n", gamma);
  printf("Vega:   %.4f\n", vega);
  printf("Theta:  %.4f\n", theta);
  printf("Rho:    %.4f\n", rho);
  printf("\nDauer für %d Wiederholungen: %.6f Sekunden\n", N, seconds);
  printf("Durchschnitt pro Aufruf: %.6f µs\n", (seconds / N) * 1e6);
  return 0;
}