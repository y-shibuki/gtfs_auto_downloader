"""
使い方：
Crawlerフォルダの下にある.pyファイルを、定期的に実行し続けます。
プログラムが動いている間にCrawlerフォルダにファイルを入れれば、途中からでも処理が実行されるようになっています。
一時的に取得を停止する際には、Crawlerフォルダから別のフォルダに、該当のPythonファイルを動かしてください。
処理を中止する際には、ターミナルでCtrl + Cを押してください。

・バックグラウンドで実行
nohup python main.py > output_log/out.log &
・実行状況の確認
ps u
・実行を止める
PIDにはps uで確認したプロセスIDを記入
kill -KILL PID
"""

import subprocess
import glob
import time
import datetime
from collections import defaultdict

def crawlers_20():
    # Crawlerフォルダの下にある.pyファイルを実行
    for crawler_file in glob.glob("./Crawler/20/*.py"):
        try:
            subprocess.run(["python", crawler_file], check=True)
        except subprocess.CalledProcessError as e:
            print(e)

def crawlers_60():
    # Crawlerフォルダの下にある.pyファイルを実行
    for crawler_file in glob.glob("./Crawler/60/*.py"):
        try:
            subprocess.run(["python", crawler_file], check=True)
        except subprocess.CalledProcessError as e:
            print(e)

def crawlers_120():
    # Crawlerフォルダの下にある.pyファイルを実行
    for crawler_file in glob.glob("./Crawler/120/*.py"):
        try:
            subprocess.run(["python", crawler_file], check=True)
        except subprocess.CalledProcessError as e:
            print(e)

def wait_until_min():
    now = datetime.datetime.now()
    time.sleep(60 - now.second - datetime.datetime.now().microsecond / 10**6)

def wait_until_sec(interval=1):
    time.sleep(interval - datetime.datetime.now().microsecond / 10**6)

intervals = {
    crawlers_20: 20,
    crawlers_60: 60,
    crawlers_120: 120
}

last_execution = defaultdict(0)
INTERVAL = 10

if __name__ == "__main__":
    # 開始時刻を0.000秒に揃える
    wait_until_min()

    while True:
        for func, interval in intervals.items():
            if last_execution[func] >= interval:
                last_execution[func] = 0
                func()
            else:
                last_execution[func] += INTERVAL

        # 開始時刻をx.000秒に揃える
        wait_until_sec(interval=INTERVAL)