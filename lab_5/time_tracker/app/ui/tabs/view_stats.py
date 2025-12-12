import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageDraw
from typing import Dict
from app.core.controller import TimerController


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master, controller: TimerController, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.icons_cache = {}
        self.figure = None
        self.canvas = None

        self._setup_ui()
        # Рисуем график с небольшой задержкой, чтобы интерфейс успел прогрузиться
        self.after(500, self._draw_stats)

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight = 2)
        self.grid_columnconfigure(1, weight = 3)
        self.grid_rowconfigure(1, weight = 1)

        # Кнопка обновления
        self.btn_refresh = ctk.CTkButton(
            self, text = "🔄 Обновить данные", command = self._draw_stats, height = 30
        )
        self.btn_refresh.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = "ew")

        # Левая часть - График
        self.chart_frame = ctk.CTkFrame(self, fg_color = "transparent")
        self.chart_frame.grid(row = 1, column = 0, sticky = "nsew", padx = (10, 5), pady = 10)

        # Правая часть - Список
        self.list_frame = ctk.CTkScrollableFrame(self, label_text = "Детализация")
        self.list_frame.grid(row = 1, column = 1, sticky = "nsew", padx = (5, 10), pady = 10)

    def _draw_stats(self):
        stats = self.controller.get_activity_stats()
        self._draw_chart(stats)
        self._draw_list(stats)

    def _draw_chart(self, stats: Dict[str, int]):
        plt.close('all')  # Чистим память

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        for w in self.chart_frame.winfo_children(): w.destroy()

        if not stats:
            ctk.CTkLabel(self.chart_frame, text = "Нет данных").pack(expand = True)
            return

        sorted_items = sorted(stats.items(), key = lambda x: x[1], reverse = True)[:5]
        labels = [i[0] for i in sorted_items]
        values = [i[1] / 60 for i in sorted_items]

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize = (4, 4), dpi = 100)
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')

        ax.pie(
            values, labels = labels, autopct = '%1.0f%%', startangle = 140,
            textprops = dict(color = "w", fontsize = 9), colors = plt.cm.Pastel1.colors,
            pctdistance = 0.85
        )
        fig.gca().add_artist(plt.Circle((0, 0), 0.70, fc = '#2b2b2b'))
        ax.set_title("Топ-5 (мин)", color = "white", pad = 10, fontsize = 12)

        self.figure = fig
        self.canvas = FigureCanvasTkAgg(self.figure, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = "both", expand = True)

    def _draw_list(self, stats: Dict[str, int]):
        for w in self.list_frame.winfo_children(): w.destroy()

        if not stats: return

        sorted_items = sorted(stats.items(), key = lambda x: x[1], reverse = True)
        total_sec = sum(stats.values())

        for app, sec in sorted_items:
            if sec < 5: continue

            row = ctk.CTkFrame(self.list_frame, fg_color = "transparent")
            row.pack(fill = "x", pady = 5)
            row.grid_columnconfigure(2, weight = 1)

            # Иконка
            ctk.CTkLabel(row, text = "", image = self._get_icon(app)).grid(row = 0, column = 0, rowspan = 2, padx = 10)

            # Текст
            ctk.CTkLabel(row, text = app, font = ("Arial", 13, "bold"), anchor = "w").grid(row = 0, column = 1,
                                                                                           sticky = "w")

            # Время
            mins = sec // 60
            t_str = f"{mins // 60} ч {mins % 60} мин" if mins > 60 else (f"{mins} мин" if mins > 0 else f"{sec} сек")
            ctk.CTkLabel(row, text = t_str, text_color = "gray").grid(row = 0, column = 3, sticky = "e", padx = 5)

            # Прогресс
            pr = ctk.CTkProgressBar(row, height = 6, width = 150)
            pr.grid(row = 1, column = 1, columnspan = 3, sticky = "ew", pady = (0, 5))
            pr.set(sec / total_sec)

    def _get_icon(self, name: str):
        if name in self.icons_cache: return self.icons_cache[name]

        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD", "#D4A5A5"]
        bg = colors[hash(name) % len(colors)]

        img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 40, 40), fill = bg)
        draw.text((20, 20), name[0].upper() if name else "?", fill = "white", anchor = "mm", font_size = 20)

        ctk_img = ctk.CTkImage(img, size = (30, 30))
        self.icons_cache[name] = ctk_img
        return ctk_img