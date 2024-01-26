# SAFpy

[![Python application](https://github.com/chris-hld/SAFpy/actions/workflows/python-safpy.yml/badge.svg)](https://github.com/chris-hld/SAFpy/actions/workflows/python-safpy.yml)

This is a Python binding / wrapper for
https://github.com/leomccormack/Spatial_Audio_Framework

So far, there are a bunch of functions exposed, please feel free to 
add/contribute more if needed!


Quickstart
---
1. Clone SAFpy, SAF is provided as a submodule, and change to the folder

```git clone --recursive https://github.com/chris-hld/SAFpy && cd SAFpy```

2. Go to the SAF folder and compile SAF, see instructions in its [docs](https://github.com/leomccormack/Spatial_Audio_Framework/blob/master/README.md). 
For example with

```cmake -S . -B build -DSAF_PERFORMANCE_LIB=SAF_USE_OPEN_BLAS_AND_LAPACKE && cmake --build ./build```

3. Install numpy and CFFI (in the environment you want to use), e.g. `conda install numpy cffi`
4. Now we need to build *safpy*, which creates the module. 
Running `pip install -e .` (with `.` in the SAFpy folder) builds it automatically and installs any potentially missing Python dependencies.
6. (Optional) Test if everything works, run `pytest -vvv` in the SAFpy folder.


Details
---
You can also build SAFpy manually, e.g., for debugging, with 
`python safpy_build.py`.

By default, it assumes SAF in a subdirectory, which is obtained by `git submodule update --init --recursive `. 
In case you want to use a different location, you can simply adapt the variable `saf_path` in `safpy_build.py` if needed.
There you also have access to change the SAF performance library options, in case the default is not working for you.

If in trouble you can have a look at the CI steps [here](https://github.com/chris-hld/SAFpy/blob/master/.github/workflows/python-safpy.yml).

Usage
---
Use *safpy* as a python package.
Have a look at `examples/test_call.py`!
