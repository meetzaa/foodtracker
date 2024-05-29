from tkinter import Canvas, Label, Button, Entry, PhotoImage, Listbox, END, messagebox, font
from .base_page import BasePage
from logic.calories_calc import DailyIntake, calculate_calories
from google.cloud import firestore
from firebase_config import db  # Ensure this is correctly importing your Firestore configuration
from pathlib import Path

class AddFoodPage(BasePage):
    def __init__(self, master, controller, user_key=None, selected_meal=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.selected_meal = selected_meal
        self.configure(bg="#DAE6E4")

        self.daily_intake = DailyIntake()

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("back.png", 22, 17, 42, 36, lambda: self.go_back()),
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img = PhotoImage(file=self.relative_to_assets(image_name))
            self.images.append(img)

            button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command, bg="#DAE6E4")
            button.place(x=x, y=y, width=width, height=height)
            button.image = img

        customFont = font.Font(family="Consolas", size=15)

        self.selected_foods_listbox = Listbox(self, width=50, height=10, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                              highlightthickness=0, relief="flat")
        self.selected_foods_listbox.place(x=230, y=50)

        self.search_entry = Entry(self, bd=4, relief="sunken", font=customFont, width=35)
        self.search_entry.place(x=230, y=230)

        self.suggestion_listbox = Listbox(self, width=50, height=10, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                          highlightthickness=0, relief="flat")
        self.suggestion_listbox.place(x=230, y=270)

        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.suggestion_listbox.bind("<Double-Button-1>", self.add_food_to_list)
        self.selected_foods_listbox.bind("<Delete>", self.delete_selected_food)
        self.selected_foods_listbox.bind("<BackSpace>", self.delete_selected_food)

        add_button = Button(self, text="Search", command=self.search_action)
        add_button.place(x=500, y=230)

    def update_suggestions(self, event):
        search_text = self.search_entry.get().lower()
        self.suggestion_listbox.delete(0, END)
        suggestions = self.daily_intake.find_food_suggestions(search_text)

        for suggestion in suggestions:
            description = getattr(suggestion, 'description', 'Unknown')
            calories = calculate_calories(suggestion)
            self.suggestion_listbox.insert(END, f"{description} - {calories} kcal")

    def add_food_to_list(self, event):
        selected_food_index = self.suggestion_listbox.curselection()
        if selected_food_index:
            selected_food_name = self.suggestion_listbox.get(selected_food_index)
            self.selected_foods_listbox.insert(END, selected_food_name)

    def search_action(self):
        food_name = self.search_entry.get().lower().strip()
        found_food = self.daily_intake.find_food(food_name)
        if found_food:
            messagebox.showinfo("Găsit", f"Alimentul '{food_name}' a fost găsit.")
        else:
            messagebox.showerror("Negăsit", f"Alimentul '{food_name}' nu a fost găsit.")

    def delete_selected_food(self, event):
        selected_index = self.selected_foods_listbox.curselection()
        if selected_index:
            self.selected_foods_listbox.delete(selected_index)

    def go_back(self):
        food_items = []
        for item in self.selected_foods_listbox.get(0, END):
            description, calories = item.rsplit(' - ', 1)
            calories = float(calories.split()[0])
            food_items.append({"description": description, "calories": calories})

        try:
            # Query to find the user document with the specified user_key
            users_ref = db.collection('users')
            query = users_ref.where('user_key', '==', self.user_key).stream()

            user_doc = None
            for doc in query:
                user_doc = doc
                break

            if user_doc is None:
                raise Exception("User not found")

            user_id = user_doc.id
            user_ref = db.collection('users').document(user_id).collection('meals').document(self.selected_meal)
            for food in food_items:
                user_ref.collection('items').add(food)

            messagebox.showinfo("Success", "Food added successfully")
            self.controller.show_page("LogFoodPage", self.user_key)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add food: {e}")

    def update(self, user_key, selected_meal):
        self.user_key = user_key
        self.selected_meal = selected_meal
        # Additional update logic if needed

    def relative_to_assets(self, path: str) -> str:
        return str(Path(__file__).parent.parent / 'assets' / 'frame15' / path)