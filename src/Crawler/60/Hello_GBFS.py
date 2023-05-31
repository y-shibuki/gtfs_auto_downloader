import datetime
import json
import os
import warnings

import requests

warnings.simplefilter('error')

# ハローサイクリング（GBFS）
# https://ckan.odpt.org/dataset/c_bikeshare_gbfs-openstreet
# 冨岡さんのライセンスキーで取得
if __name__ == "__main__":
    API_KEY = os.environ.get("ODPT_KEY")

    operator = "ハローサイクリング"
    data_type = "GBFS"
    date = datetime.datetime.now()
    folder_path = f"./data/{operator}/{data_type}/{date.strftime('%Y年%m月%d日')}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with requests.get(f"https://api.odpt.org/api/v4/gbfs/hellocycling/station_status.json?acl:consumerKey={API_KEY}") as response:
        d = json.loads(response.text)
    with open(f"{folder_path}/{date.strftime('%H%M%S')}.json", 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
