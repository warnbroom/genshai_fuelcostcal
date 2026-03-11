import requests
from bs4 import BeautifulSoup
import json
import re

def get_prices():
    url = "https://webgia.com/gia-xang-dau/petrolimex/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Chỉ quét trong các thẻ <tr> (dòng của bảng) để chính xác nhất
        rows = soup.find_all('tr')
        data = {"RON95": 0, "DO": 0}

        for row in rows:
            text = row.get_text(separator=' ', strip=True)
            
            # 1. Xử lý giá RON 95-V
            if "RON 95-V" in text and data["RON95"] == 0:
                # Regex này chỉ tìm các số có 5 chữ số (ví dụ 23.560)
                numbers = re.findall(r'\d{2}\.\d{3}', text)
                if numbers:
                    data["RON95"] = int(numbers[0].replace('.', ''))
            
            # 2. Xử lý giá Dầu DO 0,001S-V
            if "0,001S-V" in text and data["DO"] == 0:
                # Quan trọng: Xóa bỏ chữ "0,001" trong tên sản phẩm để Regex không bốc nhầm
                clean_text = text.replace("0,001", "")
                numbers = re.findall(r'\d{2}\.\d{3}', clean_text)
                if numbers:
                    data["DO"] = int(numbers[0].replace('.', ''))

        # Nếu không cào được (web lỗi), dùng giá dự phòng (Fallback)
        # Lưu ý: Bạn nên cập nhật số này sát với giá thực tế hiện tại
        if data["RON95"] == 0: data["RON95"] = 23560 
        if data["DO"] == 0: data["DO"] = 18910

        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Cập nhật thành công:", data)

    except Exception as e:
        print(f"Lỗi: {e}")
        # Ghi giá mặc định nếu sập nguồn
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump({"RON95": 23560, "DO": 18910}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_prices()
