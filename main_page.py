from tkinter import *
from tkinter.font import Font
from pathlib import Path
from LogIn import setup_login_page
from SignUp import setup_signup_page
from tkinter import Tk, Canvas, Label, Button, PhotoImage



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

import json

with open("serviceAccountKey.json") as f:
    service_account_info = json.load(f)

def blink_caret(caret, canvas, delay_ms=600):
    current_state = canvas.itemcget(caret, "state")
    new_state = "hidden" if current_state == "normal" else "normal"
    canvas.itemconfig(caret, state=new_state)
    canvas.after(delay_ms, blink_caret, caret, canvas)


def add_delete_text(word_list, label, canvas, delay_ms=150, is_adding=True, index=0):
    if not word_list:
        return

    word = word_list[index] if index < len(word_list) else ""

    if is_adding:
        label_text = label.cget("text")
        if len(label_text) < len(word):
            label.config(text=word[:len(label_text) + 1])
            canvas.after(delay_ms, add_delete_text, word_list, label, canvas, delay_ms, True, index)
        else:
            next_index = (index + 1) % len(word_list)
            canvas.after(delay_ms, add_delete_text, word_list, label, canvas, delay_ms, False, next_index)
    else:
        if label.cget("text"):
            label.config(text=label.cget("text")[:-1])
            canvas.after(delay_ms, add_delete_text, word_list, label, canvas, delay_ms, False, index)
        else:
            canvas.after(delay_ms, add_delete_text, word_list, label, canvas, delay_ms, True, index)
def show_login():
    for widget in window.winfo_children():
        widget.destroy()
    setup_login_page(window)

def show_signup():
    for widget in window.winfo_children():
        widget.destroy()
    setup_signup_page(window)


window = Tk()
window.geometry("937x503")
window.configure(bg="#FFFCF1")

canvas = Canvas(window, bg="#FFFCF1", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(679.0, 365.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(200.0, 251.0, image=image_image_2)


JFont = Font(family="Consolas", slant="italic", size=17)
JNFont = Font(family="Consolas", slant="italic", size=17, weight="bold")
bigFont = Font(family="Consolas", slant="italic", underline=1, size=18)
secondFont = Font(family="Consolas", slant="italic", underline=0)
youFont = Font(family="Consolas", weight="bold", slant="italic")
EatFont = Font(family="Consolas", size=17, slant="italic")

labels = [
    ("Start your journey", JFont, 560, 340, "#FFFFFF"),
    ("NOW", JNFont, 640, 370, "#FFFFFF"),
    ("Who's counting?", bigFont, 435,51, "#FFFCF1"),
    ("We are! So ", secondFont, 435, 91, "#FFFCF1"),
    ("you", youFont, 553, 91, "#FFFCF1"),
    ("don't have to!", secondFont, 593, 91, "#FFFCF1"),
    ("Eat", EatFont, 433, 119, "#FFFCF1")
]

for text, font,  x, y,bg in labels:
    Label(window, text=text, font=font, bg=bg).place(x=x, y=y)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_LogIn = Button(window, image=button_image_1, borderwidth=0, highlightthickness=0, command=show_login, relief="flat")
button_LogIn.place(x=445.0, y=209.0, width=214.0, height=49.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_SignUp = Button(window, image=button_image_2, borderwidth=0, highlightthickness=0, command=show_signup, relief="flat")
button_SignUp.place(x=695.0, y=210.0, width=214.0, height=49.0)

text_label = Label(window, font=EatFont, bg="#FFFCF1", fg="#649089", text="")
text_label.place(x=480, y=119)

window.after(700, add_delete_text, ["Healthy", "Better", "Smart"], text_label, canvas)

window.resizable(False, False)
window.mainloop()