import glob
import gzip
import os
import tarfile

import dotenv

# 環境変数の読み込み
dotenv.load_dotenv("./.env.local")

if __name__ == "__main__":
    folder_path = os.environ.get("FOLDER_PATH") or "."

    if not os.path.exists(f"{folder_path}/zip"):
        raise FileNotFoundError(f"{folder_path}/zip")

    if not os.path.exists(f"{folder_path}/data"):
        os.makedirs(f"{folder_path}/data")

    for path in glob.glob(f"{folder_path}/zip/*.tar.gz"):
        try:
            with tarfile.open(path, 'r:gz') as tar:
                tar.extractall(path=folder_path)
        except:
            print("gzファイルが破損しています。")
        else:
            os.remove(path)
