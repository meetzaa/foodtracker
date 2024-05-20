import pandas as pd
import CaloriesCalc
import requests

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

    def get_food_portion(self, food_name):
        api_endpoint = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": "7809eebb",
            "x-app-key": "c44b1f48db5ab8f5c94ecf33d57f7093",
            "x-remote-user-id": "0",
            "Content-Type": "application/json"
        }
        data = {
            "query": food_name
        }
        response = requests.post(api_endpoint, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if 'foods' in data and len(data['foods']) > 0:
                food_data = data['foods'][0]
                portion_size = food_data.get('serving_weight_grams', None)
                if portion_size is not None:
                    return food_name, portion_size
        print("Portion size not found for this food.")
        return None, None
    def add_meal(self, meal_type):
        while True:
            food_name = input("Enter the name of the food: ")
            portion_size = self.get_food_portion(food_name)
            if portion_size:
                food_name, weight = portion_size
                for food in self.foods:
                    if food_name.lower() in food.description.lower():
                        calories = CaloriesCalc.calculate_calories(food, weight)
                        self.intake_calories += calories
                        print(f"{food_name} contains approximately {calories:.2f} calories.")
                        break
                else:
                    print("Food not found in the database.")
            else:
                print("Portion size not available for this food.")

            more_meals = input("Do you want to add more foods to this meal? (yes/no): ")
            if more_meals.lower() != 'yes':
                break

def main():
    daily_intake = DailyIntake()
    daily_intake.load_food_data('food.csv')

    while True:
        meal_type = input("Enter the meal type (Breakfast, lunch, or dinner), or 'done' to finish the day: ")

        if meal_type.lower() == 'done':
            print(f"Total calorie intake for today is: {daily_intake.intake_calories:.2f} calories.")
            break

        if meal_type.lower() not in ['breakfast', 'lunch', 'dinner']:
            print("Invalid meal type. Please enter 'breakfast', 'lunch', 'dinner', or 'done' to finish the day.")
            continue

        print(f"Add foods for {meal_type}:")
        daily_intake.add_meal(meal_type)

if __name__ == "__main__":
    main()
