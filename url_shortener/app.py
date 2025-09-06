from fastapi import FastAPI, HTTPException
import json
import random
import string
import logging
from pathlib import Path

app = FastAPI()

# Setup logging
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# File to store URLs
URL_FILE = "urls.json"

# Load existing URLs or create empty
try:
    with open(URL_FILE, "r") as f:
        urls = json.load(f)
except FileNotFoundError:
    urls = {}

def save_urls():
    with open(URL_FILE, "w") as f:
        json.dump(urls, f)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def create_short_url(long_url: str):
    short_code = generate_short_code()
    urls[short_code] = long_url
    save_urls()
    logging.info(f"Short URL created: {short_code} -> {long_url}")
    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code in urls:
        long_url = urls[short_code]
        logging.info(f"Redirecting {short_code} to {long_url}")
        return {"original_url": long_url}
    else:
        logging.warning(f"Short code {short_code} not found")
        raise HTTPException(status_code=404, detail="URL not found")