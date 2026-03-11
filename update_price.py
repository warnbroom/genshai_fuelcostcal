import requests
from bs4 import BeautifulSoup
import json
import re

def get_prices():
    url = "https://www.petrolimex.com.vn/thong-tin-khach-hang.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lấy text và làm sạch các khoảng trắng lạ
        clean_text = " ".join(soup.get_text().split())
        
        # Giá mặc định (Phòng hờ)
        data = {"RON95": 27640, "DO": 30530}

        # Regex mới: Tìm từ khóa "95-V", bỏ qua các ký tự không phải số, rồi lấy nhóm số có dấu chấm
        # Mục tiêu: Bắt được con số đầu tiên xuất hiện sau chữ "95-V"
        ron95_search = re.search(r"95-V[^\d]*(\d{2}\.\d{3})", clean_text)
        if ron95_search:
            data["RON95"] = int(ron95_search.group(1).replace('.', ''))
            print(f"Bắt được giá RON95: {data['RON95']}")

        # Mục tiêu: Bắt được con số đầu tiên xuất hiện sau chữ "0,001S-V" hoặc "DO"
        do_search = re.search(r"0,001S-V[^\d]*(\d{2}\.\d{3})", clean_text)
        if do_search:
            data["DO"] = int(do_search.group(1).replace('.', ''))
            print(f"Bắt được giá DO: {data['DO']}")

        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Đã ghi file prices.json thành công.")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_prices()
