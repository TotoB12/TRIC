cmake_minimum_required(VERSION 3.14)

project(DataRecorder)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add vcpkg toolchain
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake")

# find_package(realsense2 REQUIRED)
find_package(Eigen3 3.3 REQUIRED NO_MODULE)
find_package(nlohmann_json REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

add_executable(DataRecorder main.cpp)

target_include_directories(DataRecorder PRIVATE ${realsense2_INCLUDE_DIR} ${EIGEN3_INCLUDE_DIR} ${Boost_INCLUDE_DIRS})
target_link_libraries(DataRecorder PRIVATE realsense2::realsense2 Eigen3::Eigen nlohmann_json::nlohmann_json Boost::system)
