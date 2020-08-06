import os.path
from cffi import FFI
ffibuilder = FFI()

home_dir = os.path.expanduser('~')
this_dir = os.path.abspath(os.path.dirname(__file__))
saf_path = os.path.join(this_dir, '..', '..', 'Spatial_Audio_Framework')

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""

typedef float _Complex float_complex;
typedef double _Complex double_complex;

typedef enum _AFSTFT_FDDATA_FORMAT{
    AFSTFT_BANDS_CH_TIME, /**< nBands x nChannels x nTimeHops */
    AFSTFT_TIME_CH_BANDS  /**< nTimeHops x nChannels x nBands */

}AFSTFT_FDDATA_FORMAT;


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

void generateVBAPgainTable3D(/* Input arguments */
                             float* ls_dirs_deg,
                             int L,
                             int az_res_deg,
                             int el_res_deg,
                             int omitLargeTriangles,
                             int enableDummies,
                             float spread,
                             /* Output arguments */
                             float** gtable,
                             int* N_gtable,
                             int* nTriangles);

void afSTFT_create(void ** const phSTFT,
                   int nCHin,
                   int nCHout,
                   int hopsize,
                   int lowDelayMode,
                   int hybridmode,
                   AFSTFT_FDDATA_FORMAT format);

""")

# Populate these
c_header_source = ""
include_dirs = []
libraries = []
library_dirs = []


# CHOOSE PERFORMANCE LIB HERE FOR NOW:
SAF_PERFORMANCE_LIB = "SAF_USE_INTEL_MKL"

if SAF_PERFORMANCE_LIB == "SAF_USE_INTEL_MKL":
    c_header_source += """
    #define SAF_USE_INTEL_MKL
    """
    libraries.append("mkl_rt")
    # for: conda install mkl mkl-include
    include_dirs += [f"{home_dir}/anaconda3/include", "/opt/anaconda3/include/"]
    library_dirs += [f"{home_dir}/anaconda3/lib/", "/opt/anaconda3/lib/"]

if SAF_PERFORMANCE_LIB == "SAF_USE_OPEN_BLAS_AND_LAPACKE":
    c_header_source += """
    #define SAF_USE_OPEN_BLAS_AND_LAPACKE
    """
    libraries.append('lapacke')

if SAF_PERFORMANCE_LIB == "SAF_USE_APPLE_ACCELERATE":
    c_header_source += """
    #define SAF_USE_APPLE_ACCELERATE
    """

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
c_header_source += f"""
    #include "{saf_path}/framework/include/saf.h"  // the C header of the lib
    """
libraries.append(saf_path + "/build/framework/saf")  # lib name, for the linker

print("Compiling _safpy with:")
print(f"C_Header_Source: {c_header_source}")
print(f"include_dirs: {include_dirs}")
print(f"libraries: {libraries}")
print(f"library_dirs: {library_dirs}")


ffibuilder.set_source("_safpy", c_header_source, include_dirs=include_dirs,
                      libraries=libraries, library_dirs=library_dirs)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
