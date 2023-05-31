import tarfile
import glob
import os

if __name__ == "__main__":
    if not os.path.exists("./data"):
        os.makedirs("./data")

    for path in glob.glob("./zip/*.tar.xz"):
        try:
            with tarfile.open(path, 'r:xz') as tar:
                tar.extractall()
        finally:
            os.remove(path)
