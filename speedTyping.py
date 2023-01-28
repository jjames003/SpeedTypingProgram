import time
import difflib
import random
import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox

from matplotlib.pyplot import savefig

def accuracy(sentence, typed_sentence):
    return difflib.SequenceMatcher(None, sentence, typed_sentence).ratio() * 100

def typing_speed(sentence, elapsed_time):
    return len(sentence.split()) / (elapsed_time / 60)
    

def on_submit():
    global sentence
    global start_time
    typed_sentence = entry.get()
    end_time = time.time()
    elapsed_time = end_time - start_time
    acc = accuracy(sentence, typed_sentence)
    wpm = typing_speed(sentence, elapsed_time)
    messagebox.showinfo("Results", f"Time: {elapsed_time:.2f} seconds, Accuracy: {acc:.2f}%, WPM: {wpm:.2f}")
    save_results(username, elapsed_time, acc)
    reset()
    change_sentence()
    start_time = time.time()

def reset():
    entry.delete(0, 'end')

def save_results(username, elapsed_time, acc):
    with open("results.txt", "a") as file:
        file.write(f"{username},{elapsed_time:.2f},{acc:.2f}\n")
        file.close

def show_leaderboard():
    with open("results.txt", "r") as file:
        results = file.readlines()
    sorted_results = sorted(results, key=lambda x: (float(x.split(',')[2]), float(x.split(',')[1])))
    leaderboard_text = "Username | Time (seconds) | Accuracy (%)\n" + "\n".join([f"{r.split(',')[0]} | {float(r.split(',')[1]):.2f} | {float(r.split(',')[2]):.2f}" for r in sorted_results])
    messagebox.showinfo("Leaderboard", leaderboard_text)

def change_sentence():
    global sentence
    with open("sentences.txt", "r") as file:
        sentences = file.readlines()
        sentence = random.choice(sentences)
        label.config(text=sentence)

def speed_typing():
    global sentence
    global start_time
    while True:
        change_sentence()
        start_time = time.time()
        root.mainloop()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Speed Typer Game - Joel James")
root.configure(bg="white")

username = simpledialog.askstring("Username", "What is your name?",parent=root)
answer = messagebox.askyesno("Leaderboard", "Would you like to see the leaderboard before you start playing?")
if answer:
    show_leaderboard()

label = tk.Label(root, text="", font=("Arial", 16), bg="white")
label.pack(pady=20)

entry = tk.Entry(root, font=("Arial", 16), width=50)
entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit", font=("Arial", 16), command=on_submit)
submit_button.pack(pady=20)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

label.place(relx=0.5, rely=0.1, anchor="center")
entry.place(relx=0.5, rely=0.5, anchor="center")
submit_button.place(relx=0.5, rely=0.9, anchor="center")

speed_typing()
