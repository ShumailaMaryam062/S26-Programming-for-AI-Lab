import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

file_name = "data.json"


def get_data():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_folder, file_name)

    with open(full_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)

    return all_data


lost_found_data = get_data()


def check_words(user_text, words_list):
    text = user_text.lower()

    for word in words_list:
        if word.lower() in text:
            return True

    return False


def contact_info():
    contact_data = lost_found_data["contact"]

    msg = (
        f"Lost & Found Contact {lost_found_data['campus']}\n\n"
        f"Office: {contact_data['office']}\n"
        f"Address: {contact_data['address']}\n"
        f"Phone: {contact_data['phone']}\n"
        f"UAN: {contact_data['uan']}\n"
        f"Email: {contact_data['email']}"
    )

    return msg


def places_info():
    places = lost_found_data["common_locations"]

    msg = "Common places to check:\n"

    for i, place in enumerate(places, start=1):
        msg += f"{i}) {place}\n"

    return msg.strip()


def find_item_type(user_msg):

    if check_words(user_msg, ["id card", "student card", "card"]):
        return "id_card"

    if check_words(user_msg, ["wallet"]):
        return "wallet"

    if check_words(user_msg, ["charger", "adapter", "charging", "cable", "power bank"]):
        return "charger"

    if check_words(user_msg, ["book", "notebook", "copy", "notes"]):
        return "book"

    if check_words(user_msg, ["key", "keys"]):
        return "keys"

    if check_words(user_msg, ["usb", "flash", "pendrive", "pen drive", "flash drive"]):
        return "usb"

    return "default"


def make_reply(user_msg):
    user_msg = user_msg.lower().strip()
    normal_replies = lost_found_data.get("replies", {})

    # checking empty msg
    if user_msg == "":
        return normal_replies.get("empty", "Please enter a message.")

  
    if check_words(user_msg, ["hello", "hi", "hey", "salam", "assalam", "greetings"]):
        return normal_replies.get("greeting", "Hello! How can I help you?")

  
    if check_words(user_msg, ["contact", "office", "security", "student affairs", "email", "phone"]):
        return contact_info()

   
    if check_words(user_msg, ["common", "location", "locations", "where", "check", "look"]):
        return places_info()

  
    if check_words(user_msg, ["found", "picked up", "discover", "found a"]):
        item_name = find_item_type(user_msg)
        found_msgs = lost_found_data.get("found_replies", {})

        final_reply = found_msgs.get(
            item_name,
            found_msgs.get("default", "Please submit the found item to Security Office or Student Affairs.")
        )

        safety_msg = lost_found_data.get("safe_handling_tip", "")
        if safety_msg:
            final_reply += f"\n\nSafety Tip: {safety_msg}"

        return final_reply

   
    if check_words(user_msg, ["lost", "missing", "lose", "can't find", "lost a"]):
        item_name = find_item_type(user_msg)
        lost_msgs = lost_found_data.get("lost_replies", {})

        return lost_msgs.get(
            item_name,
            lost_msgs.get("default", "Please check the Lost & Found office at Student Affairs.")
        )

   
    if check_words(user_msg, ["thanks", "thank you", "bye", "goodbye", "see you"]):
        return normal_replies.get("thanks", "You're welcome! Feel free to ask if you need anything else.")

    return normal_replies.get(
        "default",
        "I didn't understand that. Please tell me what you lost or found."
    )


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_data = request.get_json()

        if not user_data or "message" not in user_data:
            return jsonify({"error": "Invalid request format"}), 400

        user_msg = user_data["message"]
        answer = make_reply(user_msg)

        return jsonify({"reply": answer})

    except Exception as e:
        print("Some error occured:", e)
        return jsonify({"error": "An error occurred while processing your message"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)