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


if __name__ == "__main__":
    print("取得を開始します")
    # 20秒ごとに実行
    # Ctrl + Cを押さない限り、実行し続ける
    while True:
        # Crawlerフォルダの下にある.pyファイルを実行
        for crawler_file in glob.glob("./Crawler/*.py"):
            try:
                subprocess.run(["python", crawler_file], check=True)
            except subprocess.CalledProcessError as e:
                print(e)

        time.sleep(20)