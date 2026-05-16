import tkinter as tk
from tkinter import ttk, font
from datetime import datetime, date
import calendar

LIFESPAN_YEARS = 80
COLS = 40
GREEN  = "#1D9E75"
AMBER  = "#BA7517"
EMPTY  = "#e0e0e0"
BG     = "#f9f9f7"
CARD   = "#efefed"
TEXT   = "#1a1a1a"
MUTED  = "#6b6b68"

class LifeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Life in Days")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.birth_date = None
        self.tick_job   = None
        self.squares    = []

        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self.root, bg=BG, padx=28, pady=24)
        outer.pack(fill="both", expand=True)

        # Title
        tk.Label(outer, text="your life in days", bg=BG, fg=TEXT,
                 font=("Helvetica", 18, "bold")).pack(anchor="w")
        tk.Label(outer, text="Every square is one day.  Green = lived.  The rest awaits.",
                 bg=BG, fg=MUTED, font=("Helvetica", 11)).pack(anchor="w", pady=(2, 18))

        # ── Date picker row ──────────────────────────────────────────
        row = tk.Frame(outer, bg=BG)
        row.pack(anchor="w")

        # Month
        self._label(row, "month").grid(row=0, column=0, sticky="w", padx=(0,2))
        self.month_var = tk.StringVar(value="January")
        months = list(calendar.month_name)[1:]
        month_cb = ttk.Combobox(row, textvariable=self.month_var,
                                values=months, state="readonly", width=11)
        month_cb.grid(row=1, column=0, padx=(0, 8))
        month_cb.bind("<<ComboboxSelected>>", self._refresh_days)

        # Day
        self._label(row, "day").grid(row=0, column=1, sticky="w", padx=(0,2))
        self.day_var = tk.StringVar(value="1")
        self.day_cb  = ttk.Combobox(row, textvariable=self.day_var,
                                    values=[str(i) for i in range(1, 32)],
                                    state="readonly", width=5)
        self.day_cb.grid(row=1, column=1, padx=(0, 8))

        # Year
        self._label(row, "year").grid(row=0, column=2, sticky="w", padx=(0,2))
        self.year_var = tk.StringVar(value="1973")
        year_entry = tk.Entry(row, textvariable=self.year_var, width=6,
                              relief="flat", bg="white", fg=TEXT,
                              font=("Helvetica", 12), bd=1,
                              highlightthickness=1, highlightbackground="#cccccc")
        year_entry.grid(row=1, column=2, padx=(0, 14), ipady=3)
        year_entry.bind("<Return>", lambda e: self.calculate())

        # Button
        tk.Button(row, text="calculate →", command=self.calculate,
                  bg=BG, fg=TEXT, font=("Helvetica", 12),
                  relief="solid", bd=1, padx=14, pady=3,
                  cursor="hand2", activebackground=CARD).grid(row=1, column=3)

        # Error label
        self.err_label = tk.Label(outer, text="", bg=BG, fg="#c0392b",
                                  font=("Helvetica", 11))
        self.err_label.pack(anchor="w", pady=(4, 0))

        # Stats cards 
        self.stats_frame = tk.Frame(outer, bg=BG)
        self.stats_frame.pack(anchor="w", fill="x", pady=(14, 0))

        self.stat_vars = {}
        labels_keys = [
            ("years old",      "years"),
            ("months lived",   "months"),
            ("days lived",     "days_lived"),
            ("days ahead",     "days_ahead"),
            ("% of 80-yr life","pct"),
            ("seconds alive",  "seconds"),
        ]
        for i, (lbl, key) in enumerate(labels_keys):
            var = tk.StringVar(value="—")
            self.stat_vars[key] = var
            card = tk.Frame(self.stats_frame, bg=CARD, padx=12, pady=8)
            card.grid(row=0, column=i, padx=(0, 8), sticky="nsew")
            self.stats_frame.columnconfigure(i, weight=1)
            tk.Label(card, textvariable=var, bg=CARD, fg=TEXT,
                     font=("Helvetica", 15, "bold")).pack(anchor="w")
            tk.Label(card, text=lbl, bg=CARD, fg=MUTED,
                     font=("Helvetica", 9)).pack(anchor="w")
            
        self.ticker_label = tk.Label(outer, text="", bg=BG, fg=MUTED,
                                      font=("Courier", 10))
        self.ticker_label.pack(anchor="w", pady=(10, 0))
        # Separator
        self.sep = ttk.Separator(outer, orient="horizontal")
        self.sep.pack(fill="x", pady=16)

        #  Legend 
        leg = tk.Frame(outer, bg=BG)
        leg.pack(anchor="w", pady=(0, 8))
        self._dot(leg, GREEN, "square").pack(side="left")
        tk.Label(leg, text="days lived", bg=BG, fg=MUTED,
                 font=("Helvetica", 10)).pack(side="left", padx=(4, 16))
        self._dot(leg, AMBER, "circle").pack(side="left")
        tk.Label(leg, text="today", bg=BG, fg=MUTED,
                 font=("Helvetica", 10)).pack(side="left", padx=(4, 16))
        self._dot(leg, EMPTY, "square").pack(side="left")
        tk.Label(leg, text="days ahead (to age 80)", bg=BG, fg=MUTED,
                 font=("Helvetica", 10)).pack(side="left", padx=(4, 0))

        #  Grid note 
        self.grid_note = tk.Label(outer, text="", bg=BG, fg=MUTED,
                                  font=("Helvetica", 9))
        self.grid_note.pack(anchor="w", pady=(0, 6))

        #  Canvas for squares 
        self.canvas_frame = tk.Frame(outer, bg=BG)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=BG,
                                highlightthickness=0)
        vsb = ttk.Scrollbar(self.canvas_frame, orient="vertical",
                             command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Mouse-wheel scroll
        self.canvas.bind("<MouseWheel>",
                         lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))
        self.canvas.bind("<Button-4>",
                         lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Button-5>",
                         lambda e: self.canvas.yview_scroll(1, "units"))

        # # Ticker
        # self.ticker_label = tk.Label(outer, text="", bg=BG, fg=MUTED,
        #                              font=("Courier", 10))
        # self.ticker_label.pack(anchor="w", pady=(10, 0))

        # self._refresh_days()

    #  Helpers 

    def _label(self, parent, text):
        return tk.Label(parent, text=text, bg=BG, fg=MUTED,
                        font=("Helvetica", 10))

    def _dot(self, parent, color, shape):
        c = tk.Canvas(parent, width=12, height=12, bg=BG,
                      highlightthickness=0)
        if shape == "circle":
            c.create_oval(1, 1, 11, 11, fill=color, outline="")
        else:
            c.create_rectangle(1, 1, 11, 11, fill=color,
                                outline="#cccccc" if color == EMPTY else "")
        return c

    def _refresh_days(self, *_):
        try:
            month_idx = list(calendar.month_name).index(self.month_var.get())
            year      = int(self.year_var.get() or 1973)
            max_days  = calendar.monthrange(year, month_idx)[1]
        except Exception:
            max_days = 31
        cur = int(self.day_var.get() or 1)
        days = [str(i) for i in range(1, max_days + 1)]
        self.day_cb["values"] = days
        self.day_var.set(str(min(cur, max_days)))

    #   logic 

    def calculate(self):
        try:
            month_idx = list(calendar.month_name).index(self.month_var.get())
            day  = int(self.day_var.get())
            year = int(self.year_var.get())
            birth = date(year, month_idx, day)
        except Exception:
            self.err_label.config(text="Please enter a valid date.")
            return

        today = date.today()
        if birth >= today:
            self.err_label.config(text="Please enter a valid  date.")
            return

        self.err_label.config(text="")
        self.birth_date = birth

        end_date    = date(year + LIFESPAN_YEARS, month_idx, day)
        total_days  = (end_date - birth).days
        lived_days  = (today - birth).days

        self._update_stats(lived_days, total_days)
        self._draw_grid(lived_days, total_days)

        self.grid_note.config(
            text=f"total squares {total_days:,} each 1 =  day of {LIFESPAN_YEARS} -year lifespan"
        )

        if self.tick_job:
            self.root.after_cancel(self.tick_job)
            self.tick_job = None

        self._tick()
    def _days_between(self, a, b):
        return (b - a).days

    def _update_stats(self, lived, total):
        today = date.today()
        b     = self.birth_date
        years  = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
        months = (today.year * 12 + today.month) - (b.year * 12 + b.month)
        if today.day < b.day:
            months -= 1
        pct = round(lived / total * 100)

        self.stat_vars["years"].set(str(years))
        self.stat_vars["months"].set(f"{months:,}")
        self.stat_vars["days_lived"].set(f"{lived:,}")
        self.stat_vars["days_ahead"].set(f"{total - lived:,}")
        self.stat_vars["pct"].set(f"{pct}%")
        

    def _tick(self):
        if not self.birth_date:
            return
        now   = datetime.now()
        birth = datetime(self.birth_date.year,
                         self.birth_date.month,
                         self.birth_date.day)
        total_sec = int((now - birth).total_seconds())
        self.stat_vars["seconds"].set(f"{total_sec:,}")

        midnight   = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elapsed    = now - midnight
        h  = int(elapsed.total_seconds() // 3600)
        mi = int((elapsed.total_seconds() % 3600) // 60)
        s  = int(elapsed.total_seconds() % 60)
        pct_day = round((elapsed.total_seconds() / 86400) * 100, 1)
        time_text = f"today: {h:02d}:{mi:02d}:{s:02d} elapsed | {pct_day}% of today done"
        progress_text = f"You are {h} hours into today"

        self.ticker_label.config(
            text= time_text +  "\n" + progress_text 
            )
        
        self.tick_job = self.root.after(1000, self._tick)

    #  Grid drawing 

    def _draw_grid(self, lived, total):
        self.canvas.delete("all")
        self.squares = []
        self._lived = lived
        self._total = total
        self._render_squares()

    def _on_canvas_resize(self, event):
        if self._lived is not None:
            self._render_squares()

    def _render_squares(self):
        if not hasattr(self, "_lived") or self._lived is None:
            return
        lived = self._lived
        total = self._total

        self.canvas.delete("all")
        SZ   = 9
        GAP  = 2
        STEP = SZ + GAP
        cw   = self.canvas.winfo_width() or 800
        cols = max(1, (cw - 10) // STEP)
        MAX  = min(total, 36500)

        for i in range(MAX):
            col = i % cols
            row = i // cols
            x   = 8 + col * STEP
            y   = 8 + row * STEP

            if i < lived - 1:
                color   = GREEN
                outline = ""
                oval    = False
            elif i == lived - 1:
                color   = AMBER
                outline = ""
                oval    = True
            else:
                color   = EMPTY
                outline = "#cccccc"
                oval    = False

            if oval:
                self.canvas.create_oval(x, y, x+SZ, y+SZ,
                                        fill=color, outline=outline)
            else:
                self.canvas.create_rectangle(x, y, x+SZ, y+SZ,
                                             fill=color, outline=outline)

        rows_used = (MAX - 1) // cols + 1
        total_h   = 8 + rows_used * STEP + 8
        self.canvas.configure(scrollregion=(0, 0, cw, total_h),
                               height=min(total_h, 480))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("920x760")
    app = LifeApp(root)
    root.mainloop()