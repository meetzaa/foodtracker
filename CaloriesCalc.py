import tkinter as tk
from tkinter import font, Listbox, END, messagebox
import pandas as pd

class Food:
    def __init__(self, category, description, fat, carbohydrates, protein):
        self.category = category
        self.description = description
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.protein = protein

def calculate_calories(food, weight=100):
    calories = (food.fat * 9 + food.carbohydrates * 4 + food.protein * 4) * (weight / 100)
    return calories

class DailyIntake:
    def __init__(self):
        self.foods = []
        self.load_food_data('food.csv')

    def load_food_data(self, file_path):
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            food = Food(row['Category'], row['Description'], row['Data.Fat.Total Lipid'], row['Data.Carbohydrate'], row['Data.Protein'])
            self.foods.append(food)

    def find_food_suggestions(self, food_name):
        if food_name is None:
            return []
        food_name = food_name.lower().strip()
        suggestions = [food for food in self.foods if food_name in food.description.lower()]
        return suggestions

    def find_food(self, food_name):
        suggestions = self.find_food_suggestions(food_name)
        return suggestions[0] if suggestions else None

daily_intake = DailyIntake()
