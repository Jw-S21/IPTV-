import cloudscraper
import re

# لينك المسلسل الذي أرسلته للتجربة
TEST_URL = "https://asd.pics/selary/%d9%85%d8%b3%d9%84%d8%b3%d9%84-%d9%87%d9%8a-%d9%83%d9%8a%d9%85%d9%8a%d8%a7/"

def scrape():
    # استخدام cloudscraper لتجاوز حماية الموقع
    scraper = cloudscraper.create_scraper()
    
    try:
        print(f"جاري فحص المسلسل: {TEST_URL}")
        response = scraper.get(TEST_URL, timeout=20)
        
        m3u_content = "#EXTM3U\n"
        
        # البحث عن روابط cdn.boutique أو أي روابط فيديو mp4
        # أضفت بحثاً عن الروابط حتى لو كانت داخل جافا سكريبت
        video_links = re.findall(r'(https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+video\.mp4)', response.text)
        
        if not video_links:
            # محاولة البحث عن روابط السيرفرات المشهورة التي يضعها الموقع
            video_links = re.findall(r'(https?://[^\s"\'<>]+(?:\.mp4|\.m3u8))', response.text)

        if video_links:
            # إزالة التكرار
            unique_links = list(set(video_links))
            for i, link in enumerate(unique_links):
                m3u_content += f"#EXTINF:-1, الحلقة {i+1}\n{link}\n"
                print(f"✅ تم العثور على رابط: {link}")
        else:
            print("❌ لم يتم العثور على روابط فيديو مباشرة في هذه الصفحة.")

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    scrape()
