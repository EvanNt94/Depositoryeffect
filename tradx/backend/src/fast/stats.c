#include <math.h>
#include "stats.h"

double normal_pdf(double x) {
    return (1.0 / sqrt(2.0 * M_PI)) * exp(-0.5 * x * x);
}

double normal_cdf(double x) {
    // Abramowitz & Stegun approximation
    // (Can be improved later)
    return 0.5 * erfc(-x / sqrt(2.0));
}