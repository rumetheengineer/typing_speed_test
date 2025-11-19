from tkinter import *
from tkinter import messagebox
import time
import random
from typing_stats import TypingStats
import sv_ttk
from tkinter import ttk


class TypingSpeedTest:
  
    DEFAULT_TEXT = "The quick brown fox jumps over the lazy dog."
    REFRESH_RATE = 100
    IGNORED_KEYS = [16, 17, 18, 20]

    def __init__(self, text_file=None):

        self.window = Tk()
        self.window.title("Typing Speed Test")
        #Initial state variables
        self.is_running = False
        self.start_time = None
        self.refresh = None
        self.stats = TypingStats()
        self.counter = 0

        self.correct_text = self.load_text(text_file) if text_file else self.DEFAULT_TEXT

        self.setup_ui()

    def setup_ui(self):
        self.frame = Frame(self.window)
        self.frame.pack(padx=10, pady=10)

        # Text to type
        self.display_label = ttk.Label(
            self.frame,
            text=self.correct_text,
            font=("Arial", 24),
            justify="center",
            wraplength=600
        )
        self.display_label.grid(row=0, column=0, columnspan=3, padx=5, pady=20)
        
        # Input entry
        self.entry = Entry(self.frame, font=("Courier", 22, "bold"), width=50)
        self.entry.grid(row=1, column=0, columnspan=3, padx=5, pady=20)
        self.entry.focus()
        self.entry.bind('<KeyPress>', self.start)
        self.entry.bind('<KeyRelease>', self.check_input)

        # Result label
        self.result_label = Label(
            self.frame,
            text='Start typing to begin...',
            font=("Arial", 18, "bold"),
            fg="blue",
            justify="center"
        )
        self.result_label.grid(row=2, column=0, columnspan=3, padx=5, pady=20)
        sv_ttk.set_theme("dark")
        
        # Reset button
        self.reset_button = ttk.Button(
            self.frame, 
            text="Reset", 
            command=self.reset,
            width=15
            # font=("Arial", 14)
        )
        self.reset_button.grid(row=3, column=1, padx=5, pady=20)


    def load_text(self, text_file=None) -> str:
        file = text_file if text_file else "texts.txt"
        texts = [self.DEFAULT_TEXT]
        try:
            with open(file, 'r') as file:
                texts = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror(f"File not found: '{text_file}\nUsing default text")
        except Exception as e:
            messagebox.showerror(f"Error loading text file: {e}\nUsing default text.")
        else:
            return random.choice(texts)
    
    def start(self, event=None):
        if not self.is_running and event.keycode not in self.IGNORED_KEYS:
            self.is_running = True
            self.start_time = time.time()
            self.update()

    def update(self):
        if  not self.is_running:
            return
        
        if self.start_time is not None:
            self.stats.time_spent = time.time() - self.start_time
            self.stats.characters_typed = len(self.entry.get())
            self.stats.words_typed = len(self.entry.get().split())
            self.stats.accuracy = self.calculate_accuracy()

        self.result_label.config(text=self.stats.summary)
        self.refresh = self.window.after(self.REFRESH_RATE, self.update)

    def calculate_accuracy(self) -> float:
        typed_text = self.entry.get()
        if self.counter >0:
            acc = len(self.correct_text) - self.counter //  len(self.correct_text) * 100
            return acc

        correct_ans = sum(
            1 for i, letter in enumerate(typed_text) if i < len(self.correct_text) and letter == self.correct_text[i]
        )

        return (correct_ans / len(typed_text) * 100) if typed_text else 0.00
    
    def check_input(self, event=None):
        typed_text = self.entry.get()
        correct = self.correct_text[:len(typed_text)]

        if typed_text.lower() == correct.lower():
            self.entry.config(fg="green")
        else:
            self.entry.config(fg="red")
            if typed_text[-1] != correct[len(typed_text)-1]:
                self.counter += 1


        if typed_text == self.correct_text:
            self.terminate()

    def terminate(self):
        self.is_running = False
        if self.refresh:
            self.window.after_cancel(self.refresh)
            self.refresh = None
        if self.start_time is not None:
            self.stats.time_spent = time.time() - self.start_time

        messagebox.showinfo("Test Complete", self.stats.summary)

    def reset(self):
        self.is_running = False
        if self.refresh:
            self.window.after_cancel(self.refresh)
            self.refresh = None
        self.start_time = None
        self.stats = TypingStats()
        self.correct_text = self.load_text(text_file="texts.txt")
        self.entry.delete(0, END)
        self.entry.config(fg="black")
        self.entry.focus()
        self.result_label.config(text='Start typing to begin...')



app = TypingSpeedTest(text_file="texts.txt")
app.window.mainloop()
