import tkinter as tk
from tkinter import Entry, Listbox, END, messagebox, font, Button
from logic.calories_calc import DailyIntake, calculate_calories
from utils.utils import get_user_document_by_key
from firebase_config import db  # Import the db object
import json
import os

class AddFoodPopup(tk.Toplevel):
    def __init__(self, master, user_key=None, selected_meal=None):
        super().__init__(master)
        self.title("Add Food")
        self.geometry("400x300")  # Smaller size
        self.configure(bg="#DAE6E4")

        self.user_key = user_key
        self.selected_meal = selected_meal

        self.daily_intake = DailyIntake()

        customFont = font.Font(family="Consolas", size=12)  # Smaller font size

        self.selected_foods_listbox = Listbox(self, width=40, height=5, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                              highlightthickness=0, relief="flat")
        self.selected_foods_listbox.pack(pady=5)

        self.search_entry = Entry(self, bd=4, relief="sunken", font=customFont, width=30)
        self.search_entry.pack(pady=5)

        self.suggestion_listbox = Listbox(self, width=40, height=5, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                          highlightthickness=0, relief="flat")
        self.suggestion_listbox.pack(pady=5)

        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.suggestion_listbox.bind("<Double-Button-1>", self.add_food_to_list)
        self.selected_foods_listbox.bind("<Delete>", self.delete_selected_food)
        self.selected_foods_listbox.bind("<BackSpace>", self.delete_selected_food)

        button_frame = tk.Frame(self, bg="#DAE6E4")
        button_frame.pack(pady=5)

        add_button = Button(button_frame, text="Search", command=self.search_action)
        add_button.pack(side=tk.LEFT, padx=5)

        save_button = Button(button_frame, text="Save Food", command=self.save_food)
        save_button.pack(side=tk.RIGHT, padx=5)

        self.restore_meals()

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

    def restore_meals(self):
        # Logic for restoring meals from JSON or another source
        pass

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

    def save_food(self):
        food_items = self.selected_foods_listbox.get(0, END)
        if food_items:
            food_details = []
            total_calories = 0
            for item in food_items:
                food_name, calories = item.rsplit(' - ', 1)
                calories = float(calories.split()[0])  # Convert to float instead of int
                total_calories += calories
                food_details.append({"name": food_name, "calories": calories})

            try:
                # Find the user document by user_key
                user_doc_id, user_data = get_user_document_by_key(self.user_key)
                if user_doc_id is None:
                    messagebox.showerror("Error", "User not found.")
                    return

                # Update the data with new food details and total calories
                if self.selected_meal not in user_data:
                    user_data[self.selected_meal] = []
                user_data[self.selected_meal].extend(food_details)

                if "cals" not in user_data:
                    user_data["cals"] = 0
                user_data["cals"] += total_calories

                # Save the updated data back to Firebase
                db.collection('users').document(user_doc_id).set(user_data)

                messagebox.showinfo("Saved", "Food items have been saved successfully.")
            except Exception as e:
                print(f"Error saving food data: {e}")
                messagebox.showerror("Error", f"Failed to save food data: {e}")
        else:
            messagebox.showwarning("Empty", "No food items to save.")
