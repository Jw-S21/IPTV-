import requests
from bs4 import BeautifulSoup
import re
import time

# الرابط الأساسي الذي يحتوي على قائمة المسلسلات
BASE_URL = "https://asd.pics/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86/ramadan-series-2026/"

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://asd.pics/'
    }
    session = requests.Session()
    
    try:
        print("1. الدخول لصفحة تصنيف رمضان 2026...")
        response = session.get(BASE_URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج روابط المسلسلات الفردية من صفحة التصنيف
        # نبحث عن المقالات أو الروابط التي تؤدي لصفحات المسلسلات
        articles = soup.find_all('article')
        series_links = []
        for art in articles:
            a_tag = art.find('a', href=True)
            if a_tag:
                series_links.append((a_tag.get('title') or "مسلسل", a_tag['href']))
        
        print(f"تم العثور على {len(series_links)} مسلسل. نبدأ الغوص في الحلقات...")

        m3u_content = "#EXTM3U\n"
        
        for title, series_url in series_links:
            try:
                print(f"جاري فحص: {title}...")
                # الدخول لصفحة المسلسل/الحلقة
                res = session.get(series_url, headers=headers, timeout=15)
                
                # البحث عن رابط الفيديو المباشر داخل الصفحة
                # نركز على النمط الذي اكتشفته أنت في الـ Elements
                video_match = re.search(r'src="(https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+video\.mp4)"', res.text)
                
                if video_match:
                    video_url = video_match.group(1)
                    m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
                    print(f"✅ تم استخراج الرابط لـ {title}")
                else:
                    # محاولة ثانية ببحث أوسع عن أي mp4
                    alt_match = re.search(r'(https?://[^\s"\'<>]+video\.mp4)', res.text)
                    if alt_match:
                        video_url = alt_match.group(1)
                        m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
                
                # ننتظر ثانية بين كل مسلسل لتجنب الحظر
                time.sleep(1)
                
            except Exception as e:
                print(f"فشل استخراج {title}: {e}")
                continue

        # حفظ الملف النهائي
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("--- تم تحديث قائمة M3U بنجاح ---")

    except Exception as e:
        print(f"خطأ في الاتصال بالموقع: {e}")

if __name__ == "__main__":
    scrape()
