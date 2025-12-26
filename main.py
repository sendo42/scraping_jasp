import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import config
import jasp_operations as jasp

def main():
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-web-security")
    opts.add_experimental_option("prefs", config.CHROME_PREFS)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    is_first_file = True

    try:
        # inputディレクトリ内の全CSVを取得
        csv_files = [f for f in os.listdir(config.INPUT_DIR) if f.endswith('.csv')]
        
        if not csv_files:
            print("処理対象のCSVファイルが見つかりません。")
            return

        # ページ初期化
        jasp.setup_jasp_page(driver)

        for filename in csv_files:
            file_path = os.path.join(config.INPUT_DIR, filename)
            print(f"\n======== 処理開始: {filename} ========")
            
            # データ入力タブへ移動
            jasp.select_data_input_by_index(driver)

            # アップロード
            jasp.upload_csv(driver, file_path, is_first_run=is_first_file)
            is_first_file = False
            
            # Decomp設定と実行
            jasp.set_decomp_parameters(driver)
            
            # PDF ダウンロード
            jasp.download_pdf(driver)

            # その他の手法を順番に実行（例: 0〜7まで全部やる場合）
            # for i in range(len(config.METHODS)):
            #     print(f"解析手法実行中: {config.METHODS[i]}")
            #     jasp.select_other_method_by_index(driver, i, config.METHODS)
            #     jasp.download_pdf(driver)
                
            print(f"完了: {filename}")

    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
    finally:
        print("全タスク終了。ブラウザを閉じます。")
        driver.quit()

if __name__ == "__main__":
    main()