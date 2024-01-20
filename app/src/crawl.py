"""
使い方：
Crawlerフォルダの下にある.pyファイルを、定期的に実行し続けます。
プログラムが動いている間にCrawlerフォルダにファイルを入れれば、途中からでも処理が実行されるようになっています。
一時的に取得を停止する際には、Crawlerフォルダから別のフォルダに、該当のPythonファイルを動かしてください。

呼び出しの引数には実行間隔を指定してください。
>> crawl.py 20
"""

import glob
import os
import subprocess
import sys

import dotenv

from utils.logger import getLogger

# 環境変数の読み込み
dotenv.load_dotenv("./.env.local")

logger = getLogger(__name__)

if __name__ == "__main__":
    if not os.path.exists(f"./src/Crawler/{sys.argv[1]}/"):
        logger.error("パスが存在しません")
        exit()

    # Crawlerフォルダの下にある.pyファイルを実行
    for crawler_file in glob.glob(f"./src/Crawler/{sys.argv[1]}/*.py"):
        try:
            subprocess.run(["python", crawler_file], check=True)
            logger.info(f"{os.path.splitext(os.path.basename(crawler_file))[0]},OK")
        except subprocess.CalledProcessError:
            logger.warning(f"{os.path.splitext(os.path.basename(crawler_file))[0]},NG")
