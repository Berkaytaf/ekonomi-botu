import yfinance as yf
import os
from datetime import datetime

def haber_getir(ticker_obj, kategori_adi):
    news_list = ticker_obj.news[:3] # Her kategoriden son 3 haber
    if not news_list:
        return f"<p style='color:#64748b;'>{kategori_adi} için şu an yeni haber yok.</p>"
    
    html = ""
    for haber in news_list:
        baslik = haber.get('title', 'Başlık Yok')
        link = haber.get('link', '#')
        html += f'<div class="news-item"><a href="{link}" target="_blank">● {baslik}</a></div>'
    return html

def ekonomi_sayfasi_olustur():
    # 1. VERİLERİ ÇEK
    altin_t = yf.Ticker("GC=F")
    gumus_t = yf.Ticker("SI=F")
    genel_t = yf.Ticker("USDTRY=X")
    dolar_tl = genel_t.history(period="1d")['Close'].iloc[-1]

    g_altin = round((altin_t.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl, 2)
    g_gumus = round((gumus_t.history(period="1d")['Close'].iloc[-1] / 31.1035) * dolar_tl, 2)
    guncelleme = datetime.now().strftime('%d/%m/%Y %H:%M')

    # 2. PENCERELERİ HAZIRLA
    altin_haberleri = haber_getir(altin_t, "Altın")
    gumus_haberleri = haber_getir(gumus_t, "Gümüş")
    genel_haberler = haber_getir(genel_t, "Genel Ekonomi")

    # 3. HTML & CSS
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
            .price-card {{ background: #1e293b; padding: 15px 25px; border-radius: 10px; border: 1px solid #334155; min-width: 180px; }}
            .price-card span {{ display: block; font-size: 0.8em; color: #94a3b8; }}
            .price-card b {{ font-size: 1.5em; color: #fbbf24; }}
            
            .window-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: auto; }}
            .window {{ background: #111827; border-radius: 12px; border: 1px solid #1f2937; overflow: hidden; }}
            .window-header {{ background: #1f2937; padding: 10px 15px; font-weight: bold; font-size: 0.9em; display: flex; align-items: center; }}
            .window-header::before {{ content: ''; width: 10px; height: 10px; background: #ef4444; border-radius: 50%; margin-right: 8px; box-shadow: 15px 0 #fbbf24, 30px 0 #22c55e; }}
            .window-content {{ padding: 15px; min-height: 150px; }}
            
            .news-item {{ border-bottom: 1px solid #1f2937; padding: 8px 0; font-size: 0.9em; }}
            .news-item:last-child {{ border: none; }}
            .news-item a {{ color: #38bdf8; text-decoration: none; line-height: 1.4; }}
            .news-item a:hover {{ color: #7dd3fc; }}
            .footer {{ text-align: center; margin-top: 40px; color: #4b5563; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Ekonomi Takip Merkezi</h1>
            <p>Veriler saatlik olarak otomatik güncellenmektedir.</p>
        </div>

        <div class="price-bar">
            <div class="price-card"><span>Gram Altın</span><b>{g_altin} TL</b></div>
            <div class="price-card"><span>Gram Gümüş</span><b>{g_gumus} TL</b></div>
            <div class="price-card"><span>Dolar / TL</span><b>{round(dolar_tl, 2)} TL</b></div>
        </div>

        <div class="window-grid">
            <div class="window">
                <div class="window-header">Altın Haberleri</div>
                <div class="window-content">{altin_haberleri}</div>
            </div>
            <div class="window">
                <div class="window-header">Gümüş Haberleri</div>
                <div class="window-content">{gumus_haberleri}</div>
            </div>
            <div class="window">
                <div class="window-header">Genel Ekonomi</div>
                <div class="window-content">{genel_haberler}</div>
            </div>
        </div>

        <div class="footer">Son Güncelleme: {guncelleme} | Kaynak: Yahoo Finance</div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_icerik)

if __name__ == "__main__":
    ekonomi_sayfasi_olustur()
