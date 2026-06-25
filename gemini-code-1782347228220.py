import os
import csv
import requests

# 原始 CSV 文件的 URL
CSV_URL = "https://raw.githubusercontent.com/xgonce/Cloudflare_IP/refs/heads/main/result.csv"
# 输出文件的保存路径（保存在根目录下，方便后续推送到私库）
OUTPUT_FILE = "cf_ips.txt"

def download_and_parse():
    print(f"📥 正在从 GitHub 获取最新的 Cloudflare IP 列表...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(CSV_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ 下载失败，状态码: {response.status_code}")
            return
        
        # 将下载的文本按行切分，提供给 csv 解析器
        lines = response.text.strip().split('\n')
        reader = csv.reader(lines)
        
        # 读取表头
        header = next(reader, None)
        if not header:
            print("❌ CSV 文件为空")
            return
        
        results = []
        for row in reader:
            # 健壮性检查：确保行数据完整（至少包含 IP, 端口, 归属国等基础列）
            if len(row) < 5:
                continue
                
            ip = row[0].strip()          # 第一列：IP
            port = row[2].strip()        # 第三列：端口
            country = row[4].strip()     # 第五列：CF归属国
            
            # 跳过表头重复行或空行
            if "IP" in ip or not ip:
                continue
            
            # 将归属国转换为小写（例如 CA -> ca, TW -> tw）
            country_lower = country.lower()
            
            # 拼接成你需要的格式: IP:端口#归属国
            formatted_line = f"{ip}:{port}#{country_lower}"
            results.append(formatted_line)
            
        # 将结果写入文件
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
            
        print(f"✅ 解析完成！成功提取 {len(results)} 个 IP 节点，已保存至: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"⚠️ 处理过程中发生异常: {e}")

if __name__ == "__main__":
    download_and_parse()