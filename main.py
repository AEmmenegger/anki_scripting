import requests
import pyautogui
import keyboard
import base64
import time
url = 'http://localhost:8765'

last_updated_note_id = None


def get_newest_card_id_note_id(collection_name='初めての日本語能力試験-単語'):
    # Find all cards in the specified deck
    query = f"deck:{collection_name} added:1"
    payload = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": query
        }
    }
    response = requests.post(url, json=payload)
    card_ids = response.json().get('result', [])
    if card_ids:
        newest_card_id = max(card_ids)
        # Fetch info for the newest card ID to get its note ID
        payload = {
            "action": "cardsInfo",
            "version": 6,
            "params": {
                "cards": [newest_card_id]
            }
        }
        response = requests.post(url, json=payload)
        card_info = response.json().get('result', [])
        if card_info:
            note_id = card_info[0]['note']
            return newest_card_id, note_id  # Return both card and note IDs
    else:
        print("No cards found.")
        return None, None
    
    if card_ids:
        newest_card_id = max(card_ids)
        return newest_card_id
    else:
        print("No cards found.")

def upload_media_to_anki(file_path):
    
    # Open the file in binary mode, read it, and encode its contents in base64
    with open(file_path, 'rb') as image_file:
        # base64 encode & decode to get a string that's JSON-friendly
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    
    payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": file_path,
            "data": encoded_image
        }
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def get_newest_card_info(collection_name='初めての日本語能力試験-単語'):
    # Find all cards in the specified deck
    query = f"deck:{collection_name} added:1"
    payload = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": query
        }
    }
    response = requests.post(url, json=payload)
    card_ids = response.json().get('result', [])
    
    if card_ids:
        # Assuming the newest card has the highest ID
        newest_card_id = max(card_ids)
        
        # Fetch info for the newest card ID
        payload = {
            "action": "cardsInfo",
            "version": 6,
            "params": {
                "cards": [newest_card_id]
            }
        }
        response = requests.post(url, json=payload)
        card_info = response.json().get('result', [])
        print(card_info)
        
        if card_info:
            card = card_info[0]
            print(card.get('fields'))
            print(f"Card ID: {card.get('cardId')}")
            print(f"Front: {card.get('fields').get('SentKanji', {}).get('value', 'N/A')}")
            print(f"Back: {card.get('fields').get('SentFurigana', {}).get('value', 'N/A')}")
            #print(card.get('fields'))
        else:
            print("No card info found.")
    else:
        print("No cards found.")

def update_card_with_screenshot(note_id, image_file_name):
    # Adjust the payload to target the 'Image' field and embed the image using an <img> tag
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {
                    "Image": f"<img src='{image_file_name}'>", # Updating this to target the 'Image' field
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    return response.json()

get_newest_card_info()




def add_screenshot_to_newest_card():
    newest_card_id, note_id = get_newest_card_id_note_id()
    screenshot = pyautogui.screenshot()
    file_path = str(newest_card_id) +'.png'
    screenshot.save(file_path)
    print(upload_media_to_anki(file_path))
    print(update_card_with_screenshot(note_id, file_path))





def main():
    _, last_updated_note_id = get_newest_card_id_note_id()
    print (last_updated_note_id)
    while(True):
        newest_note_id = get_newest_card_id_note_id()[1]
        if newest_note_id != last_updated_note_id and newest_note_id is not None:
            add_screenshot_to_newest_card()
            last_updated_note_id = newest_note_id
        time.sleep(3)

if __name__ == "__main__":
    try:
        # Hold down the Shift key
        keyboard.press('shift')
        
        # Run the main part of your script
        main()
    finally:
        # No matter what happens in the script, release the Shift key at the end
        keyboard.release('shift')