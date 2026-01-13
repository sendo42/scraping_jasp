import discord_notify as notify

e = "testだぜ"
count = -1
elapsed = 10


notify.notify_discord(
    f"予期せぬエラーが発生しました： {e}\n"
    f"処理したファイルの数：           {count}\n"
    f"経過時間：                       {elapsed}秒"
)