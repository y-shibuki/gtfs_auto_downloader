import tarfile
import datetime
import os
import glob
import shutil

if __name__ == "__main__":
    if not os.path.exists("./zip"):
        os.makedirs("./zip")

    lst = list(set([x.split("/")[-1] for x in glob.glob("./data/*/*/????年??月??日")]))
    today = datetime.datetime.now().strftime("%Y年%m月%d日")

    while len(lst) > 0:
        # XXXX年XX月XX日を取得
        folder_path = lst.pop()

        # 当日は圧縮処理の対象外
        if folder_path == today:
            continue

        try:
            # tarfileに圧縮
            with tarfile.open(f"./zip/{folder_path}.tar.gz", "w:gz") as f:
                for path in glob.glob(f"./data/*/*/{folder_path}"):
                    f.add(path)
        finally:
            # 圧縮に成功したら削除
            for path in glob.glob(f"./data/*/*/{folder_path}"):
                shutil.rmtree(path)
