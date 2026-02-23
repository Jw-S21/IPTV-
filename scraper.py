import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def human_like_scrape():
    # إعدادات المتصفح للعمل داخل سيرفرات GitHub (بدون واجهة رسومية)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # تمويه المتصفح ليتخطى كاشفات البوتات
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # تشغيل المتصفح
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # رابط المسلسل الذي سنقوم بتجربته
    target_url = "https://asd.pics/selary/%d9%85%d8%b3%d9%84%d8%b3%d9%84-%d9%87%d9%8a-%d9%83%d9%8ي%d9%85%d9%8a%d8%a7/"
    
    try:
        print(f"🚀 البدء في محاكاة التصفح البشري لرابط: {target_url}")
        driver.get(target_url)
        
        # الانتظار الأول: كأننا نقرأ تفاصيل المسلسل
        print("⏳ الانتظار لتحميل العناصر الأساسية...")
        time.sleep(10) 
        
        # حركة بشرية: التمرير لأسفل لتفعيل مشغل الفيديو
        print("🖱️ التمرير لأسفل (Scrolling) لتنشيط الصفحة...")
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(5)

        # استخراج "روح الصفحة" (Page Source) بعد عمل الجافا سكريبت
        raw_content = driver.page_source
        
        # البحث عن الرابط بصيغة Regex (النمط الذي اكتشفناه سابقاً)
        video_pattern = r'(https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+video\.mp4)'
        found_links = re.findall(video_pattern, raw_content)
        
        m3u_content = "#EXTM3U\n"
        
        if found_links:
            # إزالة التكرارات وتنظيف الروابط من علامات الهروب (\)
            clean_links = list(dict.fromkeys([link.replace('\\', '') for link in found_links]))
            for i, link in enumerate(clean_links):
                m3u_content += f"#EXTINF:-1, الحلقة {i+1}\n{link}\n"
                print(f"✅ تم العثور على رابط فيديو حقيقي: {link}")
        else:
            print("❌ للأسف، حتى مع المتصفح الحقيقي لم يظهر الرابط المباشر في الكود.")
            # محاولة أخيرة: البحث عن أي mp4
            alt_links = re.findall(r'(https?://[^\s"\'<> ]+\.mp4)', raw_content)
            for i, link in enumerate(list(dict.fromkeys(alt_links))[:5]):
                m3u_content += f"#EXTINF:-1, فيديو احتياطي {i+1}\n{link}\n"

        # حفظ الملف
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("💾 تم تحديث ملف playlist.m3u بنجاح!")

    except Exception as e:
        print(f"⚠️ حدث خطأ تقني: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    human_like_scrape()
