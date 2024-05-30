import tkinter as tk
<<<<<<< Updated upstream
from tkinter import ttk

class FoodTrackingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Tracking App")
        self.geometry("600x400")
=======
from ui.signup_page import SignupPage
from ui.gravity_check_page import GravityCheckPage
from ui.login_page import LoginPage
from ui.app_page1 import AppPage1
from ui.profile_page import ProfilePage
from ui.profile2_page import Profile2Page
from ui.log_food_page import LogFoodPage
from ui.today_activity_page import TodayActivityPage  # Import TodayActivityPage
from ui.goal_page import GoalPage
from ui.goal_info_page import GoalInfoPage
from ui.goal_final_page import GoalFinalPage
from ui.see_more_page import SeeMorePage
from ui.settings_page import SettingsPage  # Add this import if it exists
from ui.controller import Controller
from ui.main_page import MainPage

def main():
    root = tk.Tk()
    root.geometry("937x503")
    controller = Controller(root)

    # Add pages
    controller.add_page("MainPage", MainPage)
    controller.add_page("SignupPage", SignupPage)
    controller.add_page("GravityCheckPage", GravityCheckPage)
    controller.add_page("LoginPage", LoginPage)
    controller.add_page("AppPage1", AppPage1)
    controller.add_page("ProfilePage", ProfilePage)
    controller.add_page("Profile2Page", Profile2Page)
    controller.add_page("LogFoodPage", LogFoodPage)
    controller.add_page("TodayActivityPage", TodayActivityPage)  # Add TodayActivityPage here
    controller.add_page("GoalPage", GoalPage)
    controller.add_page("GoalInfoPage", GoalInfoPage)
    controller.add_page("GoalFinalPage", GoalFinalPage)
    controller.add_page("SeeMorePage", SeeMorePage)
    controller.add_page("SettingsPage", SettingsPage)  # Add this page if it exists
>>>>>>> Stashed changes

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Welcome to Food Tracking App", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        categories_frame = ttk.Frame(self)
        categories_frame.pack(pady=20)

        food_tracking_button = ttk.Button(categories_frame, text="Food Tracking Summary",
                                          command=self.food_tracking_summary, style="Main.TButton")
        food_tracking_button.pack(fill=tk.X, padx=20, pady=5)

        bmi_calculator_button = ttk.Button(categories_frame, text="BMI Calculator", command=self.bmi_calculator_summary,
                                           style="Main.TButton")
        bmi_calculator_button.pack(fill=tk.X, padx=20, pady=5)

        nutrients_calculator_button = ttk.Button(categories_frame, text="Nutrients Calculator",
                                                 command=self.nutrients_calculator_summary, style="Main.TButton")
        nutrients_calculator_button.pack(fill=tk.X, padx=20, pady=5)

        calendar_frame = ttk.Frame(self)
        calendar_frame.pack(pady=20)

        calendar_label = ttk.Label(calendar_frame, text="Calendar View", font=("Helvetica", 16))
        calendar_label.pack()

        calorie_intake_label = ttk.Label(self, text="Final Calorie Intake: 2500 kcal", font=("Helvetica", 12))
        calorie_intake_label.pack(pady=20)

    def food_tracking_summary(self):
        pass

    def bmi_calculator_summary(self):
        pass

    def nutrients_calculator_summary(self):
        pass

if __name__ == "__main__":
    app = FoodTrackingApp()

    style = ttk.Style()
    style.configure("Main.TButton", font=("Helvetica", 14), foreground="black", background="#e3f2fd", borderwidth=0)

    app.mainloop()
