import yfinance as yf
import requests
import os
import pandas as pd

def analiz_et(rsi):
    if rsi < 30: return "📉 Çok düştü abi, buralardan tepki gelebilir (Alım fırsatı mı?)"
    elif rsi > 70: return "📈 Çok şişti abi, buralardan kâr satışı gelebilir (Dikkat!)"
    else: return "↕️ Trend şu an dengeli, sert bir hareket görünmüyor."

def ekonomi_raporu():
    try:
        # 1. VERİ ÇEKME (Altın, Gümüş, Dolar)
        altin = yf.Ticker("GC=F")
        gumus = yf.Ticker("SI=F")
        dolar_tl = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]

        # 2. RSI HESAPLAMA (Geleceği tahmin etmek için teknik gösterge)
        # Son 14 günlük veriyi alıp basit bir RSI hesabı yapıyoruz
        def get_rsi(ticker):
            hist = ticker.history(period="20d")
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            return 100 - (100 / (1+rs.iloc[-1]))

        rsi_altin = get_rsi(altin)
        
        # 3. FİYAT HESAPLAMA (Gram Bazında)
        g_altin = (altin.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl
        g_gumus = (gumus.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl

        # 4. HABER ANALİZİ (Trende göre basit yorum)
        # Gemini'ye para vermemek için fiyatın dünkü kapanışa göre yönüne bakıyoruz
        prev_altin = altin.history(period="2d")['Close'].iloc[0]
        yon = "🚀 Yükseliş eğilimi var" if g_altin > (prev_altin/31.1035)*dolar_tl else "🔻 Hafif geri çekilme var"

        # 5. MESAJI OLUŞTURMA
        mesaj = (
            f"🔔 *ABİ EKONOMİ RAPORU GELDİ*\n\n"
            f"💰 *Gram Altın:* {round(g_altin, 2)} TL\n"
            f"🥈 *Gram Gümüş:* {round(g_gumus, 2)} TL\n"
            f"💵 *Dolar/TL:* {round(dolar_tl, 2)} TL\n\n"
            f"📊 *Piyasa Yorumu:* {yon}\n"
            f"🔍 *Teknik Analiz:* {analiz_et(rsi_altin)}\n\n"
            f"⚠️ _Not: Bunlar hobi amaçlı verilerdir abi, yatırım tavsiyesi değildir!_"
        )

        # Telegram Gönderimi
        token = os.getenv("TELE_TOKEN")
        chat_id = os.getenv("TELE_CHAT_ID")
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": mesaj, "parse_mode": "Markdown"})

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    ekonomi_raporu()
