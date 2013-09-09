from distutils.core import setup, Extension

biopredyn_module = Extension(
    '_libbiopredyn',
    sources=['biopredynPYTHON_wrap.cxx', 'biopredyn.cxx'],
    )

setup(name='libbiopredyn',
      version='1.0',
      py_modules=['libbiopredyn'],
      )
