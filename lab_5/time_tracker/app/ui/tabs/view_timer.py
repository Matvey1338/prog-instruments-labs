import customtkinter as ctk
from app.core.controller import TimerController


class TimerFrame(ctk.CTkFrame):
    def __init__(self, master, controller: TimerController, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self._setup_ui()
        # Запускаем локальный цикл обновления времени
        self._update_timer_display()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(2, weight = 1)

        # 1. Панель ввода
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ew")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text = "Над чем работаем?")
        self.task_entry.pack(side = "left", fill = "x", expand = True, padx = (10, 10), pady = 10)

        self.action_button = ctk.CTkButton(
            self.input_frame,
            text = "Старт",
            command = self._on_action_button_click,
            fg_color = "green",
            hover_color = "darkgreen"
        )
        self.action_button.pack(side = "right", padx = (0, 10))

        # 2. Табло
        self.timer_label = ctk.CTkLabel(self, text = "00:00:00", font = ("Roboto Medium", 60))
        self.timer_label.grid(row = 1, column = 0, pady = (0, 20))

        # 3. История
        self.history_frame = ctk.CTkScrollableFrame(self, label_text = "История задач")
        self.history_frame.grid(row = 2, column = 0, padx = 10, pady = (0, 10), sticky = "nsew")

        self._refresh_history_ui()

    def _on_action_button_click(self):
        if not self.controller.is_running:
            # START
            self.controller.start_timer(self.task_entry.get())
            self.action_button.configure(text = "Стоп", fg_color = "red", hover_color = "darkred")
            self.task_entry.configure(state = "disabled")
        else:
            # STOP
            self.controller.stop_timer()
            self.action_button.configure(text = "Старт", fg_color = "green", hover_color = "darkgreen")
            self.task_entry.configure(state = "normal")
            self.task_entry.delete(0, 'end')
            self.timer_label.configure(text = "00:00:00")
            self._refresh_history_ui()

    def _update_timer_display(self):
        if self.controller.is_running:
            self.timer_label.configure(text = self.controller.get_elapsed_time_str())
        self.after(1000, self._update_timer_display)

    def _refresh_history_ui(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        entries = self.controller.get_history()
        for entry in entries:
            row = ctk.CTkFrame(self.history_frame)
            row.pack(fill = "x", pady = 2)
            row.grid_columnconfigure(0, weight = 1)

            ctk.CTkLabel(row, text = entry.task_name, anchor = "w", font = ("Arial", 14, "bold")).grid(row = 0,
                                                                                                       column = 0,
                                                                                                       padx = 10,
                                                                                                       pady = 5,
                                                                                                       sticky = "ew")
            ctk.CTkLabel(row, text = entry.date_str, text_color = "gray60", font = ("Arial", 12)).grid(row = 0,
                                                                                                       column = 1,
                                                                                                       padx = 5)
            ctk.CTkLabel(row, text = entry.duration, text_color = "gray90").grid(row = 0, column = 2, padx = 5)

            ctk.CTkButton(
                row, text = "✎", width = 30, fg_color = "transparent", text_color = "gray",
                command = lambda e=entry: self._on_edit_click(e)
            ).grid(row = 0, column = 3)

            ctk.CTkButton(
                row, text = "✕", width = 30, fg_color = "transparent", text_color = "red",
                command = lambda id=entry.id: self._on_delete_click(id)
            ).grid(row = 0, column = 4, padx = (0, 5))

    def _on_edit_click(self, entry):
        dialog = ctk.CTkInputDialog(text = "Новое название:", title = "Ред.")
        if res := dialog.get_input():
            self.controller.rename_task(entry.id, res)
            self._refresh_history_ui()

    def _on_delete_click(self, entry_id):
        self.controller.delete_task(entry_id)
        self._refresh_history_ui()