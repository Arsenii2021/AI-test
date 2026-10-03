#include <algorithm>
#include <array>
#include <iostream>
#include <onnxruntime_cxx_api.h>
#include <opencv2/opencv.hpp>

namespace {

cv::Mat preprocess(const cv::Mat& src, int size) {
  cv::Mat gray, resized, f32;
  cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);
  cv::resize(gray, resized, cv::Size(size, size), 0, 0, cv::INTER_AREA);
  resized.convertTo(f32, CV_32FC1, 1.0 / 255.0);
  return f32;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 3) {
    std::cerr << "usage: infer <model.onnx> <image> [size]\n";
    return 1;
  }

  const char* model_path = argv[1];
  const cv::Mat image = cv::imread(argv[2]);
  if (image.empty()) {
    std::cerr << "cannot read " << argv[2] << "\n";
    return 1;
  }
  const int size = argc > 3 ? std::stoi(argv[3]) : 128;
  cv::Mat input = preprocess(image, size);
  if (!input.isContinuous()) {
    input = input.clone();
  }

  Ort::Env env{ORT_LOGGING_LEVEL_WARNING, "vision_qa"};
  Ort::SessionOptions opts;
  opts.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
  Ort::Session session{env, model_path, opts};
  Ort::AllocatorWithDefaultOptions allocator;

  const auto in_name = session.GetInputNameAllocated(0, allocator);
  const auto out_name = session.GetOutputNameAllocated(0, allocator);
  const char* in_names[] = {in_name.get()};
  const char* out_names[] = {out_name.get()};

  const std::array<int64_t, 4> shape{1, size, size, 1};
  auto memory = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
  Ort::Value tensor = Ort::Value::CreateTensor<float>(
      memory, reinterpret_cast<float*>(input.data), static_cast<size_t>(size * size),
      shape.data(), shape.size());

  auto outputs = session.Run(Ort::RunOptions{nullptr}, in_names, &tensor, 1, out_names, 1);
  const float* probs = outputs.front().GetTensorData<float>();
  const auto info = outputs.front().GetTensorTypeAndShapeInfo();
  const size_t n = info.GetElementCount();
  const size_t best = static_cast<size_t>(std::distance(probs, std::max_element(probs, probs + n)));

  static const char* kLabels[] = {"boot", "login", "ready", "error"};
  if (best < 4) {
    std::cout << kLabels[best] << "\t" << probs[best] << "\n";
  } else {
    std::cout << best << "\t" << probs[best] << "\n";
  }
  return 0;
}
