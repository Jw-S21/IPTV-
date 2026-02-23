import requests
from bs4 import BeautifulSoup
import re

# الرابط الرئيسي لقسم مسلسلات رمضان
MAIN_URL = "https://asd.pics/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86/ramadan-series-2026/"

def scrape():
    # إضافة Headers لجعل السكربت يظهر كأنه متصفح حقيقي لتجنب الحظر
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://asd.pics/'
    }
    
    try:
        print("جاري الدخول للموقع...")
        response = requests.get(MAIN_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج روابط الحلقات من الصفحة الرئيسية
        # نبحث عن الروابط التي تحتوي على كلمة ramadan-series-2026
        all_links = soup.find_all('a', href=True)
        episode_pages = []
        for l in all_links:
            href = l['href']
            if "/ramadan-series-2026/" in href and href != MAIN_URL:
                if href not in episode_pages:
                    episode_pages.append(href)

        print(f"تم العثور على {len(episode_pages)} صفحة. جاري استخراج روابط الفيديو...")

        m3u_content = "#EXTM3U\n"
        
        for pg in episode_pages:
            try:
                # الدخول لصفحة الفيديو
                r = requests.get(pg, headers=headers)
                # البحث عن رابط mp4 الذي ينتهي بـ video.mp4 ويحتوي على boutique
                # هذا هو التعديل السحري بناءً على الرابط الذي أرسلته
                video_match = re.search(r'https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+video\.mp4', r.text)
                
                if video_match:
                    video_url = video_match.group(0)
                    # استخراج اسم الحلقة من الرابط لجعل القائمة جميلة
                    title = pg.rstrip('/').split('/')[-1].replace('-', ' ')
                    m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
                    print(f"تم بنجاح صيد: {title}")
                else:
                    # محاولة ثانية ببحث أوسع إذا فشل البحث الأول
                    video_match_alt = re.search(r'https?://[^\s"\'<>]+video\.mp4', r.text)
                    if video_match_alt:
                        video_url = video_match_alt.group(0)
                        title = pg.rstrip('/').split('/')[-1].replace('-', ' ')
                        m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
            except:
                continue

        # حفظ النتائج في ملف
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("تم تحديث ملف playlist.m3u بنجاح!")
            
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    scrape()
