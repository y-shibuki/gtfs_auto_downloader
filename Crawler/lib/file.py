import datetime
import os


def get_file_name(operator="富山地鉄", date_type="TripUpdates") -> str:
    date: datetime = datetime.datetime.now()
    folder_path: str = f"./{operator}/{date_type}/{date.strftime('%Y年%m月%d日')}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return f"{folder_path}/{date.strftime('%H%M%S')}.json"