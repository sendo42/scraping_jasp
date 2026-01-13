import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import config
import jasp_operations as jasp
import discord_notify as notify
import progress

def main():
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-web-security")
    opts.add_experimental_option("prefs", config.CHROME_PREFS)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    progress_file = os.path.join(config.OUTPUT_DIR, "progress.txt")
    done_files = progress.load_progress(progress_file)

    count = 0
    start = time.time()
    try:
        csv_files = [f for f in os.listdir(config.INPUT_DIR) if f.endswith('.csv')]
        
        if not csv_files:
            print("処理対象のCSVファイルが見つかりません。")
            return

        for filename in csv_files:

            if filename in done_files:
                print(f"スキップ（処理済み）: {filename}")
                continue

            file_path = os.path.join(config.INPUT_DIR, filename)
            base_name = os.path.splitext(filename)[0]
            
            # --- 保存名の定義 ---
            pdf_name = f"{base_name}.pdf"
            target_csv_name = f"{base_name}.csv" # ここを定義

            print(f"\n======== 処理開始: {filename} ========")
            if count == 0:
                jasp.setup_jasp_page(driver)
            
            # データ入力タブへ移動
            jasp.select_data_input_by_index(driver)

            # アップロード
            jasp.upload_csv(driver, file_path, count)
            
            # Decomp設定と実行
            jasp.set_decomp_parameters(driver)
            
            # --- PDF ダウンロードとリネーム ---
            # 引数に OUTPUT_DIR と 新しい名前を渡す
            jasp.download_pdf(driver, config.OUTPUT_DIR, pdf_name)
            jasp.download_csv_from_table(driver, config.OUTPUT_DIR, target_csv_name)

            print(f"完了: {filename}")
            progress.save_progress(progress_file, filename)
            count += 1
    
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        print(f"処理したファイルの数： {count}")
        end = time.time()
        elapsed = end - start

        notify.notify_discord(
            f"予期せぬエラーが発生しました： {e}\n"
            f"処理したファイルの数：           {count}i\n"
            f"経過時間：                       {elapsed}秒"
        )

    finally:
        print("全タスク終了。ブラウザを閉じます。")
        driver.quit()

if __name__ == "__main__":
    while True:
        remaining_before = progress.count_remaining_files()

        if remaining_before == 0:
            print("✅ すべての CSV を処理しました。終了します。")
            break

        print(f"🔁 残り {remaining_before} 件。新しいブラウザで処理を開始します。")

        main()  # ← 1回の main は「少数（例: 1〜30件）」だけ処理する

        remaining_after = progress.count_remaining_files()

        if remaining_after == remaining_before:
            # 進捗が進んでいない = 異常

            notify.notify_discord(
                f"進捗が更新されていません。院生室のWifiはついてますが、サーバー側に問題があるかもしれません。"
            )
            raise RuntimeError(
                "進捗が更新されていません。無限ループ防止のため停止します。"
            )

