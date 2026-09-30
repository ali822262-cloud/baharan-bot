import urllib.request, urllib.parse, json, time, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "GAPGPTMASKTOKENid05t313fgdX0X"
API = "https://tapi.bale.ai/bot" + TOKEN

KNOWLEDGE = {
    "سلام": "سلام و درود! 🌱 به پشتیبانی تخصصی شرکت کلات آهن بهاران خوش آمدید.\nچطور می‌توانم در زمینه تغذیه باغات، کودها و رفع مشکلات خاک (شوری/قلیاییت) کمکتان کنم؟",
    "آهن": "📌 **کلات آهن بهاران:**\nکمبود آهن باعث زردی برگ‌های جوان (کلروز) می‌شود.\nکلات‌های آهن بهاران با فرمولاسیون ویژه (EDDHA / HBED) در خاک‌های آهکی و قلیایی ایران پایداری بالا و جذب فوق‌العاده دارند.\nاطلاعات بیشتر: https://baharan.co/",
    "شوری": "📌 **راهکار شوری و قلیاییت خاک:**\nشرکت کلات آهن بهاران ترکیبات اصلاح‌کننده خاک و کودهای اختصاصی مقاوم به تنش شوری ارائه می‌دهد تا جذب عناصر غذایی در شرایط سخت تسهیل شود.",
    "تغذیه": "📌 **تغذیه زمستانه و بهاره باغات:**\nاستفاده از چالکود زمستانه و کودهای فروت‌ست در اوایل فصل برای بهبود گل‌انگیزی و باردهی درختان بسیار ضروری است.",
    "محصولات": "🌱 **سبد محصولات بهاران:**\n۱. کودهای کلاته ریزمغذی (آهن، روی، منگنز)\n۲. خانواده محصولات فرمولایف و مانتیس\n۳. کودهای NPK و محرک‌های رشد\nمشاهده کاتالوگ کامل: https://baharan.co/products",
    "تماس": "📞 **ارتباط با واحد فروش و مشاوره فنی:**\nاصفهان، شرکت کلات آهن بهاران\nوب‌سایت: https://baharan.co/"
}

def get_smart_reply(text):
    text_lower = text.strip().lower()
    for key, ans in KNOWLEDGE.items():
        if key in text_lower:
            return ans
    return ("🌱 پیام شما دریافت شد.\n"
            "برای مشاوره تخصصی در زمینه کلات آهن، اصلاح شوری خاک یا محصولات باغبانی به سایت سر بزنید:\n"
            "🌐 https://baharan.co/\n"
            "یا کلماتی مانند «آهن»، «شوری»، «محصولات» یا «تماس» را ارسال کنید.")

def call(method, data=None):
    url = API + "/" + method
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except Exception as e:
        print("API error:", e)
        return None

offset = 0

def run_bot():
    global offset
    call("deleteWebhook", {"url": ""})
    while True:
        res = call("getUpdates", {"offset": offset, "timeout": 30})
        if not res or not res.get("ok"):
            time.sleep(3)
            continue
        for upd in res.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message")
            if not msg or "text" not in msg:
                continue
            text, chat_id = msg["text"], msg["chat"]["id"]
            reply = get_smart_reply(text)
            call("sendMessage", {"chat_id": chat_id, "text": reply})

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Baharan Bot is Running!")
    def log_message(self, *a):
        pass

threading.Thread(target=run_bot, daemon=True).start()
port = int(os.environ.get("PORT", 10000))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
