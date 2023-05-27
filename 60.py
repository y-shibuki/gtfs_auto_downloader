"""
使い方：
Crawlerフォルダの下にある.pyファイルを、定期的に実行し続けます。
プログラムが動いている間にCrawlerフォルダにファイルを入れれば、途中からでも処理が実行されるようになっています。
一時的に取得を停止する際には、Crawlerフォルダから別のフォルダに、該当のPythonファイルを動かしてください。

このプログラムは60秒間隔で稼働します
"""

import subprocess
import glob
import os


if __name__ == "__main__":
    # Crawlerフォルダの下にある.pyファイルを実行
    for crawler_file in glob.glob("./Crawler/60/*.py"):
        try:
            subprocess.run(["python", crawler_file], check=True)
            print(f"{os.path.splitext(os.path.basename(crawler_file))[0]},OK")
        except subprocess.CalledProcessError:
            print(f"{os.path.splitext(os.path.basename(crawler_file))[0]},NG")
