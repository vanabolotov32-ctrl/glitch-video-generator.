import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import os
import threading
import numpy as np
from datetime import datetime
from pathlib import Path
from moviepy import VideoFileClip

LANGUAGES = {
    "Русский": {
        "title": "Otomad Глитч Генератор Полного Видео",
        "file_label": "Выбранный файл:",
        "log_label": "Логи процесса:",
        "btn_run": "ГЕНЕРИРОВАТЬ ГЛИЧ",
        "btn_close": "ЗАКРЫТЬ",
        "btn_browse": "ОБЗОР...",
        "ready": "Система готова к работе.",
        "err_not_found": "Файл '{}' не найден!",
        "log_start": "[СТАРТ] Загрузка видео: {}...",
        "log_fx": "[ЭФФЕКТЫ] Наложение жестких Otomad-полос (Slit-Scan)...",
        "log_render_file": "[РЕНДЕР] Сохранение в файл AVI: {}",
        "log_render_start": "[РЕНДЕР] Запуск сборки кодеком mpeg4. Пожалуйста, подождите...",
        "log_success": "[УСПЕХ] Готово! Видео сохранено как: {}",
        "msg_success": "Глитч-видео успешно сохранено в {}!",
        "log_err": "[ОШИБКА] Что-то пошло не так: {}",
        "msg_err_title": "Ошибка сборки",
        "explorer_title": "Выбор видеофайла",
        "explorer_select": "ВЫБРАТЬ",
        "explorer_cancel": "ОТМЕНА",
        "explorer_no_files": "Видеофайлы не найдены.",
        "lang_select_title": "Выбор языка / Language",
        "lang_select_btn": "ОК / START"
    },
    "English": {
        "title": "Full Video Otomad Glitch Generator",
        "file_label": "Selected file:",
        "log_label": "Process logs:",
        "btn_run": "GENERATE GLITCH",
        "btn_close": "CLOSE",
        "btn_browse": "BROWSE...",
        "ready": "System is ready.",
        "err_not_found": "File '{}' not found!",
        "log_start": "[START] Loading video: {}...",
        "log_fx": "[EFFECTS] Applying hard Otomad slit-scan lines...",
        "log_render_file": "[RENDER] Saving to AVI file: {}",
        "log_render_start": "[RENDER] Starting mpeg4 render. Please wait...",
        "log_success": "[SUCCESS] Done! Video saved as: {}",
        "msg_success": "Glitch video successfully saved to {}!",
        "log_err": "[ERROR] Something went wrong: {}",
        "msg_err_title": "Build Error",
        "explorer_title": "Select Video File",
        "explorer_select": "SELECT",
        "explorer_cancel": "CANCEL",
        "explorer_no_files": "No video files found.",
        "lang_select_title": "Select Language",
        "lang_select_btn": "OK / START"
    }
}

class GlitchApp:
    def __init__(self, root, lang):
        self.root = root
        self.current_lang = lang
        
        self.root.title("Otomad Glitch Maker")
        self.root.geometry("550x500")

        # Панель смены языка внутри программы
        lang_frame = tk.Frame(root)
        lang_frame.pack(anchor=tk.E, padx=20, pady=5)
        tk.Label(lang_frame, text="Language / Язык:").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value=self.current_lang)
        self.lang_menu = tk.OptionMenu(lang_frame, self.lang_var, *LANGUAGES.keys(), command=self.change_language)
        self.lang_menu.pack(side=tk.LEFT, padx=5)

        self.lbl_title = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.lbl_title.pack(pady=5)

        # Выбор файла
        file_frame = tk.Frame(root)
        file_frame.pack(pady=5, fill=tk.X, padx=20)
        self.lbl_file = tk.Label(file_frame, text="")
        self.lbl_file.pack(side=tk.LEFT)
        
        self.ent_filename = tk.Entry(file_frame, width=25, state='readonly')
        self.ent_filename.pack(side=tk.LEFT, padx=10)
        self.set_selected_filename("59835.mp4")

        self.btn_browse = tk.Button(file_frame, text="", command=self.open_custom_explorer, bg="#4a4a4a", fg="white")
        self.btn_browse.pack(side=tk.LEFT, padx=5)

        # Текстовое поле логов
        self.lbl_log = tk.Label(root, text="")
        self.lbl_log.pack(anchor=tk.W, padx=20, pady=(10, 0))
        self.log_area = scrolledtext.ScrolledText(root, width=62, height=12, font=("Courier", 9))
        self.log_area.pack(pady=5, padx=20)
        
        # Кнопки управления
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        self.btn_run = tk.Button(btn_frame, text="", command=self.start_generation, 
                                 bg="green", fg="white", font=("Arial", 10, "bold"), width=22)
        self.btn_run.pack(side=tk.LEFT, padx=10)

        self.btn_close = tk.Button(btn_frame, text="", command=root.quit, 
                               bg="red", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_close.pack(side=tk.LEFT, padx=10)

        self.update_ui_text()
        self.log(LANGUAGES[self.current_lang]["ready"])

    def set_selected_filename(self, text):
        self.ent_filename.config(state='normal')
        self.ent_filename.delete(0, tk.END)
        self.ent_filename.insert(0, text)
        self.ent_filename.config(state='readonly')

    def change_language(self, selected_lang):
        self.current_lang = selected_lang
        self.update_ui_text()

    def update_ui_text(self):
        texts = LANGUAGES[self.current_lang]
        self.lbl_title.config(text=texts["title"])
        self.lbl_file.config(text=texts["file_label"])
        self.lbl_log.config(text=texts["log_label"])
        self.btn_run.config(text=texts["btn_run"])
        self.btn_close.config(text=texts["btn_close"])
        self.btn_browse.config(text=texts["btn_browse"])

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def open_custom_explorer(self):
        texts = LANGUAGES[self.current_lang]
        exp_win = tk.Toplevel(self.root)
        exp_win.title(texts["explorer_title"])
        exp_win.geometry("350x300")
        exp_win.transient(self.root)
        exp_win.grab_set()

        tk.Label(exp_win, text=texts["explorer_title"], font=("Arial", 10, "bold")).pack(pady=5)
        frame = tk.Frame(exp_win)
        frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=15)
        
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 9))
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.3gp', '.flv')
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.lower().endswith(video_extensions)]

        if not files:
            listbox.insert(tk.END, f"({texts['explorer_no_files']})")
            listbox.config(state='disabled')
        else:
            for f in files:
                listbox.insert(tk.END, f)
            listbox.select_set(0)

        def on_select():
            if files:
                selection = listbox.curselection()
                if selection:
                    self.set_selected_filename(listbox.get(selection[0]))
            exp_win.destroy()

        btn_frame = tk.Frame(exp_win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text=texts["explorer_select"], bg="green", fg="white", width=12, command=on_select).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=texts["explorer_cancel"], bg="gray", fg="white", width=12, command=exp_win.destroy).pack(side=tk.LEFT, padx=5)

    def start_generation(self):
        input_file = self.ent_filename.get().strip()
        texts = LANGUAGES[self.current_lang]
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", texts["err_not_found"].format(input_file))
            return

        self.btn_run.config(state='disabled')
        threading.Thread(target=self.make_full_video_glitch, args=(input_file,), daemon=True).start()

    def make_full_video_glitch(self, input_file):
        texts = LANGUAGES[self.current_lang]
        try:
            file_path = Path(input_file)
            base_name = file_path.stem
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{base_name}_glitched_{current_time}.avi"

            self.log(texts["log_start"].format(input_file))
            video = VideoFileClip(input_file)
            
            self.log(texts["log_fx"])

            # Slit-Scan процессор идеально прямых монолитных полос
            def glitch_frame_processor(get_frame, t):
                frame = get_frame(t)
                h, w, c = frame.shape
                
                # Меняем режим полос каждые 0.5 сек для динамики
                mode = int(t * 2) % 4
                
                if mode == 0:
                    # Горизонтальные прямые полосы во весь экран
                    single_row = frame[int(h * 0.5), :, :]
                    glitched = np.tile(single_row, (h, 1, 1))
                    
                elif mode == 1:
                    # Вертикальные монолитные столбы во весь экран
                    single_col = frame[:, int(w * 0.5), :]
                    glitched = np.tile(single_col, (w, 1, 1)).transpose(1, 0, 2)
                    
                elif mode == 2:
                    # Движущиеся по вертикали полосы
                    dynamic_y = int((h * 0.3) + (h * 0.4 * (t % 1)))
                    single_row = frame[dynamic_y, :, :]
                    glitched = np.tile(single_row, (h, 1, 1))
                    
                else:
                    # Горизонтальные полосы с быстрым зеркальным отражением
                    single_row = frame[int(h * 0.4), :, :]
                    glitched = np.tile(single_row, (h, 1, 1))
                    glitched = np.fliplr(glitched)

                return glitched

            glitched_video = video.transform(glitch_frame_processor)

            self.log(texts["log_render_file"].format(output_file))
            self.log(texts["log_render_start"])
            
            glitched_video.write_videofile(output_file, fps=24, codec="mpeg4", audio_codec="mp3", logger=None)

            video.close()
            glitched_video.close()
            
            self.log(texts["log_success"].format(output_file))
            messagebox.showinfo("Success", texts["msg_success"].format(output_file))
            
        except Exception as e:
            self.log(texts["log_err"].format(str(e)))
            messagebox.showerror(texts["msg_err_title"], str(e))
        finally:
            self.btn_run.config(state='normal')


def show_language_selector():
    lang_win = tk.Tk()
    lang_win.title("Language")
    lang_win.geometry("300x150")
    lang_win.eval('tk::PlaceWindow . center')

    tk.Label(lang_win, text="Выберите язык интерфейса\nSelect interface language:", font=("Arial", 10)).pack(pady=10)
    
    selected_lang = tk.StringVar(value="Русский")
    menu = tk.OptionMenu(lang_win, selected_lang, *LANGUAGES.keys())
    menu.pack(pady=5)

    def on_confirm():
        choice = selected_lang.get()
        lang_win.destroy()
        
        main_root = tk.Tk()
        GlitchApp(main_root, choice)
        main_root.mainloop()

    tk.Button(lang_win, text="OK / START", bg="green", fg="white", font=("Arial", 9, "bold"), width=15, command=on_confirm).pack(pady=10)
    lang_win.mainloop()


if __name__ == "__main__":
    show_language_selector()
