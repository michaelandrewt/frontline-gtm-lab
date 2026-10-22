#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace {
std::string lower(std::string value) {
    std::transform(value.begin(), value.end(), value.begin(),
                   [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return value;
}

std::string escape(const std::string& value) {
    std::string out;
    for (char c : value) {
        if (c == '"' || c == '\\') out += '\\';
        if (c == '\n' || c == '\r') out += ' ';
        else out += c;
    }
    return out;
}

std::string evidence_sentence(const std::string& text, std::size_t at) {
    std::size_t start = text.rfind('.', at);
    start = start == std::string::npos ? 0 : start + 1;
    std::size_t end = text.find('.', at);
    end = end == std::string::npos ? text.size() : end + 1;
    while (start < end && std::isspace(static_cast<unsigned char>(text[start]))) ++start;
    return text.substr(start, end - start);
}
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: deal_ledger TRANSCRIPT_FILE\n";
        return 2;
    }
    std::ifstream input(argv[1]);
    if (!input) {
        std::cerr << "could not read transcript\n";
        return 2;
    }
    std::ostringstream buffer;
    buffer << input.rdbuf();
    const std::string text = buffer.str();
    const std::string normalized = lower(text);

    const std::vector<std::pair<std::string, std::vector<std::string>>> fields = {
        {"economic_buyer", {"economic buyer", "decision maker", "sign off"}},
        {"pain", {"pain", "problem", "manual", "slow", "risk"}},
        {"timeline", {"timeline", "deadline", "by friday", "this quarter", "launch"}},
        {"budget", {"budget", "approved funds", "price"}},
        {"next_step", {"next step", "follow up", "schedule", "send"}}
    };

    std::cout << "{\"fields\":[";
    bool first = true;
    int found_count = 0;
    for (const auto& field : fields) {
        std::size_t position = std::string::npos;
        for (const auto& keyword : field.second) {
            position = normalized.find(keyword);
            if (position != std::string::npos) break;
        }
        if (!first) std::cout << ',';
        first = false;
        const bool found = position != std::string::npos;
        if (found) ++found_count;
        std::cout << "{\"field\":\"" << field.first << "\",\"status\":\""
                  << (found ? "evidence_found" : "missing") << "\",\"evidence\":\""
                  << (found ? escape(evidence_sentence(text, position)) : "") << "\",\"confidence\":"
                  << (found ? "0.78" : "0.0") << '}';
    }
    const int completeness = found_count * 20;
    std::cout << "],\"completeness\":" << completeness
              << ",\"approval_required\":true,\"write_status\":\"proposed_only\"}\n";
    return 0;
}

