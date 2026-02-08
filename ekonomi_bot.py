import yfinance as yf
import os
from datetime import datetime

def ekonomi_sayfasi_olustur():
    # 1. VERİ ÇEKME
    altin_ticker = yf.Ticker("GC=F")
    gumus_ticker = yf.Ticker("SI=F")
    dolar_tl = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]

    g_altin = round((altin_ticker.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl, 2)
    g_gumus = round((gumus_ticker.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl, 2)
    guncelleme = datetime.now().strftime('%d/%m/%Y %H:%M')

    # 2. HABERLERİ ÇEKME (Ücretsiz yfinance haberleri)
    haberler_html = ""
    all_news = altin_ticker.news[:3] + gumus_ticker.news[:3] # En güncel 6 haber
    
    for haber in all_news:
        baslik = haber.get('title', 'Haber Başlığı Yok')
        link = haber.get('link', '#')
        kaynak = haber.get('publisher', 'Ekonomi Servisi')
        haberler_html += f"""
        <div class="news-item">
            <a href="{link}" target="_blank">{baslik}</a>
            <p style="font-size: 0.8em; color: #888;">Kaynak: {kaynak}</p>
        </div>"""

    # 3. HTML TASARIMI
    html_icerik = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Canlı Ekonomi Takip Portalı</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; }}
            .card-grid {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 20px; }}
            .card {{ background: #1e293b; padding: 20px; border-radius: 12px; width: 220px; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }}
            .price {{ font-size: 1.8em; color: #fbbf24; font-weight: bold; margin: 10px 0; }}
            .label {{ color: #94a3b8; font-weight: 600; }}
            .news-section {{ margin-top: 40px; text-align: left; background: #1e293b; padding: 20px; border-radius: 12px; }}
            .news-item {{ border-bottom: 1px solid #334155; padding: 10px 0; }}
            .news-item a {{ color: #38bdf8; text-decoration: none; font-weight: 500; }}
            .news-item a:hover {{ text-decoration: underline; }}
            .footer {{ margin-top: 30px; color: #64748b; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📈 Canlı Ekonomi Takip</h1>
            <p>Piyasalardaki anlık değişimler ve son haberler.</p>
            
            <div class="card-grid">
                <div class="card"><div class="label">Gram Altın</div><div class="price">{g_altin} TL</div></div>
                <div class="card"><div class="label">Gram Gümüş</div><div class="price">{g_gumus} TL</div></div>
                <div class="card"><div class="label">Dolar / TL</div><div class="price">{round(dolar_tl, 2)} TL</div></div>
            </div>

            <div class="news-section">
                <h3>📰 Son Gelişmeler</h3>
                {haberler_html if haberler_html else "<p>Şu an yeni haber bulunamadı.</p>"}
            </div>

            <div class="footer">Son Güncelleme: {guncelleme} | Veriler hobi amaçlıdır.</div>
        </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_icerik)

if __name__ == "__main__":
    ekonomi_sayfasi_olustur()
