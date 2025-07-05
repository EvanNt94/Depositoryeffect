#include "option.h"
#include "stats.h"
#include <math.h>

static double d1(double S, double K, double T, double r, double sigma) {
    return (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T));
}

static double d2(double d1, double sigma, double T) {
    return d1 - sigma * sqrt(T);
}

double black_scholes_price(char flag, double S, double K, double T, double r, double sigma) {
    double d_1 = d1(S, K, T, r, sigma);
    double d_2 = d2(d_1, sigma, T);
    if (flag == 'c') {
        return S * normal_cdf(d_1) - K * exp(-r * T) * normal_cdf(d_2);
    } else {
        return K * exp(-r * T) * normal_cdf(-d_2) - S * normal_cdf(-d_1);
    }
}

void option_all_greeks(
    char flag,
    double S, double K, double T, double r, double sigma,
    double* price,
    double* delta,
    double* gamma,
    double* vega,
    double* theta,
    double* rho
) {
    double d_1 = d1(S, K, T, r, sigma);
    double d_2 = d2(d_1, sigma, T);
    double nd1 = normal_pdf(d_1);
    double Nd1 = normal_cdf(d_1);
    double Nd2 = normal_cdf(d_2);

    double discount = exp(-r * T);

    if (flag == 'c') {
        *price = S * Nd1 - K * discount * Nd2;
        *delta = Nd1;
        *theta = - (S * nd1 * sigma) / (2 * sqrt(T)) - r * K * discount * Nd2;
        *rho = K * T * discount * Nd2;
    } else {
        *price = K * discount * normal_cdf(-d_2) - S * normal_cdf(-d_1);
        *delta = Nd1 - 1;
        *theta = - (S * nd1 * sigma) / (2 * sqrt(T)) + r * K * discount * normal_cdf(-d_2);
        *rho = -K * T * discount * normal_cdf(-d_2);
    }

    *gamma = nd1 / (S * sigma * sqrt(T));
    *vega = S * nd1 * sqrt(T);
}

double implied_volatility(char flag, double S, double K, double T, double r, double market_price) {
    const double tol = 1e-6;
    const int max_iter = 100;
    double sigma_low = 1e-5;
    double sigma_high = 5.0;
    double sigma;

    for (int i = 0; i < max_iter; ++i) {
        sigma = 0.5 * (sigma_low + sigma_high);
        double price = black_scholes_price(flag, S, K, T, r, sigma);
        double diff = price - market_price;

        if (fabs(diff) < tol) {
            return sigma;
        }

        if (diff > 0.0) {
            sigma_high = sigma;
        } else {
            sigma_low = sigma;
        }
    }

    return sigma; // return best effort if no convergence
}
