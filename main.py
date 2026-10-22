import customtkinter as ctk
from datetime import datetime

# إعداد المظهر العام لتطبيق الكمبيوتر
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue") 

class PensionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة
        self.title("برنامج حساب راتب التقاعد - خالد فارس")
        self.geometry("550x650")
        self.resizable(False, False)

        # العنوان الرئيسي
        self.title_label = ctk.CTkLabel(self, text="حساب التقاعد", font=ctk.CTkFont(family="Arial", size=26, weight="bold"))
        self.title_label.pack(pady=20)

        # 1. حقل تاريخ الالتحاق
        self.date1_label = ctk.CTkLabel(self, text=" بالوظيفة الالتحاق تاريخ (يوم / شهر / سنة):", font=ctk.CTkFont(size=14, weight="bold"))
        self.date1_label.pack(pady=2)
        self.date1_entry = ctk.CTkEntry(self, placeholder_text="مثال: 01/07/1994", width=320, justify="center", font=ctk.CTkFont(size=14))
        self.date1_entry.pack(pady=5)

        # 2. حقل تاريخ التقاعد
        self.date2_label = ctk.CTkLabel(self, text="التقاعد تاريخ  (يوم / شهر / سنة):", font=ctk.CTkFont(size=14, weight="bold"))
        self.date2_label.pack(pady=2)
        self.date2_entry = ctk.CTkEntry(self, placeholder_text="مثال: 10/10/2026", width=320, justify="center", font=ctk.CTkFont(size=14))
        self.date2_entry.pack(pady=5)

        # 3. حقل الراتب الحالي (تم تعديل العنوان المطلوب هنا)
        self.salary_label = ctk.CTkLabel(self, text="التقاعد قبل الحالي الراتب", font=ctk.CTkFont(size=14, weight="bold"))
        self.salary_label.pack(pady=2)
        self.salary_entry = ctk.CTkEntry(self, placeholder_text="أدخل الراتب الحالي هنا (اختياري)", width=320, justify="center", font=ctk.CTkFont(size=14))
        self.salary_entry.pack(pady=5)

        # زر الحساب
        self.calc_button = ctk.CTkButton(self, text=" النسبة و المستحقات احسب", font=ctk.CTkFont(size=16, weight="bold"), command=self.calculate_pension, width=220, height=40)
        self.calc_button.pack(pady=20)

        # --- شاشة عرض النتائج التفصيلية ---
        self.results_frame = ctk.CTkFrame(self, width=460, height=200, corner_radius=10)
        self.results_frame.pack(pady=10, fill="x", padx=40)

        self.service_label = ctk.CTkLabel(self.results_frame, text=" إجمالي مدة الخدمة الكلية: --", font=ctk.CTkFont(size=14))
        self.service_label.pack(pady=6)

        self.pension_ratio_label = ctk.CTkLabel(self.results_frame, text="إجمالي نسبة التقاعد المستحقة: --", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3498db")
        self.pension_ratio_label.pack(pady=6)

        self.final_pension_label = ctk.CTkLabel(self.results_frame, text="  الراتب المتوقع بعد التقاعد: --", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2ecc71")
        self.final_pension_label.pack(pady=6)

        # التوقيع البرمجي (تم تحديث النص إلى الوحش وتعديل اللون للأحمر الفاقع)
        self.signature_label = ctk.CTkLabel(self, text="برمجة خالد فارس (الوحش)", font=ctk.CTkFont(family="Arial", size=18, weight="bold"), text_color="#ff3333")
        self.signature_label.pack(side="bottom", pady=20)

    def calculate_pension(self):
        try:
            # تنظيف الفراغات من النصوص المدخلة
            d1_text = self.date1_entry.get().strip().replace("-", "/")
            d2_text = self.date2_entry.get().strip().replace("-", "/")

            # قراءة التواريخ بصيغة يوم/شهر/سنة
            start_date = datetime.strptime(d1_text, "%d/%m/%Y")
            end_date = datetime.strptime(d2_text, "%d/%m/%Y")
            
            # تاريخ الفاصل الزمني المعتمد (1 سبتمبر 2006)
            pivot_date = datetime(2006, 9, 1)

            if end_date < start_date:
                raise ValueError("تاريخ التقاعد لا يمكن أن يكون قبل تاريخ الالتحاق!")

            total_days_p1 = 0
            total_days_p2 = 0

            # حساب توزيع الأيام زمنياً بناءً على تاريخ الفاصل 1/9/2006
            if start_date < pivot_date:
                end_p1 = min(end_date, pivot_date)
                total_days_p1 = (end_p1 - start_date).days
            
            if end_date > pivot_date:
                start_p2 = max(start_date, pivot_date)
                total_days_p2 = (end_date - start_p2).days

            # تحويل الأيام الكلية إلى سنوات دقيقة
            years_p1 = total_days_p1 / 365.25
            years_p2 = total_days_p2 / 365.25
            total_years_exact = years_p1 + years_p2

            # تطبيق المعادلات المالية
            ratio_p1 = years_p1 * 2.67  
            ratio_p2 = years_p2 * 2.00  
            total_ratio = ratio_p1 + ratio_p2

            # حساب الراتب المتوقع بعد التقاعد
            salary_input_text = self.salary_entry.get().strip()
            if salary_input_text:
                salary_before = float(salary_input_text)
                salary_after = salary_before * (total_ratio / 100)
                salary_after_text = f"{salary_after:,.2f}"
            else:
                salary_after_text = "لم يتم إدخال الراتب الحالي"

            # تحديث شاشة النتائج
            self.service_label.configure(text=f"إجمالي مدة الخدمة الكلية: {total_years_exact:.2f} سنة")
            self.pension_ratio_label.configure(text=f"إجمالي نسبة التقاعد المستحقة: {total_ratio:.2f}%")
            self.final_pension_label.configure(text=f"الراتب المتوقع بعد التقاعد: {salary_after_text}")
            self.final_pension_label.configure(text_color="#2ecc71")

        except ValueError as e:
            self.pension_ratio_label.configure(text="خطأ في الإدخال!")
            if "strptime" in str(e):
                self.final_pension_label.configure(text="يرجى كتابة التاريخ بصيغة صحيحة: يوم/شهر/سنة", text_color="#e74c3c")
            else:
                self.final_pension_label.configure(text=str(e), text_color="#e74c3c")

# تشغيل التطبيق
if __name__ == "__main__":
    app = PensionApp()
    app.mainloop()

