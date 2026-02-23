import requests
import re

# لينك المسلسل الذي أرسلته للتجربة
TARGET_URL = "https://asd.pics/selary/%d9%85%d8%b3%d9%84%d8%b3%d9%84-%d9%87%d9%8a-%d9%83%d9%8ي%d9%85%d9%8a%d8%a7/"

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://asd.pics/'
    }
    
    try:
        print(f"جاري فحص الصفحة: {TARGET_URL}")
        response = requests.get(TARGET_URL, headers=headers, timeout=20)
        
        # البحث عن أي رابط يحتوي على boutique وينتهي بـ mp4
        # استخدمنا بحثاً واسعاً جداً هنا لتجاوز أي حماية
        links = re.findall(r'(https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+video\.mp4)', response.text)
        
        m3u_content = "#EXTM3U\n"
        
        if links:
            # إزالة التكرار
            unique_links = list(dict.fromkeys(links))
            for i, link in enumerate(unique_links):
                m3u_content += f"#EXTINF:-1, الحلقة {i+1}\n{link}\n"
                print(f"✅ تم العثور على رابط: {link}")
        else:
            # محاولة أخيرة: البحث عن أي mp4 مباشر في الصفحة
            alt_links = re.findall(r'(https?://[^\s"\'<> ]+\.mp4)', response.text)
            for i, link in enumerate(list(dict.fromkeys(alt_links))):
                if "boutique" in link or "cdn" in link:
                    m3u_content += f"#EXTINF:-1, فيديو {i+1}\n{link}\n"
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("تم تحديث الملف بنجاح!")
            
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    scrape()
