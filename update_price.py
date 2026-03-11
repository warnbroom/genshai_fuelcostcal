import requests
from bs4 import BeautifulSoup
import json
import re

def get_prices():
    url = "https://www.petrolimex.com.vn/thong-tin-khach-hang.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lấy toàn bộ text của trang web, xóa khoảng trắng thừa
        clean_text = " ".join(soup.get_text().split())
        
        # Giá dự phòng (trong trường hợp không quét được)
        data = {"RON95": 27640, "DO": 30530}

        # Regex giải thích: 
        # Tìm cụm từ "RON 95-V", bỏ qua các ký tự ở giữa, 
        # lấy chuỗi số có định dạng XX.XXX (ví dụ 22.140)
        ron95_match = re.search(r"RON 95-V.*?(\d{2}\.\d{3})", clean_text)
        if ron95_match:
            data["RON95"] = int(ron95_match.group(1).replace('.', ''))

        do_match = re.search(r"0,001S-V.*?(\d{2}\.\d{3})", clean_text)
        if do_match:
            data["DO"] = int(do_match.group(1).replace('.', ''))

        # Ghi log để bạn kiểm tra trong tab Actions
        print(f"Dữ liệu tìm được: {data}")

        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_prices()
