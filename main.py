"""
使い方：
Crawlerフォルダの下にある.pyファイルを、定期的に実行し続けます。
プログラムが動いている間にCrawlerフォルダにファイルを入れれば、途中からでも処理が実行されるようになっています。
一時的に取得を停止する際には、Crawlerフォルダから別のフォルダに、該当のPythonファイルを動かしてください。
処理を中止する際には、ターミナルでCtrl + Cを押してください。

・バックグラウンドで実行
nohup python main.py > log/out.log 2> log/error.log &
・実行状況の確認
ps x
・実行を止める
PIDにはps xで確認したプロセスIDを記入
kill -KILL PID
"""

import subprocess
import glob
import time
import datetime
from collections import defaultdict
import os


def crawlers(folder_path):
    # Crawlerフォルダの下にある.pyファイルを実行
    for crawler_file in glob.glob(folder_path):
        try:
            subprocess.run(["python", crawler_file], check=True)
            print(f"{os.path.splitext(os.path.basename(crawler_file))[0]},OK")
        except subprocess.CalledProcessError:
            print(f"{os.path.splitext(os.path.basename(crawler_file))[0]},NG")


def wait_until_min():
    now = datetime.datetime.now()
    time.sleep(60 - now.second - datetime.datetime.now().microsecond / 10**6)


def wait_until_sec(interval=1):
    time.sleep(interval - datetime.datetime.now().microsecond / 10**6)


intervals = {
    "./Crawler/20/*.py": 20,
    "./Crawler/60/*.py": 60,
    "./Crawler/120/*.py": 120,
}

last_execution = defaultdict(int)
INTERVAL = 1

if __name__ == "__main__":
    # 開始時刻を0.000秒に揃える
    wait_until_min()

    while True:
        current_time = time.time()
        for folder_path, interval in intervals.items():
            if round(current_time - last_execution[folder_path]) >= interval:
                last_execution[folder_path] = time.time()
                crawlers(folder_path)

        # 開始時刻をx.000秒に揃える
        wait_until_sec(interval=INTERVAL)
