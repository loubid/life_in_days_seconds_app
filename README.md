# 🟢 Your Life in Days

> *Every square is one day. Green = lived. The rest awaits.*

A desktop application built with Python and Tkinter that visualizes your entire life as a grid of squares — one square per day — giving you a powerful, visual reminder of how your time is being spent.

---

## 📌 What Is This?

**Your Life in Days** is a mortality visualization tool inspired by the concept of "memento mori" — a reminder that life is finite. By seeing your entire lifespan represented as individual squares on a screen, you gain a visceral, intuitive sense of:

- How much time you have already lived
- How much time remains (based on an 80-year lifespan)
- What percentage of today you have already used

This is not just a clock or a calendar. It is a perspective tool.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🟩 **Life Grid** | Every square = 1 day of your life. Green = lived, amber = today, grey = future |
| 📊 **Live Stats** | Shows your age in years, months, days lived, days ahead, % of lifespan used, and seconds alive — all updating in real time |
| ⏱️ **Daily Ticker** | Shows the current time elapsed today and what percentage of today is done, updating every second |
| 📅 **Birth Date Picker** | Simple dropdown-based date picker for month, day, and year |
| 🖱️ **Scrollable Grid** | The life grid is scrollable so you can explore all your days |

---

## 🖥️ How to Run

### Requirements
- Python 3.x
- Tkinter (comes built-in with Python on Windows and Mac)

### Steps

**1. Clone or download the project:**
```bash
git clone https://github.com/your-username/life-in-days.git
cd life-in-days
```

**2. Run the app:**
```bash
python lifes.py
```

**3. Enter your birth date and click `calculate →`**

That's it. No external libraries needed.

---


## 🧠 How It Works

### The Grid
- The app calculates the total number of days in an 80-year lifespan from your birth date
- Each day is drawn as a small square (9×9 pixels) on a canvas
- Squares are colored based on whether that day is in the past, present, or future:
  - 🟩 **Green** — days already lived
  - 🟠 **Amber circle** — today
  - ⬜ **Grey** — days still ahead

### The Stats Cards
Six live statistics are displayed at the top:
1. **Years old** — your current age
2. **Months lived** — total months since birth
3. **Days lived** — total days since birth
4. **Days ahead** — days remaining until age 80
5. **% of 80-yr life** — percentage of your lifespan used
6. **Seconds alive** — live counter, updates every second

### The Daily Ticker
Below the stats, a live ticker shows:
```
today: 14:23:10 elapsed  |  59.9% of today done
You are 14 hours into today
```
This updates every second using `root.after(1000, self._tick)` — a recursive timer built into Tkinter.

---

## ⚙️ Key Code Concepts

### Why `86400`?
```python
pct_day = round((elapsed.total_seconds() / 86400) * 100, 1)
```
`86400` = 60 seconds × 60 minutes × 24 hours = total seconds in one day. Dividing elapsed seconds by this gives the fraction of the day that has passed.

### Why `root.after(1000, self._tick)`?
Tkinter doesn't support threads easily for UI updates. `root.after(1000, fn)` schedules a function to run after 1000 milliseconds (1 second) without freezing the UI. `_tick` calls itself this way every second, creating a live clock.

### Why is the grid capped at 36,500 squares?
```python
MAX = min(total, 36500)
```
`36500 ≈ 100 years × 365 days`. This is a performance cap to prevent the canvas from rendering too many shapes and slowing down the app.

---

## 🎨 Design Choices

| Choice | Reason |
|---|---|
| Muted, warm color palette | Keeps the app calm and reflective, not alarming |
| Small 9px squares | Allows thousands of days to fit on screen at once |
| Amber circle for today | Stands out clearly among the grid |
| Courier font for ticker | Monospace font prevents the text from jumping as numbers change width |

---

## 🚀 Possible Future Improvements

- [ ] Add custom lifespan (not just 80 years)
- [ ] Add a "week view" or "year view" mode
- [ ] Export the grid as an image
- [ ] Add a motivational quote that updates daily
- [ ] Dark mode toggle

---

## 👨‍💻 Author

Built by **Loubid** — a Computer Science student with a focus on Computing and Data Science.

---

## 📄 License

This project is open source and free to use.
