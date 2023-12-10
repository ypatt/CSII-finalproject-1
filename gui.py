import tkinter as tk
from tkinter import ttk, messagebox
import statistics
from logic import calculate_grade

class GradingApp(tk.Tk):
    """
    A tkinter application for grading students. It allows the user to enter student names and scores,
    calculate grades, and view statistics like mean score, median score, passing rate, and failing rate.

    Attributes:
        scores (list): List to store the scores of students.
        names (list): List to store the names of students.
    """
    def __init__(self):
        """
        Initialize the GradingApp with a specified title and geometry. It also initializes the scores
        and names list and calls the create_widgets method to build the GUI components.
        """
        super().__init__()
        self.title("UNO Gradulator 9000")
        self.geometry("500x600")  # Increased width from 400 to 500
        self.minsize(500, 600)  # Minimum size
        self.maxsize(500, 600)  # Maximum size

        self.scores = []
        self.names = []
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges all the widgets (labels, entries, buttons, treeview for scores display,
        and scrollbar) inside the main application window.
        """
        # Labels and entries for name and score
        tk.Label(self, text="Student Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10)
        self.display_name = tk.Entry(self, font=("Arial", 16), bd=3, relief="ridge")
        self.display_name.grid(row=1, column=0, columnspan=4, padx=10, sticky="we")

        tk.Label(self, text="Student Score:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10)
        self.display_current = tk.Entry(self, font=("Arial", 16), bd=3, relief="ridge")
        self.display_current.grid(row=3, column=0, columnspan=4, padx=10, sticky="we")

        # Number pad buttons
        self.buttons = [
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2),
            ('0', 7, 1),
        ]

        for (text, row, col) in self.buttons:
            button = tk.Button(self, text=text, command=lambda t=text: self.on_button_press(t))
            button.grid(row=row, column=col, sticky="nsew")

        # Enter Score, Delete, Clear, and Submit Scores buttons
        tk.Button(self, text="Enter Score", command=self.on_enter_score).grid(row=7, column=2, sticky="nsew")
        tk.Button(self, text="Del", command=self.on_delete).grid(row=7, column=0, sticky="nsew")
        tk.Button(self, text="Clear", command=self.on_clear).grid(row=8, column=0, sticky="nsew")
        tk.Button(self, text="Reset Scores", command=self.on_clear).grid(row=8, column=1, sticky="nsew")
        tk.Button(self, text="Submit Scores", command=self.on_submit_scores, bg="red").grid(row=8, column=2, sticky="nsew")

        # Treeview for displaying scores in a table
        self.tree = ttk.Treeview(self, columns=('Count', 'Name', 'Score', 'Grade'), show='headings')
        self.tree.heading('Count', text='Count')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Score', text='Score')
        self.tree.heading('Grade', text='Grade')
        self.tree.column('Count', width=100)
        self.tree.column('Name', width=100)
        self.tree.column('Score', width=100)
        self.tree.column('Grade', width=100)
        self.tree.grid(row=12, column=0, columnspan=3, sticky='nsew', pady=5)

        # Configure row and column weights for grid layout
        for i in range(13):
            self.grid_rowconfigure(i, weight=1)
            for j in range(4):
                self.grid_columnconfigure(j, weight=1)

        # Configure and place the scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=12, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

                    
    def on_button_press(self, value):
        """
        Appends the value of the pressed number pad button to the score entry field.

        Args:
            value (str): The value of the button pressed.
        """
        self.display_current.insert(tk.END, value)

    def on_enter_score(self):
        """
        Handles the logic for entering a score. It checks for valid input, updates the scores and names list,
        and updates the treeview with the new score and a placeholder for grade.
        """
        score_str = self.display_current.get()
        name_str = self.display_name.get() or f"Student {len(self.scores) + 1}"

        if not score_str.strip():
            messagebox.showerror("Error", "Please enter a numeric score.")
            return

        try:
            score = int(score_str)
            if score < 0:
                raise ValueError("Score cannot be negative")
            self.scores.append(score)
            self.names.append(name_str)
            self.tree.insert('', 'end', values=(len(self.scores), name_str, score, 'Pending'))
            self.display_current.delete(0, tk.END)
            self.display_name.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Invalid input. Please enter a numeric score.")

    def on_submit_scores(self):
        """
        Submits the entered scores. It updates the grades in the table based on the scores and
        displays the statistics in a new window.
        """
        if not self.scores:
            messagebox.showinfo("No Scores", "Please enter at least one score before submitting.")
            return

        # Update the grades in the table
        for i, item in enumerate(self.tree.get_children()):
            score = self.scores[i]
            grade = calculate_grade(score, max(self.scores))
            self.tree.item(item, values=(i+1, self.names[i], score, grade))

        # Show the statistics in a new window
        self.show_statistics()

    def show_statistics(self):
        """
        Calculates and displays statistics such as mean score, median score, passing rate, and failing rate.
        It also shows the counts of each grade in a table.
        """
        if not self.scores:
            messagebox.showinfo("Info", "No scores available for statistics.")
            return

        stats_window = tk.Toplevel(self)
        stats_window.title("Statistics")
        stats_window.geometry("285x315")

        # Calculate statistics
        average = statistics.mean(self.scores)
        median = statistics.median(self.scores)
        best_score = max(self.scores)
        worst_score = min(self.scores)
        passing_scores = [s for s in self.scores if calculate_grade(s, best_score) != 'F']
        passing_rate = len(passing_scores) / len(self.scores) * 100
        failing_rate = 100 - passing_rate

        # Count grades
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for score in self.scores:
            grade = calculate_grade(score, best_score)
            if grade in grade_counts:
                grade_counts[grade] += 1

        # Display other statistics
        tk.Label(stats_window, text=f"Mean Score: {average:.2f}").pack()
        tk.Label(stats_window, text=f"Median Score: {median}").pack()
        tk.Label(stats_window, text=f"Best Score: {best_score} ({self.names[self.scores.index(best_score)]})").pack()
        tk.Label(stats_window, text=f"Worst Score: {worst_score} ({self.names[self.scores.index(worst_score)]})").pack()
        tk.Label(stats_window, text=f"Passing Rate: {passing_rate:.2f}%").pack()
        tk.Label(stats_window, text=f"Failing Rate: {failing_rate:.2f}%").pack()

        # Configure Treeview style
        style = ttk.Style(self)
        style.configure("Treeview", font=('Arial', 12))
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.configure("Treeview", rowheight=25)

        # Grades table
        grades_tree = ttk.Treeview(stats_window, columns=('Grade', 'Count'), show='headings')
        grades_tree.heading('Grade', text='Grade')
        grades_tree.heading('Count', text='Count')
        grades_tree.column('Grade', width=50, anchor='center')
        grades_tree.column('Count', width=50, anchor='center')

        # Insert grade counts
        for grade in ['A', 'B', 'C', 'D', 'F']:
            grades_tree.insert('', 'end', values=(grade, grade_counts[grade]))

        grades_tree.pack(pady=5)

    def on_clear(self):
        """
        Clears the score entry field, and resets the scores and names lists and the treeview.
        """
        self.display_current.delete(0, tk.END)
        self.scores = []
        self.names = []
        for i in self.tree.get_children():
            self.tree.delete(i)

    def on_delete(self):
        """
        Deletes the last character from the score entry field.
        """
        current_text = self.display_current.get()
        self.display_current.delete(len(current_text)-1, tk.END)

if __name__ == "__main__":
    app = GradingApp()
    app.mainloop()
