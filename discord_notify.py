import requests
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# =========================
# Discord 通知関数
# =========================
DISCORD_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1460539717396463619/"
    "25CjpdnUoGpivE8G4XyYF25o5pwGwX4jPor6UGrhEKPlaoLvfTVYEPg3FVZelUEzn-0a"
)

def notify_discord(message: str):
    payload = {
        "content": message
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

