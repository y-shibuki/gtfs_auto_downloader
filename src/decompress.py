import glob
import os
import tarfile

if __name__ == "__main__":
    if not os.path.exists("./data"):
        os.makedirs("./data")

    for path in glob.glob("./zip/*.tar.gz"):
        try:
            with tarfile.open(path, 'r:gz') as tar:
                tar.extractall()
        finally:
            os.remove(path)
