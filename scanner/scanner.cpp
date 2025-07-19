// scanner.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <json.hpp>
#include <openssl/evp.h>     // Nova API para hash

// Função para calcular SHA256 usando a nova API EVP
std::string sha256(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) return "";

    EVP_MD_CTX* context = EVP_MD_CTX_new();
    if (!context) return "";

    if (!EVP_DigestInit_ex(context, EVP_sha256(), nullptr)) {
        EVP_MD_CTX_free(context);
        return "";
    }

    char buf[4096];
    while (file.read(buf, sizeof(buf))) {
        if (!EVP_DigestUpdate(context, buf, file.gcount())) {
            EVP_MD_CTX_free(context);
            return "";
        }
    }
    if (!EVP_DigestUpdate(context, buf, file.gcount())) {
        EVP_MD_CTX_free(context);
        return "";
    }

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int lengthOfHash = 0;
    if (!EVP_DigestFinal_ex(context, hash, &lengthOfHash)) {
        EVP_MD_CTX_free(context);
        return "";
    }

    EVP_MD_CTX_free(context);

    std::ostringstream oss;
    for (unsigned int i = 0; i < lengthOfHash; i++) {
        oss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return oss.str();
}

// Restante do código permanece o mesmo...
std::vector<std::string> extract_strings(const std::string& filename, size_t minlen=6) {
    std::ifstream file(filename, std::ios::binary);
    std::vector<std::string> result;
    if (!file) return result;
    std::string current;
    char c;
    while (file.get(c)) {
        if (isprint((unsigned char)c) || c == '\t') {
            current += c;
        } else {
            if (current.size() >= minlen) result.push_back(current);
            current.clear();
        }
    }
    if (current.size() >= minlen) result.push_back(current);
    return result;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "{\"error\": \"Usage: scannepr.exe <file>\"}" << std::endl;
        return 1;
    }
    std::string file = argv[1];
    nlohmann::json j;
    j["file"] = file;
    j["sha256"] = sha256(file);
    j["strings"] = extract_strings(file);
    std::cout << j.dump() << std::endl;
    return 0;
}