cmake_minimum_required(VERSION 3.18.1)
project(shiksha_llama LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_library(ggml-base SHARED IMPORTED)
set_target_properties(ggml-base PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libggml-base.so"
)

add_library(ggml-cpu SHARED IMPORTED)
set_target_properties(ggml-cpu PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libggml-cpu.so"
)

add_library(ggml SHARED IMPORTED)
set_target_properties(ggml PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libggml.so"
)

add_library(llama SHARED IMPORTED)
set_target_properties(llama PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libllama.so"
)

add_library(shiksha_llama SHARED
    shiksha_llama_jni.cpp
)

find_library(log-lib log)
find_library(android-lib android)

target_link_libraries(shiksha_llama
    PRIVATE
    llama
    ggml
    ggml-cpu
    ggml-base
    ${log-lib}
    ${android-lib}
)

