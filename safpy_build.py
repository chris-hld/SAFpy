import os.path
import sys
from cffi import FFI
ffibuilder = FFI()

home_dir = os.path.expanduser('~')
this_dir = os.path.abspath(os.path.dirname(__file__))
# define saf_path here, assumes SAF parallel to safpy by default.
saf_path = os.path.join(this_dir, ".", "Spatial_Audio_Framework")

# Populate these
c_header_source = ""
include_dirs = []
libraries = []
library_dirs = []

saf_performance_lib = []
extra_link_args = []

# Sensible default, please adjust if needed.
# In case of doubt, you can also check numpy.show_config() for its BLAS
print("Detected platform: " + sys.platform) 
if sys.platform == "darwin":
    print("SAFPY using default Apple Accelerate")
    extra_link_args.extend(['-Wl,-framework', '-Wl,Accelerate'])
else:
    print("SAFPY using default OpenBLAS/LAPACKE")
    saf_performance_lib.extend(["openblas", "lapacke"])


# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""

#define SAF_VERSION ...
                
""")

ffibuilder.cdef("""

typedef enum _AFSTFT_FDDATA_FORMAT{
    AFSTFT_BANDS_CH_TIME, /**< nBands x nChannels x nTimeHops */
    AFSTFT_TIME_CH_BANDS  /**< nTimeHops x nChannels x nBands */

}AFSTFT_FDDATA_FORMAT;

void *malloc(size_t size);
void free(void *ptr);

/**
 * 2-D malloc (contiguously allocated, so use free() as usual to deallocate)
 */
void** malloc2d(size_t dim1, size_t dim2, size_t data_size);

/**
 * 2-D calloc (contiguously allocated, so use free() as usual to deallocate)
 */
void** calloc2d(size_t dim1, size_t dim2, size_t data_size);

/**
 * 3-D malloc (contiguously allocated, so use free() as usual to deallocate)
 */
void*** malloc3d(size_t dim1, size_t dim2, size_t dim3, size_t data_size);

/**
 * 3-D calloc (contiguously allocated, so use free() as usual to deallocate)
 */
void*** calloc3d(size_t dim1, size_t dim2, size_t dim3, size_t data_size);



long double factorial(int n);

void getSHreal(/* Input Arguments */
            int order,
            float* dirs_rad,
            int nDirs,
            /* Output Arguments */
            float* Y);

void getSHreal_recur(/* Input Arguments */
            int order,
            float* dirs_rad,
            int nDirs,
            /* Output Arguments */
            float* Y);

void getSHreal_part
(
    int order_start,
    int order_end,
    float* dirs_rad,
    int nDirs,
    float* Y);

void getSHcomplex(/* Input Arguments */
                    int order,
                    float* dirs_rad,
                    int nDirs,
                    /* Output Arguments */
                    float _Complex* Y);

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

void afSTFT_destroy(void ** const phSTFT);

int afSTFT_getNBands(void * const hSTFT);

void afSTFT_getCentreFreqs(void * const hSTFT,
                           float fs,
                           int nBands,
                           float* freqVector);

int afSTFT_getProcDelay(void * const hSTFT);

void afSTFT_clearBuffers(void * const hSTFT);

void afSTFT_forward(void * const hSTFT,
                    float** dataTD,
                    int framesize,
                    float _Complex*** dataFD);

void afSTFT_backward(void * const hSTFT,
                     float _Complex*** dataFD,
                     int framesize,
                     float** dataTD);

void afSTFT_forward_flat(void * const hSTFT,
                         float* dataTD,
                         int framesize,
                         float _Complex* dataFD);

void afSTFT_backward_flat(void * const hSTFT,
                          float _Complex* dataFD,
                          int framesize,
                          float* dataTD);

void latticeDecorrelator_create(void ** phDecor,
                                float fs,
                                int hopsize,
                                float * freqVector,
                                int nBands,
                                int nCH,
                                int * orders,
                                float * freqCutoffs,
                                int nCutoffs,
                                int maxDelay,
                                int lookupOffset,
                                float enComp_coeff);

void latticeDecorrelator_destroy(void ** phDecor);

void latticeDecorrelator_reset(void * hDecor);

void latticeDecorrelator_apply(void * hDecor,
                               float _Complex *** inFrame,
                               int nTimeSlots,
                               float _Complex *** decorFrame);
void transientDucker_create(void ** 	phDucker,
                            int 	nCH,
                            int 	nBands);

void transientDucker_destroy(void ** phDucker);

void transientDucker_apply(void * hDucker,
                           float _Complex *** inFrame,
                           int nTimeSlots,
                           float alpha,
                           float beta,
                           float _Complex *** residualFrame,
                           float _Complex *** transientFrame);

""")

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
c_header_source += f"""
    #include <complex.h> 
    #include "{saf_path}/framework/include/saf.h"  // the C header of the lib
    """
libraries.append(saf_path + "/build/framework/saf")  # lib name, for the linker

libraries.extend(saf_performance_lib)

print("Compiling _safpy with:")
print(f"C_Header_Source: {c_header_source}")
print(f"include_dirs: {include_dirs}")
print(f"libraries: {libraries}")
print(f"library_dirs: {library_dirs}")
print(f"extra_link_args: {extra_link_args}")



ffibuilder.set_source("_safpy", c_header_source, include_dirs=include_dirs,
                      libraries=libraries, library_dirs=library_dirs, 
                      extra_link_args=extra_link_args)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
