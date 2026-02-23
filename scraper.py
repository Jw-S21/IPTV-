import requests
import re
import base64

# الرابط الأساسي
BASE_URL = "https://asd.pics/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86/ramadan-series-2026/"

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://asd.pics/',
        'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3'
    }
    
    session = requests.Session()
    
    try:
        print("جاري سحب قائمة المسلسلات...")
        response = session.get(BASE_URL, headers=headers, timeout=20)
        # استخراج كافة الروابط التي قد تكون لمسلسلات
        potential_links = re.findall(r'https://asd\.pics/[^/\s"\'<>]+/', response.text)
        series_pages = list(set([l for l in potential_links if len(l) > 35 and "category" not in l]))

        m3u_content = "#EXTM3U\n"
        count = 0

        for pg in series_pages:
            try:
                res = session.get(pg, headers=headers, timeout=15)
                # 1. البحث عن رابط مباشر (mp4/m3u8)
                video_url = None
                match = re.search(r'(https?://[^\s"\'<>]+(?:cdn\.boutique|video\.mp4|playlist\.m3u8)[^\s"\'<> ]*)', res.text)
                
                if match:
                    video_url = match.group(1).replace('\\', '') # تنظيف الرابط من علامات الهروب
                
                # 2. إذا لم يجد، يبحث عن روابط مشفرة (بصيغة Base64) أحياناً يستخدمونها لإخفاء الرابط
                if not video_url:
                    b64_matches = re.findall(r'aHR0cHM6Ly[A-Za-z0-9+/=]+', res.text)
                    for b in b64_matches:
                        try:
                            decoded = base64.b64decode(b).decode('utf-8')
                            if "cdn.boutique" in decoded or ".mp4" in decoded:
                                video_url = decoded
                                break
                        except: continue

                if video_url:
                    title = pg.strip('/').split('/')[-1].replace('-', ' ')
                    m3u_content += f"#EXTINF:-1, {title}\n{video_url}\n"
                    count += 1
                    print(f"✅ وجدنا رابطاً: {title}")
            except: continue

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"تم بنجاح! الروابط المستخرجة: {count}")

    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    scrape()
