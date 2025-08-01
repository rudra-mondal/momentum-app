# Momentum: Your Personal Habit Tracker

**Momentum is a sophisticated, offline desktop application designed to help you build and maintain positive habits by providing real-time tracking, motivational insights, and mindfulness tools.**

Built for those on a journey of self-improvement, Momentum goes beyond simple day counting. It provides a visual "Success Path" to normalize the ups and downs of motivation and includes an integrated "Urge Surfing" tool to help you navigate challenging moments with mindfulness instead of willpower alone.

Your journey is personal, and so is your data. **Momentum is 100% private and works completely offline.** All your information is stored locally on your machine in a `data.json` file and is never sent anywhere.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/downloads/)
[![UI Framework](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)](https://github.com/TomSchimansky/CustomTkinter)

---

<img  alt="Screenshot 2025-08-02 014309" src="https://github.com/user-attachments/assets/d76a2a27-0e03-4e82-8723-a1df82a4c7fb" />

<h4 align="center">
  <i>
The main dashboard, showing the current streak and the Motivation Success Path.
  </i>
</h4>

## ✨ Key Features

-   **Sleek, Modern Dashboard:** A clean, dark-themed interface built with CustomTkinter that's easy on the eyes and keeps you focused on what matters.
-   **Real-time Streak Tracking:** Your current streak is displayed prominently and updates every second, giving you a constant sense of progress.
-   **Best Streak Record:** Automatically tracks and displays your longest streak, serving as a powerful motivator.
-   **Comprehensive History:** Logs every completed streak, allowing you to look back on your progress and learn from your journey.

### The Motivation Success Path (Interactive Graph)
This is Momentum's cornerstone feature. Instead of a linear progress bar, it displays a realistic curve of subjective motivation over a 90-day journey.
-   **Visualize Your Journey:** See common stages like the initial "Pumped Up" phase, the challenging "Flatline," and the eventual "New Normal."
-   **Track Your Position:** A bright marker shows exactly where **YOU** are on this path, normalizing your feelings and showing you what might be next.
-   **Interactive Exploration:** Hover over any point on the graph to see the day number and corresponding motivation level.

### Urge Surfing Tool (Mindfulness-Based Intervention)
When you feel an urge, fighting it can be exhausting. The Urge Surfing tool helps you build a different skill: mindful acceptance.
-   **Guided Breathing Exercise:** A pop-up window guides you through a calming 4-7-8 breathing cycle ("Breathe In... Hold... Breathe Out...").
-   **Ride the Wave:** Based on the psychological principle that urges are temporary waves of energy that will pass if not acted upon. This tool helps you ride out the wave until it subsides.

---

## 🔬 The Philosophy Behind Momentum

Momentum is designed with a specific philosophy in mind:

1.  **Normalization over Judgment:** The Motivation Graph shows that low motivation is a normal, predictable part of the journey. This helps reduce feelings of failure during tough times and encourages persistence.
2.  **Mindfulness over Brute Force:** The Urge Surfing tool teaches a valuable skill from Acceptance and Commitment Therapy (ACT). Instead of fighting an urge, you learn to observe it without judgment, reducing its power over you.
3.  **Data for Insight, Not Obsession:** Tracking your streak is motivating, but the goal is self-improvement, not just a high number. The combination of the timer, graph, and history provides a holistic view of your progress.

---

## 💻 Technology Stack

-   **UI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern look and feel.
-   **Data Visualization:** [Matplotlib](https://matplotlib.org/) for creating the interactive motivation graph.
-   **Numerical Operations:** [NumPy](https://numpy.org/) for interpolating data points on the graph.
-   **Core Logic:** Standard Python 3 libraries (`tkinter`, `json`, `datetime`).

---

## 🛠️ Installation & Usage

Follow these steps to get Momentum running on your local machine.

#### Prerequisites
-   **Python 3.8+**
-   **Git**

#### 1. Clone the Repository
Open your terminal and clone the project:
```bash
git clone https://github.com/rudra-mondal/momentum-app.git
cd momentum-app
```

#### 2. Create a Virtual Environment (Recommended)
This keeps the project's dependencies isolated from your system's Python installation.
```bash
# On macOS and Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

#### 3. Install Dependencies
Install all the required Python libraries using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
Start the app with this command:
```bash
python main.py
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rudra-mondal/momentum-app/issues).

1.  **Fork** the repository.
2.  Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4.  **Push** to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a **Pull Request**.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
