cmake_minimum_required(VERSION 3.20)
project(vision_qa_infer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED COMPONENTS core imgcodecs imgproc)

if(NOT DEFINED ONNXRUNTIME_ROOT)
  set(ONNXRUNTIME_ROOT "$ENV{ONNXRUNTIME_ROOT}")
endif()

add_executable(infer infer.cpp)
target_include_directories(infer PRIVATE ${OpenCV_INCLUDE_DIRS} ${ONNXRUNTIME_ROOT}/include)
target_link_directories(infer PRIVATE ${ONNXRUNTIME_ROOT}/lib)
target_link_libraries(infer PRIVATE ${OpenCV_LIBS} onnxruntime)
