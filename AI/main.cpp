// Author: Arsenii Kostenko
// PyTorch предоставляет C++-версию своего модуля — библиотеку LibTorch. Её можно скачать (cxx11 ABI) и расположить рядом с будущей программой:
// wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.0.0%2Bcpu.zip
// unzip libtorch-cxx11-abi-shared-with-deps-2.0.0%2Bcpu.zip
// Author: Arsenii Kostenko
#include <chrono>
#include <iostream>
#include <clipp.h>
#include <fstream>
#include <codecvt>
#include <locale>
#include <set>
#include <torch/script.h>
#include <torch/torch.h>
#include <onnxruntime_cxx_api.h>

int main() {
    // Загрузка модели ONNX
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING);
    Ort::SessionOptions session_options;
    session_options.SetIntraOpNumThreads(1);
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    const std::string model_path = "path/to/your/model.onnx";
    Ort::Session session(env, model_path.c_str(), session_options);

    // Загрузка и предобработка изображения
    const std::string image_path = "path/to/image.jpg";
    cv::Mat image = cv::imread(image_path);
    cv::cvtColor(image, image, cv::COLOR_BGR2RGB);
    cv::resize(image, image, cv::Size(224, 224)); // Необходимо будет изменить размер в соответствии с дальнейшей моделью
    image.convertTo(image, CV_32FC3, 1.0 / 255); // Приведение к формату float32 и нормализация

    // Копирование данных изображения в Tensor
    std::vector<float> input_data(image.ptr<float>(), image.ptr<float>() + image.total() * image.channels());
    auto input_tensor = torch::from_blob(input_data.data(), {1, image.rows, image.cols, image.channels()});
    input_tensor = input_tensor.permute({0, 3, 1, 2}); // Изменение порядка размерностей

    // Получение указателя на входные и выходные тензоры
    Ort::AllocatorWithDefaultOptions allocator;
    Ort::MemoryInfo input_memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    Ort::Value input_tensor_onnx = Ort::Value::CreateTensor<float>(input_memory_info, input_tensor.data_ptr<float>(), input_tensor.numel(), input_tensor.sizes().data(), input_tensor.sizes().size());
    const char* input_names[] = {session.GetInputName(0, allocator)};
    std::vector<const Ort::Value*> input_tensors = {&input_tensor_onnx};

    Ort::MemoryInfo output_memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    const char* output_name = session.GetOutputName(0, allocator);
    std::vector<Ort::Value> output_tensors(1);

    // Запуск инференса
    session.Run(Ort::RunOptions{nullptr}, input_names, input_tensors.data(), input_tensors.size(), &output_name, output_tensors.data(), output_tensors.size());

    // Получение результатов
    Ort::Value& output_tensor_onnx = output_tensors.front();
    std::vector<float> output_data(output_tensor_onnx.GetTensorMutableData<float>(), output_tensor_onnx.GetTensorMutableData<float>() + output_tensor_onnx.GetTensorTypeAndShapeInfo().GetElementCount());

    // Печать результатов
    std::cout << "Predicted probabilities:" << std::endl;
    for (float prob : output_data) {
        std::cout << prob << std::endl;
    }

    return 0;
}
