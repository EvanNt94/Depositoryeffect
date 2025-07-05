#ifndef OPTION_H
#define OPTION_H

double black_scholes_price(char flag, double S, double K, double T, double r, double sigma);
double option_delta(char flag, double S, double K, double T, double r, double sigma);
double option_gamma(double S, double K, double T, double r, double sigma);
double option_vega(double S, double K, double T, double r, double sigma);
double option_theta(char flag, double S, double K, double T, double r, double sigma);
double option_rho(char flag, double S, double K, double T, double r, double sigma);
void option_all_greeks(
    char flag,
    double S, double K, double T, double r, double sigma,
    double* price,
    double* delta,
    double* gamma,
    double* vega,
    double* theta,
    double* rho
);
double implied_volatility(char flag, double S, double K, double T, double r, double market_price);
#endif