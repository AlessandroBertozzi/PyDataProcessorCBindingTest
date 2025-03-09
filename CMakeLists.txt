cmake_minimum_required(VERSION 3.10)
project(PyDataProcessor)

# Compila con C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Trova Python e pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Crea il modulo Python
pybind11_add_module(data_processor DataProcessor.cpp)

# Opzioni di ottimizzazione
if(NOT MSVC)
  target_compile_options(data_processor PRIVATE -O3)
endif()
