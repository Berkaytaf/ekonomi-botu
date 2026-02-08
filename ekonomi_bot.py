import yfinance as yf
import os
from datetime import datetime

def haber_getir(ticker_list, kategori_adi):
    all_html = ""
    found_news = 0
    for t in ticker_list:
        ticker_obj = yf.Ticker(t)
        news = ticker_obj.news[:2] # Her sembolden 2 haber
        for h in news:
            baslik = h.get('title')
            link = h.get('link', '#')
            if baslik and found_news < 4:
                all_html += f'<div class="news-item"><a href="{link}" target="_blank">● {baslik}</a></div>'
                found_news += 1
    
    return all_html if all_html else f"<p style='color:#64748b;'>{kategori_adi} piyasası şu an durgun.</p>"

def ekonomi_sayfasi_olustur():
    # 1. VERİLERİ ÇEK
    altin_v = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
    gumus_v = yf.Ticker("SI=F").history(period="1d")['Close'].iloc[-1]
    dolar_tl = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]

    g_altin = round((altin_v / 31.1035) * dolar_tl, 2)
    g_gumus = round((gumus_v / 31.1035) * dolar_tl, 2)
    guncelleme = datetime.now().strftime('%d/%m/%Y %H:%M')

    # 2. HABER PENCERELERİ (Genişletilmiş Kaynaklar)
    # Haber gelme ihtimalini artırmak için benzer sembolleri ekledik
    altin_h = haber_getir(["GC=F", "GLD", "AUY"], "Altın")
    gumus_h = haber_getir(["SI=F", "SLV"], "Gümüş")
    genel_h = haber_getir(["USDTRY=X", "TRY=X", "^TNX"], "Genel Ekonomi")

    # 3. YENİ PENCERELİ TASARIM
    html_icerik = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ekonomi Takip Merkezi</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; background: #0b0f19; color: #e2e8f0; margin: 0; padding: 20px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .price-bar {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
            .price-card {{ background: #1e293b; padding: 15px 25px; border-radius: 10px; border: 1px solid #334155; min-width: 180px; text-align:center; }}
            .price-card span {{ display: block; font-size: 0.8em; color: #94a3b8; }}
            .price-card b {{ font-size: 1.5em; color: #fbbf24; }}
            
            .window-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; max-width: 1200px; margin: auto; }}
            .window {{ background: #111827; border-radius: 12px; border: 1px solid #1f2937; overflow: hidden; }}
            .window-header {{ background: #1f2937; padding: 10px 15px; font-weight: bold; font-size: 0.9em; display: flex; align-items: center; }}
            .window-header::before {{ content: ''; width: 10px; height: 10px; background: #ef4444; border-radius: 50%; margin-right: 8px; box-shadow: 15px 0 #fbbf24, 30px 0 #22c55e; }}
            .window-content {{ padding: 15px; min-height: 120px; }}
            
            .news-item {{ border-bottom: 1px solid #1f2937; padding: 10px 0; font-size: 0.85em; }}
            .news-item a {{ color: #38bdf8; text-decoration: none; line-height: 1.4; }}
            .footer {{ text-align: center; margin-top: 40px; color: #4b5563; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="header"><h1>📊 Ekonomi Takip Merkezi</h1><p>Saatlik Otomatik Güncelleme</p></div>
        <div class="price-bar">
            <div class="price-card"><span>Gram Altın</span><b>{g_altin} TL</b></div>
            <div class="price-card"><span>Gram Gümüş</span><b>{g_gumus} TL</b></div>
            <div class="price-card"><span>Dolar / TL</span><b>{round(dolar_tl, 2)} TL</b></div>
        </div>
        <div class="window-grid">
            <div class="window"><div class="window-header">Altın Haberleri</div><div class="window-content">{altin_h}</div></div>
            <div class="window"><div class="window-header">Gümüş Haberleri</div><div class="window-content">{gumus_h}</div></div>
            <div class="window"><div class="window-header">Genel Ekonomi</div><div class="window-content">{genel_h}</div></div>
        </div>
        <div class="footer">Son Güncelleme: {guncelleme} | Veriler hobi amaçlıdır.</div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_icerik)

if __name__ == "__main__":
    ekonomi_sayfasi_olustur()
