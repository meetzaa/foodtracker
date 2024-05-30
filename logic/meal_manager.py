from firebase_config import db

class MealManager:
    def __init__(self, user_key):
        self.user_key = user_key
        self.meals_collection = db.collection("users").document(self.user_key).collection("meals")

    def get_meal(self, meal_type):
        meal_doc = self.meals_collection.document(meal_type).get()
        if meal_doc.exists:
            meal_data = meal_doc.to_dict()
            foods = meal_data.get("foods", [])
            total_calories = meal_data.get("total_calories", 0)
            return foods, total_calories
        return [], 0

    def add_food_to_meal(self, meal_type, food_name, calories):
        meal_doc_ref = self.meals_collection.document(meal_type)
        meal_doc = meal_doc_ref.get()
        if meal_doc.exists:
            meal_data = meal_doc.to_dict()
            foods = meal_data.get("foods", [])
            total_calories = meal_data.get("total_calories", 0)
        else:
            foods = []
            total_calories = 0
        foods.append({"name": food_name, "calories": calories})
        total_calories += calories
        meal_doc_ref.set({"foods": foods, "total_calories": total_calories})