import cloudscraper
import re

# الرابط الذي أرسلته
TARGET_URL = "https://egibest.live/"

def scrape():
    # استخدام cloudscraper ضروري جداً هنا لتجاوز حماية Cloudflare
    scraper = cloudscraper.create_scraper()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': TARGET_URL
    }

    try:
        print(f"جاري محاولة فحص إيجي بست: {TARGET_URL}")
        response = scraper.get(TARGET_URL, headers=headers, timeout=30)
        
        # إيجي بست يضع روابط الأفلام والمسلسلات في وسوم 'a' بداخلها 'href'
        # سنحاول جمع أول 20 رابط يظهر في الصفحة الرئيسية
        links = re.findall(r'href="(https://egibest\.live/[^"]+)"', response.text)
        links = list(dict.fromkeys(links))[:20] 

        m3u_content = "#EXTM3U\n"
        count = 0

        for link in links:
            try:
                # الدخول لصفحة الفيلم/الحلقة
                res = scraper.get(link, headers=headers, timeout=15)
                
                # البحث عن روابط الفيديو المباشرة أو روابط السيرفرات
                # إيجي بست غالباً يستخدم روابط تحتوي على /v/ أو سيرفرات خارجية
                video_match = re.search(r'(https?://[^\s"\'<> ]+(?:\.mp4|\.m3u8|/v/|/e/)[^\s"\'<> ]*)', res.text)
                
                if video_match:
                    video_url = video_match.group(1).replace('\\', '')
                    title = link.strip('/').split('/')[-1].replace('-', ' ')
                    m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
                    count += 1
                    print(f"✅ تم صيد رابط: {title}")
            except:
                continue

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print(f"تم الانتهاء! الروابط التي تم جمعها: {count}")

    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    scrape()
