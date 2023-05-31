import datetime
import os
import warnings
warnings.simplefilter('error')

import requests
import json


# 関東自動車（GTFS-RT）
# 公共交通データHUBシステムから取得
# https://www.ptd-hs.jp/
# 吉田のライセンスキーで取得
if __name__ == "__main__":
    operator = "関東自動車"
    data_type = "VehiclePosition"
    date = datetime.datetime.now()
    folder_path = f"./data/{operator}/{data_type}/{date.strftime('%Y年%m月%d日')}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with requests.get("https://www.ptd-hs.jp/GetVehiclePosition?uid=EIS19x0j6mhQlIHjDjVLjW6Adlq2&agency_id=0904&output=json") as response:
        d = json.loads(response.text)
    with open(f"{folder_path}/{date.strftime('%H%M%S')}.json", 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
