import yfinance as yf
import os
from datetime import datetime

def ekonomi_sayfasi_olustur():
    # 1. VERİ ÇEKME
    altin = yf.Ticker("GC=F")
    gumus = yf.Ticker("SI=F")
    dolar_tl = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]

    g_altin = round((altin.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl, 2)
    g_gumus = round((gumus.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl, 2)
    guncelleme = datetime.now().strftime('%d/%m/%Y %H:%M')

    # 2. HTML TASARIMI (Modern ve Karanlık Tema)
    html_icerik = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Berkay Ekonomi Portalı</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #121212; color: white; text-align: center; padding: 50px; }}
            .card {{ background: #1e1e1e; padding: 20px; border-radius: 15px; display: inline-block; width: 300px; margin: 10px; border: 1px solid #333; }}
            .price {{ font-size: 2em; color: #f1c40f; font-weight: bold; }}
            .label {{ color: #bbb; margin-bottom: 10px; }}
            .footer {{ margin-top: 30px; color: #666; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <h1>📊 Berkay Ekonomi Portalı</h1>
        <p>Abi senin için anlık güncelleniyor.</p>
        
        <div class="card">
            <div class="label">Gram Altın</div>
            <div class="price">{g_altin} TL</div>
        </div>

        <div class="card">
            <div class="label">Gram Gümüş</div>
            <div class="price">{g_gumus} TL</div>
        </div>

        <div class="card">
            <div class="label">Dolar/TL</div>
            <div class="price">{round(dolar_tl, 2)} TL</div>
        </div>

        <div class="footer">Son Güncelleme: {guncelleme} | Yatırım tavsiyesi değildir abi!</div>
    </body>
    </html>
    """

    # 3. DOSYAYI KAYDET
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_icerik)

if __name__ == "__main__":
    ekonomi_sayfasi_olustur()
