from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from datetime import datetime

class PensionApp(App):
    def build(self):
        self.title = "Pension Calculator - Khalid Fares"
        
        # خلفية داكنة مريحة
        Window.clearcolor = (0.1, 0.12, 0.15, 1)

        scroll = ScrollView()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # 1. العنوان
        main_layout.add_widget(Label(text="Pension Calculator", font_size='26sp', bold=True, size_hint_y=None, height=50))

        # 2. تاريخ الالتحاق
        main_layout.add_widget(Label(text="Employment Start Date (DD/MM/YYYY):", font_size='14sp', bold=True, size_hint_y=None, height=30))
        self.date1_entry = TextInput(placeholder_text="e.g. 01/07/1994", halign="center", multiline=False, size_hint_y=None, height=45, font_size='14sp')
        main_layout.add_widget(self.date1_entry)

        # 3. تاريخ التقاعد
        main_layout.add_widget(Label(text="Retirement Date (DD/MM/YYYY):", font_size='14sp', bold=True, size_hint_y=None, height=30))
        self.date2_entry = TextInput(placeholder_text="e.g. 10/10/2026", halign="center", multiline=False, size_hint_y=None, height=45, font_size='14sp')
        main_layout.add_widget(self.date2_entry)

        # 4. الراتب
        main_layout.add_widget(Label(text="Current Salary (Optional):", font_size='14sp', bold=True, size_hint_y=None, height=30))
        self.salary_entry = TextInput(placeholder_text="Enter your salary here", halign="center", multiline=False, size_hint_y=None, height=45, font_size='14sp')
        main_layout.add_widget(self.salary_entry)

        # 5. زر الحساب
        calc_button = Button(text="Calculate Pension", font_size='16sp', bold=True, background_color=(0.2, 0.4, 0.8, 1), size_hint_y=None, height=50)
        calc_button.bind(on_press=self.calculate_pension)
        main_layout.add_widget(calc_button)

        # --- شاشة النتائج ---
        self.service_label = Label(text="Total Service Period: --", font_size='14sp', size_hint_y=None, height=35)
        main_layout.add_widget(self.service_label)

        self.pension_ratio_label = Label(text="Pension Percentage: --", font_size='16sp', bold=True, color=(0.2, 0.6, 0.9, 1), size_hint_y=None, height=35)
        main_layout.add_widget(self.pension_ratio_label)

        self.final_pension_label = Label(text="Expected Salary: --", font_size='18sp', bold=True, color=(0.2, 0.8, 0.4, 1), size_hint_y=None, height=35)
        main_layout.add_widget(self.final_pension_label)

        # 6. التوقيع
        main_layout.add_widget(Label(text="Programmed by Khalid Fares (Al-Wahsh)", font_size='16sp', bold=True, color=(1, 0.2, 0.2, 1), size_hint_y=None, height=60))

        scroll.add_widget(main_layout)
        return scroll

    def calculate_pension(self, instance):
        try:
            d1_text = self.date1_entry.text.strip().replace("-", "/")
            d2_text = self.date2_entry.text.strip().replace("-", "/")

            start_date = datetime.strptime(d1_text, "%d/%m/%Y")
            end_date = datetime.strptime(d2_text, "%d/%m/%Y")
            
            pivot_date = datetime(2006, 9, 1)

            if end_date < start_date:
                raise ValueError("Retirement date cannot be before employment date!")

            total_days_p1 = 0
            total_days_p2 = 0

            if start_date < pivot_date:
                end_p1 = min(end_date, pivot_date)
                total_days_p1 = (end_p1 - start_date).days
            
            if end_date > pivot_date:
                start_p2 = max(start_date, pivot_date)
                total_days_p2 = (end_date - start_p2).days

            years_p1 = total_days_p1 / 365.25
            years_p2 = total_days_p2 / 365.25
            total_years_exact = years_p1 + years_p2

            ratio_p1 = years_p1 * 2.67  
            ratio_p2 = years_p2 * 2.00  
            total_ratio = ratio_p1 + ratio_p2

            salary_input_text = self.salary_entry.text.strip()
            if salary_input_text:
                salary_before = float(salary_input_text)
                salary_after = salary_before * (total_ratio / 100)
                salary_after_text = f"{salary_after:,.2f}"
            else:
                salary_after_text = "Not Entered"

            self.service_label.text = f"Total Service Period: {total_years_exact:.2f} Years"
            self.pension_ratio_label.text = f"Pension Percentage: {total_ratio:.2f}%"
            self.final_pension_label.text = f"Expected Salary: {salary_after_text}"
            self.final_pension_label.color = (0.2, 0.8, 0.4, 1)

        except ValueError as e:
            self.pension_ratio_label.text = "Input Error!"
            self.final_pension_label.text = str(e)
            self.final_pension_label.color = (0.9, 0.3, 0.2, 1)

if __name__ == "__main__":
    PensionApp().run()
