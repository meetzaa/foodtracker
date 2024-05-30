import tkinter as tk
from tkinter import Canvas, Label, Button, Entry, Listbox, END, messagebox, font
from logic.calories_calc import DailyIntake, calculate_calories
from pathlib import Path
import json

class AddFoodPopup(tk.Toplevel):
    def __init__(self, master, user_key=None, selected_meal=None):
        super().__init__(master)
        self.title("Add Food")
        self.geometry("600x500")
        self.configure(bg="#DAE6E4")

        self.user_key = user_key
        self.selected_meal = selected_meal

        self.daily_intake = DailyIntake()

        customFont = font.Font(family="Consolas", size=15)

        self.selected_foods_listbox = Listbox(self, width=50, height=10, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                              highlightthickness=0, relief="flat")
        self.selected_foods_listbox.pack(pady=10)

        self.search_entry = Entry(self, bd=4, relief="sunken", font=customFont, width=35)
        self.search_entry.pack(pady=10)

        self.suggestion_listbox = Listbox(self, width=50, height=10, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                          highlightthickness=0, relief="flat")
        self.suggestion_listbox.pack(pady=10)

        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.suggestion_listbox.bind("<Double-Button-1>", self.add_food_to_list)
        self.selected_foods_listbox.bind("<Delete>", self.delete_selected_food)
        self.selected_foods_listbox.bind("<BackSpace>", self.delete_selected_food)

        add_button = Button(self, text="Search", command=self.search_action)
        add_button.pack(pady=10)

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
        # Logic for restoring meals from JSON
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

    def update(self, user_key, selected_meal):
        self.user_key = user_key
        self.selected_meal = selected_meal
        # Additional update logic if needed

