import zipfile
import datetime
import os
import glob

if __name__ == "__main__":
    now = datetime.datetime.now()
    # 一日前のフォルダパスを取得
    folder_path = (now - datetime.timedelta(days=1)).strftime("%Y年%m月%d日")

    if not os.path.exists("./zip"):
        os.makedirs("./zip")

    # "a"：上書きモード zipfile.ZIP_DEFLATED: アーカイブと圧縮を同時に行う　compresslevel=9：最大限の圧縮を行う
    with zipfile.ZipFile("./zip/data.zip", "a", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as f:
        for path in glob.glob(f"./data/**/{folder_path}/*.json", recursive=True):
            f.write(path, arcname=path.lstrip("./data"))
