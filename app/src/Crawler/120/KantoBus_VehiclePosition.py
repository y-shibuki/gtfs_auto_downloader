import datetime
import json
import os
import warnings

import requests

warnings.simplefilter('error')

# 関東自動車（GTFS-RT）
# 公共交通データHUBシステムから取得
# https://www.ptd-hs.jp/
# 吉田のライセンスキーで取得
if __name__ == "__main__":
    API_KEY = os.environ.get("PTD_HS_KEY")

    operator = "関東自動車"
    data_type = "VehiclePosition"
    date = datetime.datetime.now()
    folder_path = f"./data/{operator}/{data_type}/{date.strftime('%Y年%m月%d日')}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with requests.get(f"https://www.ptd-hs.jp/GetVehiclePosition?uid={API_KEY}&agency_id=0904&output=json") as response:
        d = json.loads(response.text)
    with open(f"{folder_path}/{date.strftime('%H%M%S')}.json", 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
