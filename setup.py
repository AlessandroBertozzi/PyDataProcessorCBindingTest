#!/usr/bin/env python3
# setup.py - Script di configurazione per compilare la libreria C++

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os

class get_pybind_include:
    """Helper class per ottenere il percorso di inclusione di pybind11"""
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

# Definisci l'estensione C++
ext_modules = [
    Extension(
        'data_processor',
        ['DataProcessor.cpp'],
        include_dirs=[
            # Percorso agli header di pybind11
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++',
        extra_compile_args=['-std=c++11']
    ),
]

# Configurazione della compilazione
class BuildExt(build_ext):
    """Una classe personalizzata di build_ext per gestire diverse opzioni di compilazione"""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append('-O3')  # Ottimizzazione massima
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
            
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
            
        build_ext.build_extensions(self)

setup(
    name='data_processor',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A data processing library implemented in C++',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0', 'numpy', 'matplotlib', 'tqdm'],
    setup_requires=['pybind11>=2.6.0'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
