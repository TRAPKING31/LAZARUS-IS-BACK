import socket
import time

# حدد البيانات
TARGET_IP = "89.46.1.130"  # IP السيرفر المستهدف
TARGET_PORT = 7008        # البورت
DURATION = 60000             # مدة الاختبار بالثواني (يمكنك زيادتها)

def test_connection():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # تحويل الـ IP إلى أجزاء (Octets) والـ Port بالشكل الصحيح لبروتوكول SAMP
        ip_bytes = bytes(map(int, TARGET_IP.split('.')))
        port_bytes = int(TARGET_PORT).to_bytes(2, 'little')
        
        # صيغة حزمة استعلام معلومات السيرفر (Information query 'i')
        payload = b'SAMP' + ip_bytes + port_bytes + b'i'
        
        end_time = time.time() + DURATION
        count = 0
        
        print(f"جاري إرسال الحزم إلى {TARGET_IP}:{TARGET_PORT}...")
        
        while time.time() < end_time:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
            
        print(f"تم إرسال {count} حزمة بنجاح.")
        
    except Exception as e:
        print(fُ"حدث خطأ: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_connection()
