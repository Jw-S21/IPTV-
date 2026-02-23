import requests
from bs4 import BeautifulSoup
import re

# الرابط الذي تريد سحب المسلسلات منه
target_url = "https://asd.pics/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86/ramadan-series-2026/"

def get_links():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # البحث عن كل المقالات (المسلسلات)
        articles = soup.find_all('article')
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for art in articles:
                title = art.find('h2').text.strip() if art.find('h2') else "مسلسل غير معروف"
                link = art.find('a')['href']
                
                # الدخول لصفحة الفيديو لسحب رابط الـ mp4 اللي انت صورته
                video_page = requests.get(link, headers=headers)
                # هذا السطر يبحث عن الرابط اللي بيبدأ بـ cdn.boutique زي اللي في صورتك
                mp4_match = re.search(r'https?://[^\s"\'<>]+cdn\.boutique[^\s"\'<>]+', video_page.text)
                
                if mp4_match:
                    direct_link = mp4_match.group(0)
                    f.write(f"#EXTINF:-1, {title}\n{direct_link}\n")
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_links()
