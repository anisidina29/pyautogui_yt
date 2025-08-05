import pyautogui
import easyocr
import time
import random
import subprocess
import sys
import requests

# Get email and password from command line arguments
EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]

# Initialize EasyOCR with Vietnamese and English
reader = easyocr.Reader(['vi', 'en'])

# Find text position function
def find_text_position(text_list):
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenads.png"
    screenshot.save(screenshot_path)
    results = reader.readtext(screenshot_path)

    for (bbox, text, prob) in results:
        for t in text_list:
            if t.lower() in text.lower():
                (top_left, _, bottom_right, _) = bbox
                x = int((top_left[0] + bottom_right[0]) / 2)
                y = int((top_left[1] + bottom_right[1]) / 2)
                return (x, y)
    return None

# Skip ad function
def skip_ad():
    try:
        skip_btn = find_text_position(["Skip", "Skip Ads"])
        if skip_btn:
            pyautogui.moveTo(*skip_btn, duration=0.3)
            pyautogui.click()
            print("Clicked Skip Ad button")
    except Exception as e:
        print(f"[ERROR] Error while skipping ad: {e}")

# Launch Chrome in fullscreen (NOT incognito)
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
video_url = "https://www.youtube.com"
subprocess.Popen(f'{chrome_path} --start-fullscreen {video_url}')

# Wait for Chrome and YouTube to load
time.sleep(5)

# Take screenshot for OCR
screenshot = pyautogui.screenshot()
screenshot_path = "screen.png"
screenshot.save(screenshot_path)

# Use OCR to detect "Sign in" button
results = reader.readtext(screenshot_path)
found = False
for (bbox, text, prob) in results:
    if "sign in" in text.lower():
        print(f"Found: {text} (confidence {prob:.2f})")
        (top_left, top_right, bottom_right, bottom_left) = bbox
        x = int((top_left[0] + bottom_right[0]) / 2)
        y = int((top_left[1] + bottom_right[1]) / 2)
        pyautogui.moveTo(x, y, duration=0.5)
        for _ in range(3):  # Click 3 times
            pyautogui.click()
            time.sleep(0.2)
        found = True
        break

if not found:
    print("Sign in button not found!")

time.sleep(5)  # Wait for login page

# Enter email
pyautogui.typewrite(EMAIL)
time.sleep(3)
pyautogui.press('enter')
time.sleep(3)

# Enter password
pyautogui.typewrite(PASSWORD)
pyautogui.press('enter')
print("Login attempt finished (if email/password is correct)")
time.sleep(5)

# Function to get links from GitHub
def get_video_links():
    url = "https://raw.githubusercontent.com/anisidina29/pyautogui_yt/refs/heads/main/links.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            links = [line.strip() for line in response.text.splitlines() if line.strip()]
            print(f"[INFO] Retrieved {len(links)} links from GitHub")
            return links
        else:
            print("[WARNING] Failed to retrieve links")
            return []
    except Exception as e:
        print(f"[ERROR] Could not fetch links: {e}")
        return []

# Get initial links
video_links = get_video_links()
current_index = 0

# Function to open a video
def open_video(link):
    subprocess.Popen(f'{chrome_path} --start-fullscreen {link}')
    time.sleep(8)
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
    pyautogui.click()
    print(f"[INFO] Playing video: {link}")

# Human-like action simulation
import pyautogui
import random
import time

def human_like_action():
    actions = (
        ["move_mouse"] * 5 +  # 50%
        ["idle"] * 2 +        # 20%
        ["backward", "forward", "volume_up", "volume_down",
         "mute", "subtitle", "pause_play", "speed_up", "speed_down"]  # 30%
    )

    action = random.choice(actions)

    if action == "backward":
        pyautogui.press('j')  # Rewind 10s
        print("[ACTION] Rewind 10s")
    elif action == "forward":
        pyautogui.press('l')  # Forward 10s
        print("[ACTION] Forward 10s")
    elif action == "volume_up":
        pyautogui.press('up')  # Volume up
        print("[ACTION] Volume up")
    elif action == "volume_down":
        pyautogui.press('down')  # Volume down
        print("[ACTION] Volume down")
    elif action == "mute":
        pyautogui.press('m')  # Mute/Unmute
        print("[ACTION] Mute/Unmute")
    elif action == "subtitle":
        pyautogui.press('c')  # Toggle subtitles
        print("[ACTION] Toggle subtitles")
    elif action == "pause_play":
        pyautogui.press('k')  # Play/Pause
        print("[ACTION] Play/Pause video")
    elif action == "speed_up":
        pyautogui.hotkey('shift', '>')  # Increase speed
        print("[ACTION] Speed up")
    elif action == "speed_down":
        pyautogui.hotkey('shift', '<')  # Decrease speed
        print("[ACTION] Speed down")
    elif action == "move_mouse":
        x = random.randint(200, 1200)
        y = random.randint(200, 700)
        pyautogui.moveTo(x, y, duration=0.5)
        print(f"[ACTION] Mouse moved to ({x},{y})")
    elif action == "idle":
        print("[ACTION] Idle (do nothing)")
        
# Start watching videos
print("Starting video watching automation...")

while True:
    try:
        if current_index >= len(video_links):
            video_links = get_video_links()
            current_index = 0

        open_video(video_links[current_index])
        current_index += 1

        watch_time = random.randint(300, 800)  # 3–5 min
        start_time = time.time()
        print(f"[INFO] Watching video for {watch_time // 60} min...")

        while time.time() - start_time < watch_time:
            skip_ad()
            human_like_action()
            time.sleep(random.randint(100, 300))

    except Exception as e:
        print(f"[ERROR] Main loop error: {e}")
