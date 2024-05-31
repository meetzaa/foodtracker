from ui.goal_final_page import GoalFinalPage
class Controller:
    def __init__(self, root):
        self.root = root
        self.pages = {}
        self.current_page = None
        self.current_goal = None

    def show_page(self, page_name, *args):
        if self.current_page is not None:
            self.current_page.place_forget()  # Hide the current page
        page = self.pages[page_name]
        page.lift()
        if args:
            page.update(*args)
        page.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_page = page

    def add_page(self, page_name, page_class, *args):
        page = page_class(self.root, self, *args)
        self.pages[page_name] = page
        page.place(x=0, y=0, relwidth=1, relheight=1)

    def show_page_with_user_key(self, page_name, user_key):
        if page_name in self.pages:
            self.pages[page_name].update(user_key)
            self.show_page(page_name, user_key)
        else:
            print(f"Page {page_name} not found")

    def set_current_goal(self, goal):
        self.current_goal = goal

    def show_goal_info_page(self, user_key, goal):
        self.set_current_goal(goal)
        if "GoalInfoPage" in self.pages:
            self.pages["GoalInfoPage"].update(user_key, goal)
            self.show_page("GoalInfoPage", user_key, goal)
        else:
            print("GoalInfoPage not found")

    def show_final_page(self, user_key, goal):
        # Preia detalii nutriționale pe baza obiectivului
        nutrition_details = {
            "Weight Loss": {"kcal": "1500 kcal", "fats": "0.5 g", "protein": "1.2 g", "carbs": "100 g"},
            "Muscle Build": {"kcal": "3000 kcal", "fats": "1 g", "protein": "2.5 g", "carbs": "350 g"},
            "Maintenance": {"kcal": "2500 kcal", "fats": "0.8 g", "protein": "2.0 g", "carbs": "200 g"}
        }.get(goal, None)

        if nutrition_details:
            if "GoalFinalPage" in self.pages:
                self.pages["GoalFinalPage"].update(user_key, nutrition_details, goal)
            else:
                self.add_page("GoalFinalPage", GoalFinalPage, user_key, nutrition_details, goal)
            self.show_page("GoalFinalPage", user_key, nutrition_details, goal)
        else:
            print(f"No nutritional details found for goal: {goal}")
