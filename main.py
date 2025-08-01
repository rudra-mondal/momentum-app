import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

# --- Constants and Configuration ---
DATA_FILE = "data.json"
APP_NAME = "Momentum"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720

# --- Color Palette (Modern & Sleek) ---
COLOR_BG = "#1E1E1E"
COLOR_FRAME = "#2D2D2D"
COLOR_TEXT = "#EAEAEA"
COLOR_TEXT_SECONDARY = "#A0A0A0"
COLOR_ACCENT = "#3498DB"  # A vibrant blue
COLOR_ACCENT_HOVER = "#2980B9"
COLOR_SUCCESS = "#2ECC71" # Green
COLOR_USER_POS = "#ADFF2F" # Lime Green
COLOR_DANGER = "#E74C3C" # Red
COLOR_DANGER_HOVER = "#C0392B"
COLOR_WARNING = "#F39C12" # Orange
COLOR_WARNING_HOVER = "#E67E22"

# --- Data Management (No changes needed here, but included for completeness) ---
class DataManager:
    """Handles loading and saving of user data."""
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """Loads data from the JSON file, or creates it if it doesn't exist."""
        if not os.path.exists(self.filename):
            return {"start_time": None, "best_streak_seconds": 0, "relapse_history": []}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"start_time": None, "best_streak_seconds": 0, "relapse_history": []}

    def save_data(self):
        """Saves the current data to the JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def start_streak(self):
        """Starts a new streak."""
        self.data['start_time'] = time.time()
        self.save_data()

    def record_relapse(self):
        """Records a relapse, updates best streak, and resets the timer."""
        if self.data['start_time']:
            end_time = time.time()
            duration_seconds = end_time - self.data['start_time']
            if duration_seconds > self.data['best_streak_seconds']:
                self.data['best_streak_seconds'] = duration_seconds
            relapse_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": duration_seconds,
                "duration_str": self.format_seconds(duration_seconds)
            }
            self.data['relapse_history'].insert(0, relapse_entry)
        self.data['start_time'] = None
        self.save_data()

    def get_current_streak_seconds(self):
        if not self.data['start_time']: return 0
        return time.time() - self.data['start_time']

    def get_best_streak_str(self):
        return self.format_seconds(self.data['best_streak_seconds'])

    @staticmethod
    def format_seconds(seconds):
        if seconds < 0: seconds = 0
        delta = timedelta(seconds=seconds)
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

# --- Main Application ---
class MomentumApp(ctk.CTk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager

        # --- Window Setup ---
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=COLOR_BG)

        self.grid_columnconfigure(0, weight=1, minsize=380)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # --- UI Components ---
        self.create_left_panel()
        self.create_right_panel()

        self.update_ui()
        self.update_timer()

    def create_left_panel(self):
        self.left_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, width=380, corner_radius=0)
        self.left_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.left_frame.grid_propagate(False)
        self.left_frame.grid_rowconfigure(5, weight=1)

        # --- Title ---
        title_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        title_label = ctk.CTkLabel(title_frame, text=APP_NAME, font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color=COLOR_TEXT)
        title_label.pack(side="left")

        # --- Current Streak Display ---
        streak_frame = ctk.CTkFrame(self.left_frame, fg_color=COLOR_FRAME, corner_radius=12)
        streak_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        current_streak_title = ctk.CTkLabel(streak_frame, text="🕒 CURRENT STREAK", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_ACCENT)
        current_streak_title.pack(pady=(15, 5))
        self.current_streak_label = ctk.CTkLabel(streak_frame, text="0d 00h 00m 00s", font=ctk.CTkFont(family="monospace", size=36, weight="bold"), text_color=COLOR_TEXT)
        self.current_streak_label.pack(pady=(0, 20))

        # --- Best Streak Display ---
        best_streak_frame = ctk.CTkFrame(self.left_frame, fg_color=COLOR_FRAME, corner_radius=12)
        best_streak_frame.grid(row=2, column=0, padx=30, pady=10, sticky="ew")
        best_streak_title = ctk.CTkLabel(best_streak_frame, text="🏆 BEST STREAK", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_SUCCESS)
        best_streak_title.pack(pady=(15, 5))
        self.best_streak_label = ctk.CTkLabel(best_streak_frame, text="0d 00h 00m 00s", font=ctk.CTkFont(family="monospace", size=24), text_color=COLOR_TEXT)
        self.best_streak_label.pack(pady=(0, 20))

        # --- Separator ---
        separator = ctk.CTkFrame(self.left_frame, height=2, fg_color=COLOR_FRAME)
        separator.grid(row=4, column=0, padx=30, pady=20, sticky="ew")

        # --- Action Buttons ---
        button_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        button_frame.grid(row=6, column=0, padx=30, pady=(10, 30), sticky="s")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        self.reset_button = ctk.CTkButton(button_frame, text="Reset Streak", command=self.confirm_relapse, fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, height=45, font=ctk.CTkFont(size=14, weight="bold"))
        self.reset_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.history_button = ctk.CTkButton(button_frame, text="View History", command=self.show_history, height=40)
        self.history_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.panic_button = ctk.CTkButton(button_frame, text="Urge Surfing Tool", command=self.open_urge_tool, fg_color=COLOR_WARNING, hover_color=COLOR_WARNING_HOVER, height=40)
        self.panic_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.start_button = ctk.CTkButton(self.left_frame, text="🚀 Start Your Journey", command=self.start_journey, font=ctk.CTkFont(size=22, weight="bold"), height=70, corner_radius=15, fg_color=COLOR_SUCCESS, hover_color=COLOR_ACCENT)

    def create_right_panel(self):
        self.right_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=12)
        self.right_frame.grid(row=0, column=1, padx=(0, 30), pady=30, sticky="nsew")

        self.stages_data = [
            {"name": "Decision", "day": 0, "motivation": 8}, {"name": "Pumped Up", "day": 7, "motivation": 9.5},
            {"name": "Confusion", "day": 15, "motivation": 4}, {"name": "Flatline Start", "day": 20, "motivation": 6},
            {"name": "Flatline End", "day": 30, "motivation": 7.5}, {"name": "Boring Stage", "day": 45, "motivation": 3},
            {"name": "New Normal", "day": 90, "motivation": 9}
        ]
        
        self.fig, self.ax = plt.subplots(facecolor=COLOR_FRAME)
        self.setup_motivation_graph()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.draw()
        
        # --- Interactive Hover Elements ---
        self.hover_line = None
        self.hover_dot = None
        self.hover_text = None
        self.user_position_marker = None
        self.user_position_text = None
        
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.canvas.mpl_connect('axes_leave_event', self.on_leave_axes)

    def setup_motivation_graph(self):
        self.ax.clear()
        days = [s["day"] for s in self.stages_data]
        motivation = [s["motivation"] for s in self.stages_data]

        self.ax.plot(days, motivation, marker='o', linestyle='-', color=COLOR_ACCENT, linewidth=2.5, markersize=8, markerfacecolor=COLOR_ACCENT_HOVER, markeredgecolor=COLOR_FRAME)
        self.ax.set_title('The Motivation Success Path', fontsize=18, fontweight='bold', color=COLOR_TEXT)
        self.ax.set_xlabel('Days on Journey', fontsize=12, color=COLOR_TEXT_SECONDARY)
        self.ax.set_ylabel('Subjective Motivation (0-10)', fontsize=12, color=COLOR_TEXT_SECONDARY)
        self.ax.set_facecolor(COLOR_FRAME)
        self.ax.grid(True, linestyle='--', alpha=0.2, color=COLOR_TEXT_SECONDARY)
        
        # Clean up aesthetics
        self.ax.tick_params(axis='x', colors=COLOR_TEXT_SECONDARY)
        self.ax.tick_params(axis='y', colors=COLOR_TEXT_SECONDARY)
        for spine in ['top', 'right']: self.ax.spines[spine].set_visible(False)
        for spine in ['left', 'bottom']: self.ax.spines[spine].set_color(COLOR_TEXT_SECONDARY)
        self.ax.set_ylim(0, 11)
        self.ax.set_xlim(-2, 92)

        for stage in self.stages_data:
            self.ax.text(stage['day'], stage['motivation'] + 0.3, stage['name'], color=COLOR_TEXT, fontsize=9, ha='center')

        self.fig.tight_layout(pad=2.5)
    
    # --- INTERACTIVE GRAPH METHODS ---
    def on_hover(self, event):
        if event.inaxes != self.ax:
            self.hide_hover_elements()
            return

        days_data = [s["day"] for s in self.stages_data]
        motivation_data = [s["motivation"] for s in self.stages_data]
        
        # Interpolate to find motivation level at mouse's day-coordinate
        hover_day = event.xdata
        hover_motivation = np.interp(hover_day, days_data, motivation_data)

        self.hide_hover_elements() # Clear previous hover elements

        # Draw new hover line
        self.hover_line = self.ax.axvline(x=hover_day, color=COLOR_WARNING, linestyle='--', linewidth=1.5, alpha=0.8)
        
        # Draw new hover dot
        self.hover_dot, = self.ax.plot(hover_day, hover_motivation, 'o', markersize=10, markerfacecolor=COLOR_WARNING, markeredgecolor='white')

        # Draw new hover text
        text_content = f"Day: {hover_day:.1f}\nMotiv: {hover_motivation:.1f}/10"
        self.hover_text = self.ax.text(hover_day + 2, hover_motivation, text_content, 
                                       bbox=dict(boxstyle="round,pad=0.5", fc=COLOR_BG, ec=COLOR_WARNING, alpha=0.9),
                                       color=COLOR_TEXT, fontsize=10)

        self.canvas.draw_idle()

    def on_leave_axes(self, event):
        self.hide_hover_elements()
        self.canvas.draw_idle()

    def hide_hover_elements(self):
        if self.hover_line: self.hover_line.remove(); self.hover_line = None
        if self.hover_dot: self.hover_dot.remove(); self.hover_dot = None
        if self.hover_text: self.hover_text.remove(); self.hover_text = None

    def update_motivation_graph(self):
        if self.user_position_marker: self.user_position_marker.remove()
        if self.user_position_text: self.user_position_text.remove()

        current_seconds = self.data_manager.get_current_streak_seconds()
        current_days = current_seconds / (24 * 3600)
        
        if current_days > 0:
            days_data = [s["day"] for s in self.stages_data]
            motivation_data = [s["motivation"] for s in self.stages_data]
            user_motivation = np.interp(current_days, days_data, motivation_data)

            self.user_position_marker, = self.ax.plot(current_days, user_motivation, 'o', markersize=15, markerfacecolor=COLOR_USER_POS, markeredgecolor='white', markeredgewidth=2, zorder=10)
            self.user_position_text = self.ax.text(current_days, user_motivation + 0.6, 'YOU', color=COLOR_USER_POS, fontsize=11, fontweight='bold', ha='center', zorder=10)
        
        self.canvas.draw_idle() # Use draw_idle for smoother updates

    def update_timer(self):
        self.current_streak_label.configure(text=self.data_manager.format_seconds(self.data_manager.get_current_streak_seconds()))
        self.update_motivation_graph()
        self.after(1000, self.update_timer)

    def update_ui(self):
        self.best_streak_label.configure(text=self.data_manager.get_best_streak_str())
        if self.data_manager.data['start_time'] is None:
            self.start_button.grid(row=1, column=0, rowspan=2, padx=30, pady=20, sticky="nsew")
            self.reset_button.configure(state="disabled")
        else:
            self.start_button.grid_remove()
            self.reset_button.configure(state="normal")
        self.update_motivation_graph()

    def start_journey(self):
        self.data_manager.start_streak()
        self.update_ui()
    
    def confirm_relapse(self):
        is_sure = messagebox.askyesno(title="Confirm Relapse", message="Are you sure you want to reset your streak? This action will be logged.", icon='warning')
        if is_sure:
            self.data_manager.record_relapse()
            self.data_manager.start_streak()
            messagebox.showinfo("New Start", "Relapse recorded. A new journey begins now. Stay strong!")
            self.update_ui()

    def show_history(self):
        history = self.data_manager.data['relapse_history']
        
        history_window = ctk.CTkToplevel(self)
        history_window.title("Streak History")
        history_window.geometry("500x550")
        history_window.transient(self)
        history_window.grab_set()

        scroll_frame = ctk.CTkScrollableFrame(history_window, label_text="Your Past Streaks", label_font=ctk.CTkFont(size=16, weight="bold"))
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        if not history:
            ctk.CTkLabel(scroll_frame, text="No history yet. Keep going!", font=ctk.CTkFont(size=14)).pack(pady=20)
            return

        for i, entry in enumerate(history):
            entry_frame = ctk.CTkFrame(scroll_frame, corner_radius=8, fg_color=COLOR_FRAME)
            entry_frame.pack(fill="x", pady=5, padx=5)
            
            label_title = ctk.CTkLabel(entry_frame, text=f"Streak #{len(history) - i}", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_ACCENT)
            label_title.pack(anchor="w", padx=15, pady=(10, 0))
            
            label_duration = ctk.CTkLabel(entry_frame, text=f"Duration: {entry['duration_str']}", font=ctk.CTkFont(size=12))
            label_duration.pack(anchor="w", padx=15)
            
            label_date = ctk.CTkLabel(entry_frame, text=f"Ended: {entry['date']}", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_SECONDARY)
            label_date.pack(anchor="w", padx=15, pady=(0, 10))

    def open_urge_tool(self):
        UrgeToolWindow(self)


# --- ENHANCED URGE TOOL WINDOW ---
class UrgeToolWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Urge Surfing Tool")
        self.geometry("450x350")
        self.transient(master)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Breathing cycle: [text, color, duration in ms]
        self.breathing_cycle = [
            ("Breathe In...", "#3498DB", 4000), 
            ("Hold...", "#2ECC71", 7000), 
            ("Breathe Out...", "#E74C3C", 8000)
        ]
        self.cycle_index = 0
        self.after_id = None

        self.create_widgets()
        self.start_animation()
    
    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Ride the Wave", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, pady=(30, 10))
        
        instructions = ctk.CTkLabel(self, text="An urge is a temporary wave of energy. \nIt will pass. Focus on your breath.", font=ctk.CTkFont(size=14), text_color=COLOR_TEXT_SECONDARY)
        instructions.grid(row=1, column=0, pady=5, padx=20)

        self.guide_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=32, weight="bold"))
        self.guide_label.grid(row=2, column=0, pady=20, sticky="nsew")

        close_button = ctk.CTkButton(self, text="I Feel Calmer", command=self.close_window, height=45, font=ctk.CTkFont(size=14, weight="bold"))
        close_button.grid(row=3, column=0, pady=(10, 30), padx=50, sticky="ew")
        
    def start_animation(self):
        text, color, duration = self.breathing_cycle[self.cycle_index]
        self.guide_label.configure(text=text, text_color=color)
        
        self.cycle_index = (self.cycle_index + 1) % len(self.breathing_cycle)
        self.after_id = self.after(duration, self.start_animation)

    def close_window(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.destroy()


if __name__ == "__main__":
    dm = DataManager(DATA_FILE)
    app = MomentumApp(dm)
    app.mainloop()