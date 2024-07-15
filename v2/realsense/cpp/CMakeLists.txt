cmake_minimum_required(VERSION 3.10)
project(HelloRealsense)

# Specify C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_CXX_EXTENSIONS NO)

# Manually specify the paths to the RealSense SDK
set(REALSENSE2_INCLUDE_DIR "C:/Program Files (x86)/Intel RealSense SDK 2.0/include")
set(REALSENSE2_LIBRARY_DIR "C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64")

# Manually add the include and library directories for RealSense
include_directories(${REALSENSE2_INCLUDE_DIR})
link_directories(${REALSENSE2_LIBRARY_DIR})

find_package(Boost REQUIRED COMPONENTS system)
find_package(GDAL REQUIRED)

add_executable(hello main.cpp)
target_include_directories(hello PRIVATE ${Boost_INCLUDE_DIRS} ${GDAL_INCLUDE_DIRS})
target_link_libraries(hello realsense2 Boost::system GDAL::GDAL)
