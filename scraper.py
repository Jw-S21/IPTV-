import requests
import re
import cloudscraper

# رابط المسلسل الجديد
TARGET_URL = "https://sflix.film/ar/detail/and-we-forget-what-was-mdblj-ll-rby-qHzpIGACh63?id=2602968303974895304"

def scrape():
    # استخدام cloudscraper لتجاوز حماية الموقع الأساسية
    scraper = cloudscraper.create_scraper()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://sflix.film/'
    }

    try:
        print(f"جاري محاولة فحص الموقع الجديد: {TARGET_URL}")
        response = scraper.get(TARGET_URL, headers=headers, timeout=30)
        
        # المواقع دي غالباً بتستخدم روابط بث تنتهي بـ .m3u8
        # إحنا بندور على أي رابط فيديو (mp4) أو رابط بث (m3u8) مخفي في الكود
        video_patterns = [
            r'(https?://[^\s"\'<> ]+\.m3u8[^\s"\'<> ]*)',
            r'(https?://[^\s"\'<> ]+\.mp4[^\s"\'<> ]*)',
            r'(https?://[^\s"\'<> ]+cdn[^\s"\'<> ]+)'
        ]
        
        all_found_links = []
        for pattern in video_patterns:
            matches = re.findall(pattern, response.text)
            all_found_links.extend(matches)

        m3u_content = "#EXTM3U\n"
        
        if all_found_links:
            unique_links = list(dict.fromkeys(all_found_links))
            for i, link in enumerate(unique_links):
                # تنظيف الرابط من أي رموز تشفير زائدة
                clean_link = link.replace('\\', '')
                m3u_content += f"#EXTINF:-1, سيرفر {i+1}\n{clean_link}\n"
                print(f"✅ تم العثور على: {clean_link}")
        else:
            print("❌ الموقع ده محمي جداً، الروابط مش ظاهرة في السورس.")

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print("تمت العملية بنجاح.")

    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    scrape()
