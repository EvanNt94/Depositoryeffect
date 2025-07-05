from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef("""
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
""")

ffibuilder.set_source(
    "_option_cffi",
    '#include "option.h"',
    sources=["option.c", "stats.c"],
    libraries=["m"],
    include_dirs=["."],  # ggf. Pfad zu option.h
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)