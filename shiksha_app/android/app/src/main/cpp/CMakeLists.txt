cmake_minimum_required(VERSION 3.18.1)
project(shiksha_llama LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(shiksha_llama SHARED
    shiksha_llama_jni.cpp
)

find_library(log-lib log)
find_library(android-lib android)

target_link_libraries(shiksha_llama
    PRIVATE
    ${log-lib}
    ${android-lib}
)
