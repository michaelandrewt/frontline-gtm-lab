#include <algorithm>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

namespace {
double bounded(const char* raw, const char* name) {
    char* end = nullptr;
    const double value = std::strtod(raw, &end);
    if (end == raw || *end != '\0' || value < 0.0 || value > 100.0) {
        throw std::invalid_argument(std::string(name) + " must be between 0 and 100");
    }
    return value;
}

std::string band(double score) {
    if (score >= 80.0) return "priority";
    if (score >= 60.0) return "review";
    return "hold";
}
}

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "usage: signal_relay FIT INTENT TIMING CONFIDENCE\n";
        return 2;
    }
    try {
        const double fit = bounded(argv[1], "fit");
        const double intent = bounded(argv[2], "intent");
        const double timing = bounded(argv[3], "timing");
        const double confidence = bounded(argv[4], "confidence");
        const double raw = fit * 0.40 + intent * 0.30 + timing * 0.20 + confidence * 0.10;
        const double score = raw * (0.70 + confidence / 333.333333);

        std::cout << std::fixed << std::setprecision(1)
                  << "{\"score\":" << std::min(100.0, score)
                  << ",\"band\":\"" << band(score)
                  << "\",\"weights\":{\"fit\":0.4,\"intent\":0.3,\"timing\":0.2,\"confidence\":0.1}"
                  << ",\"approval_required\":true}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
    return 0;
}

