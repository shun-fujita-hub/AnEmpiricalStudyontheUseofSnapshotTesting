import os

def mkdir(path):
    if not os.path.exists(path):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(path)