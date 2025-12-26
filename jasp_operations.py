import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def wait_and_click(driver, xpath, timeout=60):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    return element

def overwrite_input(driver, element_id, value):
    """全選択して上書き入力する"""
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, element_id)))
    element.send_keys(Keys.COMMAND + "a")
    element.send_keys(Keys.BACKSPACE)
    element.send_keys(str(value))
    element.send_keys(Keys.ENTER)

def setup_jasp_page(driver):
    """初期ページロードとデータ読込メニューへの移動"""
    driver.get("https://jasp.ism.ac.jp/RS-Decomp")
    iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.shiny-frame")))
    driver.switch_to.frame(iframe)
    wait_and_click(driver, "//*[@id='page_menu']/li[2]/a")

def upload_csv(driver, file_path, is_first_run=True):
    """CSVの読込設定とアップロード。2回目以降はモード選択をスキップする。"""
    
    if is_first_run:
        print("初回実行：ファイル読込モードを設定します")
        wait_and_click(driver, "//div[contains(@class, 'selectize-input')]")
        time.sleep(1)
        
        file_opt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-value='fileinput']"))
        )
        driver.execute_script("arguments[0].click();", file_opt)
        time.sleep(1)
        
        wait_and_click(driver, "//*[@id='dataApply']")
    else:
        print("2回目以降：モード設定をスキップしてファイルを直接送信します")
    file_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "file1"))
    )
    import os
    file_input.send_keys(os.path.abspath(file_path))
    driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", file_input)
    time.sleep(3)
    wait_and_click(driver, "//*[@id='do']")
    print(f"ファイル {os.path.basename(file_path)} の読み込み完了")

def set_decomp_parameters(driver, period="11", trend="3", seasonal="2", ar="2"):
    """Decompタブ内の各種パラメータ設定"""
    # 周期
    period_input = wait_and_click(driver, "//*[@id='period1-selectized']")
    period_input.send_keys(period)
    time.sleep(1)
    period_input.send_keys(Keys.ENTER)
    
    # 対数変換 (TRUE)
    wait_and_click(driver, "//input[@name='log' and @value='TRUE']")
    
    # 各種次数
    overwrite_input(driver, "trend.order", trend)
    overwrite_input(driver, "seasonal.order", seasonal)
    overwrite_input(driver, "ar.order", ar)
    
    # 曜日効果 (TRUE)
    wait_and_click(driver, "//input[@name='trade' and @value='TRUE']")
    
    # 実行
    wait_and_click(driver, "//*[@id='run1']")
    time.sleep(2)

def select_data_input_by_index(driver):
    """データ入力タブへ切り替えて手法を選択"""
    # タブ切り替え
    wait_and_click(driver, "//a[@data-value='データ入力']")
    time.sleep(2)

def select_other_method_by_index(driver, index, methods_list):
    """その他の手法タブへ切り替えて手法を選択"""
    # タブ切り替え
    wait_and_click(driver, "//a[@data-value='その他の手法']")
    
    # 手法選択プルダウンの枠をクリック
    parent_div = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='func-selectized']/.."))
    )
    parent_div.click()
    time.sleep(1)

    # 特定の手法を選択
    method_value = methods_list[index]
    xpath_option = f"//div[@data-value='{method_value}']"
    option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_option)))
    driver.execute_script("arguments[0].click();", option_element)
    
    # 実行
    wait_and_click(driver, "//*[@id='run2']")
    time.sleep(3)

def download_pdf(driver):
    """PDFダウンロードボタンのクリック"""
    wait_and_click(driver, "//*[@id='downloadPDF1']")
    time.sleep(5) # ダウンロード完了待ち