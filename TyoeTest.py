from tkinter import *
import random as r
import time

font = ("Courier New", 14)
title_font = ("Helvetica", 24, "bold")
bg_color = "#41436A"
button_color = "#984063"
text_color = "#FE9677"
box_fg = "#000000"
box_bg = "#FFFFFF"

with open("sentences.txt", "r") as f:
    sentences = f.read().splitlines()

random_sentences = r.sample(sentences, 20)
text_to_display = " ".join(random_sentences)
words = text_to_display.split()

start_word_index = 0
words_per_chunk = 35
current_chunk = " ".join(words[start_word_index:start_word_index + words_per_chunk])
current_word_index = 0
current_chunk_words = current_chunk.split()
correct_word_count = 0
total_word_count = 0
start_time = None
time_left = 60  # Timer starts at 60 seconds
timer_running = False
typing_start_time = None  # To track actual typing time

window = Tk()
window.title('Welcome to Typing Speed Calculator!')
window.config(bg=bg_color, pady=10, padx=50)

heading = Label(text="Typing Test", font=title_font, bg=bg_color, fg=text_color, padx=10, pady=10)
instruction = Label(text="Timer Begins When You Type The First Word", font=font, fg=text_color, bg=bg_color)
result_label = Label(text="", font=font, fg=text_color, bg=bg_color)
timer_label = Label(text="Time Left: 60s", font=font, fg=text_color, bg=bg_color)

sentence_display = Text(
    font=font,
    bg=box_bg,
    fg=box_fg,
    wrap=WORD,
    width=80,
    height=3,
    padx=10,
    pady=10,
    relief=SOLID,
    borderwidth=2
)

sentence_display.insert("1.0", current_chunk)
sentence_display.config(state=DISABLED)

def update_timer():
    global time_left, timer_running
    if time_left > 0 and timer_running:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        window.after(1000, update_timer)  # Call the function every 1000ms (1 second)
    elif time_left == 0:
        end_test()

def start_timer():
    global start_time, typing_start_time, timer_running
    if not timer_running:
        start_time = time.time()
        typing_start_time = time.time()  # Mark the start time for typing
        timer_running = True
        update_timer()

def on_key_release(event):
    global current_word_index, correct_word_count, total_word_count, start_time, start_word_index, current_chunk_words, time_left, timer_running, typing_start_time

    if not timer_running:
        start_timer()

    typed_text = user_entry.get()

    if event.keysym in ["space", "Return"]:
        typed_word = typed_text.strip()
        user_entry.delete(0, END)
        
        if current_word_index < len(current_chunk_words):
            expected_word = current_chunk_words[current_word_index]

            start_idx = "1.0"
            word_count = 0
            while word_count < current_word_index:
                start_idx = sentence_display.search(current_chunk_words[word_count], start_idx, stopindex=END)
                start_idx = sentence_display.index(f"{start_idx}+{len(current_chunk_words[word_count])}c")
                word_count += 1
            
            word_start = sentence_display.search(expected_word, start_idx, stopindex=END)
            word_end = sentence_display.index(f"{word_start}+{len(expected_word)}c")

            if typed_word == expected_word:
                sentence_display.tag_add("correct", word_start, word_end)
                correct_word_count += 1
            else:
                sentence_display.tag_add("incorrect", word_start, word_end)

            total_word_count += 1
            current_word_index += 1

        if current_word_index >= len(current_chunk_words):
            load_next_chunk()

    if time_left == 0:
        end_test()

def load_next_chunk():
    global current_word_index, start_word_index, current_chunk_words, current_chunk
    start_word_index += words_per_chunk
    if start_word_index < len(words):
        current_chunk = " ".join(words[start_word_index:start_word_index + words_per_chunk])
        current_chunk_words = current_chunk.split()
        current_word_index = 0
        sentence_display.config(state=NORMAL)
        sentence_display.delete("1.0", END)
        sentence_display.insert("1.0", current_chunk)
        sentence_display.config(state=DISABLED)

def end_test():
    global time_left, typing_start_time
    timer_running = False
    elapsed_time = time.time() - typing_start_time  # Time spent typing
    wpm = (total_word_count / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0
    accuracy = (correct_word_count / total_word_count) * 100 if total_word_count > 0 else 0

    result_label.config(text=f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")
    result_label.pack(pady=10)

    # Disable the entry box after the test ends
    user_entry.config(state=DISABLED)

def restart_test():
    global current_word_index, correct_word_count, total_word_count, start_time, start_word_index, current_chunk, current_chunk_words, time_left, timer_running, typing_start_time
    start_word_index = 0
    current_chunk = " ".join(words[start_word_index:start_word_index + words_per_chunk])
    current_chunk_words = current_chunk.split()
    current_word_index = 0
    correct_word_count = 0
    total_word_count = 0
    time_left = 60
    typing_start_time = None
    timer_running = False
    result_label.config(text="")
    sentence_display.config(state=NORMAL)
    sentence_display.delete("1.0", END)
    sentence_display.insert("1.0", current_chunk)
    sentence_display.config(state=DISABLED)
    timer_label.config(text="Time Left: 60s")

restart_button = Button(text="Restart Test", font=font, fg=text_color, bg=button_color, command=restart_test)

user_entry = Entry(
    font=font,
    fg=box_fg,
    bg=box_bg,
    width=80,
    relief=SOLID,
    borderwidth=2
)

user_entry.bind("<KeyRelease>", on_key_release)

sentence_display.tag_config("correct", foreground="green")
sentence_display.tag_config("incorrect", foreground="red")

heading.pack()
instruction.pack(pady=(5, 15))
sentence_display.pack(pady=15)
user_entry.pack(pady=10)
timer_label.pack(pady=10)
restart_button.pack(pady=20)

window.mainloop()
