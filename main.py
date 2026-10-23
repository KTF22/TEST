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
        self.title = "برنامج حساب راتب التقاعد - خالد فارس"
        
        # إعداد لون خلفية النافذة الأساسي (داكن مثل customtkinter)
        Window.clearcolor = (0.1, 0.12, 0.15, 1)

        # حاوية رئيسية قابلة للتمرير لضمان ظهور العناصر على كل شاشات الهواتف
        scroll = ScrollView()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # 1. العنوان الرئيسي
        main_layout.add_widget(Label(
            text="حساب التقاعد", 
            font_size='26sp', 
            bold=True, 
            size_hint_y=None, 
            height=50,
            font_name="ARIAL.TTF"
        ))

        # 2. حقل تاريخ الالتحاق
        main_layout.add_widget(Label(text="تاريخ الالتحاق بالوظيفة (يوم / شهر / سنة):", font_size='14sp', bold=True, size_hint_y=None, height=30, font_name="ARIAL.TTF"))
        self.date1_entry = TextInput(placeholder_text="مثال: 01/07/1994", halign="center", multiline=False, size_hint_y=None, height=45, font_size='14sp')
        main_layout.add_widget(self.date1_entry)

        # 3. حقل تاريخ التقاعد
        main_layout.add_widget(Label(text="تاريخ التقاعد (يوم / شهر / سنة):", font_size='14sp', bold=True, size_hint_y=None, height=30, font_name="ARIAL.TTF"))
        self.date2_entry = TextInput(placeholder_text="مثال: 10/10/2026", halign="center", multiline=False, size_hint_y=None, height=45, font_size='14sp')
        main_layout.add_widget(self.date2_entry)

        # 4. حقل الراتب الحالي
        main_layout.add_widget(Label(text="الراتب الحالي قبل التقاعد:", font_size='14sp', bold=True, size_hint_y=None, height=30, font_name="ARIAL.TTF"))
        self.salary_entry = TextInput(placeholder_text="أدخل الراتب الحالي هنا (اختياري)", halign="center", multiline=False, size_hint_y=None, height=45, font_size='14sp')
        main_layout.add_widget(self.salary_entry)

        # 5. زر الحساب الأزرق
        calc_button = Button(
            text="احسب النسبة والمستحقات", 
            font_size='16sp', 
            bold=True, 
            background_color=(0.2, 0.4, 0.8, 1), 
            size_hint_y=None, 
            height=50,
            font_name="ARIAL.TTF"
        )
        calc_button.bind(on_press=self.calculate_pension)
        main_layout.add_widget(calc_button)

        # --- شاشة عرض النتائج التفصيلية ---
        self.service_label = Label(text="إجمالي مدة الخدمة الكلية: --", font_size='14sp', size_hint_y=None, height=35, font_name="ARIAL.TTF")
        main_layout.add_widget(self.service_label)

        self.pension_ratio_label = Label(text="إجمالي نسبة التقاعد المستحقة: --", font_size='16sp', bold=True, color=(0.2, 0.6, 0.9, 1), size_hint_y=None, height=35, font_name="ARIAL.TTF")
        main_layout.add_widget(self.pension_ratio_label)

        self.final_pension_label = Label(text="الراتب المتوقع بعد التقاعد: --", font_size='18sp', bold=True, color=(0.2, 0.8, 0.4, 1), size_hint_y=None, height=35, font_name="ARIAL.TTF")
        main_layout.add_widget(self.final_pension_label)

        # 6. التوقيع البرمجي باللون الأحمر الفاقع
        main_layout.add_widget(Label(
            text="برمجة خالد فارس (الوحش)", 
            font_size='18sp', 
            bold=True, 
            color=(1, 0.2, 0.2, 1), 
            size_hint_y=None, 
            height=60,
            font_name="ARIAL.TTF"
        ))

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
                raise ValueError("تاريخ التقاعد لا يمكن أن يكون قبل تاريخ الالتحاق!")

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
                salary_after_text = "لم يتم إدخال الراتب الحالي"

            self.service_label.text = f"إجمالي مدة الخدمة الكلية: {total_years_exact:.2f} سنة"
            self.pension_ratio_label.text = f"إجمالي نسبة التقاعد المستحقة: {total_ratio:.2f}%"
            self.final_pension_label.text = f"الراتب المتوقع بعد التقاعد: {salary_after_text}"
            self.final_pension_label.color = (0.2, 0.8, 0.4, 1)

        except ValueError as e:
            self.pension_ratio_label.text = "خطأ في الإدخال!"
            if "strptime" in str(e):
                self.final_pension_label.text = "يرجى كتابة التاريخ بشكل صحيح: يوم/شهر/سنة"
                self.final_pension_label.color = (0.9, 0.3, 0.2, 1)
            else:
                self.final_pension_label.text = str(e)
                self.final_pension_label.color = (0.9, 0.3, 0.2, 1)

if __name__ == "__main__":
    PensionApp().run()
