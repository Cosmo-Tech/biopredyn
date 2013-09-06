from distutils.core import setup, Extension

biopredyn_module = Extension(
    '_biopredyn',
    sources=['biopredynPYTHON_wrap.cxx', 'biopredyn-pskel.cxx'],
    )

setup(name='biopredyn',
      version='1.0',
      py_modules=['biopredyn'],
      )
