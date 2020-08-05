from cffi import FFI
ffibuilder = FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""

    typedef float _Complex float_complex;
    typedef double _Complex double_complex;

    long double factorial(int n);

    void getSHreal(/* Input Arguments */
               int order,
               float* dirs_rad,
               int nDirs,
               /* Output Arguments */
               float* Y);

    void getSHcomplex(/* Input Arguments */
                      int order,
                      float* dirs_rad,
                      int nDirs,
                      /* Output Arguments */
                      float_complex* Y);

""")

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
c_header_source = """
    #include "../../Spatial_Audio_Framework/framework/include/saf.h"   // the C header of the library
"""

libraries = ['../../Spatial_Audio_Framework/build/framework/saf']  # library name, for the linker

# CHOOSE HERE FOR NOW:
SAF_PERFORMANCE_LIB = "SAF_USE_INTEL_MKL"

if SAF_PERFORMANCE_LIB == "SAF_USE_INTEL_MKL":
    c_header_source += """
        #define SAF_USE_INTEL_MKL
        """
    libraries.append('mkl_rt')
    library_dirs = ["/opt/anaconda3/lib/"]

if SAF_PERFORMANCE_LIB == "SAF_USE_OPEN_BLAS_AND_LAPACKE":
    c_header_source += """
        #define SAF_USE_OPEN_BLAS_AND_LAPACKE
        """
    libraries.append('lapacke')
    library_dirs = []

ffibuilder.set_source("_safpy", c_header_source, libraries=libraries,
                      library_dirs=library_dirs)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
