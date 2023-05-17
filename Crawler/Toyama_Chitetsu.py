from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
import requests
import json
from lib.file import get_file_name

# 富山県バス情報データ（GTFS-JP、GTFS-RT）
# とやまロケーションシステムで使用しているデータを、標準的なバス情報フォーマットに準じた形式で公開しています。
# GTFS-RTは、20秒おきに更新されますが、過度なアクセスは行わないようにしてください。
# https://opendata.pref.toyama.jp/pages/gtfs_jp.htm
if __name__ == "__main__":
    feed = gtfs_realtime_pb2.FeedMessage()
    with requests.get("https://gtfs-rt-files.buscatch.jp/toyama/chitetsu/TripUpdates.pb") as response:
        feed.ParseFromString(response.content)
        d: dict = json_format.MessageToDict(feed)

    with open(get_file_name("富山地鉄", "TripUpdates"), 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

    print("富山地鉄", "TripUpdates", "OK")