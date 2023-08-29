import datetime
import json
import os
import warnings

import requests
from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2

warnings.simplefilter('error')

# 富山県バス情報データ（GTFS-JP、GTFS-RT）
# とやまロケーションシステムで使用しているデータを、標準的なバス情報フォーマットに準じた形式で公開しています。
# GTFS-RTは、20秒おきに更新されますが、過度なアクセスは行わないようにしてください。
# https://opendata.pref.toyama.jp/pages/gtfs_jp.htm
if __name__ == "__main__":
    operator = "富山地鉄市内電車"
    data_type = "TripUpdate"
    date = datetime.datetime.now()
    folder_path = f"./data/{operator}/{data_type}/{date.strftime('%Y年%m月%d日')}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    feed = gtfs_realtime_pb2.FeedMessage()
    with requests.get("https://gtfs-rt-files.buscatch.jp/toyama/chitetsu_tram/TripUpdates.pb") as response:
        feed.ParseFromString(response.content)
        d = json_format.MessageToDict(feed)

    with open(f"{folder_path}/{date.strftime('%H%M%S')}.json", 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)