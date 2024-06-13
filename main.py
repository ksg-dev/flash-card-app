from tkinter import *
import pandas as pd
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
unknown_words = []


# ---------------------------- PANDAS SET UP ------------------------------- #
# Check for words_to_learn file, if exists, use that, else use French words
try:
    word_list = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    data = original_data.to_dict(orient="records")

else:
    # Convert to list of dictionaries
    data = word_list.to_dict(orient="records")


# ---------------------------- NEW CARD ------------------------------- #


def get_card():
    global current_card, flip_timer
    # every time we click on new card, timer has to be invalidated
    window.after_cancel(flip_timer)

    current_card = random.choice(data)
    fr_word = current_card["French"]
    canvas.itemconfig(lang_label, text="French", fill="black")
    canvas.itemconfig(word, text=fr_word, fill="black")

    # change back to front of card
    canvas.itemconfig(card_img, image=card_front)

    # Begin flip timer again
    flip_timer = window.after(3000, func=card_flip)


# ---------------------------- FLIP CARD ------------------------------- #


def card_flip():
    en_word = current_card["English"]

    canvas.itemconfig(card_img, image=card_back)
    canvas.itemconfig(lang_label, text="English", fill="white")
    canvas.itemconfig(word, text=en_word, fill="white")

# ---------------------------- SAVE PROGRESS ------------------------------- #


def known():
    data.remove(current_card)
    to_learn = pd.DataFrame(data)
    to_learn.to_csv("data/words_to_learn.csv", index=False)
    get_card()


# ---------------------------- UI SETUP ------------------------------- #

# Window set up
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

# call flip here so global and can be called with each card
flip_timer = window.after(3000, card_flip)

# Canvas set up
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# Add card image
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_img = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)


# add text
lang_label = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))


# Buttons
correct = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

correct_button = Button(image=correct, highlightthickness=0, command=known)
wrong_button = Button(image=wrong, highlightthickness=0, command=get_card)

correct_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)

# call card function to start w card
get_card()

window.mainloop()
