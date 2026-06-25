import csv
import requests

# 目标：GitHub 上别人公开的优秀 CF IP 数据
CSV_URL = "https://raw.githubusercontent.com/xgonce/Cloudflare_IP/refs/heads/main/result.csv"
OUTPUT_FILE = "cf_ips.txt"

def download_and_parse():
    print("📥 正在获取远程 Cloudflare IP 原始数据...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(CSV_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ 下载失败，HTTP 状态码: {response.status_code}")
            return
        
        lines = response.text.strip().split('\n')
        reader = csv.reader(lines)
        
        # 跳过表头
        next(reader, None)
        
        results = []
        for row in reader:
            if len(row) < 5:
                continue
                
            ip = row[0].strip()          # IP
            port = row[2].strip()        # 端口
            country = row[4].strip()     # CF归属国
            
            if "IP" in ip or not ip:
                continue
            
            # 格式化输出: IP:端口#归属国(小写)
            formatted_line = f"{ip}:{port}#{country.lower()}"
            results.append(formatted_line)
            
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
            
        print(f"✅ 洗洗完成！共提取 {len(results)} 个节点，已写入: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"⚠️ 脚本执行异常: {e}")

if __name__ == "__main__":
    download_and_parse()
