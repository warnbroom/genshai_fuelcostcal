import requests
import json

def get_prices():
    # DÁN CÁI URL BẠN VỪA COPY Ở BƯỚC 1 VÀO ĐÂY
    google_proxy_url = "https://script.google.com/macros/s/AKfycbzLlpJkxQmcFvrbxZdyOjiGg7cnz0y9XBuzSAvhawdUWavFnu8jfkfn_OzGhC9DtzdQTA/exec"
    
    try:
        # Google Web App thường yêu cầu chuyển hướng (Redirect)
        response = requests.get(google_proxy_url, allow_redirects=True, timeout=30)
        data = response.json()
        
        if data.get("RON95") and data.get("DO"):
            print(f"Giá lấy thành công qua Google Proxy: {data}")
            with open('prices.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            print("Google lấy được dữ liệu nhưng không thấy số giá.")
            
    except Exception as e:
        print(f"Lỗi khi gọi Google Proxy: {e}")

if __name__ == "__main__":
    get_prices()
