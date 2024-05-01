import pandas as pd
import CaloriesCalc

class Food:
    def __init__(self, category, description, fat, carbohydrates, protein):
        self.category = category
        self.description = description
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.protein = protein

class DailyIntake:
    def __init__(self):
        self.foods = []
        self.intake_calories = 0

    def load_food_data(self, file_path):
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            food = Food(row['Category'], row['Description'], row['Data.Fat.Total Lipid'], row['Data.Carbohydrate'],
                        row['Data.Protein'])
            self.foods.append(food)

    def add_meal(self, meal_type):
        while True:
            food_name = input("Introduceți numele alimentului: ")
            weight = float(input("Introduceți gramajul (în grame): "))
            for food in self.foods:
                if food_name.lower() in food.description.lower():
                    calories = CaloriesCalc.calculate_calories(food, weight)
                    self.intake_calories += calories
                    print(f"{food_name} conține aproximativ {calories:.2f} calorii.")
                    break
            else:
                print("Alimentul nu a fost găsit în baza de date.")

            more_meals = input("Doriți să adăugați și alte alimente la această masă? (da/nu): ")
            if more_meals.lower() != 'da':
                break


def main():
    daily_intake = DailyIntake()
    daily_intake.load_food_data('food.csv')

    while True:
        meal_type = input("Introduceți tipul mesei (Breakfast, lunch sau dinner), sau 'done' pentru a finaliza ziua: ")

        if meal_type.lower() == 'done':
            print(f"Aportul total de calorii pentru ziua de astăzi este: {daily_intake.intake_calories:.2f} calorii.")
            break

        if meal_type.lower() not in ['breakfast', 'lunch', 'dinner']:
            print(
                "Tip de masă invalid. Vă rugăm să introduceți 'breakfast', 'lunch', 'dinner', sau 'done' pentru a finaliza ziua.")
            continue

        print(f"Adăugați alimentele pentru {meal_type}:")
        daily_intake.add_meal(meal_type)


if __name__ == "__main__":
    main()
