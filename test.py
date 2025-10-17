from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

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
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/aside/section/ul/ul/li[2]/a"))
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
print("✅ 'ファイル読込み(CSV/テキスト)' をクリックしました！")

# print(html_snippet[:2000])  # 長すぎる場合に備えて先頭500文字だけ出力
# target.click()
# time.sleep(10)

# 次へボタンが有効になるまで待機してクリック
next_btn = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "dataApply"))
)


next_btn.click()
print("次へボタンをクリックしました！")



file_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "file1")))
attached = driver.execute_script("return arguments[0].files.length;", file_input)
print(f"📎 DOM上で認識されたファイル数: {attached}")

file_input.send_keys("/Users/labo/Downloads/test.csv")
print("📂 ファイル送信済み")

driver.execute_script("""
var input = arguments[0];
var evt = new Event('change', { bubbles: true });
input.dispatchEvent(evt);
""", file_input)
print("✅ change イベント発火完了")

attached = driver.execute_script("return arguments[0].files.length;", file_input)
print(f"📎 DOM上で認識されたファイル数: {attached}")

time.sleep(3)

execution = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "do"))
)

execution.click()


run = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "run1"))
)

run.click()

time.sleep(5)

downloadPDF = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, "downloadPDF1"))
)

downloadPDF.click()


time.sleep(20)

driver.quit()
