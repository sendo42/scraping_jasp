import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import glob


def wait_and_click(driver, xpath, timeout=300):
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

def upload_csv(driver, file_path, count):
    """CSVの読込設定とアップロード。2回目以降はモード選択をスキップする。"""
    
    if count % 30 == 0:
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

def set_decomp_parameters(driver, period="12", trend="2", seasonal="1", ar="2"):
    """Decompタブ内の各種パラメータ設定"""
    # 周期
    period_input = wait_and_click(driver, "//*[@id='period1-selectized']")
    period_input.send_keys(period)
    time.sleep(1)
    period_input.send_keys(Keys.ENTER)
    
    # 対数変換 (TRUE)
    # wait_and_click(driver, "//input[@name='log' and @value='TRUE']")
    
    # 各種次数
    overwrite_input(driver, "trend.order", trend)
    overwrite_input(driver, "seasonal.order", seasonal)
    overwrite_input(driver, "ar.order", ar)
    
    # 曜日効果 (TRUE)
    # wait_and_click(driver, "//input[@name='trade' and @value='TRUE']")
    
    # 実行
    wait_and_click(driver, "//*[@id='run1']")
    time.sleep(2)

def select_data_input_by_index(driver):
    """データ入力タブへ切り替えて手法を選択"""
    # タブ切り替え
    wait_and_click(driver, "//a[@data-value='データ入力']")
    time.sleep(2)

def download_csv_from_table(driver, output_dir, new_name):
    """
    出力データタブ内のCSVダウンロードボタンを押し、指定した名前にリネームする
    StaleElementReferenceException 対策済み
    """
    # 1. 「出力データ」タブをクリックして移動（もし移動していなければ）
    print("📂 '出力データ' タブに切り替えています...")
    wait_and_click(driver, "//a[@data-value='出力データ']")
    time.sleep(3) # タブ切り替え後の描画待ち

    # 2. ダウンロード前のCSVファイルリストを取得
    before_files = set(glob.glob(os.path.join(output_dir, "*.csv")))

    # 3. CSVダウンロードボタンをクリック (再試行付き)
    xpath = "//button[contains(@class, 'buttons-csv')]"
    print("⏳ CSVダウンロードボタンを探索中...")
    
    success = False
    for i in range(3): # 最大3回再試行
        try:
            # 要素が現れるのを待つ
            WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, xpath)))
            csv_buttons = driver.find_elements(By.XPATH, xpath)
            
            if csv_buttons:
                target_button = csv_buttons[-1]
                # JSでクリック（これ自体がStale対策にもなる）
                driver.execute_script("arguments[0].click();", target_button)
                success = True
                break
        except Exception as e:
            print(f"⚠️ 試行 {i+1} 回目: 要素が不安定です。再試行します... ({e})")
            time.sleep(2)
            continue

    if not success:
        print("❌ CSVダウンロードボタンのクリックに失敗しました")
        return

    # 4. ファイルが出現するまで待機（最大180秒）
    print(f"📥 {new_name} をダウンロード中...")
    timeout = 180
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        time.sleep(2)
        after_files = set(glob.glob(os.path.join(output_dir, "*.csv")))
        new_files = after_files - before_files
        
        if new_files:
            downloaded_file = list(new_files)[0]
            if not downloaded_file.endswith('.crdownload'):
                time.sleep(1)
                final_path = os.path.join(output_dir, new_name)
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(downloaded_file, final_path)
                print(f"✅ CSV保存完了: {new_name}")
                return
                
    print(f"❌ {new_name} の保存がタイムアウトしました")




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

def download_pdf(driver, output_dir, new_name):
    """
    PDFをダウンロードし、指定した名前にリネームする
    new_name: リネーム後の名前 (例: 'test.pdf')
    """
    # 1. ダウンロード前のフォルダ内のファイルリストを取得
    before_files = set(glob.glob(os.path.join(output_dir, "*.pdf")))

    # 2. ダウンロードボタンをクリック
    wait_and_click(driver, "//*[@id='downloadPDF1']")
    
    # 3. ファイルが出現するまで待機（最大30秒）
    print(f"📥 {new_name} をダウンロード中...")
    timeout = 30
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        time.sleep(1)
        after_files = set(glob.glob(os.path.join(output_dir, "*.pdf")))
        new_files = after_files - before_files
        
        if new_files:
            # 新しく増えたファイル（RSDxxx.pdf）を特定
            downloaded_file = list(new_files)[0]
            
            # .crdownload (Chromeのダウンロード中一時ファイル) でないことを確認
            if not downloaded_file.endswith('.crdownload'):
                # リネーム実行
                final_path = os.path.join(output_dir, new_name)
                
                # 同名のファイルが既にある場合は削除（上書き）
                if os.path.exists(final_path):
                    os.remove(final_path)
                    
                os.rename(downloaded_file, final_path)
                print(f"✅ 保存完了: {new_name}")
                return
                
    print(f"❌ {new_name} のダウンロードがタイムアウトしました")