# logic/goal.py

current_goal = None

def set_goal_and_show_info(goal, master, user_key, controller):
    global current_goal
    current_goal = goal

    # Now show the GoalInfoPage
    controller.show_page("GoalInfoPage", user_key, goal)
