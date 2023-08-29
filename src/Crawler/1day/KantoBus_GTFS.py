import glob
import io
import json
import os
import warnings
import zipfile

import pandas as pd
import requests

warnings.simplefilter("error")

# 関東自動車（GTFS-RT）
# 公共交通データHUBシステムから取得
# https://www.ptd-hs.jp/
# 吉田のライセンスキーで取得
if __name__ == "__main__":
    API_KEY = os.environ.get("PTD_HS_KEY")

    operator = "関東自動車"
    data_type = "GTFS"
    folder_path = f"./data/{operator}/{data_type}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with requests.get(
        "https://www.ptd-hs.jp/GetAgencyDetail?agency_id=0904"
    ) as response:
        df = pd.DataFrame(
            json.loads(json.dumps(response.json(), ensure_ascii=False))["Datas"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    version_list = (
        df.query("timestamp > '2023/5/1'")
        .sort_values(by="timestamp")["version"]
        .to_list()
    )
    crawled_version_list = [
        folder.split("/")[-1] for folder in glob.glob(f"{folder_path}/*")
    ]

    # サーバー上に公開されているが、収集されていないデータを、差集合で判別
    for version in list(set(version_list) - set(crawled_version_list)):
        url = f"https://www.ptd-hs.jp/GetContentData?uid={API_KEY}&agency_id=0904&output=json&type=static&version={version}"
        print(url)
        with (
            requests.get(url) as response,
            io.BytesIO(response.content) as bytes_io,
            zipfile.ZipFile(bytes_io) as zip,
        ):
            zip.extractall(f"{folder_path}/{version}")
