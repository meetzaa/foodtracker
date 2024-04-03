import tkinter as tk
from tkinter import ttk

class FoodTrackingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Tracking App")
        self.geometry("600x400")

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
