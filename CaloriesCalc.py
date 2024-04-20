import pandas as pd

class Food:
    def __init__(self, category, description, fat, carbohydrates, protein):
        self.category = category
        self.description = description
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.protein = protein

def load_food_data(file_path):
    foods = []
    data = pd.read_csv(file_path)
    for index, row in data.iterrows():
        food = Food(row['Category'], row['Description'], row['Data.Fat.Total Lipid'], row['Data.Carbohydrate'], row['Data.Protein'])
        foods.append(food)
    return foods

def calculate_calories(food, weight):
    calories = (food.fat * 9) + (food.carbohydrates * 4) + (food.protein * 4)
    return calories * (weight / 100)

def main():
    foods = load_food_data('food.csv')
    while True:
        food_name = input("Introduceți numele alimentului: ")
        weight = float(input("Introduceți gramajul (în grame): "))
        for food in foods:
            if food_name.lower() in food.description.lower():
                calories = calculate_calories(food, weight)
                print(f"{food_name} conține aproximativ {calories:.2f} calorii.")
                break
        else:
            print("Alimentul nu a fost găsit în baza de date.")

if __name__ == "__main__":
    main()
