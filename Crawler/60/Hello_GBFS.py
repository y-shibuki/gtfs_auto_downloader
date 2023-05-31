import datetime
import os
import warnings
warnings.simplefilter('error')

import requests
import json


# ハローサイクリング（GBFS）
# 
# 冨岡さんのライセンスキーで取得
if __name__ == "__main__":
    operator = "ハローサイクリング"
    data_type = "GBFS"
    date = datetime.datetime.now()
    folder_path = f"./data/{operator}/{data_type}/{date.strftime('%Y年%m月%d日')}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with requests.get("https://api.odpt.org/api/v4/gbfs/hellocycling/station_status.json?acl:consumerKey=0270907a53691415af5e4027f1d2aac16e7a5515a39a7c939457c80d5f87866a") as response:
        d = json.loads(response.text)
    with open(f"{folder_path}/{date.strftime('%H%M%S')}.json", 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
