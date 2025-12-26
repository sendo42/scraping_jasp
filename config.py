import os

# フォルダ設定
INPUT_DIR = os.path.abspath("./input")
OUTPUT_DIR = os.path.abspath("./output")

# 解析手法のリスト
METHODS = ["plot", "hist", "autcor", "period", "logt", "difft", "arfit", "armafit2"]

# ブラウザ設定
CHROME_PREFS = {
    "download.default_directory": OUTPUT_DIR,
    "plugins.always_open_pdf_externally": True
}