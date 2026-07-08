import discord
from discord.ext import commands, tasks
import random
import os
import json 
import asyncio
from keep_alive import keep_alive 
from datetime import datetime, timezone
from typing import Optional, Dict, Union
from discord.ui import View, Select, Button, Modal, TextInput
from draw_figure import generate_figure
import re

# =============================================================
# 1. AYARLAR VE SABİT DEĞİŞKENLER
# =============================================================
SUNUCU_ADI = "Vortex League"
GUILD_ID = 1522977509497503876
OWNER_ID = 1243258148232368286
DEGER_YETKILISI_ROL_ID = 1523744204839190578   # @Değer Yetkilisi | 💵
ANTRENMAN_KANAL_ID = 1523744311789748524          # #🎽║antrenman
ANTRENMAN_BILDIRI_KANAL_ID = 1523744312867684402  # #🛎️║antrenman-bildiri
INSTAGRAM_KANAL_ID = 1523744316655407184          # #📸║instagram
KAYIT_KANAL_ID = 1523744285349122078              # #🔒║kayıt-duyuru
KAYIT_YETKILI_ROL_ID = 1523744206395543574        # @Kayıt Yetkilisi | ✏️
KAYITSIZ_ROL_ID = 1523744222321049723             # @Kayıtsız
LOG_KANAL_ID = 1523744362255745034                # #🔮・giriş-çıkış-log
SOHBET_KANAL_ID = 1523744322682490943             # #💬║sohbet
TICKET_KANAL_ID = 1523744309579350088             # #🎫║ticket
DESTEK_KATEGORI_ID = 1523744257167462451          # 📁 Nitelik Kazanma / Ticket
YETKILI_1_ID = 1523744199575470141                # @Admin
YETKILI_2_ID = 1523744204839190578                # @Değer Yetkilisi | 💵
BASKAN_ROL_ID = 1523744209847451668               # @Takım Başkanı
TEKNIK_DIREKTOR_ROL_ID = 1523744209847451668      # @Teknik Direktör
KAPTAN_ROL_ID = 1523744223239864402               # @Kaptan
FUTBOLCU_ROL_ID = 1523744220102393887             # @Futbolcu
ILAN_VER_KANAL_ID = 1523744325186486434           # #🤖║bot-komut
TRANSFER_LISTESI_ID = 1523744329519333448         # #💵║transfer-masası
DEGER_LOG = 1523745549650755845                   # #değer-bildirme
KAYITLI_ROL_ID = 1523744220102393887              # @Futbolcu
quiz_channel_id = 1523744325186486434             # #🤖║bot-komut
ÜYE_ROL_ID = 1523744219712327680                 # @Üye

ROLLER = {
    "futbolcu": FUTBOLCU_ROL_ID,
    "kayitli": KAYITLI_ROL_ID,
    "kayitsiz": KAYITSIZ_ROL_ID,
    "üye" : ÜYE_ROL_ID,
    "baskan": BASKAN_ROL_ID
}

TAKIM_ROLLERI = {
    1523744210669404240: "Galatasaray",
    1523744211608797304: "Beşiktaş",
    1523744212263108691: "Fenerbahçe",
    1523744214251343903: "Bayern Münih",
    1523744215039869030: "Barcelona",
    1523744216117674125: "İnter",
    1523744217715707924: "Real Madrid",
    1523744218751959060: "Juventus",
}

TAKIM_LOGOLARI = {
    "Galatasaray": "https://i.imgur.com/jMzNz3a.png",
    "Beşiktaş": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Be%C5%9Fikta%C5%9F_JK_logo.svg/100px-Be%C5%9Fikta%C5%9F_JK_logo.svg.png",
    "Fenerbahçe": "https://i.imgur.com/z4f1YfN.png",
    "Bayern Münih": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282002%E2%80%932017%29.svg/100px-FC_Bayern_M%C3%BCnchen_logo_%282002%E2%80%932017%29.svg.png",
    "Barcelona": "https://i.imgur.com/w6TqTzL.png",
    "İnter": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/100px-FC_Internazionale_Milano_2021.svg.png",
    "Real Madrid": "https://i.imgur.com/gJ6hL6x.png",
    "Juventus": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Juventus_FC_2017_icon_%28black%29.svg/100px-Juventus_FC_2017_icon_%28black%29.svg.png",
}

TAKIM_RENKLERI = {
    "Galatasaray": 0xd4031c,
    "Beşiktaş": 0x1a1a1a,
    "Fenerbahçe": 0xffee00,
    "Bayern Münih": 0xdc052d,
    "Barcelona": 0xa50044,
    "İnter": 0x0068a8,
    "Real Madrid": 0xffffff,
    "Juventus": 0x1a1a1a,
}

PARA_DOSYA      = "para.json"
ANTRENMAN_DOSYA = "antrenman.json"
STAT_DOSYA      = "stats.json"
NITELIK_DOSYA   = "nitelikler.json"

NITELIK_YETKILI_ROL_ID = DEGER_YETKILISI_ROL_ID

KATEGORILER = {
    "Atak":     ["Orta Açma", "Bitiricilik", "Kafa İsabeti", "Kısa Pas", "Voleler"],
    "Savunma":  ["Ayakta Müdahale", "Kayarak Müdahale", "Top Kesme"],
    "Beceri":   ["Dribbling", "Falso", "Serbest Vuruş İsabeti", "Uzun Pas", "Top Kontrolü"],
    "Güç":      ["Şut Gücü", "Zıplama", "Dayanıklılık", "Güç", "Uzaktan Şut"],
    "Hareket":  ["Hızlanma", "Sprint Hızı", "Çeviklik", "Reaksiyonlar", "Denge"],
    "Mentalite":["Agresiflik", "Pozisyon Alma", "Görüş", "Penaltı"],
    "Kaleci":   ["Kaleci Atlayışı", "Kaleci Top Kontrolü", "Kaleci Vuruşu", "Kaleci Pozisyon Alma", "Kaleci Refleksler"],
}

GANT_DOSYA    = "gant.json"
AANT_DOSYA    = "aant.json"
GANT_LIMIT    = 50
AANT_LIMIT    = 100
GANT_KANAL_ID = 1523744313879838825   # #🥈║gümüş-ant  ← gerekirse güncelle
AANT_KANAL_ID = 1523744314833395744   # #🥇║altın-ant  ← gerekirse güncelle

STAT_ISIMLER = {
    "antrenman":       "🏋️ Antrenman",
    "penalti_atilan":  "🥅 Penaltı Atılan",
    "penalti_gol":     "⚽ Penaltı Golü",
    "post":            "📸 Post",
    "kayit_yapildi":   "📋 Kayıt Yapıldı",
    "nitelik_eklendi": "⭐ Nitelik Eklendi",
}

BECERI_KANAL_ID = 1523744315120291951   # #⭐║beceri-antrenman
BECERI_DOSYA    = "beceri.json"
MAX_FULL        = 2
BECERI_BEKLEME  = 3000  # 50 dakika (saniye)

BECERILER = {
    "sut":      {"isim": "Şut Becerisi",     "max": 70, "emoji": "🎯"},
    "defans":   {"isim": "Defans Becerisi",   "max": 55, "emoji": "🛡️"},
    "calim":    {"isim": "Çalım Becerisi",    "max": 50, "emoji": "⚡"},
    "dribling": {"isim": "Dribling Becerisi", "max": 60, "emoji": "🔄"},
    "kurtaris": {"isim": "Kurtarış Becerisi", "max": 65, "emoji": "🧤"},
    "pas":      {"isim": "Pas Becerisi",      "max": 60, "emoji": "📐"},
}

# =============================================================
# 2. BOT VE INTENTS TANIMLAMA
# =============================================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# =============================================================
# OWNER BYPASS — Owner tüm komutları, tüm yetki kontrollerini geçer
# =============================================================
_orig_has_permissions = commands.has_permissions

def _owner_bypass_has_permissions(**perms):
    orig = _orig_has_permissions(**perms)
    async def _pred(ctx: commands.Context) -> bool:
        if ctx.author.id == OWNER_ID:
            return True
        return await orig.predicate(ctx)
    return commands.check(_pred)

commands.has_permissions = _owner_bypass_has_permissions

# =============================================================
# 3. YARDIMCI FONKSİYONLAR (JSON, KULLANICI VERİSİ vb.)
# =============================================================
def veri_yukle(dosya_adi, varsayilan_deger={}):
    if not os.path.exists(dosya_adi):
        veri_kaydet(dosya_adi, varsayilan_deger)
        return varsayilan_deger
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, TypeError, FileNotFoundError):
        veri_kaydet(dosya_adi, varsayilan_deger)
        return varsayilan_deger

def veri_kaydet(dosya_adi, data):
    try:
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"HATA - {dosya_adi} kaydedilemedi: {e}")

antrenman_sayaci = veri_yukle(ANTRENMAN_DOSYA, {})

def get_user_para_data(user_id):
    data = veri_yukle(PARA_DOSYA)
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"cash": 0, "bank": 0}
    return data, data[user_id]

def stat_oku():
    return veri_yukle(STAT_DOSYA, {})

def stat_yaz(data):
    veri_kaydet(STAT_DOSYA, data)

def stat_ekle(uid: str, key: str, miktar: int = 1):
    data = stat_oku()
    uid = str(uid)
    if uid not in data:
        data[uid] = {}
    data[uid][key] = data[uid].get(key, 0) + miktar
    stat_yaz(data)

def nt_oku():
    return veri_yukle(NITELIK_DOSYA, {})

def nt_yaz(data):
    veri_kaydet(NITELIK_DOSYA, data)

def ant_oku(dosya):
    return veri_yukle(dosya, {})

def ant_yaz(dosya, data):
    veri_kaydet(dosya, data)

def ant_embed_devam(oyuncu: discord.Member, mevcut: int, limit: int, tip: str) -> discord.Embed:
    emoji  = "🥈" if tip == "gumus" else "🥇"
    renk   = 0xc0c0c0 if tip == "gumus" else 0xf1c40f
    baslik = "Gümüş Antrenman" if tip == "gumus" else "Altın Antrenman"
    dolu   = round((mevcut / limit) * 20)
    bar    = "█" * dolu + "░" * (20 - dolu)
    embed  = discord.Embed(color=renk)
    embed.set_author(name=f"{emoji} {baslik}", icon_url=oyuncu.display_avatar.url)
    embed.description = (
        f"**{oyuncu.display_name}** antrenman yapıyor!\n"
        f"{'─'*30}\n"
        f"`{bar}` **{mevcut}/{limit}**\n"
        f"{'─'*30}\n"
        f"⏱️ Bir sonraki antrenman için **1 saat** bekle."
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • {baslik}  •  {datetime.now().strftime('%H:%M')}")
    return embed

def ant_embed_limit(oyuncu: discord.Member, limit: int, tip: str) -> discord.Embed:
    emoji  = "🥈" if tip == "gumus" else "🥇"
    renk   = 0xc0c0c0 if tip == "gumus" else 0xf1c40f
    baslik = "Gümüş Antrenman" if tip == "gumus" else "Altın Antrenman"
    embed  = discord.Embed(color=renk)
    embed.set_author(name=f"{emoji} Limit Doldu!", icon_url=oyuncu.display_avatar.url)
    embed.description = (
        f"{oyuncu.mention} **{limit}/{limit}** limitine ulaştı!\n"
        f"{'─'*30}\n"
        f"✅ {baslik} tamamlandı. Artık daha fazla antrenman yapamazsın."
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • {baslik}  •  {datetime.now().strftime('%H:%M')}")
    return embed

# --- BİLGİ YARIŞMASI ---
QUIZ_SKOR_DOSYA = "quiz_skor.json"
QUIZ_SURE       = 180   # toplam 3 dakika
IPUCU_SURE      = 90    # 1.5 dakika sonra ipucu

ZORLUK_EMOJI = {
    "çok kolay": "🟢",
    "kolay":     "🔵",
    "orta":      "🟡",
    "zor":       "🔴",
    "çok zor":   "⚫",
}

current_question: dict = {}
quiz_message: Optional[discord.Message] = None
_quiz_timer_task: Optional[asyncio.Task] = None
quiz_lock = asyncio.Lock()

def normalize_cevap(text: str) -> str:
    text = text.lower().strip()
    return text.translate(str.maketrans("şğüöıç", "sguoic"))

def quiz_embed_aktif(soru: dict) -> discord.Embed:
    zorluk = soru.get("difficulty", "orta")
    emoji  = ZORLUK_EMOJI.get(zorluk, "🟡")
    embed  = discord.Embed(color=CL_MAVI)
    embed.set_author(name=f"🧠 {SUNUCU_ADI} — Bilgi Yarışması!")
    embed.description = f"## ❓ {soru['question']}"
    embed.add_field(name="⚡ Zorluk",  value=f"{emoji} {zorluk.capitalize()}", inline=True)
    embed.add_field(name="💰 Ödül",   value=f"**{soru['points']}M€** değer",  inline=True)
    embed.add_field(name="⏱️ Süre",   value="**3 dakika**",                    inline=True)
    embed.add_field(name="📝 Katılım", value="Cevabını bu kanala yaz!", inline=False)
    embed.set_footer(text=f"⚡ {SUNUCU_ADI} • Bilgi Yarışması  •  {datetime.now().strftime('%H:%M')}")
    return embed

def quiz_embed_kapandi(soru: dict, kazanan: Optional[discord.Member] = None) -> discord.Embed:
    if kazanan:
        embed = discord.Embed(color=CL_YESIL)
        embed.set_author(name=f"🎉 {kazanan.display_name} Doğru Bildi!", icon_url=kazanan.display_avatar.url)
        embed.description = (
            f"{kazanan.mention} soruyu doğru cevapladı!\n"
            f"{'━'*28}\n"
            f"✅ **Cevap:** {soru['answer']}\n"
            f"💰 **Ödül:** {soru['points']}M€ değer"
        )
    else:
        embed = discord.Embed(color=CL_KIRMIZI)
        embed.set_author(name="⏱️ Süre Doldu!")
        embed.description = (
            f"Kimse bilemedi!\n"
            f"{'━'*28}\n"
            f"✅ **Doğru cevap:** {soru['answer']}"
        )
    embed.set_footer(text=f"⚡ {SUNUCU_ADI} • Bilgi Yarışması  •  {datetime.now().strftime('%H:%M')}")
    return embed

async def _quiz_timer(channel: discord.TextChannel):
    global current_question, quiz_message
    try:
        await asyncio.sleep(IPUCU_SURE)
        if current_question:
            hint = current_question.get("hint", "")
            if hint:
                ipucu = discord.Embed(color=0xe67e22)
                ipucu.set_author(name="💡 İpucu!")
                ipucu.description = f"**{hint}**\n\n⏳ 1.5 dakika kaldı!"
                ipucu.set_footer(text=f"{SUNUCU_ADI} • Bilgi Yarışması")
                await channel.send(embed=ipucu)

        await asyncio.sleep(QUIZ_SURE - IPUCU_SURE)

        soru = None
        async with quiz_lock:
            if current_question:
                soru = current_question.copy()
                current_question.clear()

        if soru:
            await channel.send(embed=quiz_embed_kapandi(soru, kazanan=None))
            if quiz_message:
                try:
                    await quiz_message.edit(embed=quiz_embed_kapandi(soru))
                except Exception:
                    pass
    except asyncio.CancelledError:
        pass

async def post_soru(channel: discord.TextChannel) -> bool:
    global current_question, quiz_message, _quiz_timer_task
    async with quiz_lock:
        if current_question:
            return False
        with open('questions.json', 'r', encoding='utf-8') as f:
            sorular = json.load(f)
        soru = random.choice(sorular)
        current_question = soru

    quiz_message = await channel.send(embed=quiz_embed_aktif(soru))
    if _quiz_timer_task and not _quiz_timer_task.done():
        _quiz_timer_task.cancel()
    _quiz_timer_task = asyncio.create_task(_quiz_timer(channel))
    return True

async def ask_question_loop():
    """Arka planda periyodik olarak soru soran döngü."""
    await bot.wait_until_ready()
    quiz_channel = bot.get_channel(quiz_channel_id)
    if not quiz_channel:
        print(f"HATA: Bilgi Yarışması kanalı (ID: {quiz_channel_id}) bulunamadı.")
        return
    while not bot.is_closed():
        wait_time = random.randint(2 * 1200, 5 * 1200)
        await asyncio.sleep(wait_time)
        await post_soru(quiz_channel)

# =============================================================
# 4. EVENTLER (on_ready, on_member_join vb.)
# =============================================================
@bot.event
async def on_ready():
    if not self_ping.is_running():
        self_ping.start()
    print(f"✅ {bot.user} AKTİF! {SUNUCU_ADI} Sistemi Hazır.")

CL_MAVI   = 0x00b4d8   # Crystal League ana rengi
CL_YESIL  = 0x00d47a
CL_KIRMIZI= 0xff4757
CL_ALTIN  = 0xffd700

def _zaman():
    return datetime.now().strftime('%d.%m.%Y %H:%M')

def embed_hata(baslik: str, aciklama: str) -> discord.Embed:
    e = discord.Embed(color=CL_KIRMIZI)
    e.set_author(name=f"❌  {baslik}")
    e.description = aciklama
    e.set_footer(text=f"⚡ {SUNUCU_ADI}  •  {_zaman()}")
    return e

def embed_basari(baslik: str, aciklama: str) -> discord.Embed:
    e = discord.Embed(color=CL_YESIL)
    e.set_author(name=f"✅  {baslik}")
    e.description = aciklama
    e.set_footer(text=f"⚡ {SUNUCU_ADI}  •  {_zaman()}")
    return e

def embed_bilgi(baslik: str, renk: int = CL_MAVI) -> discord.Embed:
    e = discord.Embed(title=baslik, color=renk)
    e.set_footer(text=f"⚡ {SUNUCU_ADI}  •  {_zaman()}")
    return e

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        kullanilan = ctx.message.content.split()[0][1:]
        embed = discord.Embed(color=CL_KIRMIZI)
        embed.set_author(name=f"💎 {SUNUCU_ADI} — Bilinmeyen Komut", icon_url=ctx.guild.icon.url if ctx.guild and ctx.guild.icon else None)
        embed.description = f"**`.{kullanilan}`** diye bir komut yok.\n`.yardım` yazarak komut listesine bakabilirsin."
        embed.set_footer(text=f"⚡ {SUNUCU_ADI}  •  {_zaman()}")
        await ctx.send(embed=embed, delete_after=8)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=embed_hata("Yetersiz Yetki", "Bu komutu kullanmak için yetkin yok!"), delete_after=8)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embed_hata("Eksik Argüman", f"Komutu doğru kullan:\n`.{ctx.command.name} {ctx.command.signature}`"), delete_after=8)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=embed_hata("Bekleme Süresi", f"Bu komutu tekrar kullanmak için **{error.retry_after:.0f} saniye** bekle!"), delete_after=8)
    else:
        print(f"Bir hata oluştu: {error}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(KAYIT_KANAL_ID)
    if not channel or not isinstance(channel, discord.TextChannel):
        return

    simdi = datetime.now(timezone.utc)
    hesap_yasi = (simdi - member.created_at).days

    if hesap_yasi >= 30: guvenlik = "🟢 Güvenilir"
    elif hesap_yasi >= 7: guvenlik = "🟡 Şüpheli"
    else: guvenlik = "🔴 Yeni Hesap"

    embed = discord.Embed(color=CL_MAVI)
    embed.set_author(
        name=f"💎 {SUNUCU_ADI} — Yeni Oyuncu",
        icon_url=member.guild.icon.url if member.guild.icon else None
    )
    embed.description = (
        f"## 🎉 Aramıza hoş geldin, {member.mention}!\n"
        f"{'━' * 30}\n"
        f"Sunucumuzun **{member.guild.member_count}.** üyesi oldun."
    )
    embed.add_field(name="👤 Kullanıcı", value=f"`{member.name}`", inline=True)
    embed.add_field(name="🆔 ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="🛡️ Güvenlik", value=guvenlik, inline=True)
    embed.add_field(name="📅 Hesap Oluşturma", value=member.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="⏳ Hesap Yaşı", value=f"**{hesap_yasi}** gün", inline=True)
    embed.add_field(name="📋 Durum", value="```\nKayıt Bekliyor...\n```", inline=False)
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"⚡ {SUNUCU_ADI} • Kayıt Sistemi  •  {simdi.strftime('%d.%m.%Y %H:%M')}")

    await channel.send(content=f"🚨 <@&{KAYIT_YETKILI_ROL_ID}> yeni kayıt!", embed=embed)
    
@bot.event
async def on_message(message):
    """Kanala gönderilen her mesajı kontrol eder."""
    global current_question
    if message.author.bot or not message.guild:
        await bot.process_commands(message)
        return

    soru_kazanildi = None
    kazanan = None
    async with quiz_lock:
        if current_question and message.channel.id == quiz_channel_id:
            if normalize_cevap(message.content) == normalize_cevap(current_question['answer']):
                soru_kazanildi = current_question.copy()
                kazanan = message.author
                current_question.clear()

    if soru_kazanildi and kazanan:
        if _quiz_timer_task and not _quiz_timer_task.done():
            _quiz_timer_task.cancel()
        skor_data = veri_yukle(QUIZ_SKOR_DOSYA, {})
        uid = str(kazanan.id)
        if uid not in skor_data:
            skor_data[uid] = {"dogru": 0, "isim": kazanan.display_name}
        skor_data[uid]["dogru"] += 1
        skor_data[uid]["isim"] = kazanan.display_name
        veri_kaydet(QUIZ_SKOR_DOSYA, skor_data)
        await message.channel.send(embed=quiz_embed_kapandi(soru_kazanildi, kazanan=kazanan))
        if quiz_message:
            try:
                await quiz_message.edit(embed=quiz_embed_kapandi(soru_kazanildi, kazanan=kazanan))
            except Exception:
                pass

    await bot.process_commands(message)   
# =============================================================
# 5. DEĞER SİSTEMİ (GELİŞMİŞ TASARIM)
# =============================================================
def parse_deger(deger_str):
    return float(deger_str.upper().replace('M', '').replace('€', '').replace(',', '.').strip())

def deger_bar(deger: float) -> str:
    """0–350M aralığında görsel bir ilerleme çubuğu oluşturur."""
    filled = min(int(deger * 20 / 350), 20)
    empty = 20 - filled
    return "█" * filled + "░" * empty

def deger_tier(deger: float) -> tuple[str, int]:
    """Değere göre seviye etiketi ve renk döndürür."""
    if deger >= 150:
        return ("👑 Efsane", 0xffd700)
    elif deger >= 100:
        return ("💎 Dünya Yıldızı", 0x00cfff)
    elif deger >= 70:
        return ("🔥 Elit", 0xff6b35)
    elif deger >= 40:
        return ("⚡ Yükselen", 0x7c3aed)
    elif deger >= 20:
        return ("🌱 Umut Vadeden", 0x2ecc71)
    else:
        return ("📋 Sıradan", 0x95a5a6)

async def deger_guncelle(ctx, m, miktar, sebep, islem):
    izinli_roller = [DEGER_YETKILISI_ROL_ID, YETKILI_1_ID]
    sahip_mi = (
        ctx.author.id == OWNER_ID or
        (isinstance(ctx.author, discord.Member) and
         any(ctx.author.get_role(r) for r in izinli_roller))
    )
    if not sahip_mi:
        return await ctx.send("❌ Bu komutu kullanmak için **Değer Yetkilisi** rolüne ihtiyacın var!")
    try:
        val = parse_deger(miktar)
        parcalar = m.display_name.split(" | ")
        if len(parcalar) < 4:
            return await ctx.send(
                embed=discord.Embed(
                    title="❌ Format Hatası",
                    description="Oyuncunun nick formatı hatalı!\n\n**Doğru format:**\n`İsim | Mevki | Takım | 0M€`",
                    color=0xe74c3c
                )
            )
        isim, mevki, takim, deger = parcalar[0].strip(), parcalar[1].strip(), parcalar[2].strip(), parcalar[3].strip()
        eski = parse_deger(deger)
        # Takımı nickten değil, oyuncunun rollerinden çek
        rol_takim = next((TAKIM_ROLLERI[r.id] for r in m.roles if r.id in TAKIM_ROLLERI), takim)

        if islem == "artir":
            yeni = eski + val
            renk = 0x00d084
            yön_emoji = "📈"
            yön_text = f"+{val:g}M€"
            baslik = "📈 PİYASA DEĞERİ ARTIRILDI"
            banner_renk = "🟢"
        else:
            yeni = max(0, eski - val)
            renk = 0xff4444
            yön_emoji = "📉"
            yön_text = f"-{val:g}M€"
            baslik = "📉 PİYASA DEĞERİ DÜŞÜRÜLDÜ"
            banner_renk = "🔴"

        await m.edit(nick=f"{isim} | {mevki} | {takim} | {yeni:g}M€")

        tier_label, tier_color = deger_tier(yeni)
        bar = deger_bar(yeni)
        zaman = datetime.now(timezone.utc).strftime('%d/%m/%Y • %H:%M')

        embed = discord.Embed(color=renk)
        embed.set_author(
            name=f"{SUNUCU_ADI} | Piyasa Değeri",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else None
        )

        embed.description = (
            f"## {baslik}\n"
            f"{'─' * 32}\n"
            f"**{m.mention}** adlı oyuncunun piyasa değeri güncellendi. {banner_renk}"
        )

        embed.add_field(
            name="👤 Oyuncu Bilgileri",
            value=(
                f"```\n"
                f"Ad     : {isim}\n"
                f"Mevki  : {mevki}\n"
                f"Takım  : {rol_takim}\n"
                f"```"
            ),
            inline=False
        )

        embed.add_field(
            name="💰 Değer Değişimi",
            value=(
                f"**Eski:** `{eski:g}M€`\n"
                f"**Yeni:** `{yeni:g}M€`\n"
                f"**Fark:** `{yön_text}`"
            ),
            inline=True
        )

        embed.add_field(
            name=f"🏅 Seviye",
            value=f"{tier_label}\n`{yeni:g}M€`",
            inline=True
        )

        embed.add_field(
            name=f"📊 Değer Göstergesi (0–350M€)",
            value=f"`{bar}` **{yeni:g}M€**",
            inline=False
        )

        embed.add_field(
            name="📝 Güncelleme Sebebi",
            value=f"*{sebep}*",
            inline=False
        )

        embed.set_thumbnail(url=m.display_avatar.url)
        embed.set_footer(
            text=f"Yetkili: {ctx.author.display_name}  •  {zaman}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)
        log = bot.get_channel(DEGER_LOG)
        if log:
            await log.send(embed=embed)

    except Exception as ex:
        print(ex)
        await ctx.send(
            embed=discord.Embed(
                title="❌ Komut Hatası",
                description="**Doğru kullanım:**\n`.değerver @üye 2M sebep`\n`.değersil @üye 2M sebep`",
                color=0xe74c3c
            )
        )

@bot.command(name='değerver')
async def deger_ver(ctx, m: discord.Member, miktar: str, *, sebep: str = "Belirtilmedi"):
    await deger_guncelle(ctx, m, miktar, sebep, "artir")

@bot.command(name='değersil')
async def deger_sil(ctx, m: discord.Member, miktar: str, *, sebep: str = "Belirtilmedi"):
    await deger_guncelle(ctx, m, miktar, sebep, "azalt")

@bot.command(name="endeğerli", aliases=["topoyuncu"])
async def en_degerli_listesi(ctx):
    oyuncular = []
    for uye in ctx.guild.members:
        if uye.bot or len(parcalar := uye.display_name.split(" | ")) < 4:
            continue
        try:
            deger = float(parcalar[3].upper().replace("M", "").replace("€", "").replace(",", ".").strip())
            oyuncular.append({
                "uye": uye,
                "isim": parcalar[0].strip(),
                "mevki": parcalar[1].strip(),
                "takim": parcalar[2].strip(),
                "deger": deger
            })
        except:
            continue

    if not oyuncular:
        return await ctx.send(
            embed=discord.Embed(
                title="❌ Oyuncu Bulunamadı",
                description="Değer bilgisi bulunan oyuncu yok.",
                color=0xe74c3c
            )
        )

    oyuncular.sort(key=lambda x: x["deger"], reverse=True)
    toplam_deger = sum(o["deger"] for o in oyuncular)
    ortalama = round(toplam_deger / len(oyuncular), 1)
    en_yuksek = oyuncular[0]["deger"]

    embed = discord.Embed(
        title="🏆 EN DEĞERLİ OYUNCULAR",
        color=0xffd700
    )
    if ctx.guild.icon:
        embed.set_author(name=f"{SUNUCU_ADI} | Piyasa Sıralaması", icon_url=ctx.guild.icon.url)

    siralama_emojiler = {1: "🥇", 2: "🥈", 3: "🥉"}
    yazi = ""
    for i, oyuncu in enumerate(oyuncular[:10], start=1):
        sira = siralama_emojiler.get(i, f"`{i:02d}`")
        tier_label, _ = deger_tier(oyuncu["deger"])
        yazi += (
            f"{sira} **{oyuncu['isim']}** — {oyuncu['uye'].mention}\n"
            f"┣ ⚽ `{oyuncu['mevki']}` • 🏟️ `{oyuncu['takim']}`\n"
            f"┗ 💰 **{oyuncu['deger']:g}M€**  {tier_label}\n\n"
        )

    embed.description = yazi

    embed.add_field(name="👥 Toplam Oyuncu", value=f"**{len(oyuncular)}**", inline=True)
    embed.add_field(name="📊 Lig Ortalaması", value=f"**{ortalama}M€**", inline=True)
    embed.add_field(name="💸 Toplam Piyasa", value=f"**{toplam_deger:g}M€**", inline=True)
    embed.add_field(
        name="📈 Piyasa Durumu",
        value=f"`{deger_bar(min(en_yuksek, 350))}` {en_yuksek:g}M€",
        inline=False
    )

    embed.set_footer(text=f"Sorgulayan: {ctx.author.display_name}  •  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    await ctx.send(embed=embed)

def oyuncu_listesi_olustur(guild):
    oyuncular = []
    for uye in guild.members:
        if uye.bot or len(parcalar := uye.display_name.split(" | ")) < 4:
            continue
        try:
            deger = float(parcalar[3].upper().replace("M", "").replace("€", "").replace(",", ".").strip())
            oyuncular.append({
                "uye": uye,
                "isim": parcalar[0].strip(),
                "mevki": parcalar[1].strip(),
                "takim": parcalar[2].strip(),
                "deger": deger
            })
        except:
            continue
    return oyuncular

@bot.command(name="endeğerliler", aliases=["topoyuncular"])
async def en_degerli_listesi2(ctx):
    oyuncular = oyuncu_listesi_olustur(ctx.guild)
    if not oyuncular:
        return await ctx.send(embed=discord.Embed(title="❌ Oyuncu Bulunamadı", description="Değer bilgisi bulunan oyuncu yok.", color=0xe74c3c))

    oyuncular.sort(key=lambda x: x["deger"], reverse=True)
    toplam_deger = sum(o["deger"] for o in oyuncular)
    ortalama = round(toplam_deger / len(oyuncular), 1)
    en_yuksek = oyuncular[0]["deger"]

    siralama_emojiler = {1: "🥇", 2: "🥈", 3: "🥉"}
    yazi = ""
    for i, oyuncu in enumerate(oyuncular[:10], start=1):
        sira = siralama_emojiler.get(i, f"`#{i}`")
        tier_label, _ = deger_tier(oyuncu["deger"])
        bar = "█" * min(int(oyuncu["deger"] / 10), 10) + "░" * (10 - min(int(oyuncu["deger"] / 10), 10))
        yazi += (
            f"{sira} **{oyuncu['isim']}**\n"
            f"┣ ⚽ `{oyuncu['mevki']}` • 🏟️ `{oyuncu['takim']}`\n"
            f"┣ 💰 **{oyuncu['deger']:g}M€** {tier_label}\n"
            f"┗ `{bar}`\n\n"
        )

    embed = discord.Embed(title="👑 EN DEĞERLİ OYUNCULAR", description=yazi, color=0xffd700)
    if ctx.guild.icon:
        embed.set_author(name=f"{SUNUCU_ADI} | Piyasa Sıralaması", icon_url=ctx.guild.icon.url)
    embed.add_field(name="👥 Toplam Oyuncu", value=f"**{len(oyuncular)}**", inline=True)
    embed.add_field(name="📊 Lig Ortalaması", value=f"**{ortalama}M€**", inline=True)
    embed.add_field(name="💸 Toplam Piyasa", value=f"**{toplam_deger:g}M€**", inline=True)
    embed.set_footer(text=f"Sorgulayan: {ctx.author.display_name}  •  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    await ctx.send(embed=embed)

@bot.command(name="takımdeğer", aliases=["takimsiralama", "takımsıralama", "takimdeğer"])
async def takim_deger_sirala(ctx):
    oyuncular = oyuncu_listesi_olustur(ctx.guild)
    if not oyuncular:
        return await ctx.send(embed=discord.Embed(title="❌ Oyuncu Bulunamadı", description="Değer bilgisi bulunan oyuncu yok.", color=0xe74c3c))

    takimlar = {}
    for o in oyuncular:
        t = o["takim"]
        if t not in takimlar:
            takimlar[t] = {"toplam": 0, "oyuncular": [], "en_degerli": 0}
        takimlar[t]["toplam"] += o["deger"]
        takimlar[t]["oyuncular"].append(o)
        if o["deger"] > takimlar[t]["en_degerli"]:
            takimlar[t]["en_degerli"] = o["deger"]
            takimlar[t]["en_degerli_isim"] = o["isim"]

    siralanmis = sorted(takimlar.items(), key=lambda x: x[1]["toplam"], reverse=True)
    toplam_piyasa = sum(t["toplam"] for _, t in siralanmis)

    siralama_emojiler = {1: "🥇", 2: "🥈", 3: "🥉"}
    yazi = ""
    for i, (takim_adi, bilgi) in enumerate(siralanmis, start=1):
        sira = siralama_emojiler.get(i, f"`#{i}`")
        oyuncu_sayisi = len(bilgi["oyuncular"])
        ortalama = round(bilgi["toplam"] / oyuncu_sayisi, 1)
        bar = "█" * min(int(bilgi["toplam"] / 50), 10) + "░" * (10 - min(int(bilgi["toplam"] / 50), 10))
        yulduz = bilgi.get("en_degerli_isim", "?")
        yazi += (
            f"{sira} **{takim_adi}**\n"
            f"┣ 💰 Toplam: **{bilgi['toplam']:g}M€** • Ort: **{ortalama}M€**\n"
            f"┣ 👥 {oyuncu_sayisi} oyuncu • ⭐ {yulduz}\n"
            f"┗ `{bar}`\n\n"
        )

    embed = discord.Embed(title="🏆 TAKIM DEĞER SIRALAMASI", description=yazi, color=0x7c3aed)
    if ctx.guild.icon:
        embed.set_author(name=f"{SUNUCU_ADI} | Takım Piyasası", icon_url=ctx.guild.icon.url)
    embed.add_field(name="🏟️ Toplam Takım", value=f"**{len(siralanmis)}**", inline=True)
    embed.add_field(name="👥 Toplam Oyuncu", value=f"**{len(oyuncular)}**", inline=True)
    embed.add_field(name="💸 Toplam Piyasa", value=f"**{toplam_piyasa:g}M€**", inline=True)
    embed.set_footer(text=f"Sorgulayan: {ctx.author.display_name}  •  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    await ctx.send(embed=embed)

# =============================================================
# 6. GERİ YÜKLENEN TÜM ESKİ KOMUTLAR
# =============================================================
@bot.command(name='ara')
async def oyuncu_ara(ctx, *, aranan_kelime: str):
    """Sunucudaki üyeleri takma adlarına göre arar ve sonuçları listeler."""
    aranan_kelime = aranan_kelime.lower()
    bulunan_uyeler = []
    for uye in ctx.guild.members:
        if aranan_kelime in uye.display_name.lower():
            bulunan_uyeler.append(uye)
    embed = discord.Embed(title="Oyuncu Arama Sonucu", color=discord.Color.from_rgb(113, 107, 224))
    if not bulunan_uyeler:
        embed.description = f"`{aranan_kelime}` ile eşleşen bir oyuncu bulunamadı."
    else:
        aciklama = ""
        for i, uye in enumerate(bulunan_uyeler, 1):
            aciklama += f"{i}. {uye.mention}\n"
        embed.description = aciklama
        embed.add_field(name="Aranan", value=f"`{aranan_kelime}`", inline=True)
        embed.add_field(name="Bulunan", value=f"`{len(bulunan_uyeler)}`", inline=True)
    zaman_damgasi = datetime.now().strftime("bugün saat %H:%M")
    embed.set_footer(text=f"Toplam {len(bulunan_uyeler)} kişi bulundu • {zaman_damgasi}")
    await ctx.send(embed=embed)

# --- GENEL KOMUTLAR ---
@bot.command(name="şart")
async def sart_mesaji(ctx):
    rol_al_kanali_id = 1509959514122747995
    embed = discord.Embed(
        title="📢 Katılım Şartları",
        description=f"Lige katılabilmek veya devam edebilmek için lütfen <#{rol_al_kanali_id}> kanalından en az **1 adet rol** alınız.",
        color=discord.Color.blue(),
        timestamp=datetime.now(timezone.utc)
    )
    embed.add_field(name="📌 Önemli Not", value="İşlemleri tamamladıktan sonra yetkililere bilgi veriniz, size yardımcı olacaklardır.", inline=False)
    embed.set_footer(text=f"{SUNUCU_ADI} Kayıt Sistemi")
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Rol Al Kanalına Git", url=f"https://discord.com/channels/{ctx.guild.id}/{rol_al_kanali_id}", style=discord.ButtonStyle.link))
    await ctx.send(embed=embed, view=view)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    e = discord.Embed(color=CL_MAVI)
    e.set_author(name=f"💎 {SUNUCU_ADI} — Bot Durumu", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    e.description = f"🏓 **Pong!** Bot aktif ve çalışıyor.\n\n⚡ **Gecikme:** `{latency}ms`"
    e.set_footer(text=f"⚡ {SUNUCU_ADI}  •  {_zaman()}")
    await ctx.send(embed=e)

@bot.command(name="idler")
async def idler(ctx):
    """Owner için: sunucudaki tüm kanal ve rollerin ID'lerini listeler."""
    if ctx.author.id != OWNER_ID:
        return
    guild = ctx.guild
    if not guild:
        return

    # KANALLAR
    kanal_satirlar = []
    for ch in sorted(guild.channels, key=lambda c: (str(type(c).__name__), c.name)):
        if isinstance(ch, discord.CategoryChannel):
            kanal_satirlar.append(f"📁 **[KATEGORİ]** {ch.name} → `{ch.id}`")
        elif isinstance(ch, discord.TextChannel):
            kanal_satirlar.append(f"💬 #{ch.name} → `{ch.id}`")
        elif isinstance(ch, discord.VoiceChannel):
            kanal_satirlar.append(f"🔊 {ch.name} → `{ch.id}`")

    # ROLLER
    rol_satirlar = []
    for rol in sorted(guild.roles[1:], key=lambda r: -r.position):  # @everyone hariç
        rol_satirlar.append(f"🏅 @{rol.name} → `{rol.id}`")

    # Kanalları böl (Discord 4096 karakter limiti)
    def bolum_gonder(satirlar, baslik):
        parcalar = []
        parca = ""
        for s in satirlar:
            if len(parca) + len(s) + 1 > 3900:
                parcalar.append(parca)
                parca = s + "\n"
            else:
                parca += s + "\n"
        if parca:
            parcalar.append(parca)
        return [(baslik if i == 0 else f"{baslik} (devam {i+1})", p) for i, p in enumerate(parcalar)]

    embeds = []
    for baslik, icerik in bolum_gonder(kanal_satirlar, "📡 KANALLAR"):
        e = discord.Embed(title=baslik, description=icerik, color=CL_MAVI)
        embeds.append(e)
    for baslik, icerik in bolum_gonder(rol_satirlar, "🏅 ROLLER"):
        e = discord.Embed(title=baslik, description=icerik, color=CL_ALTIN)
        embeds.append(e)

    for e in embeds:
        e.set_footer(text=f"⚡ {guild.name}  •  {_zaman()}")
        await ctx.author.send(embed=e)

    await ctx.send("📬 ID listesi DM'ine gönderildi!", delete_after=5)
    try:
        await ctx.message.delete()
    except Exception:
        pass

# --- EĞLENCE KOMUTLARI ---
@bot.command(name='duello')
async def penalti_duellosu(ctx, rakip: discord.Member = None):
    koseler = ["sol", "orta", "sağ"]
    if rakip is None: # AI MOD
        await ctx.send(f"🏟️ {ctx.author.mention} vs 🧤 **KALECİ (AI)**\nİlk **5 gol** atan kazanır!")
        skor = {ctx.author: 0, "kaleci": 0}
        while skor[ctx.author] < 5 and skor["kaleci"] < 5:
            await ctx.send("🎯 Köşe seç: `sol / orta / sağ`")
            try:
                msg = await bot.wait_for('message', timeout=10, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                secim = msg.content.lower()
                if secim not in koseler: secim = random.choice(koseler)
            except asyncio.TimeoutError:
                secim = random.choice(koseler)
            kaleci = random.choice(koseler)
            await asyncio.sleep(1)
            if secim == kaleci:
                sonuc = "🧤 KALECİ KURTARDI!"; skor["kaleci"] += 1
            else:
                sonuc = "⚽ GOOOOOL!"; skor[ctx.author] += 1
            e = discord.Embed(description=f"{sonuc}\n\n👉 Sen: **{secim}** | Kaleci: **{kaleci}**\n📊 Skor: **{skor[ctx.author]} - {skor['kaleci']}**", color=0x3498db)
            await ctx.send(embed=e)
        kazanan_text = ctx.author.mention if skor[ctx.author] >= 5 else "🧤 KALECİ"
        await ctx.send(embed=discord.Embed(title="🏆 DÜELLO BİTTİ", description=f"🥇 Kazanan: {kazanan_text}", color=0x2ecc71))
        return
    if rakip == ctx.author: return await ctx.send("❓ Kendinle oynayamazsın!")
    await ctx.send(f"🏟️ {ctx.author.mention} vs {rakip.mention}\nİlk **5 gol** atan kazanır!")
    skor = {ctx.author: 0, rakip: 0}; siradaki = ctx.author
    while skor[ctx.author] < 5 and skor[rakip] < 5:
        await ctx.send(f"🎯 {siradaki.mention} şut atıyor! `sol / orta / sağ`")
        try:
            msg = await bot.wait_for('message', timeout=10, check=lambda m: m.author == siradaki and m.channel == ctx.channel)
            secim = msg.content.lower()
            if secim not in koseler: secim = random.choice(koseler)
        except asyncio.TimeoutError:
            secim = random.choice(koseler)
        kaleci = random.choice(koseler)
        await asyncio.sleep(1)
        if secim == kaleci: sonuc = "🧤 KALECİ KURTARDI!"
        else: sonuc = "⚽ GOOOOOL!"; skor[siradaki] += 1
        e = discord.Embed(description=f"{sonuc}\n\n👉 Şut: **{secim}** | Kaleci: **{kaleci}**\n📊 Skor: **{skor[ctx.author]} - {skor[rakip]}**", color=0x5865F2)
        await ctx.send(embed=e)
        siradaki = rakip if siradaki == ctx.author else ctx.author
    kazanan = ctx.author if skor[ctx.author] >= 5 else rakip
    await ctx.send(embed=discord.Embed(title="🏆 PENALTI DÜELLOSU BİTTİ", description=f"📊 Skor: **{skor[ctx.author]} - {skor[rakip]}**\n🥇 Kazanan: {kazanan.mention}", color=0x2ecc71))

@bot.command(name='yazıtura')
async def yazi_tura(ctx):
    mesaj = await ctx.send("🪙 Para havaya atılıyor...")
    animasyon = ["🪙", "💫", "🪙", "💫"]
    for a in animasyon:
        await asyncio.sleep(0.4)
        await mesaj.edit(content=a)
    sonuc = random.choice(["Yazı", "Tura"])
    e = discord.Embed(color=CL_ALTIN)
    e.set_author(name=f"🪙 {SUNUCU_ADI} — Yazı Tura", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    e.description = f"## {sonuc}"
    e.set_footer(text=f"{ctx.author.display_name}  •  {_zaman()}")
    await mesaj.edit(content=None, embed=e)

@bot.command(name='roll')
async def roll(ctx, *, secenekler: Optional[str] = None):
    if secenekler is None:
        sonuc = str(random.randint(1, 10))
    else:
        if "," in secenekler: liste = [s.strip() for s in secenekler.split(",")]
        else: liste = secenekler.split()
        if len(liste) == 2 and liste[0].isdigit() and liste[1].isdigit():
            sonuc = str(random.randint(int(liste[0]), int(liste[1])))
        else:
            sonuc = random.choice(liste)
    e = discord.Embed(color=CL_MAVI)
    e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    e.description = f"## 🎲 Roll Sonucu\n🎯  **{sonuc}**"
    e.set_footer(text=f"⚡ {SUNUCU_ADI}  •  {_zaman()}")
    await ctx.send(embed=e)

@bot.command(name='ship')
async def ship_olcer(ctx, kisi1: Optional[discord.Member] = None, kisi2: Optional[discord.Member] = None):
    if kisi1 is None or kisi2 is None: return await ctx.send("❓ **Kullanım:** `.ship @kişi1 @kişi2`")
    oran = random.randint(0, 100)
    bar = "❤️" * int(oran / 10) + "🖤" * (10 - int(oran / 10))
    if oran < 20: yorum = "💔 Arkadaş kalmanız daha hayırlı gibi..."
    elif oran < 50: yorum = "👀 Biraz zorlansa olur gibi ama emin değilim."
    elif oran < 80: yorum = "💖 Vay canına! Aranızda ciddi bir çekim var."
    else: yorum = "💍 Nikah memurunu çağırın! Bu iş bitmiş. 🔥"
    embed = discord.Embed(color=0xff4757)
    embed.set_author(name=f"💘 {SUNUCU_ADI} — Aşk Ölçer", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    embed.description = f"## {kisi1.mention} ❤️ {kisi2.mention}"
    embed.add_field(name=f"💝 Aşk Oranı: %{oran}", value=bar, inline=False)
    embed.add_field(name="💬 Yorum", value=yorum, inline=False)
    if kisi1.avatar: embed.set_thumbnail(url=kisi1.avatar.url)
    embed.set_footer(text=f"{ctx.author.display_name} tarafından eşleştirildi  •  {_zaman()}")
    await ctx.send(embed=embed)

@bot.command(name='kaçcm')
async def kaccm(ctx, üye: discord.Member = None):
    üye = üye or ctx.author
    boy = random.randint(1,31)
    notlar = ""
    if boy == 31: notlar = "\n\n😏 *Sayı manidar...*"
    elif boy <= 5: notlar = "\n\n🤏 *Üzülme, karakteri yeter...*"
    elif boy >= 15: notlar = "\n\n🚀 *Maşallah, bu ne hal!*"
    e = discord.Embed(title="📏 Boy Ölçümü Yapıldı!", description=f"{üye.mention} kişisinin ölçümleri tamamlandı.\n\n**Sonuç:** `{boy}cm`{notlar}", color=0xff00ff)
    e.set_footer(text="Bu sonuçlar bilimsel bir değer taşımamaktadır.")
    await ctx.send(embed=e)

@bot.command(name='halısaha')
async def halisaha(ctx, rakip: discord.Member = None):
    if not rakip or rakip == ctx.author: return await ctx.send("⚽ Rakip etiketle! (`.halısaha @kişi`)")
    oyuncular = ["Ronaldo", "Messi", "Neymar", "Mbappe", "Haaland", "Salah", "De Bruyne", "Vinicius", "Benzema", "Kane"]
    gol_olaylari = []
    skor1, skor2 = 0, 0
    mesaj = await ctx.send("🏟️ Maç başlıyor...")
    for dakika in range(1, 91, 10):
        await asyncio.sleep(1)
        if random.random() < 0.4:
            atan = random.choice([ctx.author, rakip])
            oyuncu = random.choice(oyuncular)
            if atan == ctx.author: skor1 += 1; gol_olaylari.append(f"{dakika}' ⚽ {oyuncu} ({ctx.author.display_name})")
            else: skor2 += 1; gol_olaylari.append(f"{dakika}' ⚽ {oyuncu} ({rakip.display_name})")
        if dakika == 45: await mesaj.edit(content=f"⏸️ İlk yarı bitti!\n📊 {ctx.author.display_name} {skor1} - {skor2} {rakip.display_name}")
    if skor1 > skor2: kazanan = ctx.author.mention; embed_renk = CL_YESIL
    elif skor2 > skor1: kazanan = rakip.mention; embed_renk = CL_KIRMIZI
    else: kazanan = "🤝 Berabere"; embed_renk = CL_MAVI
    embed = discord.Embed(color=embed_renk)
    embed.set_author(name=f"🏟️ {SUNUCU_ADI} — Halısaha Sonucu", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    embed.description = f"## 📊 {ctx.author.display_name}  {skor1} — {skor2}  {rakip.display_name}"
    embed.add_field(name="⚽ Goller", value="\n".join(gol_olaylari) if gol_olaylari else "Gol olmadı 😐", inline=False)
    embed.add_field(name="🏆 Sonuç", value=kazanan, inline=False)
    embed.set_footer(text=f"⚡ {SUNUCU_ADI} • Halısaha Sistemi  •  {_zaman()}")
    if ctx.author.avatar: embed.set_thumbnail(url=ctx.author.avatar.url)
    await mesaj.edit(content="✅ Maç bitti!")
    await ctx.send(embed=embed)

class PenaltiV(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=20)
        self.ctx = ctx
        self.used = False
    async def sonuc(self, interaction, yon):
        if interaction.user.id != self.ctx.author.id or self.used: return
        self.used = True; self.clear_items()
        ihtimal = random.choices(["Gol", "Kaleci", "Aut", "Direk"], weights=[40, 30, 20, 10], k=1)[0]
        stat_ekle(str(self.ctx.author.id), 'penalti_atilan')
        if ihtimal == "Gol":
            stat_ekle(str(self.ctx.author.id), 'penalti_gol')
            baslik, renk, mesaj, gif = "⚽ GOOOOOL!", 0x2ecc71, f"**{yon} köşeye** mükemmel vuruş! Gol!", "https://media.tenor.com/3m8QvQ6qZQ0AAAAC/soccer-goal.gif"
        elif ihtimal == "Kaleci":
            baslik, renk, mesaj, gif = "🧤 KALECİ KURTARDI!", 0xe74c3c, f"Kaleci topu **{yon}** köşeden çıkardı!", "https://media.tenor.com/8J7f9K1gk9AAAAAC/goalkeeper-save.gif"
        elif ihtimal == "Aut":
            baslik, renk, mesaj, gif = "🏟️ AUT!", 0x95a5a6, f"Top çok farklı gitti! **{yon}** isabetsiz!", "https://media.tenor.com/6hQq9p2f9XAAAAAC/miss-shot.gif"
        else:
            baslik, renk, mesaj, gif = "💥 DİREK!", 0xf39c12, "İnanılmaz! Top direkten döndü!", "https://media.tenor.com/9pKx1d2fQ3MAAAAC/football-hit-post.gif"
        e = discord.Embed(title=baslik, description=f"## {mesaj}", color=renk)
        e.add_field(name="🎯 Vuruş", value=yon, inline=True).add_field(name="🥅 Sonuç", value=ihtimal, inline=True)
        e.set_image(url=gif).set_footer(text=f"{self.ctx.author.display_name} • Penaltı Sistemi")
        await interaction.response.edit_message(embed=e, view=self)
    @discord.ui.button(label="Sol", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def sol(self, interaction, button): await self.sonuc(interaction, "Sol")
    @discord.ui.button(label="Orta", style=discord.ButtonStyle.primary, emoji="↕️")
    async def orta(self, interaction, button): await self.sonuc(interaction, "Orta")
    @discord.ui.button(label="Sağ", style=discord.ButtonStyle.primary, emoji="➡️")
    async def sag(self, interaction, button): await self.sonuc(interaction, "Sağ")

@bot.command(name='penaltı')
async def penalti(ctx):
    e = discord.Embed(color=CL_MAVI)
    e.set_author(name=f"💎 {SUNUCU_ADI} — Penaltı Noktası", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    e.description = "## 🥅 Kaleci hazır!\nKöşeni seç ve şutunu çek!"
    e.set_footer(text=f"⏱️ 20 saniye içinde karar ver!  •  {ctx.author.display_name}")
    if ctx.author.avatar: e.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=e, view=PenaltiV(ctx))

@bot.command(name='çiz')
async def ciz(ctx):
    async with ctx.typing():
        buf = generate_figure()
        file = discord.File(buf, filename="figure.png")
        embed = discord.Embed(title="🎨 Oyuncu Analiz Grafiği", color=CL_MAVI)
        embed.set_image(url="attachment://figure.png")
        embed.set_footer(text=f"⚡ {SUNUCU_ADI} • {ctx.author.display_name}  •  {_zaman()}")
        await ctx.send(embed=embed, file=file)

# --- KAYIT VE KULLANICI İŞLEMLERİ ---
class KayitPaneli(discord.ui.View):
    def __init__(self, yetkili: discord.Member, uye: discord.Member, isim: str, panel_mesaji=None):
        super().__init__(timeout=60)
        self.yetkili     = yetkili
        self.uye         = uye
        self.isim        = isim
        self.panel_mesaji = panel_mesaji
        self.tamamlandi  = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.yetkili.id:
            await interaction.response.send_message(
                "❌ Bu paneli yalnızca kayıt yapan yetkili kullanabilir!", ephemeral=True
            )
            return False
        return True

    async def _kayit_yap(self, interaction: discord.Interaction, rol_id: int, rol_adi: str, rol_emoji: str):
        if self.tamamlandi:
            return
        self.tamamlandi = True
        self.clear_items()

        guild = interaction.guild
        kayitsiz_rolu = guild.get_role(KAYITSIZ_ROL_ID)
        hedef_rol     = guild.get_role(rol_id)

        try:
            await self.uye.edit(nick=self.isim)
            if kayitsiz_rolu and kayitsiz_rolu in self.uye.roles:
                await self.uye.remove_roles(kayitsiz_rolu)
            if hedef_rol:
                await self.uye.add_roles(hedef_rol)
        except discord.Forbidden:
            await interaction.response.edit_message(
                embed=embed_hata("Yetki Hatası", "Botun bu üyeyi düzenleme yetkisi yok!"), view=None
            )
            return

        hesap_yasi = (datetime.now(timezone.utc) - self.uye.created_at).days
        sonuc_embed = discord.Embed(color=CL_YESIL)
        sonuc_embed.set_author(
            name=f"💎 {SUNUCU_ADI} — Kayıt Tamamlandı",
            icon_url=guild.icon.url if guild.icon else None
        )
        sonuc_embed.description = (
            f"## ✅ {self.uye.mention} kayıt edildi!\n"
            f"{'━' * 30}\n"
            f"📛 **Nick:** {self.isim}\n"
            f"🏅 **Rol:** {rol_emoji} {rol_adi}\n"
            f"📅 **Hesap Yaşı:** {hesap_yasi} gün\n"
            f"👑 **Yetkili:** {self.yetkili.mention}"
        )
        sonuc_embed.set_thumbnail(url=self.uye.display_avatar.url)
        sonuc_embed.set_footer(text=f"⚡ {SUNUCU_ADI} • Kayıt Sistemi  •  {_zaman()}")

        await interaction.response.edit_message(embed=sonuc_embed, view=None)

        sohbet_kanal = guild.get_channel(SOHBET_KANAL_ID)
        if sohbet_kanal:
            duyuru = discord.Embed(color=CL_YESIL)
            duyuru.set_author(name=f"🎉 Yeni Üye — {SUNUCU_ADI}", icon_url=guild.icon.url if guild.icon else None)
            duyuru.description = (
                f"{self.uye.mention} aramıza katıldı! Hoş geldin!\n"
                f"{'━' * 28}\n"
                f"📛 **Nick:** {self.isim}\n"
                f"🏅 **Rol:** {rol_emoji} {rol_adi}"
            )
            duyuru.set_thumbnail(url=self.uye.display_avatar.url)
            duyuru.set_footer(text=f"⚡ {SUNUCU_ADI} • Kayıt Sistemi  •  {_zaman()}")
            await sohbet_kanal.send(content=f"🎉 {self.uye.mention}", embed=duyuru)

        log_kanal = guild.get_channel(LOG_KANAL_ID)
        if log_kanal and log_kanal != sohbet_kanal:
            await log_kanal.send(embed=sonuc_embed)

        stat_ekle(str(self.yetkili.id), 'kayit_yapildi')

    async def on_timeout(self):
        self.clear_items()
        if self.panel_mesaji and not self.tamamlandi:
            try:
                zaman_doldu = embed_hata("Kayıt Paneli Zaman Aşımı", "60 saniye içinde seçim yapılmadı. Tekrar dene.")
                await self.panel_mesaji.edit(embed=zaman_doldu, view=None)
            except Exception:
                pass

    @discord.ui.button(label="Futbolcu", style=discord.ButtonStyle.primary, emoji="⚽")
    async def futbolcu_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._kayit_yap(interaction, FUTBOLCU_ROL_ID, "Futbolcu", "⚽")

    @discord.ui.button(label="Teknik Direktör", style=discord.ButtonStyle.success, emoji="🎯")
    async def teknik_direktor_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._kayit_yap(interaction, TEKNIK_DIREKTOR_ROL_ID, "Teknik Direktör", "🎯")

    @discord.ui.button(label="Üye", style=discord.ButtonStyle.secondary, emoji="👤")
    async def uye_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._kayit_yap(interaction, ÜYE_ROL_ID, "Üye", "👤")


@bot.command(name="kayıt", aliases=["k"])
async def kayit(ctx, uye: discord.Member, *, isim: str):
    if not (ctx.author.id == OWNER_ID or ctx.author.guild_permissions.administrator or ctx.author.get_role(KAYIT_YETKILI_ROL_ID)):
        return await ctx.send(embed=embed_hata("Yetersiz Yetki", "Kayıt yetkine sahip değilsin!"), delete_after=5)

    hesap_yasi = (datetime.now(timezone.utc) - uye.created_at).days
    if hesap_yasi >= 30:
        guvenlik = "✅ Güvenilir"
    elif hesap_yasi >= 7:
        guvenlik = "🟡 Şüpheli"
    else:
        guvenlik = "🔴 Yeni Hesap"

    panel_embed = discord.Embed(color=CL_MAVI)
    panel_embed.set_author(
        name=f"💎 {SUNUCU_ADI} — Kayıt Paneli",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
    )
    panel_embed.description = "📋 Aşağıdan kayıt türünü seçiniz."
    panel_embed.add_field(name="👤 Kullanıcı", value=uye.mention, inline=False)
    panel_embed.add_field(name="📛 Nick",      value=f"`{isim}`",  inline=True)
    panel_embed.add_field(name="🛡️ Güvenlik",  value=guvenlik,     inline=True)
    if uye.avatar:
        panel_embed.set_thumbnail(url=uye.avatar.url)
    panel_embed.set_footer(text=f"60 saniye içinde seçim yapılmalıdır.  •  bugün saat {datetime.now().strftime('%H:%M')}")

    view = KayitPaneli(ctx.author, uye, isim)
    panel_mesaji = await ctx.send(embed=panel_embed, view=view)
    view.panel_mesaji = panel_mesaji

    try:
        await ctx.message.delete()
    except Exception:
        pass

@bot.command(name='kver')
@commands.has_permissions(manage_roles=True)
async def kayitsiz_ver(ctx, m: discord.Member):
    ks_rol = ctx.guild.get_role(KAYITSIZ_ROL_ID)
    if not ks_rol: return await ctx.send("❌ Kayıtsız rolü ID'si bulunamadı!")
    try:
        await m.edit(roles=[ks_rol])
        e = discord.Embed(title="🚪 Üye Kayıtsıza Atıldı", color=0x34495e, description=f"{m.mention} üzerindeki tüm roller temizlendi ve **Kayıtsız** rolü verildi.")
        e.add_field(name="👑 Yetkili:", value=ctx.author.mention, inline=True)
        if m.avatar: e.set_thumbnail(url=m.avatar.url)
        e.set_footer(text=f"{SUNUCU_ADI} • {datetime.now().strftime('%H:%M')}")
        await ctx.send(embed=e)
    except discord.Forbidden:
        await ctx.send("❌ **Hata:** Botun yetkisi bu üyeyi düzenlemeye yetmiyor!")

# --- EKONOMİ ---
def para_bar(miktar: int, maks: int = 100000) -> str:
    filled = min(int(miktar * 10 / maks), 10)
    return "█" * filled + "░" * (10 - filled)

@bot.command(name='para')
async def para_goster(ctx, uye: discord.Member = None):
    uye = uye or ctx.author
    data, k = get_user_para_data(uye.id)
    toplam = k["cash"] + k["bank"]
    embed = discord.Embed(color=0xf1c40f)
    embed.set_author(name=f"💰 {uye.display_name} — Cüzdan", icon_url=uye.display_avatar.url)
    embed.description = (
        f"{'─' * 30}\n"
        f"💵 **Nakit:** `{k['cash']:,}₺`\n"
        f"🏦 **Banka:** `{k['bank']:,}₺`\n"
        f"{'─' * 30}\n"
        f"📊 **Toplam:** `{toplam:,}₺`\n"
        f"`{para_bar(toplam)}`"
    )
    embed.set_thumbnail(url=uye.display_avatar.url)
    embed.set_footer(text=f"{SUNUCU_ADI} • Ekonomi  •  {datetime.now().strftime('%H:%M')}")
    await ctx.send(embed=embed)

@bot.command(name='deposit', aliases=["yatır"])
async def deposit(ctx, miktar: int):
    if miktar <= 0:
        return await ctx.send(embed=embed_hata("Geçersiz Miktar", "0'dan büyük bir miktar gir."), delete_after=5)
    data, k = get_user_para_data(ctx.author.id)
    if k["cash"] < miktar:
        return await ctx.send(embed=embed_hata("Yetersiz Nakit", f"Nakitin: **{k['cash']:,}₺**"), delete_after=5)
    k["cash"] -= miktar
    k["bank"] += miktar
    veri_kaydet(PARA_DOSYA, data)
    embed = discord.Embed(color=0x2ecc71)
    embed.set_author(name="🏦 Para Yatırıldı", icon_url=ctx.author.display_avatar.url)
    embed.description = (
        f"**{miktar:,}₺** başarıyla bankana yatırıldı.\n"
        f"{'─' * 28}\n"
        f"💵 Nakit → `{k['cash']:,}₺`\n"
        f"🏦 Banka → `{k['bank']:,}₺`"
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • Ekonomi")
    await ctx.send(embed=embed)

@bot.command(name='withdraw', aliases=["çek"])
async def withdraw(ctx, miktar: int):
    if miktar <= 0:
        return await ctx.send(embed=embed_hata("Geçersiz Miktar", "0'dan büyük bir miktar gir."), delete_after=5)
    data, k = get_user_para_data(ctx.author.id)
    if k["bank"] < miktar:
        return await ctx.send(embed=embed_hata("Yetersiz Bakiye", f"Bankandaki para: **{k['bank']:,}₺**"), delete_after=5)
    k["bank"] -= miktar
    k["cash"] += miktar
    veri_kaydet(PARA_DOSYA, data)
    embed = discord.Embed(color=0x3498db)
    embed.set_author(name="💵 Para Çekildi", icon_url=ctx.author.display_avatar.url)
    embed.description = (
        f"**{miktar:,}₺** bankandan çekildi.\n"
        f"{'─' * 28}\n"
        f"💵 Nakit → `{k['cash']:,}₺`\n"
        f"🏦 Banka → `{k['bank']:,}₺`"
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • Ekonomi")
    await ctx.send(embed=embed)

@bot.command(name='pay', aliases=["ver", "gönder"])
async def pay(ctx, alici: discord.Member, miktar: int):
    if miktar <= 0:
        return await ctx.send(embed=embed_hata("Geçersiz Miktar", "0'dan büyük bir miktar gir."), delete_after=5)
    if alici == ctx.author:
        return await ctx.send(embed=embed_hata("Hata", "Kendine para gönderemezsin!"), delete_after=5)
    data, gonderen = get_user_para_data(ctx.author.id)
    if gonderen["cash"] < miktar:
        return await ctx.send(embed=embed_hata("Yetersiz Nakit", f"Nakitin: **{gonderen['cash']:,}₺**"), delete_after=5)
    alici_id = str(alici.id)
    if alici_id not in data:
        data[alici_id] = {"cash": 0, "bank": 0}
    alan = data[alici_id]
    gonderen["cash"] -= miktar
    alan["cash"] += miktar
    veri_kaydet(PARA_DOSYA, data)
    embed = discord.Embed(color=0x9b59b6)
    embed.set_author(name="💸 Para Transferi", icon_url=ctx.author.display_avatar.url)
    embed.description = (
        f"{ctx.author.mention} **→** {alici.mention}\n"
        f"{'─' * 28}\n"
        f"💸 Transfer: **{miktar:,}₺**\n"
        f"✅ İşlem başarıyla tamamlandı!"
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • Ekonomi  •  {datetime.now().strftime('%H:%M')}")
    await ctx.send(embed=embed)

@bot.command(name='para-ekle')
@commands.has_permissions(administrator=True)
async def para_ver_admin(ctx, uye: discord.Member, miktar: int):
    data, k = get_user_para_data(uye.id)
    k["cash"] += miktar
    veri_kaydet(PARA_DOSYA, data)
    embed = discord.Embed(color=0x2ecc71)
    embed.set_author(name="✅ Para Eklendi", icon_url=ctx.author.display_avatar.url)
    embed.description = (
        f"{uye.mention} hesabına **{miktar:,}₺** eklendi.\n"
        f"{'─' * 28}\n"
        f"💵 Yeni nakit: `{k['cash']:,}₺`"
    )
    embed.set_footer(text=f"Yetkili: {ctx.author.display_name}  •  {SUNUCU_ADI}")
    await ctx.send(embed=embed)

@bot.command(name='para-sil')
@commands.has_permissions(administrator=True)
async def para_sil_admin(ctx, uye: discord.Member, miktar: int):
    if miktar <= 0:
        return await ctx.send(embed=embed_hata("Geçersiz Miktar", "0'dan büyük bir miktar gir."), delete_after=5)
    data, k = get_user_para_data(uye.id)
    toplam = k["cash"] + k["bank"]
    if miktar > toplam:
        return await ctx.send(embed=embed_hata("Yetersiz Bakiye", f"{uye.mention} adlı kişinin toplam parası: **{toplam:,}₺**"), delete_after=5)
    kalan = miktar
    nakit_sil = min(kalan, k["cash"])
    k["cash"] -= nakit_sil
    kalan -= nakit_sil
    if kalan > 0:
        k["bank"] -= kalan
    veri_kaydet(PARA_DOSYA, data)
    embed = discord.Embed(color=0xe74c3c)
    embed.set_author(name="🗑️ Para Silindi", icon_url=ctx.author.display_avatar.url)
    embed.description = (
        f"{uye.mention} hesabından **{miktar:,}₺** silindi.\n"
        f"{'─' * 28}\n"
        f"💵 Nakit: `{k['cash']:,}₺`\n"
        f"🏦 Banka: `{k['bank']:,}₺`"
    )
    embed.set_footer(text=f"Yetkili: {ctx.author.display_name}  •  {SUNUCU_ADI}")
    await ctx.send(embed=embed)

@bot.command(name='para-sıfırla')
@commands.has_permissions(administrator=True)
async def para_sifirla_admin(ctx, uye: discord.Member):
    data, k = get_user_para_data(uye.id)
    eski_toplam = k["cash"] + k["bank"]
    k["cash"] = 0
    k["bank"] = 0
    veri_kaydet(PARA_DOSYA, data)
    embed = discord.Embed(color=0xe74c3c)
    embed.set_author(name="🔄 Para Sıfırlandı", icon_url=ctx.author.display_avatar.url)
    embed.description = (
        f"{uye.mention} hesabındaki tüm para silindi.\n"
        f"{'─' * 28}\n"
        f"🗑️ Silinen miktar: **{eski_toplam:,}₺**\n"
        f"💰 Yeni bakiye: `0₺`"
    )
    embed.set_footer(text=f"Yetkili: {ctx.author.display_name}  •  {SUNUCU_ADI}")
    await ctx.send(embed=embed)

@bot.command(name='zenginler', aliases=["topzengin", "liderboard"])
async def zenginler(ctx):
    data = veri_yukle(PARA_DOSYA)
    siralama = []
    for uid, bilgi in data.items():
        toplam = bilgi.get("cash", 0) + bilgi.get("bank", 0)
        if toplam > 0:
            member = ctx.guild.get_member(int(uid))
            siralama.append((member, toplam, bilgi.get("cash", 0), bilgi.get("bank", 0)))
    siralama.sort(key=lambda x: x[1], reverse=True)
    siralama = siralama[:10]
    if not siralama:
        return await ctx.send(embed=embed_hata("Veri Yok", "Henüz kayıtlı para verisi bulunmuyor."))

    sira_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}
    yazi = ""
    for i, (member, toplam, nakit, banka) in enumerate(siralama, 1):
        isim = member.display_name if member else f"Kullanıcı ({list(data.keys())[i-1]})"
        sira = sira_emoji.get(i, f"`#{i}`")
        bar = para_bar(toplam, siralama[0][1] if siralama[0][1] > 0 else 1)
        yazi += (
            f"{sira} **{isim}**\n"
            f"┣ 💵 Nakit: `{nakit:,}₺` • 🏦 Banka: `{banka:,}₺`\n"
            f"┗ 💰 Toplam: **{toplam:,}₺**  `{bar}`\n\n"
        )

    embed = discord.Embed(color=0xffd700)
    embed.set_author(
        name=f"💎 {SUNUCU_ADI} — Zenginler Listesi",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
    )
    embed.description = yazi
    embed.add_field(name="👥 Listelenen", value=f"**{len(siralama)}** kişi", inline=True)
    embed.add_field(name="🏆 En Zengin", value=f"**{siralama[0][1]:,}₺**", inline=True)
    embed.set_footer(text=f"{SUNUCU_ADI} • Ekonomi  •  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    await ctx.send(embed=embed)

# --- GELİŞİM (.ant) ---
@bot.command(name='ant')
@commands.cooldown(1, 3600, commands.BucketType.user)
async def ant(ctx):
    if ctx.channel.id != ANTRENMAN_KANAL_ID:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f"❌ Bu komutu sadece <#{ANTRENMAN_KANAL_ID}> kanalında kullanabilirsin!", delete_after=5)
    u = str(ctx.author.id)
    c = antrenman_sayaci.get(u, 0) + 1
    antrenman_sayaci[u] = c
    veri_kaydet(ANTRENMAN_DOSYA, antrenman_sayaci)
    stat_ekle(u, 'antrenman')
    progress = c % 10
    if progress != 0:
        bar = "🟦" * progress + "⬜" * (10 - progress)
        e = discord.Embed(color=0x3498db)
        e.set_author(name="🏃 Antrenman Devam Ediyor", icon_url=ctx.author.display_avatar.url)
        e.description = (
            f"⚽ {ctx.author.mention} sahada yoğun çalışıyor...\n"
            f"{'─'*30}\n"
            f"📊 Tur: **{progress}/10**  •  📈 Toplam: **{c}**\n"
            f"{bar}"
        )
        e.set_thumbnail(url=ctx.author.display_avatar.url)
        e.set_footer(text=f"{SUNUCU_ADI} • Antrenman  •  {datetime.now().strftime('%H:%M')}")
        await ctx.send(embed=e)
    else:
        antrenman_sayaci[u] = 0
        veri_kaydet(ANTRENMAN_DOSYA, antrenman_sayaci)
        e = discord.Embed(color=0x2ecc71)
        e.set_author(name="🔥 Antrenman Tamamlandı!", icon_url=ctx.author.display_avatar.url)
        e.description = (
            f"## ⚽ {ctx.author.mention} — Mükemmel Performans!\n"
            f"{'─'*30}\n"
            f"💪 Fizik gücü arttı\n"
            f"📈 Form seviyesi yükseldi"
        )
        e.set_image(url="https://media1.tenor.com/m/dmH0nGUtvGQAAAAC/futbol-entrenar.gif")
        e.set_footer(text=f"{SUNUCU_ADI} • Antrenman Sistemi")
        await ctx.send(embed=e)
        bk = bot.get_channel(ANTRENMAN_BILDIRI_KANAL_ID)
        if bk:
            notify = discord.Embed(color=0xf1c40f)
            notify.set_author(name="📢 Oyuncu Gelişimi Tamamlandı", icon_url=ctx.author.display_avatar.url)
            notify.description = (
                f"⚽ {ctx.author.mention} antrenmanını tamamladı!\n"
                f"{'─'*28}\n"
                f"🏆 **10/10** tur tamamlandı."
            )
            notify.set_footer(text=f"{SUNUCU_ADI} • {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            await bk.send(embed=notify)

@ant.error
async def ant_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        kalan = int(error.retry_after)
        dk, sn = divmod(kalan, 60)
        await ctx.send(
            embed=embed_hata("Bekleme Süresi", f"Bir sonraki antrenman için **{dk}dk {sn}sn** beklemelisin."),
            delete_after=10
        )

# --- GÜMÜŞ ANTRENMAN (.gant) ---
@bot.command(name='gant')
@commands.cooldown(1, 3600, commands.BucketType.user)
async def gant(ctx):
    if ctx.channel.id != GANT_KANAL_ID:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(
            embed=embed_hata("Yanlış Kanal", f"Bu komutu sadece <#{GANT_KANAL_ID}> kanalında kullanabilirsin!"),
            delete_after=5
        )
    if not ctx.author.get_role(FUTBOLCU_ROL_ID):
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(
            embed=embed_hata("Yetki Yok", "Bu komutu kullanmak için **Futbolcu** rolüne sahip olmalısın!"),
            delete_after=5
        )
    try: await ctx.message.delete()
    except Exception: pass
    data = ant_oku(GANT_DOSYA)
    uid  = str(ctx.author.id)
    mevcut = data.get(uid, 0)
    if mevcut >= GANT_LIMIT:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed=ant_embed_limit(ctx.author, GANT_LIMIT, "gumus"))
    mevcut += 1
    data[uid] = mevcut
    ant_yaz(GANT_DOSYA, data)
    await ctx.send(embed=ant_embed_devam(ctx.author, mevcut, GANT_LIMIT, "gumus"))

@gant.error
async def gant_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        kalan = int(error.retry_after)
        dk, sn = divmod(kalan, 60)
        await ctx.send(
            embed=embed_hata("Bekleme Süresi", f"Bir sonraki gümüş antrenman için **{dk}dk {sn}sn** beklemelisin."),
            delete_after=10
        )
        try: await ctx.message.delete()
        except Exception: pass

# --- ALTIN ANTRENMAN (.aant) ---
@bot.command(name='aant')
@commands.cooldown(1, 3600, commands.BucketType.user)
async def aant(ctx):
    if ctx.channel.id != AANT_KANAL_ID:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(
            embed=embed_hata("Yanlış Kanal", f"Bu komutu sadece <#{AANT_KANAL_ID}> kanalında kullanabilirsin!"),
            delete_after=5
        )
    if not ctx.author.get_role(FUTBOLCU_ROL_ID):
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(
            embed=embed_hata("Yetki Yok", "Bu komutu kullanmak için **Futbolcu** rolüne sahip olmalısın!"),
            delete_after=5
        )
    try: await ctx.message.delete()
    except Exception: pass
    data = ant_oku(AANT_DOSYA)
    uid  = str(ctx.author.id)
    mevcut = data.get(uid, 0)
    if mevcut >= AANT_LIMIT:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed=ant_embed_limit(ctx.author, AANT_LIMIT, "altin"))
    mevcut += 1
    data[uid] = mevcut
    ant_yaz(AANT_DOSYA, data)
    await ctx.send(embed=ant_embed_devam(ctx.author, mevcut, AANT_LIMIT, "altin"))

@aant.error
async def aant_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        kalan = int(error.retry_after)
        dk, sn = divmod(kalan, 60)
        await ctx.send(
            embed=embed_hata("Bekleme Süresi", f"Bir sonraki altın antrenman için **{dk}dk {sn}sn** beklemelisin."),
            delete_after=10
        )
        try: await ctx.message.delete()
        except Exception: pass

# --- ANTRENMAN SKOR / SIFIRLA ---
@bot.command(name='antskor')
async def antskor(ctx, tip: str = "gumus"):
    tip = tip.lower().replace("ü", "u").replace("ı", "i")
    if tip in ("altin", "altan", "aant", "a"):
        dosya, limit, etiket, emoji = AANT_DOSYA, AANT_LIMIT, "Altın Antrenman", "🥇"
    else:
        dosya, limit, etiket, emoji = GANT_DOSYA, GANT_LIMIT, "Gümüş Antrenman", "🥈"
    data = ant_oku(dosya)
    if not data:
        return await ctx.send(embed=embed_hata(etiket, "Henüz hiç antrenman yapılmamış!"))
    sirali = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
    embed  = discord.Embed(color=0xf1c40f if emoji == "🥇" else 0xc0c0c0)
    embed.set_author(
        name=f"{emoji} {etiket} — Skor Tablosu",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
    )
    madalya = ["🥇", "🥈", "🥉"]
    desc = f"{'─'*30}\n"
    for i, (uid, sayi) in enumerate(sirali):
        member = ctx.guild.get_member(int(uid))
        isim   = member.display_name if member else f"ID:{uid}"
        prefix = madalya[i] if i < 3 else f"**#{i+1}**"
        bar_dolu = round((sayi / limit) * 10)
        mini_bar = "█" * bar_dolu + "░" * (10 - bar_dolu)
        desc += f"{prefix} **{isim}** — `{mini_bar}` **{sayi}/{limit}**\n"
    desc += f"{'─'*30}"
    embed.description = desc
    embed.set_footer(text=f"{SUNUCU_ADI} • {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    await ctx.send(embed=embed)

@bot.command(name='antsifirla')
@commands.has_permissions(administrator=True)
async def antsifirla(ctx, tip: str, uye: discord.Member = None):
    tip_n  = tip.lower().replace("ü", "u").replace("ı", "i")
    dosya  = AANT_DOSYA if tip_n in ("altin", "aant") else GANT_DOSYA
    etiket = "Altın" if tip_n in ("altin", "aant") else "Gümüş"
    data   = ant_oku(dosya)
    if uye:
        data[str(uye.id)] = 0
        ant_yaz(dosya, data)
        await ctx.send(embed=embed_basari(f"{etiket} Antrenman Sıfırlandı", f"{uye.mention} için {etiket.lower()} antrenman sayacı sıfırlandı."))
    else:
        ant_yaz(dosya, {})
        await ctx.send(embed=embed_basari(f"{etiket} Antrenman Sıfırlandı", f"Tüm oyuncuların {etiket.lower()} antrenman sayacı sıfırlandı."))

# --- BECERİ ANTRENMANı (.beceri) ---
def beceri_veri_yukle(uid: int):
    data = veri_yukle(BECERI_DOSYA, {})
    key = str(uid)
    if key not in data:
        data[key] = {k: 0 for k in BECERILER}
        data[key]["full_sayisi"] = 0
        data[key]["son_antrenman"] = 0
        data[key]["aktif_beceri"] = None
    else:
        for k in BECERILER:
            data[key].setdefault(k, 0)
        data[key].setdefault("full_sayisi", 0)
        data[key].setdefault("son_antrenman", 0)
        data[key].setdefault("aktif_beceri", None)
    return data, data[key]

def beceri_secim_embed(member: discord.Member, kayit: dict) -> discord.Embed:
    embed = discord.Embed(color=0x9b59b6)
    embed.set_author(name=f"⭐ {member.display_name} — Beceri Seçimi", icon_url=member.display_avatar.url)
    desc = f"Hangi beceriyi antrenman yapmak istiyorsun? Aşağıdan seç.\n{'─' * 30}\n"
    for key, b in BECERILER.items():
        cur = kayit.get(key, 0)
        mx = b["max"]
        filled = int((cur / mx) * 10)
        bar = "█" * filled + "░" * (10 - filled)
        tag = " ✅" if cur >= mx else ""
        desc += f"{b['emoji']} **{b['isim']}**: `{cur}/{mx}`{tag}\n`{bar}`\n"
    desc += f"{'─' * 30}\n⭐ **Dolu Beceri:** `{kayit.get('full_sayisi', 0)}/{MAX_FULL}`"
    embed.description = desc
    embed.set_footer(text=f"{SUNUCU_ADI} • Beceri Sistemi  •  {datetime.now().strftime('%H:%M')}")
    return embed

class BeceriSelect(discord.ui.Select):
    def __init__(self, uid: int, kayit: dict):
        self.uid = uid
        options = []
        for key, b in BECERILER.items():
            cur = kayit.get(key, 0)
            full = cur >= b["max"]
            label = f"{b['isim']} ({cur}/{b['max']})"
            desc = "✅ Dolu — başka beceri seç" if full else "Antrenman için seç"
            options.append(discord.SelectOption(label=label, value=key, emoji=b["emoji"], description=desc))
        super().__init__(placeholder="🏃 Hangi beceriyi çalışmak istiyorsun?", options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.uid:
            return await interaction.response.send_message("❌ Bu panel sana ait değil.", ephemeral=True)
        data, kayit = beceri_veri_yukle(self.uid)
        secilen = self.values[0]
        b = BECERILER[secilen]
        if kayit.get(secilen, 0) >= b["max"]:
            return await interaction.response.send_message(f"❌ **{b['isim']}** zaten dolu! Başka bir beceri seç.", ephemeral=True)
        kayit["aktif_beceri"] = secilen
        veri_kaydet(BECERI_DOSYA, data)
        embed = discord.Embed(color=0x3498db)
        embed.set_author(name=f"⭐ {interaction.user.display_name} — Beceri Seçildi", icon_url=interaction.user.display_avatar.url)
        embed.description = (
            f"{b['emoji']} **{b['isim']}** seçildi!\n"
            f"{'─' * 30}\n"
            f"Antrenman yapmak için tekrar **`.beceri`** yaz.\n"
            f"⏱️ Her antrenman arası **{BECERI_BEKLEME // 60} dakika** beklemelisin."
        )
        embed.set_footer(text=f"{SUNUCU_ADI} • Beceri Sistemi  •  {datetime.now().strftime('%H:%M')}")
        await interaction.response.edit_message(embed=embed, view=None)

class BeceriView(discord.ui.View):
    def __init__(self, uid: int, kayit: dict):
        super().__init__(timeout=60)
        self.add_item(BeceriSelect(uid, kayit))

@bot.command(name="beceri")
async def beceri_komutu(ctx):
    if ctx.channel.id != BECERI_KANAL_ID:
        return await ctx.send(
            f"❌ Bu komutu sadece <#{BECERI_KANAL_ID}> kanalında kullanabilirsin!",
            delete_after=5
        )
    if not ctx.author.get_role(FUTBOLCU_ROL_ID):
        return await ctx.send(
            embed=embed_hata("Yetki Yok", "Bu komutu kullanmak için **Futbolcu** rolüne sahip olmalısın!"),
            delete_after=5
        )

    uid = ctx.author.id
    data, kayit = beceri_veri_yukle(uid)
    aktif = kayit.get("aktif_beceri")

    # Aktif beceri seçili değil → seçim paneli göster
    if aktif is None:
        embed = beceri_secim_embed(ctx.author, kayit)
        await ctx.send(embed=embed, view=BeceriView(uid, kayit))
        return

    b = BECERILER[aktif]
    cur = kayit.get(aktif, 0)
    mx = b["max"]

    # Beceri dolmuş → full_sayisi artır, sıfırla, yeni seçim paneli
    if cur >= mx:
        kayit["full_sayisi"] = kayit.get("full_sayisi", 0) + 1
        kayit["aktif_beceri"] = None
        veri_kaydet(BECERI_DOSYA, data)
        if kayit["full_sayisi"] >= MAX_FULL:
            return await ctx.send(embed=discord.Embed(
                description=(
                    f"🏆 {ctx.author.mention} tüm becerilerini tamamladı!\n"
                    f"**{MAX_FULL}/{MAX_FULL}** beceri fulllendi. Efsane bir oyuncu! ⭐"
                ),
                color=0xffd700
            ))
        embed = beceri_secim_embed(ctx.author, kayit)
        return await ctx.send(embed=embed, view=BeceriView(uid, kayit))

    # Cooldown kontrolü
    simdi = int(__import__("time").time())
    son = kayit.get("son_antrenman", 0)
    kalan = max(0, BECERI_BEKLEME - (simdi - son))
    if kalan > 0:
        dk, sn = divmod(kalan, 60)
        return await ctx.send(
            embed=embed_hata("Bekleme Süresi", f"⏱️ Sonraki beceri antrenmanı için **{dk}dk {sn}sn** bekle!"),
            delete_after=15
        )

    # Antrenman yap
    kayit[aktif] = cur + 1
    kayit["son_antrenman"] = simdi
    yeni = cur + 1
    veri_kaydet(BECERI_DOSYA, data)

    filled = int((yeni / mx) * 12)
    bar = "🟦" * filled + "⬜" * (12 - filled)
    embed = discord.Embed(color=0x2ecc71 if yeni >= mx else 0x3498db)
    embed.set_author(name=f"⭐ {ctx.author.display_name} — Beceri Antrenmanı", icon_url=ctx.author.display_avatar.url)
    if yeni >= mx:
        embed.description = (
            f"🎉 {b['emoji']} **{b['isim']}** TAMAMLANDI!\n"
            f"{'─' * 30}\n"
            f"`{'█' * 12}` **{yeni}/{mx}** ✅\n"
            f"{'─' * 30}\n"
            f"Yeni bir beceri seçmek için tekrar **`.beceri`** yaz."
        )
    else:
        embed.description = (
            f"{b['emoji']} **{b['isim']}** antrenmanı yapıldı!\n"
            f"{'─' * 30}\n"
            f"📊 İlerleme: **{yeni}/{mx}**\n"
            f"{bar}\n"
            f"{'─' * 30}\n"
            f"⏱️ Sonraki antrenman için **{BECERI_BEKLEME // 60} dakika** bekle."
        )
    embed.set_footer(text=f"{SUNUCU_ADI} • Beceri Sistemi  •  {datetime.now().strftime('%H:%M')}")
    await ctx.send(embed=embed)

# --- NİTELİK SİSTEMİ (.ekle / .nitelik-sil / .s / .nitelik-kur / .alltimegeçir) ---
async def _guncelle_nitelik_coklu(ctx, uye: discord.Member, arguments: str, is_silme_komutu: bool):
    parts = arguments.split(" | ", 1)
    attributes_str = parts[0]
    sebep = parts[1].strip() if len(parts) > 1 else ("Performans düşüklüğü" if is_silme_komutu else "Nitelik güncellendi")
    raw_updates = [s.strip() for s in attributes_str.split(',')]
    updates = []
    for u in raw_updates:
        if not u:
            continue
        match = re.match(r'([+-]?\d+)\s+(.+)', u.strip())
        if match:
            updates.append((match.group(1), match.group(2).strip()))
        else:
            return await ctx.send(
                embed=embed_hata("Format Hatası", f"`{u}` geçersiz.\nÖrnek: `.ekle @oyuncu +10 Sprint Hızı, -5 Denge | sebep`"),
                delete_after=10
            )
    if not updates:
        return await ctx.send(embed=embed_hata("Hata", "Nitelik bulunamadı."), delete_after=8)

    data = nt_oku()
    uid = str(uye.id)
    if uid not in data:
        data[uid] = {"all_time": {}, "haftalik": {}}

    degisiklik_ozeti = []
    toplam_puan = 0
    tum_nitelikler = [n for kat in KATEGORILER.values() for n in kat] + ["Zayıf Ayak"]

    for miktar_str, nitelik_adi in updates:
        nitelik_adi_lower = nitelik_adi.lower()
        try:
            miktar = int(miktar_str)
            if is_silme_komutu:
                miktar = -abs(miktar)
        except ValueError:
            continue
        hedef = None
        for n in tum_nitelikler:
            if n.lower() == nitelik_adi_lower:
                hedef = n
                break
        if not hedef:
            olasılar = [n for n in tum_nitelikler if n.lower().startswith(nitelik_adi_lower)]
            if len(olasılar) == 1:
                hedef = olasılar[0]
            elif len(olasılar) > 1:
                await ctx.send(embed=embed_hata("Belirsiz Nitelik", f"`{nitelik_adi}` için: `{', '.join(olasılar)}`"), delete_after=10)
                continue
        if not hedef:
            await ctx.send(embed=embed_hata("Geçersiz Nitelik", f"`{nitelik_adi}` bulunamadı."), delete_after=7)
            continue
        limit = 5 if hedef == "Zayıf Ayak" else 49
        data[uid].setdefault("haftalik", {})
        data[uid].setdefault("all_time", {})
        haftalik_val  = data[uid]["haftalik"].get(hedef, 0)
        yeni_haftalik = max(0, haftalik_val + miktar)
        data[uid]["haftalik"][hedef] = yeni_haftalik
        all_time_val    = data[uid]["all_time"].get(hedef, 0)
        toplam_gosterim = min(limit, all_time_val + yeni_haftalik)
        isaret = f"+{miktar}" if miktar > 0 else str(miktar)
        degisiklik_ozeti.append(f"**{hedef}:** {isaret} → `{toplam_gosterim}/{limit}`")
        toplam_puan += miktar

    nt_yaz(data)
    if not degisiklik_ozeti:
        return
    stat_ekle(uid, "nitelik_eklendi", len(degisiklik_ozeti))
    ok = "eklendi" if toplam_puan > 0 else "düşürüldü"
    embed = discord.Embed(color=0x43b581)
    embed.set_author(name=f"✅ Nitelik Güncellendi — {uye.display_name}", icon_url=uye.display_avatar.url)
    embed.description = (
        f"**Oyuncu:** {uye.mention}\n"
        f"**Sebep:** {sebep}\n"
        f"{'─'*30}\n"
        + "\n".join(degisiklik_ozeti)
        + f"\n{'─'*30}\n"
        f"**Toplam:** `{abs(toplam_puan)}` puan {ok}"
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • Nitelik  •  Yetkili: {ctx.author.display_name}")
    await ctx.send(embed=embed)

def build_nitelik_embed(uye: discord.Member, baslik: str, renk: int, nitelik_dict: dict, bos_mesaj: str) -> discord.Embed:
    toplam = sum(nitelik_dict.values()) if nitelik_dict else 0
    embed  = discord.Embed(color=renk)
    embed.set_author(name=f"👤 {uye.display_name} — İstatistikler", icon_url=uye.display_avatar.url)
    embed.set_thumbnail(url=uye.display_avatar.url)
    if not nitelik_dict or toplam == 0:
        embed.description = bos_mesaj
    else:
        desc = f"**{baslik}**\n"
        satirlar = []
        for kat, kat_nitelikler in KATEGORILER.items():
            for n in kat_nitelikler:
                if n in nitelik_dict and nitelik_dict[n] > 0:
                    satirlar.append(f"{n}: +{nitelik_dict[n]}")
        if "Zayıf Ayak" in nitelik_dict and nitelik_dict["Zayıf Ayak"] > 0:
            satirlar.append(f"Zayıf Ayak: +{nitelik_dict['Zayıf Ayak']}")
        desc += "\n".join(satirlar)
        desc += f"\n\n📈 **Toplam:** {toplam}"
        embed.description = desc
    embed.set_footer(text=f"{SUNUCU_ADI} • {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    return embed

def build_all_time_embed(uye: discord.Member, veri_seti: dict) -> discord.Embed:
    all_time = veri_seti.get("all_time", {})
    return build_nitelik_embed(
        uye, "🏆 Basılan Nitelikler", 0x5865f2, all_time,
        "*Henüz All-Time havuzuna aktarılmış nitelik yok.*"
    )

class StatsView(discord.ui.View):
    def __init__(self, uye: discord.Member, uid: str):
        super().__init__(timeout=60)
        self.uye     = uye
        self.uid     = uid
        self.message = None

    async def on_timeout(self):
        if self.message:
            try:
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)
            except discord.NotFound:
                pass

    @discord.ui.button(label="📅 Haftalık", style=discord.ButtonStyle.primary)
    async def haftalik(self, interaction: discord.Interaction, button: discord.ui.Button):
        data     = nt_oku()
        veri     = data.get(self.uid, {"haftalik": {}})
        haftalik = veri.get("haftalik", {})
        embed    = build_nitelik_embed(
            self.uye, "🎯 Basılan Nitelikler", 0x43b581, haftalik,
            "*Bu hafta henüz nitelik basılmamış.*"
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏆 All-Time", style=discord.ButtonStyle.secondary)
    async def alltime(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = nt_oku()
        veri = data.get(self.uid, {"all_time": {}})
        await interaction.response.edit_message(embed=build_all_time_embed(self.uye, veri), view=self)

@bot.command(name="ekle")
@commands.has_role(NITELIK_YETKILI_ROL_ID)
async def ekle_komutu(ctx, uye: discord.Member, *, arguments: str):
    await _guncelle_nitelik_coklu(ctx, uye, arguments, is_silme_komutu=False)

@ekle_komutu.error
async def ekle_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(embed=embed_hata("Yetki Yok", "Bu komutu kullanma yetkin yok."), delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embed_bilgi("Kullanım: `.ekle @oyuncu +10 Sprint Hızı, -5 Denge | sebep`"), delete_after=10)

@bot.command(name="nitelik-sil")
@commands.has_role(NITELIK_YETKILI_ROL_ID)
async def nitelik_sil_komutu(ctx, uye: discord.Member, *, arguments: str):
    await _guncelle_nitelik_coklu(ctx, uye, arguments, is_silme_komutu=True)

@nitelik_sil_komutu.error
async def nitelik_sil_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(embed=embed_hata("Yetki Yok", "Bu komutu kullanma yetkin yok."), delete_after=5)

@bot.command(name="s")
async def stats_panel(ctx, uye: discord.Member = None):
    uye = uye or ctx.author
    data = nt_oku()
    uid  = str(uye.id)
    if uid not in data:
        return await ctx.send(
            embed=embed_hata("Kayıt Yok", f"{uye.mention} için nitelik kaydı bulunamadı. Yetkili `.nitelik-kur @oyuncu` ile oluşturabilir."),
            delete_after=10
        )
    view = StatsView(uye, uid)
    view.message = await ctx.send(embed=build_all_time_embed(uye, data[uid]), view=view)

@bot.command(name="nitelik-kur")
@commands.has_permissions(administrator=True)
async def nitelik_kur(ctx, uye: discord.Member):
    data = nt_oku()
    uid  = str(uye.id)
    data[uid] = {"all_time": {}, "haftalik": {}}
    nt_yaz(data)
    await ctx.send(embed=embed_basari("Nitelik Kartı Oluşturuldu", f"{uye.mention} için temiz bir nitelik kartı oluşturuldu/sıfırlandı."))

@bot.command(name="alltimegeçir")
@commands.has_permissions(administrator=True)
async def all_time_gecir(ctx):
    data  = nt_oku()
    if not data:
        return await ctx.send(embed=embed_hata("Hata", "Sistemde oyuncu bulunamadı."))
    sayac = 0
    for uid, oyuncu in data.items():
        if "all_time" not in oyuncu: oyuncu["all_time"] = {}
        if "haftalik" not in oyuncu: oyuncu["haftalik"] = {}
        if oyuncu["haftalik"]:
            for nitelik, puan in oyuncu["haftalik"].items():
                limit = 5 if nitelik == "Zayıf Ayak" else 49
                oyuncu["all_time"][nitelik] = min(limit, oyuncu["all_time"].get(nitelik, 0) + puan)
            oyuncu["haftalik"] = {}
            sayac += 1
    nt_yaz(data)
    await ctx.send(embed=embed_basari(
        "All-Time Aktarımı",
        f"**{sayac}** oyuncunun haftalık verileri All-Time havuzuna aktarıldı.\nHaftalık sayaçlar sıfırlandı."
    ))

# --- TRANSFER VE KULÜP İŞLEMLERİ ---
class TeamView(discord.ui.View):
    def __init__(self, takim_rolu: discord.Role):
        super().__init__(timeout=180)
        self.takim_rolu = takim_rolu
        self.message = None
    async def on_timeout(self):
        if self.message:
            try: await self.message.edit(view=None)
            except discord.NotFound: pass

    @discord.ui.button(label="Oyuncuları Göster", style=discord.ButtonStyle.secondary, emoji="👥")
    async def show_players(self, interaction: discord.Interaction, button: discord.ui.Button):
        futbolcu_rol = interaction.guild.get_role(FUTBOLCU_ROL_ID)
        if not futbolcu_rol:
            return await interaction.response.send_message("Sistemde 'Futbolcu' rolü bulunamadı.", ephemeral=True)
        oyuncular = [m for m in self.takim_rolu.members if futbolcu_rol in m.roles]
        if not oyuncular:
            return await interaction.response.send_message("Bu takımda lisanslı futbolcu yok.", ephemeral=True)
        liste = "\n".join(f"**{i}.** {oyuncu.mention} - `{oyuncu.display_name}`" for i, oyuncu in enumerate(oyuncular[:25], 1))
        embed = discord.Embed(title=f"⚽ {self.takim_rolu.name} Kadrosu", description=liste, color=self.takim_rolu.color)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Gizle & Kapat", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def close_view(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message:
            await self.message.delete()

@bot.command(name="takım")
async def takim_komutu(ctx, *, takim_adi: str = None):
    if not takim_adi:
        return await ctx.send("❌ Kullanım: `.takım Real Madrid`")
    takim_adi_lower = takim_adi.lower().strip()
    takim_rolu = next(
        (r for r in ctx.guild.roles if takim_adi_lower in r.name.lower()),
        None
    )
    if not takim_rolu:
        return await ctx.send(f"❌ `{takim_adi}` adında bir takım rolü bulunamadı.")
    kaptan_rol = ctx.guild.get_role(KAPTAN_ROL_ID)
    futbolcu_rol = ctx.guild.get_role(FUTBOLCU_ROL_ID)
    if not futbolcu_rol:
        return await ctx.send("Sistemde 'Futbolcu' rolü ayarlı değil.")

    oyuncular = [m for m in takim_rolu.members if futbolcu_rol in m.roles]
    kaptan = next((m for m in takim_rolu.members if kaptan_rol and kaptan_rol in m.roles), None)

    toplam_deger = 0
    for m in oyuncular:
        try:
            parcalar = m.display_name.split(" | ")
            if len(parcalar) >= 4:
                deger_str = parcalar[3].upper().replace("M€", "").replace("M", "").strip()
                toplam_deger += float(deger_str)
        except (ValueError, IndexError):
            continue

    takim_adi_sade = takim_rolu.name.split(" |")[0].strip()
    embed = discord.Embed(title=f"{takim_adi_sade} Takım Formu", color=takim_rolu.color)
    if logo_url := TAKIM_LOGOLARI.get(takim_adi_sade):
        embed.set_thumbnail(url=logo_url)

    embed.add_field(name="Toplam Takım Değeri", value=f"**{toplam_deger:,.0f}M€**", inline=False)
    embed.add_field(name="Takım Etiketi", value=takim_rolu.mention, inline=False)
    embed.add_field(name="Takım Başkanı", value=kaptan.mention if kaptan else "-", inline=True)
    embed.add_field(name="Futbolcu Sayısı", value=f"{len(oyuncular)} Tescilli Oyuncu", inline=False)
    embed.set_footer(text="Kadro ve Pazar değerleri için aşağıdaki butonları kullanın.")

    view = TeamView(takim_rolu)
    message = await ctx.send(embed=embed, view=view)
    view.message = message

class TransferModal(Modal):
    def __init__(self, oyuncu: discord.Member, tip: str, mevki: str):
        self.oyuncu = oyuncu; self.tip = tip; self.mevki = mevki
        super().__init__(title=f"💰 {SUNUCU_ADI} | {tip} Formu")
        self.bedel = TextInput(label=f"Talep Edilen {tip} Bedeli 💵", placeholder="Örn: 228M€", required=True)
        self.rapor = TextInput(label="Teknik Heyet Raporu 📜", style=discord.TextStyle.paragraph, placeholder="Neden listeye eklendi?", required=True)
        self.add_item(self.bedel); self.add_item(self.rapor)
    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild: return
        kanal = interaction.guild.get_channel(TRANSFER_LISTESI_ID)
        if not isinstance(kanal, discord.TextChannel): return await interaction.response.send_message("❌ Transfer kanalı bulunamadı!", ephemeral=True)
        tip_emoji = "💰" if self.tip == "Transfer" else "🤝"; tip_renk  = 0x1a1a2e if self.tip == "Transfer" else 0x0f3460
        embed = discord.Embed(color=tip_renk)
        embed.set_author(name=f"{SUNUCU_ADI} | {self.tip.upper()} LİSTESİ", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.description = f"**{interaction.user.mention}**, {self.oyuncu.mention} adlı oyuncuyu resmi olarak **{self.tip.lower()} listesine** ekledi. {tip_emoji}"
        embed.add_field(name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", value="​", inline=False)
        embed.add_field(name="👤 Oyuncu", value=self.oyuncu.mention, inline=True).add_field(name="​", value="​", inline=True).add_field(name="👕 Mevki", value=f"`{self.mevki}`", inline=True)
        embed.add_field(name=f"{tip_emoji} {self.tip} Bedeli", value=f"**{self.bedel.value}**", inline=True).add_field(name="​", value="​", inline=True).add_field(name="🧑‍💼 Yetkili", value=interaction.user.mention, inline=True)
        embed.add_field(name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", value="​", inline=False)
        embed.add_field(name="📝 Rapor", value=f"*{self.rapor.value}*", inline=False)
        if self.oyuncu.avatar: embed.set_thumbnail(url=self.oyuncu.avatar.url)
        embed.set_footer(text=f"{SUNUCU_ADI} • {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        etiketler = f"<@&{BASKAN_ROL_ID}> <@&{KAPTAN_ROL_ID}>"
        await kanal.send(content=etiketler, embed=embed)
        await interaction.response.send_message(embed=discord.Embed(description=f"✅ İlan başarıyla {kanal.mention} kanalına gönderildi.", color=0x2ecc71), ephemeral=True)

class TransferSecimView(View):
    def __init__(self, oyuncu: discord.Member, mevki: str):
        super().__init__(timeout=60); self.oyuncu = oyuncu; self.mevki = mevki
    @discord.ui.button(label="TRANSFER LİSTESİ", style=discord.ButtonStyle.success, emoji="💰")
    async def transfer_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(TransferModal(self.oyuncu, "Transfer", self.mevki))
    @discord.ui.button(label="KİRALIK LİSTESİ", style=discord.ButtonStyle.primary, emoji="🤝")
    async def kiralik_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(TransferModal(self.oyuncu, "Kiralık", self.mevki))

@bot.command(name='ilanver')
async def ilan_ver(ctx, üye: discord.Member, mevki: str):
    yetkililer = [BASKAN_ROL_ID, KAPTAN_ROL_ID]
    if not (ctx.author.id == OWNER_ID or any(r.id in yetkililer for r in ctx.author.roles)): return await ctx.send("❌ Yetkiniz yetersiz!", delete_after=5)
    if ctx.channel.id != ILAN_VER_KANAL_ID: return await ctx.send(f"❌ Bu komutu sadece <#{ILAN_VER_KANAL_ID}> kanalında kullanabilirsin!", delete_after=5)
    embed = discord.Embed(title=f"⚡ {SUNUCU_ADI} KULÜP YÖNETİMİ", description=f"**{üye.mention}** (**{mevki}**) için işlem türünü seçin: ⬇️", color=0x010101)
    await ctx.send(embed=embed, view=TransferSecimView(üye, mevki))

@bot.command(name='transfer')
@commands.has_permissions(manage_messages=True)
async def transfer(ctx, oyuncu: discord.Member, numara: str, sure: str, *, yeni_takim: str):
    embed = discord.Embed(title="🚨 HERE WE GO! 🚨", description=f"### {oyuncu.mention} artık **{yeni_takim}** başarısı için ter dökecek!", color=0x2ecc71)
    embed.add_field(name="👕 Forma Numarası", value=f"**#{numara}**", inline=True).add_field(name="📜 Sözleşme Süresi", value=f"**{sure}**", inline=True).add_field(name="🏟️ Yeni Kulübü", value=f"**{yeni_takim}**", inline=True)
    if ctx.message.attachments: foto_url = ctx.message.attachments[0].url
    else: foto_url = oyuncu.avatar.url if oyuncu.avatar else oyuncu.default_avatar.url
    embed.set_image(url=foto_url)
    embed.set_footer(text=f"{SUNUCU_ADI} Transfer Haberleri • Yetkili: {ctx.author.display_name}")
    await ctx.send(content=f"🔔 **SON DAKİKA:** {oyuncu.mention} transferi tamamlandı!", embed=embed)
    try: await ctx.message.delete()
    except: pass
        
# --- BİLGİ YARIŞMASI KOMUTLARI ---

@bot.command(name='sorusor')
@commands.has_permissions(administrator=True)
async def sorusor(ctx):
    quiz_channel = bot.get_channel(quiz_channel_id)
    if not quiz_channel:
        return await ctx.send(embed=embed_hata("Kanal Bulunamadı", "Bilgi yarışması kanalı ayarlı değil."), delete_after=5)
    if current_question:
        return await ctx.send(embed=embed_hata("Aktif Soru Var", "Zaten cevaplanmamış bir soru var, önce o cevaplanmalı."), delete_after=5)
    ok = await post_soru(quiz_channel)
    if ok:
        try: await ctx.message.add_reaction('✅')
        except Exception: pass
    else:
        await ctx.send(embed=embed_hata("Hata", "Soru gönderilemedi."), delete_after=5)

@sorusor.error
async def sorusor_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction('❌')

@bot.command(name='bilskor', aliases=['quizskor', 'bilgiskor'])
async def bilskor(ctx):
    data = veri_yukle(QUIZ_SKOR_DOSYA, {})
    if not data:
        return await ctx.send(embed=embed_hata("Skor Tablosu", "Henüz kimse soru bilmedi!"))
    sirali = sorted(data.items(), key=lambda x: x[1]['dogru'], reverse=True)[:10]
    embed = discord.Embed(color=0xf1c40f)
    embed.set_author(
        name="📊 Bilgi Yarışması — Skor Tablosu",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty
    )
    madalya = ["🥇", "🥈", "🥉"]
    desc = f"{'─' * 30}\n"
    for i, (uid, d) in enumerate(sirali):
        prefix = madalya[i] if i < 3 else f"**#{i+1}**"
        desc += f"{prefix} **{d['isim']}** — `{d['dogru']}` doğru cevap\n"
    desc += f"{'─' * 30}"
    embed.description = desc
    embed.set_footer(text=f"{SUNUCU_ADI} • {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    await ctx.send(embed=embed)
        
@bot.command(name="takımara")
@commands.cooldown(1, 60, commands.BucketType.user)
async def takim_ara(ctx, *, mesaj="Yeni oyuncu takım arıyor! ⚽"):
    kaptan_rol = ctx.guild.get_role(KAPTAN_ROL_ID)
    embed = discord.Embed(title="📢 TRANSFER DUYURUSU", description=f"⚽ **Yeni Oyuncu Takım Arıyor!**\n\n👤 Oyuncu: {ctx.author.mention}\n\n📝 Mesaj:\n> {mesaj}\n\n🏟️ Takım başkanları ilgilenebilir!", color=0x00bfff)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text=f"{SUNUCU_ADI} Transfer Sistemi")
    await ctx.send(content=f"👔 {kaptan_rol.mention if kaptan_rol else ''} yeni transfer fırsatı!", embed=embed)

@bot.command(name="kap")
async def kap(ctx, oyuncu: discord.Member, eski_takim: str, yeni_takim: str, ucret: str = "Açıklanmadı", sozlesme: str = "Açıklanmadı"):
    yetkililer = [DEGER_YETKILISI_ROL_ID, BASKAN_ROL_ID, KAPTAN_ROL_ID]
    if not (ctx.author.id == OWNER_ID or any(ctx.author.get_role(r) for r in yetkililer)): return await ctx.send("❌ Bu komut için yetkili rolü gerekli!", delete_after=5)
    tarih = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M")
    embed = discord.Embed(title="📋 RESMİ TRANSFER BİLDİRİSİ", description=f"**{SUNUCU_ADI}** Kamuoyu Aydınlatma Platformu üzerinden aşağıdaki transfer resmi olarak tescil edilmiştir.", color=0x0d1b2a)
    embed.add_field(name="​", value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)
    embed.add_field(name="👤 Oyuncu", value=oyuncu.mention, inline=True).add_field(name="​", value="​", inline=True).add_field(name="📅 Transfer Tarihi", value=f"`{tarih}`", inline=True)
    embed.add_field(name="​", value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)
    embed.add_field(name="📤 Ayrılan Kulüp", value=f"**{eski_takim}**", inline=True).add_field(name="➡️", value="​", inline=True).add_field(name="📥 Katılan Kulüp", value=f"**{yeni_takim}**", inline=True)
    embed.add_field(name="​", value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)
    embed.add_field(name="💰 Transfer Bedeli", value=f"**{ucret}**", inline=True).add_field(name="​", value="​", inline=True).add_field(name="📋 Sözleşme Süresi", value=f"**{sozlesme}**", inline=True)
    embed.add_field(name="​", value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)
    if oyuncu.avatar: embed.set_thumbnail(url=oyuncu.avatar.url)
    if ctx.guild.icon: embed.set_author(name=f"{SUNUCU_ADI} | KAP Bildiri Sistemi", icon_url=ctx.guild.icon.url)
    embed.set_footer(text=f"Bu bildiri resmi nitelik taşımaktadır. • Yetkili: {ctx.author.display_name}")
    try: await ctx.message.delete()
    except: pass
    await ctx.send(content=oyuncu.mention, embed=embed)

# --- SUNUCU YÖNETİMİ VE ARAÇLAR ---
@bot.command(name='sil', aliases=['temizle', 'clear'])
@commands.has_permissions(manage_messages=True)
async def mesaj_sil(ctx, miktar: int = 10):
    if miktar > 100: miktar = 100
    deleted = await ctx.channel.purge(limit=miktar + 1)
    msg = await ctx.send(f"✅ **{len(deleted)-1}** adet mesaj başarıyla süpürüldü! 🧹")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name='macsaati', aliases=['msaat', 'duyuru'])
@commands.has_permissions(manage_messages=True)
async def macsaati(ctx, ev_takim: discord.Role, dep_takim: discord.Role, saat: str):
    e = discord.Embed(title=f"🚨 {SUNUCU_ADI} | HAFTANIN MAÇI", description=f"Büyük randevu için hazırlanın! \n\n⚔️ {ev_takim.mention} **vs** {dep_takim.mention}", color=0xff0000)
    e.add_field(name="🏠 Ev Sahibi", value=ev_takim.mention, inline=True).add_field(name="✈️ Deplasman", value=dep_takim.mention, inline=True).add_field(name="⏰ Başlama Saati", value=f"**{saat}**", inline=False)
    e.set_thumbnail(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3RreXByZzZ4Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxxZ29D5S4o/giphy.gif")
    e.set_image(url="https://media1.tenor.com/m/dmH0nGUtvGQAAAAC/futbol-entrenar.gif")
    e.set_footer(text=f"Duyuruyu Yapan Hakem: {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    e.timestamp = datetime.now(timezone.utc)
    await ctx.send(content=f"{ev_takim.mention} {dep_takim.mention} | **Maç saatiniz belli oldu!**", embed=e)

@bot.command(name='post')
@commands.cooldown(1, 60, commands.BucketType.user)
async def post_olustur(ctx, *, icerik: str = f"{SUNUCU_ADI} Paylaşımı"):
    if ctx.channel.id != INSTAGRAM_KANAL_ID: return await ctx.send(f"❌ Bu komutu sadece <#{INSTAGRAM_KANAL_ID}> kanalında kullanabilirsin!", delete_after=5)
    default_fotolar = ["https://source.unsplash.com/800x500/?football", "https://source.unsplash.com/800x500/?stadium"]
    if ctx.message.attachments and any(ctx.message.attachments[0].filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif']):
        foto_url = ctx.message.attachments[0].url
    else: foto_url = random.choice(default_fotolar)
    embed = discord.Embed(description=f"**{ctx.author.display_name}**\n{icerik}", color=0xe1306c)
    embed.set_author(name=f"{ctx.author.display_name} • {SUNUCU_ADI}", icon_url=ctx.author.display_avatar.url)
    embed.set_image(url=foto_url)
    embed.add_field(name="❤️ Beğeni", value=f"**{random.randint(100, 1500)}**", inline=True).add_field(name="💬 Yorum", value=f"**{random.randint(5, 150)}**", inline=True)
    embed.add_field(name="💭 Öne çıkan yorum", value=random.choice(["🔥 Efsane olmuş!", "⚽ Kral hareket!", "💯 Bu ne kalite!"]), inline=False)
    embed.set_footer(text=f"{ctx.author.display_name} • Paylaşım")
    mesaj = await ctx.send(embed=embed)
    stat_ekle(str(ctx.author.id), 'post')
    await mesaj.add_reaction("❤️"); await mesaj.add_reaction("💬"); await mesaj.add_reaction("🔥")
    try: await ctx.message.delete()
    except: pass

@bot.command(name="toplurolver")
@commands.has_permissions(manage_roles=True)
async def toplurolver(ctx, *args: Union[discord.Member, discord.Role]):
    if len(args) < 2: return await ctx.send("❌ **Eksik Kullanım!**\nDoğrusu: `.toplurolver @kişi @kişi @rol`")
    members = [a for a in args if isinstance(a, discord.Member)]
    roles = [a for a in args if isinstance(a, discord.Role)]
    if not roles: return await ctx.send("❌ **Hata:** En az bir rol etiketlemelisin!")
    target_role = roles[0]
    msg = await ctx.send(f"🔄 **{len(members)}** kullanıcı için **{target_role.name}** rolü dağıtılıyor...")
    basarili, hata = [], []
    for member in members:
        try:
            if target_role not in member.roles:
                await member.add_roles(target_role)
                basarili.append(f"`{member.name}`")
        except: hata.append(f"`{member.name}`")
    sonuc_embed = discord.Embed(title=f"🛡️ {SUNUCU_ADI} | İşlem Raporu", color=0x2ecc71, timestamp=ctx.message.created_at)
    sonuc_embed.add_field(name="📦 Verilen Rol", value=target_role.mention, inline=False)
    if basarili: sonuc_embed.add_field(name="✅ Başarılı", value=", ".join(basarili), inline=False)
    if hata: sonuc_embed.add_field(name="⚠️ Hata/Yetki Yetersiz", value=", ".join(hata), inline=False)
    sonuc_embed.set_footer(text=f"Komutu Kullanan: {ctx.author.name}")
    await msg.edit(content=None, embed=sonuc_embed)

# --- TICKET SİSTEMİ ---
TICKET_KATEGORILER = [
    discord.SelectOption(label="Transfer İşlemi",  description="Oyuncu transferi veya bonservis talebi", emoji="⚽"),
    discord.SelectOption(label="Değer / Bütçe", description="Piyasa değeri ve bütçe ile ilgili talepler", emoji="💰"),
    discord.SelectOption(label="Şikayet / Öneri", description="Şikayet bildir veya öneri sun", emoji="📋"),
    discord.SelectOption(label="Satın Alım", description="Sunucu içi satın alım işlemleri", emoji="🛒"),
    discord.SelectOption(label="Diğer", description="Yukarıdaki kategorilere uymayan talepler", emoji="🔧"),
]
class TicketDropdown(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="📂 Talep kategorini seç...", options=TICKET_KATEGORILER, min_values=1, max_values=1)
    async def callback(self, interaction: discord.Interaction):
        guild, member = interaction.guild, interaction.user
        if not guild or not isinstance(member, discord.Member): return
        category = guild.get_channel(DESTEK_KATEGORI_ID)
        if not isinstance(category, discord.CategoryChannel):
            return await interaction.response.send_message("❌ Ticket kategorisi bulunamadı.", ephemeral=True)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.get_role(YETKILI_1_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            guild.get_role(YETKILI_2_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }
        kanal_adi = f"🎫︱{member.display_name[:20].lower().replace(' ', '-')}"
        channel = await guild.create_text_channel(name=kanal_adi, category=category, overwrites=overwrites, topic=f"Talep sahibi: {member} | Kategori: {self.values[0]}")
        await interaction.response.send_message(f"✅ Destek kanalın oluşturuldu → {channel.mention}", ephemeral=True)
        embed = discord.Embed(title=f"🎫 {SUNUCU_ADI} — DESTEK TALEBİ", color=0x7c3aed)
        embed.add_field(name="👤 Talep Sahibi", value=member.mention, inline=True).add_field(name="📂 Kategori", value=f"`{self.values[0]}`", inline=True)
        embed.add_field(name="📌 Bilgi", value="Yetkililerimiz en kısa sürede seninle ilgilenecek.\nLütfen talebini **kısa ve net** şekilde açıkla.", inline=False)
        embed.set_footer(text="İşin bitince 'Kanalı Kapat' butonuna bas.")
        ping_str = f"<@&{YETKILI_1_ID}> <@&{YETKILI_2_ID}>"
        close_view = View(timeout=None)
        close_btn = Button(label="🔒 Kanalı Kapat", style=discord.ButtonStyle.danger)
        async def close_callback(inter: discord.Interaction):
            await inter.response.send_message("⚠️ Kanal **5 saniye** içinde siliniyor...")
            await asyncio.sleep(5)
            if isinstance(inter.channel, discord.TextChannel): await inter.channel.delete()
        close_btn.callback = close_callback
        close_view.add_item(close_btn)
        await channel.send(content=f"||{ping_str}|| → {member.mention}", embed=embed, view=close_view)
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None); self.add_item(TicketDropdown())
@bot.command(name="ticket-kur")
@commands.has_permissions(administrator=True)
async def ticket_kur(ctx: commands.Context):
    if ctx.channel.id != TICKET_KANAL_ID: return await ctx.send(f"❌ Bu komutu sadece <#{TICKET_KANAL_ID}> kanalında kullanabilirsin!", delete_after=5)
    panel = discord.Embed(title=f"🎫 {SUNUCU_ADI} | DESTEK MERKEZİ", description="Sunucumuzda bir sorunla mı karşılaştın? Transfer, değer veya başka bir konuda yardım mı istiyorsun?\n\n**Aşağıdan kategorini seç** — yetkili ekibimiz sana özel kanal açsın.", color=0x7c3aed)
    if ctx.guild and ctx.guild.icon: panel.set_thumbnail(url=ctx.guild.icon.url)
    panel.set_footer(text=f"{SUNUCU_ADI} • Destek Merkezi")
    await ctx.message.delete()
    await ctx.send(embed=panel, view=TicketView())

# --- STATS & YARDIM ---
@bot.command(name="stat")
async def stat_goster(ctx, uye: discord.Member = None):
    uye = uye or ctx.author
    data = stat_oku()
    uid = str(uye.id)
    stats = data.get(uid, {})
    if not stats: return await ctx.send(f"❌ **{uye.display_name}** için kayıtlı stat bulunamadı!")
    embed = discord.Embed(title=f"📊 {uye.display_name} — İstatistikler", color=0x3498db)
    if uye.avatar: embed.set_thumbnail(url=uye.avatar.url)
    for key, isim in STAT_ISIMLER.items():
        if val := stats.get(key, 0): embed.add_field(name=isim, value=f"**{val}**", inline=True)
    if not embed.fields: embed.description = "Henüz hiç stat yok."
    embed.set_footer(text=f"{SUNUCU_ADI} • Stat Sistemi")
    await ctx.send(embed=embed)

@bot.command(name="stat-sıfırla")
@commands.has_permissions(administrator=True)
async def stat_sifirla(ctx, uye: discord.Member = None):
    data = stat_oku()
    if uye is None:
        count = len(data)
        data.clear()
        desc = f"**{count}** oyuncunun tüm statları temizlendi."
    else:
        uid = str(uye.id)
        if uid in data: data.pop(uid)
        desc = f"{uye.mention} adlı oyuncunun statları temizlendi."
    stat_yaz(data)
    embed = discord.Embed(title="🔄 Statlar Sıfırlandı", description=desc, color=0xe74c3c)
    embed.set_footer(text=f"{SUNUCU_ADI} • Yetkili: {ctx.author.display_name}")
    await ctx.send(embed=embed)

class HelpMenu(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.ctx.author

    def get_embed(self, kategori: str, icerik: str) -> discord.Embed:
        e = discord.Embed(color=CL_MAVI)
        e.set_author(
            name=f"💎 {SUNUCU_ADI} — {kategori}",
            icon_url=self.ctx.guild.icon.url if self.ctx.guild and self.ctx.guild.icon else None
        )
        e.description = icerik
        e.set_footer(text=f"Prefix: .  •  {SUNUCU_ADI}  •  {datetime.now().strftime('%H:%M')}")
        return e

    @discord.ui.button(label="🏠 Ana Menü", style=discord.ButtonStyle.secondary, row=2)
    async def ana_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        icerik = (
            "Aşağıdaki butonlardan bir kategori seçerek komutları inceleyebilirsin.\n\n"
            "⚽ **Oyunlar** — Eğlence ve mini oyunlar\n"
            "💰 **Piyasa & Değer** — Oyuncu değeri ve sıralamalar\n"
            "💵 **Ekonomi** — Para sistemi\n"
            "📋 **Sunucu** — Kayıt, transfer, maç\n"
            "🛠️ **Araçlar** — Yetkili komutları"
        )
        await interaction.response.edit_message(embed=self.get_embed("Yardım Menüsü", icerik))

    @discord.ui.button(label="⚽ Oyunlar", style=discord.ButtonStyle.primary)
    async def oyunlar(self, interaction: discord.Interaction, button: discord.ui.Button):
        icerik = (
            "`.duello @kişi` — Penaltı düellosu yap\n"
            "`.halısaha @kişi` — Maç simülasyonu oyna\n"
            "`.penaltı` — Penaltı at (butonlarla)\n"
            "`.yazıtura` — Yazı-tura oyna\n"
            "`.roll [sayı/seçenek]` — Rastgele seçim yap\n"
            "`.ship @k1 @k2` — Aşk uyumunu ölç\n"
            "`.kaçcm [@kişi]` — Boy ölçümü yap\n"
            "`.çiz` — Oyuncu analiz grafiği oluştur"
        )
        await interaction.response.edit_message(embed=self.get_embed("⚽ Oyunlar", icerik))

    @discord.ui.button(label="💰 Piyasa & Değer", style=discord.ButtonStyle.success)
    async def piyasa(self, interaction: discord.Interaction, button: discord.ui.Button):
        icerik = (
            "`.değerver @oyuncu 5M sebep` — Değer artır\n"
            "`.değersil @oyuncu 5M sebep` — Değer düşür\n"
            "`.endeğerli` — En değerli 10 oyuncu\n"
            "`.endeğerliler` — Detaylı oyuncu sıralaması\n"
            "`.takımdeğer` — Takımları değere göre sırala\n"
            "`.ant` — Antrenman yap (saatlik)\n"
            "`.stat [@kişi]` — İstatistikleri görüntüle"
        )
        await interaction.response.edit_message(embed=self.get_embed("💰 Piyasa & Değer", icerik))

    @discord.ui.button(label="💵 Ekonomi", style=discord.ButtonStyle.success, row=1)
    async def ekonomi(self, interaction: discord.Interaction, button: discord.ui.Button):
        icerik = (
            "`.para [@kişi]` — Bakiye bilgilerini gör\n"
            "`.yatır <miktar>` — Bankaya para yatır\n"
            "`.çek <miktar>` — Bankadan para çek\n"
            "`.ver @kişi <miktar>` — Birinine para gönder\n"
            "`.zenginler` — En zengin 10 kişi\n"
            "`.para-ver @kişi <miktar>` — (Admin) Para ekle\n"
            "`.para-sil @kişi <miktar>` — (Admin) Para sil\n"
            "`.para-sıfırla @kişi` — (Admin) Tüm parayı sıfırla"
        )
        await interaction.response.edit_message(embed=self.get_embed("💵 Ekonomi", icerik))

    @discord.ui.button(label="📋 Sunucu", style=discord.ButtonStyle.danger, row=1)
    async def sunucu(self, interaction: discord.Interaction, button: discord.ui.Button):
        icerik = (
            "`.kayıt @kişi <isim>` — Üye kaydı yap\n"
            "`.kver @kişi` — Üyeyi kayıtsıza al\n"
            "`.transfer ...` — Transfer duyurusu yap\n"
            "`.ilanver ...` — Transfer listesine ekle\n"
            "`.macsaati @ev @dep saat` — Maç duyurusu\n"
            "`.post [içerik]` — Instagram tarzı post\n"
            "`.takım @rol` — Takım bilgilerini gör\n"
            "`.takımara` — Takım aradığını duyur"
        )
        await interaction.response.edit_message(embed=self.get_embed("📋 Sunucu", icerik))

    @discord.ui.button(label="🛠️ Araçlar", style=discord.ButtonStyle.secondary, row=1)
    async def araclar(self, interaction: discord.Interaction, button: discord.ui.Button):
        icerik = (
            "`.sil <miktar>` — Mesajları temizle\n"
            "`.toplurolver @kişiler @rol` — Toplu rol ver\n"
            "`.ticket-kur` — (Admin) Ticket panelini kur\n"
            "`.stat-sıfırla [@kişi]` — (Admin) Statları sıfırla\n"
            "`.ping` — Bot gecikmesini kontrol et"
        )
        await interaction.response.edit_message(embed=self.get_embed("🛠️ Araçlar", icerik))

@bot.command(name="help", aliases=["yardım"])
async def help_menu(ctx):
    view = HelpMenu(ctx)
    icerik = (
        "Aşağıdaki butonlardan bir kategori seçerek komutları inceleyebilirsin.\n\n"
        "⚽ **Oyunlar** — Eğlence ve mini oyunlar\n"
        "💰 **Piyasa & Değer** — Oyuncu değeri ve sıralamalar\n"
        "💵 **Ekonomi** — Para sistemi\n"
        "📋 **Sunucu** — Kayıt, transfer, maç\n"
        "🛠️ **Araçlar** — Yetkili komutları"
    )
    await ctx.send(embed=view.get_embed("Yardım Menüsü", icerik), view=view)

# --- BOT YÖNETİMİ ---
@bot.command(name="sunucuyakatıl")
async def sunucuya_katil(ctx, sunucu_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ Bu komutu sadece bot sahibi kullanabilir!", delete_after=5)

    invite_url = (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={bot.user.id}"
        f"&permissions=8"
        f"&scope=bot"
        f"&guild_id={sunucu_id}"
    )

    embed = discord.Embed(
        title="🔗 Sunucuya Katılım Linki",
        description=(
            f"**Sunucu ID:** `{sunucu_id}`\n\n"
            f"Aşağıdaki butona tıklayarak botu o sunucuya ekleyebilirsin.\n"
            f"⚠️ O sunucuda **Yönetici** yetkine sahip olman gerekiyor."
        ),
        color=0x7c3aed
    )
    embed.set_footer(text=f"{SUNUCU_ADI} • Bot Yönetimi")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Sunucuya Ekle", url=invite_url, style=discord.ButtonStyle.link, emoji="🤖"))

    try:
        await ctx.author.send(embed=embed, view=view)
        await ctx.send("✅ Link DM kutuna gönderildi!", delete_after=5)
    except discord.Forbidden:
        await ctx.send(embed=embed, view=view)

@bot.command(name="sunucular")
@commands.is_owner()
async def sunucular(ctx):
    liste = ""
    for i, guild in enumerate(bot.guilds, 1):
        liste += f"**{i}. {guild.name}** | Üye: {guild.member_count}\n"
    embed = discord.Embed(title="📊 Botun Sunucuları", description=liste, color=0x2b2d31)
    try:
        await ctx.author.send(embed=embed)
        await ctx.send("✅ Sunucu listesi DM kutuna gönderildi.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ DM kutun kapalı olduğu için listeyi gönderemedim!")

@bot.command(name="ayrıl")
@commands.is_owner()
async def ayril(ctx, sunucu_id: int):
    guild = bot.get_guild(sunucu_id)
    if guild:
        await guild.leave()
        await ctx.send(f"✅ **{guild.name}** sunucusundan ayrıldım.")
    else:
        await ctx.send(f"❌ `{sunucu_id}` ID'li sunucu bulunamadı.")

@bot.command(name="buserverdışıheryerdenayrıl")
@commands.is_owner()
async def buserverdışıheryerdenayrıl(ctx):
    mevcut_sunucu_id = ctx.guild.id
    sayac = 0
    for guild in bot.guilds:
        if guild.id != mevcut_sunucu_id:
            await guild.leave()
            sayac += 1
    await ctx.send(f"✅ Bu sunucu dışındaki **{sayac}** sunucudan ayrıldım.")

# =============================================================
# 7. BOTU BAŞLATMA
# =============================================================
@tasks.loop(minutes=4)
async def self_ping():
    pass 

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("❌ HATA: DISCORD_TOKEN ortam değişkeni bulunamadı!")
    else:
        try:
            keep_alive()
            print("✅ Keep-alive sunucusu başlatıldı.")
        except Exception as e:
            print(f"⚠️ Keep-alive başlatılamadı: {e}")

        print("🚀 Bot başlatılıyor...")
        bot.run(token)
