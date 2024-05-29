import tkinter as tk
from ui.signup_page import SignupPage
from ui.gravity_check_page import GravityCheckPage
from ui.login_page import LoginPage
from ui.app_page1 import AppPage1
from ui.profile_page import ProfilePage
from ui.profile2_page import Profile2Page
from ui.log_food_page import LogFoodPage
from ui.add_food_page import AddFoodPage
from ui.goal_page import GoalPage
from ui.goal_info_page import GoalInfoPage
from ui.goal_final_page import GoalFinalPage
from ui.see_more_page import SeeMorePage
from ui.controller import Controller
from ui.main_page import MainPage
from ui.today_activity_page import TodayActivityPage
def main():
    root = tk.Tk()
    root.geometry("937x503")
    controller = Controller(root)

    # Add pages
    controller.add_page("MainPage", MainPage)
    controller.add_page("SignupPage", SignupPage)
    controller.add_page("GravityCheckPage", GravityCheckPage)
    controller.add_page("LoginPage", LoginPage)
    controller.add_page("AppPage1", AppPage1)  # Removed explicit None
    controller.add_page("TodayActivityPage", TodayActivityPage)
    controller.add_page("ProfilePage", ProfilePage)
    controller.add_page("Profile2Page", Profile2Page)
    controller.add_page("LogFoodPage", LogFoodPage)
    controller.add_page("AddFoodPage", AddFoodPage)  # Removed explicit None
    controller.add_page("GoalPage", GoalPage)
    controller.add_page("GoalInfoPage", GoalInfoPage)
    controller.add_page("GoalFinalPage", GoalFinalPage)
    controller.add_page("SeeMorePage", SeeMorePage)

    # Show the initial page
    controller.show_page("MainPage")

    root.mainloop()

if __name__ == "__main__":
    main()

