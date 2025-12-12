import customtkinter as ctk
import threading
import pystray
from PIL import Image, ImageDraw

from app.core.controller import TimerController
from app.config import APP_TITLE, THEME, APPEARANCE_MODE
# Импортируем наши новые компоненты
from app.ui.tabs.view_timer import TimerFrame
from app.ui.tabs.view_stats import StatsFrame

ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(THEME)


class TimeTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = TimerController()
        self.tray_icon = None

        # Настройки окна
        self.title(APP_TITLE)
        self.geometry("900x600")
        self.minsize(800, 550)
        self.protocol("WM_DELETE_WINDOW", self._minimize_to_tray)

        # Сетка
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # Табы
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "nsew")

        tab_1 = self.tab_view.add("Таймер задач")
        tab_2 = self.tab_view.add("Авто-трекинг")

        # === ВСТАВЛЯЕМ НАШИ КОМПОНЕНТЫ ===
        # Передаем self (как master) и controller
        self.view_timer = TimerFrame(tab_1, self.controller)
        self.view_timer.pack(fill = "both", expand = True)

        self.view_stats = StatsFrame(tab_2, self.controller)
        self.view_stats.pack(fill = "both", expand = True)

    # === ЛОГИКА ТРЕЯ (Остается в главном окне) ===
    def _create_tray_icon(self):
        img = Image.new('RGB', (64, 64), "#1f538d")
        ImageDraw.Draw(img).ellipse((16, 16, 48, 48), fill = "white")
        return img

    def _minimize_to_tray(self):
        self.withdraw()
        if not self.tray_icon:
            menu = pystray.Menu(
                pystray.MenuItem('Открыть', self._restore_window),
                pystray.MenuItem('Выход', self._quit_app)
            )
            self.tray_icon = pystray.Icon("TimeTracker", self._create_tray_icon(), "Tracker", menu)
        threading.Thread(target = self.tray_icon.run, daemon = True).start()

    def _restore_window(self, icon, item):
        self.after(0, self._restore_main)

    def _restore_main(self):
        self.tray_icon.stop()
        self.tray_icon = None
        self.deiconify()
        self.lift()
        self.focus_force()

    def _quit_app(self, icon, item):
        self.controller.stop_all_threads()
        self.tray_icon.stop()
        self.quit()