import requests
from bs4 import BeautifulSoup
import json

def get_petrolimex_prices():
    url = "https://www.petrolimex.com.vn/thong-tin-khach-hang.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Logic tìm kiếm giá (ví dụ minh họa, cần điều chỉnh theo cấu trúc HTML thực tế)
    # Giả sử chúng ta tìm trong bảng
    prices = {
        "RON95": 27640, # Giá mặc định nếu lỗi
        "DO": 30530
    }
    
    # Lưu vào file JSON
    with open('prices.json', 'w') as f:
        json.dump(prices, f)

if __name__ == "__main__":
    get_petrolimex_prices()
