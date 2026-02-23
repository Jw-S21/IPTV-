import requests
from bs4 import BeautifulSoup
import re

# الرابط الجديد الذي أرسلته (الصفحة الرئيسية للمسلسلات)
TARGET_URL = "https://asd.pics/main4/"

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://asd.pics/'
    }
    
    session = requests.Session()
    
    try:
        print(f"جاري فحص الموقع: {TARGET_URL}")
        response = session.get(TARGET_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج روابط جميع المسلسلات/الحلقات من الصفحة الرئيسية
        # الموقع يعتمد على وسم 'article' أو 'h2' بداخلها روابط
        items = soup.find_all('article')
        if not items:
            items = soup.find_all('h2') # محاولة بديلة إذا اختلف التقسيم
            
        m3u_content = "#EXTM3U\n"
        found_count = 0

        for item in items:
            a_tag = item.find('a') if item.name != 'a' else item
            if a_tag and a_tag.get('href'):
                page_url = a_tag['href']
                title = a_tag.text.strip() or "مسلسل رمضان"
                
                try:
                    # الدخول لصفحة الفيديو
                    res = session.get(page_url, headers=headers, timeout=10)
                    
                    # البحث عن الرابط بصيغة Regex دقيقة جداً لرابط الـ mp4
                    video_match = re.search(r'https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+video\.mp4', res.text)
                    
                    if video_match:
                        video_url = video_match.group(0)
                        m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
                        found_count += 1
                        print(f"تم العثور على: {title}")
                except:
                    continue

        # حفظ النتائج
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"تم الانتهاء! إجمالي الروابط المستخرجة: {found_count}")
            
    except Exception as e:
        print(f"خطأ في السكربت: {e}")

if __name__ == "__main__":
    scrape()
