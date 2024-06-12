from tkinter import *
import pandas as pd
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
count = 0
card = None

# ---------------------------- PANDAS SET UP ------------------------------- #
# Import data
word_list = pd.read_csv("data/french_words.csv")
df = pd.DataFrame(word_list)
# Convert to list of dictionaries
data = df.to_dict(orient="records")

print(data)

# ---------------------------- NEW CARD ------------------------------- #

def reset():
    global card
    # Cancel timer
    window.after_cancel(card)
    # Reset labels and canvas
    canvas.itemconfig(lang_label, text="French")
    canvas.itemconfig(card_img, image=card_front)
    card = None

def get_card():
    global card
    reset()
    card = random.choice(data)
    fr_word = card["French"]

    canvas.itemconfig(word, text=fr_word)

    # window.after_cancel(card)

    # print(card)
    # print(fr_word)
    # print(en_word)

# new_card()
# ---------------------------- FLIP CARD ------------------------------- #


def card_flip():
    en_word = card["English"]

    canvas.itemconfig(card_img, image=card_back)
    canvas.itemconfig(lang_label, text="English", fill="white")
    canvas.itemconfig(word, text=en_word, fill="white")



# ---------------------------- UI SETUP ------------------------------- #

# Window set up
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
# window.minsize(width=900, height=650)
window.after(3000, card_flip)

# Canvas set up
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# Add card image
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_img = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)


# add text
lang_label = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
timer_text = canvas.create_text(400, 400, text="0")

# Buttons
correct = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

correct_button = Button(image=correct, highlightthickness=0, command=get_card)
wrong_button = Button(image=wrong, highlightthickness=0, command=get_card)

correct_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)


window.mainloop()


