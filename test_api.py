import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_flow():
    # 1. Root check
    try:
        res = requests.get("http://127.0.0.1:8000/")
        print("Root Check:", res.json())
    except Exception as e:
        print("Root Check Failed (Make sure server is running on 8000):", e)
        return

    # 2. Signup
    email = f"test_{int(time.time())}@example.com"
    signup_data = {
        "username": f"user_{int(time.time())}",
        "email": email,
        "password": "Password123"
    }
    res = requests.post(f"{BASE_URL}/signup", json=signup_data)
    print("Signup Status:", res.status_code)
    if res.status_code != 200:
        print("Signup Detail:", res.text)
        return
    
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Diary Entry
    diary_data = {"content": "I had a great day today! Feeling very productive."}
    res = requests.post(f"{BASE_URL}/diary", json=diary_data, headers=headers)
    print("Diary Entry Status:", res.status_code)
    if res.status_code == 200:
        entry = res.json()
        print("Diary Sentiment:", entry.get("sentiment"))
        print("Diary AI Response:", entry.get("gemini_response"))
    else:
        print("Diary Entry Detail:", res.text)

    # 4. Chat
    chat_data = {"message": "How can I improve my mood?"}
    res = requests.post(f"{BASE_URL}/chat", json=chat_data, headers=headers)
    print("Chat Status:", res.status_code)
    if res.status_code == 200:
        print("Chat Response:", res.json().get("response"))

    # 5. Mood Board
    res = requests.get(f"{BASE_URL}/mood-board?period=weekly", headers=headers)
    print("Mood Board Status:", res.status_code)
    if res.status_code == 200:
        print("Mood Board Summary:", res.json().get("dominant_mood"))

if __name__ == "__main__":
    test_flow()
