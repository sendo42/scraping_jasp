from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

import time

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

prefs = {
    "download.default_directory": OUTPUT_DIR, # 保存先をOUTPUT_DIRに固定
    # "download.prompt_for_download": False,    # ダイアログを表示しない
    "plugins.always_open_pdf_externally": True # PDFをブラウザで開かずダウンロードする
}


opts = Options()
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-gpu")
opts.add_argument("--disable-web-security")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get("https://jasp.ism.ac.jp/RS-Decomp")

# --- iframeが出現するまで待つ ---
iframe = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.shiny-frame"))
)
print("iframe を検出！中に入ります。")

# --- iframeの中に入る ---
driver.switch_to.frame(iframe)

# --- iframe内部で目的の要素を待つ ---
element = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='page_menu']/li[2]/a"))
)
element.click()
print("iframe 内の要素をクリックしました！")

# --- fileinput をクリックしたあとで ---
# time.sleep(4)  # DOM更新待ち

select_box = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/section/div/div/div[2]/div/div[1]/form/div/div/div[1]/div[1]/div/div/div/div[1]"))
)
select_box.click()
print("selectize入力部分をクリックしました")

target = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/section/div/div/div[2]/div/div[1]/form/div/div/div[1]/div[1]/div/div/div/div[2]"))
)
print(target)

# --- 「ファイル読込み(CSV/テキスト)」の要素を待つ ---
file_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@data-value='fileinput']"))
)

# --- JSでクリック ---
driver.execute_script("arguments[0].scrollIntoView(true);", file_option)
# time.sleep(5)
driver.execute_script("arguments[0].click();", file_option)
print("'ファイル読込み(CSV/テキスト)' をクリックしました！")

# print(html_snippet[:2000])  # 長すぎる場合に備えて先頭500文字だけ出力
# target.click()
# time.sleep(10)

# 次へボタンが有効になるまで待機してクリック
next_btn = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "dataApply"))
)


next_btn.click()
print("次へボタンをクリックしました！")



file_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "file1"))
)
attached = driver.execute_script("return arguments[0].files.length;", file_input)
print(f"DOM上で認識されたファイル数: {attached}")

file_input.send_keys("/Users/labo/Downloads/test.csv")
print("ファイル送信済み")

driver.execute_script("""
var input = arguments[0];
var evt = new Event('change', { bubbles: true });
input.dispatchEvent(evt);
""", file_input)
print("change イベント発火完了")

attached = driver.execute_script("return arguments[0].files.length;", file_input)
print(f"DOM上で認識されたファイル数: {attached}")

time.sleep(3)

# do で実行ボタンしてる

execution = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "do"))
)

execution.click()

## Decomp > 周期

# 1. 入力エリアを特定してクリック（フォーカスを当てる）
period_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "period1-selectized"))
)
period_input.click()

# 2. 値を入力して ENTER キーを押す（例: "12" と入力する場合）
period_input.send_keys("11")
time.sleep(1) # 候補が出るのを少し待つ
period_input.send_keys(Keys.ENTER)

print("周期の値を入力しました")


## Decomp > 対数変換

log_radio = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='log'][value='TRUE']"))
)
log_radio.click()


# 1. 要素を特定（ID: trend.order）
trend_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "trend.order"))
)

# 2. 既存の値を消去
# clear() が効かない場合があるため、全選択してBackSpaceで消すのが確実です
trend_input.send_keys(Keys.COMMAND + "a") # Macの場合 (Windowsなら Keys.CONTROL) cmd + aで全選択削除 2桁のときたすかる
trend_input.send_keys(Keys.BACKSPACE)

# 3. 新しい数値を入力（例: 3） 1-3の範囲だった。
trend_input.send_keys("3")

# 4. 確定のために ENTER または Tab を押す
trend_input.send_keys(Keys.ENTER)

print("トレンド次数を書き換えました")



# 1. 要素を特定（ID: seasonal.order）
seasonal_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "seasonal.order"))
)

# 2. 既存の値を消去
# clear() が効かない場合があるため、全選択してBackSpaceで消すのが確実です
seasonal_input.send_keys(Keys.COMMAND + "a") # Macの場合 (Windowsなら Keys.CONTROL) cmd + aで全選択削除 2桁のときたすかる
seasonal_input.send_keys(Keys.BACKSPACE)

# 3. 新しい数値を入力（例: 2） 0-2
seasonal_input.send_keys("2")

# 4. 確定のために ENTER または Tab を押す
seasonal_input.send_keys(Keys.ENTER)

print("シーズン次数を書き換えました")



# 1. 要素を特定（ID: ar.order）
ar_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "ar.order"))
)

# 2. 既存の値を消去
# clear() が効かない場合があるため、全選択してBackSpaceで消すのが確実です
ar_input.send_keys(Keys.COMMAND + "a") # Macの場合 (Windowsなら Keys.CONTROL) cmd + aで全選択削除 2桁のときたすかる
ar_input.send_keys(Keys.BACKSPACE)

# 3. 新しい数値を入力（例: 2） 0-6
ar_input.send_keys("2")

# 4. 確定のために ENTER または Tab を押す
ar_input.send_keys(Keys.ENTER)

print("AR次数を書き換えました")


## 曜日効果のやつ 名前がtradeになってるのでそうする。

trade_radio = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='trade'][value='TRUE']"))
)
trade_radio.click()

run = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "run1"))
)

run.click()

time.sleep(5)

downloadPDF = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "downloadPDF1"))
)

downloadPDF.click()



# 「その他の手法」という値を持つタブをクリック
tab_element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-value='その他の手法']"))
)
tab_element.click()
print("'その他の手法' タブに切り替えました")


# 「func-selectized」というIDの入力欄を包んでいる親の枠を探してクリック
parent_div = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/section/div/div/div[2]/div/div[1]/form/div/div/div[3]/div[1]/div/div/div/div/div[1]"))
)
parent_div.click()
print("プルダウンの枠をクリックしました")


## <div class="selectize-input items full has-options has-items"><div class="item" data-value="plot">プロット</div><input type="text" autocomplete="new-password" autofill="no" tabindex="" id="func-selectized" role="combobox" aria-expanded="false" haspopup="listbox" aria-owns="lq1oxrr5rb" style="width: 4px;"></div>
target = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/section/div/div/div[2]/div/div[1]/form/div/div/div[3]/div[1]/div/div/div/div/div[2]"))
)
print(target)


# 解析手法一覧 data-value
# plot プロット
# hist ヒストグラム
# autcor 自己相関関数
# period ピリオドグラム
# logt 対数
# difft 差分変換
# arfit ARモデルの推定
# armafit2 ARMAモデルの推定

# --- 解析手法の定義（あなたが挙げた順番通りの配列） ---
# index:  0       1       2         3         4       5        6        7
METHODS = ["plot", "hist", "autcor", "period", "logt", "difft", "arfit", "armafit2"]

def select_method_by_index(driver, index):
    """
    配列番号を指定して解析手法を選択する
    index: 0=プロット, 1=ヒストグラム, ..., 6=ARモデル, 7=ARMAモデル
    """
    if not (0 <= index < len(METHODS)):
        print(f"インデックス {index} は範囲外です。")
        return

    method_value = METHODS[index]
    print(f"手法選択を開始: {method_value} (Index: {index})")

    try:
        # 1. プルダウンの枠をクリックしてリストを展開
        # 以前のコードの id="func-selectized" を使って親要素を特定
        parent_div = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='func-selectized']/.."))
        )
        parent_div.click()
        time.sleep(1) # リストが生成されるまでわずかに待機

        # 2. 指定された data-value を持つ要素を特定してクリック
        xpath_option = f"//div[@data-value='{method_value}']"
        option_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_option))
        )

        # 3. JavaScriptで確実にクリック（スクロールして画面内に入れてからクリック）
        driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
        driver.execute_script("arguments[0].click();", option_element)
        
        print(f"解析手法 '{method_value}' (配列番号: {index}) を選択完了！")

    except Exception as e:
        print(f"手法の選択中にエラーが発生しました: {e}")

# --- 呼び出し方の例 ---

# 例1: 「ARモデルの推定 (arfit)」を選択したい場合（配列の6番目）
select_method_by_index(driver, 6)

run = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "run2"))
)

run.click()

# 例2: ループで順番にすべて実行したい場合
# for i in range(len(METHODS)):
#     select_method_by_index(driver, i)
#     # ここに「実行」や「PDF保存」の処理を入れる

time.sleep(100)

driver.quit()
