import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk, ImageEnhance
import os
import sys
import subprocess
import urllib.request  # مكتبة أساسية لفحص وتحميل التحديثات من الإنترنت
import json
import re
import customtkinter as ctkinter

# =========================================================================
# 🚀 إعدادات نظام التحديث التلقائي الرقمي
# =========================================================================
CURRENT_VERSION = "1.2.0"  # إصدار النسخة الحالية لبرنامجك

VERSION_URL = "https://raw.githubusercontent.com/abuthamoh07-del/PDF-ExpSuite/refs/heads/main/version.json"
UPDATE_DOWNLOAD_URL = "https://github.com/abuthamoh07-del/PDF-ExpSuite/raw/refs/heads/main/main.exe"

def check_for_updates():
    """فحص وجود تحديث جديد وتحميله واستبداله تلقائياً"""
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
            latest_version = data.get("version")
            update_notes = data.get("notes", "تحسينات عامة على النظام.")
           
        if latest_version and latest_version != CURRENT_VERSION:
            msg = f"🌟 يتوفر تحديث جديد بإصدار [{latest_version}]\n\nالميزات الجديدة:\n{update_notes}\n\nهل تريد التحديث الآن؟"
            if messagebox.askyesno("تحديث النظام تلقائياً", msg):
               
                progress_win = tk.Tk()
                progress_win.title("جاري تحميل التحديث...")
                progress_win.geometry("350x120")
                progress_win.configure(bg="#1a252f")
                progress_win.eval('tk::PlaceWindow . center')
               
                tk.Label(progress_win, text="جاري تنزيل الإصدار الجديد، يرجى الانتظار...", fg="white", bg="#1a252f").pack(pady=10)
                p_bar = ttk.Progressbar(progress_win, length=280, mode='determinate')
                p_bar.pack(pady=5)
                progress_win.update()

                def download_progress(count, block_size, total_size):
                    if total_size > 0:
                        progress = int(count * block_size * 100 / total_size)
                        p_bar['value'] = progress
                        progress_win.update()

                new_exe_name = "main_new.exe"
               
                urllib.request.urlretrieve(UPDATE_DOWNLOAD_URL, new_exe_name, reporthook=download_progress)
                progress_win.destroy()
               
                bat_script = f"""@echo off
                timeout /t 2 /nobreak > nul
                del "{os.path.basename(sys.argv[0])}"
                ren "{new_exe_name}" "{os.path.basename(sys.argv[0])}"
                start "" "{os.path.basename(sys.argv[0])}"
                del "%~f0"
                """
                with open("updater.bat", "w", encoding="cp1256") as bat_file:
                    bat_file.write(bat_script)
               
                messagebox.showinfo("اكتمل التحميل", "تم تحميل التحديث بنجاح! سيتم إغلاق البرنامج الآن لتثبيت الإصدار الجديد تلقائياً.")
               
                subprocess.Popen(["updater.bat"], shell=True)
                sys.exit()
    except Exception as e:
        pass

# =========================================================================
# 🛡️ قسم الحماية وأنظمة التفعيل الاحترافية
# =========================================================================

def get_device_id():
    """قراءة الرقم التسلسلي الفريد للجهاز (المذربورد أو المعالج) عبر الويندوز"""
    try:
        cmd = 'wmic csproduct get uuid'
        uuid = subprocess.check_output(cmd).decode().split('\n')[1].strip()
        return uuid
    except:
        return "DEV-967735715992-XYZ"

def check_activation():
    """التحقق من تفعيل البرنامج على جهاز المستخدم الحالي"""
    device_id = get_device_id()
    correct_key = f"{device_id}-ALBATAH"
    activation_file = "license.lic"
  
    if os.path.exists(activation_file):
        try:
            with open(activation_file, "r") as f:
                user_key = f.read().strip()
            if user_key == correct_key:
                return True
        except:
            pass
          
    activation_window = tk.Tk()
    activation_window.title("نظام حماية الملكية - تفعيل البرنامج")
    activation_window.geometry("480x280")
    activation_window.configure(bg="#c0c0c0")
  
    icon_file = resource_path("ic.ico")
    if os.path.exists(icon_file):
        activation_window.iconbitmap(icon_file)
  
    tk.Label(activation_window, text="⚠️ تنبيه: هذه النسخة غير مفعلة على هذا الجهاز!", font=("Arial", 12, "bold"), fg="#e74c3c", bg="#1a252f").pack(pady=10)
    tk.Label(activation_window, text="يرجى نسخ 'رقم الجهاز' أدناه وإرساله للمصمم للحصول على كود التفعيل:", font=("Arial", 9), fg="#ecf0f1", bg="#1a252f").pack()
  
    id_entry = tk.Entry(activation_window, font=("Arial", 10, "bold"), width=42, justify="center", bd=0, bg="#34495e", fg="#1abc9c")
    id_entry.insert(0, device_id)
    id_entry.config(state="readonly")
    id_entry.pack(pady=8, ipady=4)
  
    tk.Label(activation_window, text="أدخل مفتاح التفعيل الذي استلمته من المصمم:", font=("Arial", 10), fg="white", bg="#1a252f").pack(pady=3)
    key_entry = tk.Entry(activation_window, font=("Arial", 11), width=35, justify="center")
    key_entry.pack(ipady=2)

    tk.Label(activation_window, text="للتواصل مع المصمم 00967735715995 📞:", font=("Arial", 12, "bold"), fg="#add8e6", bg="#1a252f").pack(pady=10)
  
    def verify():
        if key_entry.get().strip() == correct_key:
            try:
                with open(activation_file, "w") as f:
                    f.write(correct_key)
                messagebox.showinfo("نجاح التفعيل", "تم تفعيل برنامجك بنجاح واحترافية!\nيرجى إعادة تشغيل البرنامج الآن.")
                activation_window.destroy()
                sys.exit()
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل حفظ ملف التفعيل: {str(e)}")
        else:
            messagebox.showerror("خطأ في التفعيل", "مفتاح التفعيل المدخل غير صحيح! راجع المصمم.")

    tk.Button(activation_window, text="تفعيل وتشغيل البرنامج الآن ✅", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=6, cursor="hand2", command=verify).pack(pady=15)
  
    activation_window.protocol("WM_DELETE_WINDOW", sys.exit)
    activation_window.mainloop()
    return False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SplashScreen:
    def __init__(self, root, on_finish_callback):
        self.root = root
        self.on_finish_callback = on_finish_callback
      
        self.root.withdraw()
        self.splash = tk.Toplevel(self.root)
        self.splash.title("جاري التحميل...")
        self.splash.overrideredirect(True)
      
        width, height = 550, 400
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        self.splash.configure(bg="#1a252f")

        main_frame = tk.Frame(self.splash, bg="#1a252f", bd=2, relief=tk.RIDGE)
        main_frame.pack(fill=tk.BOTH, expand=True)

        logo_file = resource_path("a.jpg")
        self.splash_photo = None
      
        if os.path.exists(logo_file):
            try:
                img = Image.open(logo_file)
                img = img.resize((540, 390), Image.Resampling.LANCZOS)
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(0.25)
                self.splash_photo = ImageTk.PhotoImage(img)
            except Exception:
                pass

        bg_label = tk.Label(main_frame, image=self.splash_photo, bg="#1a252f")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        lbl_title = tk.Label(main_frame, text="المستعرض الذكي والمطور لملفات PDF", font=("Arial", 16, "bold"), fg="#1abc9c", bg="#1a252f")
        lbl_title.pack(pady=(40, 10))
      
        lbl_loading = tk.Label(main_frame, text="جاري فحص التحديثات وتهيئة الملفات...", font=("Arial", 11, "italic"), fg="#ecf0f1", bg="#1a252f")
        lbl_loading.pack(pady=10)

        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=350, mode='determinate')
        self.progress.pack(pady=20)

        copyright_text = (
            "حقوق الملكية محفوظة لدى المصمم: عبدالملك محمد علي البطاح\n"
            "للتواصل والدعم الفني يرجى الإتصال على 00967735715995 📞"
        )
        lbl_copy = tk.Label(main_frame, text=copyright_text, font=("Arial", 10, "bold"), fg="#bdc3c7", bg="#1a252f", justify=tk.CENTER, pady=10)
        lbl_copy.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress_value = 0
        self.update_progress()

    def update_progress(self):
        if self.progress_value < 130:
            self.progress_value += 2
            self.progress['value'] = self.progress_value
            self.splash.after(50, self.update_progress)
        else:
            self.splash.destroy()
            self.on_finish_callback()

# =========================================================================
# 📂 التبويب الجديد: فرز وتجميع الصور المتشابهة تلقائياً (CustomTkinter)
# =========================================================================
class ImageGroupToPdfTab(ctkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.source_dir = ""
        self.output_dir = ""
        self.create_widgets()
        
    def create_widgets(self):
        self.title_label = ctkinter.CTkLabel(
            self, 
            text="أداة تجميع الصور المتشابهة إلى PDF تلقائياً", 
            font=("Cairo", 18, "bold")
        )
        self.title_label.pack(pady=20)
        
        self.source_frame = ctkinter.CTkFrame(self)
        self.source_frame.pack(pady=10, fill="x", padx=40)
        
        self.btn_browse_source = ctkinter.CTkButton(
            self.source_frame, 
            text="اختيار مجلد الصور", 
            command=self.browse_source,
            font=("Cairo", 12, "bold")
        )
        self.btn_browse_source.pack(side="right", padx=10, pady=10)
        
        self.lbl_source_path = ctkinter.CTkLabel(
            self.source_frame, 
            text="لم يتم اختيار مجلد بعد...", 
            anchor="w",
            font=("Cairo", 11)
        )
        self.lbl_source_path.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        self.output_frame = ctkinter.CTkFrame(self)
        self.output_frame.pack(pady=10, fill="x", padx=40)
        
        self.btn_browse_output = ctkinter.CTkButton(
            self.output_frame, 
            text="تحديد مجلد الحفظ", 
            command=self.browse_output,
            font=("Cairo", 12, "bold"),
            fg_color="#2c3e50",
            hover_color="#34495e"
        )
        self.btn_browse_output.pack(side="right", padx=10, pady=10)
        
        self.lbl_output_path = ctkinter.CTkLabel(
            self.output_frame, 
            text="لم يتم تحديد مجلد الحفظ بعد...", 
            anchor="w",
            font=("Cairo", 11)
        )
        self.lbl_output_path.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        self.btn_start = ctkinter.CTkButton(
            self, 
            text="ابدأ عملية الفرز والتحويل التلقائي", 
            command=self.process_images_to_pdf,
            font=("Cairo", 14, "bold"),
            fg_color="#27ae60",
            hover_color="#2ecc71",
            height=40
        )
        self.btn_start.pack(pady=30)
        
        self.log_text = ctkinter.CTkTextbox(self, width=500, height=150, font=("Consolas", 11))
        self.log_text.pack(pady=10, padx=40, fill="both", expand=True)
        
    def browse_source(self):
        directory = filedialog.askdirectory(title="اختر مجلد الصور التي تود فرزها")
        if directory:
            self.source_dir = directory
            self.lbl_source_path.configure(text=directory)
            self.log(f"تم اختيار مجلد المصدر: {directory}")
            
    def browse_output(self):
        directory = filedialog.askdirectory(title="اختر مجلد حفظ ملفات PDF الناتجة")
        if directory:
            self.output_dir = directory
            self.lbl_output_path.configure(text=directory)
            self.log(f"تم تحديد مجلد الحفظ: {directory}")
            
    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def process_images_to_pdf(self):
        if not self.source_dir or not self.output_dir:
            messagebox.showwarning("تنبيه", "الرجاء اختيار مجلد المصدر ومجلد الحفظ أولاً!")
            return
            
        self.log("جاري فحص المجلد وقراءة الصور...")
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        groups = {}
        
        try:
            files = os.listdir(self.source_dir)
            for file in files:
                if file.lower().endswith(valid_extensions):
                    match = re.split(r'[-_\s.]', file, maxsplit=1)
                    if match:
                        prefix = match[0].strip()
                        if prefix not in groups:
                            groups[prefix] = []
                        groups[prefix].append(os.path.join(self.source_dir, file))
            
            if not groups:
                self.log("لم يتم العثور على أي صور تطابق صيغة التسمية المشتركة.")
                messagebox.showinfo("انتهى", "لا توجد صور صالحة للتحويل.")
                return
                
            converted_count = 0
            for group_name, image_paths in groups.items():
                image_paths.sort()
                pdf_filename = f"{group_name}.pdf"
                pdf_output_path = os.path.join(self.output_dir, pdf_filename)
                
                image_list = []
                for img_path in image_paths:
                    try:
                        img = Image.open(img_path)
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        image_list.append(img)
                    except Exception as e:
                        self.log(f"خطأ في قراءة الصورة {os.path.basename(img_path)}: {str(e)}")
                
                if image_list:
                    image_list[0].save(
                        pdf_output_path, 
                        save_all=True, 
                        append_images=image_list[1:]
                    )
                    self.log(f"✅ تم بنجاح إنشاء: {pdf_filename} (يحتوي على {len(image_list)} صور)")
                    converted_count += 1
            
            self.log(f"🎉 اكتملت العملية بالكامل! تم إنتاج {converted_count} ملفات PDF.")
            messagebox.showinfo("نجاح العملية", f"تم إنشاء {converted_count} ملفات PDF بنجاح في مجلد الحفظ.")
            
        except Exception as e:
            self.log(f"حدث خطأ غير متوقع أثناء المعالجة: {str(e)}")
            messagebox.showerror("خطأ", f"فشلت العملية بسبب: {str(e)}")


# =========================================================================
# 🎛️ واجهة البرنامج الرئيسي (المستعرض مع الأداة الذكية)
# =========================================================================
class UltimatePDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("المستعرض الذكي والمطور لملفات PDF")
        self.root.geometry("1300x850")
        self.root.configure(bg="#2c3e50")
     
        icon_file = resource_path("ic.ico")
        if os.path.exists(icon_file):
            self.root.iconbitmap(icon_file)

        self.pdf_doc = None
        self.current_file_path = ""
        self.folder_files = []
        self.file_index = -1
        self.current_page = 0
        self.zoom_scale = 1.5
        self.rotation = 0
      
        self.search_results = []
        self.search_index = -1
      
        self.photo = None
        self.thumbnail_images = []

        # تهيئة الألسنة / التبويبات (Notebook)
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill=tk.BOTH, expand=True)

        # 1. تبويب المستعرض الرئيسي
        self.viewer_tab = tk.Frame(self.main_notebook, bg="#2c3e50")
        self.main_notebook.add(self.viewer_tab, text=" 📂 مستعرض ملفات PDF ")

        # 2. تبويب فرز وتجميع الصور (الجديد)
        self.smart_images_tab = ImageGroupToPdfTab(self.main_notebook)
        self.main_notebook.add(self.smart_images_tab, text=" 🔄 فرز وتجميع الصور المتشابهة تلقائياً ")

        # بناء واجهة المستعرض داخل التبويب الأول
        self.setup_ui()

        # اختصارات لوحة المفاتيح
        self.root.bind("<Right>", lambda e: self.next_page())
        self.root.bind("<Left>", lambda e: self.prev_page())
        self.root.bind("<Up>", lambda e: self.prev_file_wrapper(e))
        self.root.bind("<Down>", lambda e: self.next_file_wrapper(e))

    def show_main_window(self):
        self.root.deiconify()
        self.root.lift()    

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
      
        # شريط الأدوات داخل تبويب المستعرض الأول
        self.toolbar = tk.Frame(self.viewer_tab, bg="#1a252f", pady=8, padx=10)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open = tk.Button(self.toolbar, text="📂 فتح ملف", font=("Arial", 10, "bold"), bg="#3498db", fg="white", bd=0, padx=10, pady=4, cursor="hand2", command=self.open_file_dialog)
        self.btn_open.pack(side=tk.LEFT, padx=5)

        tk.Button(self.toolbar, text="⏮ الملف السابق", font=("Arial", 9), bg="#34495e", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.prev_file).pack(side=tk.LEFT, padx=2)
        tk.Button(self.toolbar, text="الملف التالي ⏭", font=("Arial", 9), bg="#34495e", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.next_file).pack(side=tk.LEFT, padx=2)

        tk.Label(self.toolbar, text="  ", bg="#1a252f").pack(side=tk.LEFT)
        tk.Button(self.toolbar, text="⬅", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.prev_page).pack(side=tk.LEFT, padx=2)
        self.page_info = tk.Label(self.toolbar, text="0 / 0", bg="#1a252f", fg="white", font=("Arial", 10, "bold"), width=10)
        self.page_info.pack(side=tk.LEFT)
        tk.Button(self.toolbar, text="➡", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.next_page).pack(side=tk.LEFT, padx=2)

        tk.Label(self.toolbar, text="   🔍 ", bg="#1a252f", fg="#bdc3c7", font=("Arial", 11)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(self.toolbar, width=18, font=("Arial", 11), bd=0, highlightthickness=1, highlightbackground="#bdc3c7")
        self.search_entry.pack(side=tk.LEFT, padx=2, ipady=3)
      
        self.search_entry.bind("<Up>", lambda e: self.prev_search_result())
        self.search_entry.bind("<Down>", lambda e: self.next_search_result())

        tk.Button(self.toolbar, text="بحث", font=("Arial", 9, "bold"), bg="#f39c12", fg="white", bd=0, padx=10, pady=3, cursor="hand2", command=self.search_text).pack(side=tk.LEFT, padx=2)
      
        self.btn_search_up = tk.Button(self.toolbar, text="🔼", font=("Arial", 8), bg="#34495e", fg="white", bd=0, padx=5, pady=2, cursor="hand2", command=self.prev_search_result)
        self.btn_search_up.pack(side=tk.LEFT, padx=1)
      
        self.btn_search_down = tk.Button(self.toolbar, text="🔽", font=("Arial", 8), bg="#34495e", fg="white", bd=0, padx=5, pady=2, cursor="hand2", command=self.next_search_result)
        self.btn_search_down.pack(side=tk.LEFT, padx=1)
      
        self.lbl_search_count = tk.Label(self.toolbar, text="", bg="#1a252f", fg="#e67e22", font=("Arial", 9, "bold"))
        self.lbl_search_count.pack(side=tk.LEFT, padx=5)

        tk.Button(self.toolbar, text="🧩 دمج ملفات PDF", font=("Arial", 9, "bold"), bg="#2ecc71", fg="white", bd=0, padx=10, pady=4, cursor="hand2", command=self.merge_pdfs_dialog).pack(side=tk.RIGHT, padx=5)
        tk.Button(self.toolbar, text="💾 استخراج صفحات", font=("Arial", 9, "bold"), bg="#9b59b6", fg="white", bd=0, padx=10, pady=4, cursor="hand2", command=self.extract_range_dialog).pack(side=tk.RIGHT, padx=5)
        tk.Button(self.toolbar, text="🔄 تدوير", font=("Arial", 9), bg="#34495e", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.rotate_page).pack(side=tk.RIGHT, padx=4)
        tk.Button(self.toolbar, text=" ➖ ", font=("Arial", 10, "bold"), bg="#7f8c8d", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.zoom_out).pack(side=tk.RIGHT, padx=2)
        tk.Button(self.toolbar, text=" ➕ ", font=("Arial", 10, "bold"), bg="#7f8c8d", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=self.zoom_in).pack(side=tk.RIGHT, padx=2)

        self.main_split_container = tk.Frame(self.viewer_tab, bg="#2c3e50")
        self.main_split_container.pack(fill=tk.BOTH, expand=True)

        self.right_sidebar = tk.Frame(self.main_split_container, bg="#2c3e50", width=220)
        self.right_sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.right_sidebar.pack_propagate(False)

        logo_file = resource_path("a.jpg")
        if os.path.exists(logo_file):
            self.side_img = Image.open(logo_file)
            self.side_img.thumbnail((200, 120))
            self.side_photo = ImageTk.PhotoImage(self.side_img)
            self.img_label = tk.Label(self.right_sidebar, image=self.side_photo, bg="#2c3e50")
            self.img_label.pack(side=tk.TOP, pady=5)

        tk.Label(self.right_sidebar, text="صفحات الملف", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(side=tk.TOP, anchor="center", padx=5, pady=2)

        self.thumbs_outer_frame = tk.Frame(self.right_sidebar, bg="#34495e", bd=1, relief=tk.SOLID)
        self.thumbs_outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.thumbs_canvas = tk.Canvas(self.thumbs_outer_frame, bg="#34495e", highlightthickness=0, width=190)
        self.thumbs_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.thumbs_scroll = tk.Scrollbar(self.thumbs_outer_frame, orient=tk.VERTICAL, command=self.thumbs_canvas.yview)
        self.thumbs_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.thumbs_canvas.configure(yscrollcommand=self.thumbs_scroll.set)

        self.thumbs_inner_frame = tk.Frame(self.thumbs_canvas, bg="#34495e")
        self.thumbs_canvas.create_window((0, 0), window=self.thumbs_inner_frame, anchor="nw")
      
        self.thumbs_canvas.bind("<Configure>", lambda e: self.thumbs_canvas.configure(scrollregion=self.thumbs_canvas.bbox("all")))

        self.left_display_panel = tk.Frame(self.main_split_container, bg="#bdc3c7")
        self.left_display_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.left_display_panel, bg="#cbd5e1", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scroll = tk.Scrollbar(self.left_display_panel, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

    def prev_file_wrapper(self, event):
        if self.root.focus_get() != self.search_entry:
            self.prev_file()

    def next_file_wrapper(self, event):
        if self.root.focus_get() != self.search_entry:
            self.next_file()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            file_path = os.path.abspath(file_path)
            self.load_new_file(file_path)
          
            folder = os.path.dirname(file_path)
            self.folder_files = [os.path.abspath(os.path.join(folder, f))
                                 for f in os.listdir(folder) if f.lower().endswith('.pdf')]
            self.folder_files.sort()
            try:
                self.file_index = self.folder_files.index(file_path)
            except ValueError:
                self.file_index = 0

    def load_new_file(self, path):
        if self.pdf_doc: self.pdf_doc.close()
        self.current_file_path = path
        self.pdf_doc = fitz.open(path)
        self.current_page = 0
        self.search_results = []
        self.search_index = -1
        self.lbl_search_count.config(text="")
        self.search_entry.delete(0, tk.END)
        self.generate_sidebar_thumbnails()
        self.render_page()
        self.root.title(f"مستعرض PDF الذكي - {os.path.basename(path)}")

    def clear_all_highlights(self):
        if not self.pdf_doc: return
        for page_num in range(len(self.pdf_doc)):
            page = self.pdf_doc.load_page(page_num)
            annots = list(page.annots())
            for annot in annots:
                if annot.type[0] == 8:
                    page.delete_annot(annot)

    def generate_sidebar_thumbnails(self):
        for widget in self.thumbs_inner_frame.winfo_children():
            widget.destroy()
        self.thumbnail_images.clear()

        if not self.pdf_doc: return

        for i in range(len(self.pdf_doc)):
            page = self.pdf_doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            thumb_photo = ImageTk.PhotoImage(img)
            self.thumbnail_images.append(thumb_photo)

            item_frame = tk.Frame(self.thumbs_inner_frame, bg="#34495e", pady=6, cursor="hand2")
            item_frame.pack(side=tk.TOP, fill=tk.X, padx=5)

            if i == self.current_page:
                item_frame.config(bg="#1abc9c")

            lbl_thumb = tk.Label(item_frame, image=thumb_photo, bg="#2c3e50" if i != self.current_page else "#1abc9c")
            lbl_thumb.pack(side=tk.TOP, pady=2)

            lbl_num = tk.Label(item_frame, text=f"صفحة {i + 1}", font=("Arial", 8, "bold"), fg="white", bg=item_frame["bg"])
            lbl_num.pack(side=tk.TOP)

            for widget in (item_frame, lbl_thumb, lbl_num):
                widget.bind("<Button-1>", lambda e, page_num=i: self.jump_to_page(page_num))

        self.thumbs_inner_frame.update_idletasks()
        self.thumbs_canvas.configure(scrollregion=self.thumbs_canvas.bbox("all"))

    def jump_to_page(self, page_num):
        if self.pdf_doc:
            self.current_page = page_num
            self.render_page()

    def update_sidebar_selection(self):
        for idx, child in enumerate(self.thumbs_inner_frame.winfo_children()):
            if idx == self.current_page:
                child.config(bg="#1abc9c")
                for sub in child.winfo_children():
                    sub.config(bg="#1abc9c")
            else:
                child.config(bg="#34495e")
                for sub in child.winfo_children():
                    sub.config(bg="#34495e" if isinstance(sub, tk.Label) and sub["text"].startswith("صفحة") else "#2c3e50")

    def search_text(self):
        if not self.pdf_doc: return
        self.clear_all_highlights()
      
        term = self.search_entry.get().strip()
        self.search_results = []
        self.search_index = -1
      
        if not term:
            self.lbl_search_count.config(text="")
            self.render_page()
            return

        for pg_num in range(len(self.pdf_doc)):
            page = self.pdf_doc.load_page(pg_num)
            if page.search_for(term):
                self.search_results.append(pg_num)
      
        if self.search_results:
            self.search_index = 0
            self.current_page = self.search_results[self.search_index]
            self.lbl_search_count.config(text=f"1 / {len(self.search_results)}")
            self.render_page()
            self.thumbs_canvas.yview_moveto(self.current_page / len(self.pdf_doc))
        else:
            self.lbl_search_count.config(text="0 وجد")
            self.render_page()
            messagebox.showinfo("البحث", "لم يتم العثور على نتائج للنص المدخل")

    def next_search_result(self):
        if self.search_results and self.search_index < len(self.search_results) - 1:
            self.search_index += 1
            self.current_page = self.search_results[self.search_index]
            self.lbl_search_count.config(text=f"{self.search_index + 1} / {len(self.search_results)}")
            self.render_page()
            self.thumbs_canvas.yview_moveto(self.current_page / len(self.pdf_doc))
        return "break"

    def prev_search_result(self):
        if self.search_results and self.search_index > 0:
            self.search_index -= 1
            self.current_page = self.search_results[self.search_index]
            self.lbl_search_count.config(text=f"{self.search_index + 1} / {len(self.search_results)}")
            self.render_page()
            self.thumbs_canvas.yview_moveto(self.current_page / len(self.pdf_doc))
        return "break"

    def render_page(self):
        if not self.pdf_doc: return
        page = self.pdf_doc.load_page(self.current_page)
      
        term = self.search_entry.get().strip()
        if term:
            for inst in page.search_for(term):
                page.add_highlight_annot(inst)

        mat = fitz.Matrix(self.zoom_scale, self.zoom_scale).prerotate(self.rotation)
        pix = page.get_pixmap(matrix=mat)
     
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.photo = ImageTk.PhotoImage(img)
     
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))
        self.page_info.config(text=f"{self.current_page + 1} / {len(self.pdf_doc)}")
        self.update_sidebar_selection()

    def next_file(self):
        if self.folder_files and self.file_index < len(self.folder_files) - 1:
            self.file_index += 1
            self.load_new_file(self.folder_files[self.file_index])

    def prev_file(self):
        if self.folder_files and self.file_index > 0:
            self.file_index -= 1
            self.load_new_file(self.folder_files[self.file_index])

    def extract_range_dialog(self):
        if not self.pdf_doc: return
        dialog = tk.Toplevel(self.root)
        dialog.title("استخراج صفحات")
        tk.Label(dialog, text="من:").grid(row=0, column=0, padx=5, pady=5)
        s_e = tk.Entry(dialog); s_e.grid(row=0, column=1, padx=5, pady=5); s_e.insert(0, "1")
        tk.Label(dialog, text="إلى:").grid(row=1, column=0, padx=5, pady=5)
        e_e = tk.Entry(dialog); e_e.grid(row=1, column=1, padx=5, pady=5); e_e.insert(0, str(len(self.pdf_doc)))
     
        def save():
            try:
                path = filedialog.asksaveasfilename(defaultextension=".pdf")
                if path:
                    new = fitz.open()
                    new.insert_pdf(self.pdf_doc, from_page=int(s_e.get())-1, to_page=int(e_e.get())-1)
                    new.save(path)
                    new.close(); dialog.destroy()
                    messagebox.showinfo("نجاح", "تم حفظ الملف المستخرج بنجاح")
            except: messagebox.showerror("خطأ", "تأكد من صحة أرقام النطاق")
        tk.Button(dialog, text="حفظ الآن", bg="#2ecc71", fg="white", command=save).grid(row=2, columnspan=2, pady=10)

    def merge_pdfs_dialog(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if not files: return
      
        dialog = tk.Toplevel(self.root)
        dialog.title("دمج ملفات PDF")
        dialog.geometry("400x250")
        dialog.configure(bg="#2c3e50")
      
        tk.Label(dialog, text="📝 الملفات التي تم تحديدها للدمج:", font=("Arial", 11, "bold"), fg="white", bg="#2c3e50").pack(pady=10)
      
        listbox = tk.Listbox(dialog, bg="#34495e", fg="white", font=("Arial", 9))
        listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        for f in files:
            listbox.insert(tk.END, os.path.basename(f))
          
        def execute_merge():
            try:
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
                if save_path:
                    merged_pdf = fitz.open()
                    for file_path in files:
                        current_pdf = fitz.open(file_path)
                        merged_pdf.insert_pdf(current_pdf)
                        current_pdf.close()
                  
                    merged_pdf.save(save_path)
                    merged_pdf.close()
                    dialog.destroy()
                    messagebox.showinfo("نجاح", "تم دمج وحفظ الملف بنجاح واحترافية!")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء عملية الدمج:\n{str(e)}")

        tk.Button(dialog, text="اضغط هنا لحفظ الملف المدمج 💾", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", bd=0, pady=6, cursor="hand2", command=execute_merge).pack(pady=10)

    def next_page(self):
        if self.pdf_doc and self.current_page < len(self.pdf_doc)-1:
            self.current_page += 1; self.render_page()
    def prev_page(self):
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1; self.render_page()
    def zoom_in(self): self.zoom_scale += 0.2; self.render_page()
    def zoom_out(self):
        if self.zoom_scale > 0.4: self.zoom_scale -= 0.2; self.render_page()
    def rotate_page(self): self.rotation = (self.rotation + 90) % 360; self.render_page()


# =========================================================================
# 🚦 نقطة انطلاق تشغيل البرنامج
# =========================================================================
if __name__ == "__main__":
    # 🌟 خطوة 1: فحص التحديثات أولاً
    check_for_updates()
   
    # 🌟 خطوة 2: استدعاء نظام فحص رخصة الترخيص
    check_activation()
  
    # 🌟 خطوة 3: تشغيل البرنامج وشاشة التحميل
    root = tk.Tk()
    app = UltimatePDFViewer(root)
    splash = SplashScreen(root, app.show_main_window)
    root.mainloop()
