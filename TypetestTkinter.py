import tkinter as tk
from tkinter import messagebox
import random
import time

class HinglishTypingTestApp:
    def __init__  (self, root):
        self.root = root
        self.root.title("Hinglish Typing Test")
        self.root.geometry("900x650")
        
        # Hinglish text passages (Hindi words in Roman script mixed with English)
        self.passages = [
            "Mera naam Rahul hai aur main ek software engineer hoon. I work at a tech startup in Bangalore.",
            "Aaj kal ke zamaane mein internet ka use bahut important ho gaya hai. Without it, life would be very difficult.",
            "Kya aapne kabhi online shopping ki hai? Amazon and Flipkart pe bahut saare offers milte hain.",
            "Mere papa kahte hain ki padhai karo aur life mein successful bano. But success ka definition har kisi ke liye alag hota hai.",
            "Weekend pe main apne friends ke saath mall jata hoon. Waha hum movie dekhte hain aur delicious food khate hain.",
            "Mumbai ki local trains mein travel karna ek unique experience hai. You haven't seen India until you've tried it!",
            "Aajkal ke bachche bahut smart hote hain. They know how to use smartphones better than their parents.",
            "Meri favorite hobby cricket khelna hai. I play every Sunday with my colony friends.",
            "Ghar ka khana sabse best hota hai, no matter how fancy restaurant food you eat.",
            "Social media ne humari life ko easy aur complicated dono banaya hai. It's a double-edged sword."
        ]
        
        self.current_passage = ""
        self.start_time = 0
        self.running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        self.title_label = tk.Label(self.root, text="Hinglish Typing Speed Test", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)
        
        # Instructions
        self.instructions = tk.Label(self.root, 
                                    text="Type the following Hinglish text as quickly and accurately as possible.\nPress 'Start Test' to begin.",
                                    font=("Arial", 12))
        self.instructions.pack(pady=10)
        
        # Text to type
        self.text_to_type = tk.Text(self.root, height=6, width=85, wrap="word", 
                                   font=("Arial", 12), padx=10, pady=10)
        self.text_to_type.pack(pady=10)
        self.text_to_type.config(state="disabled")
        
        # User input
        self.user_input = tk.Text(self.root, height=6, width=85, wrap="word", 
                                font=("Arial", 12), padx=10, pady=10)
        self.user_input.pack(pady=10)
        self.user_input.config(state="disabled")
        
        # Stats frame
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.pack(pady=10)
        
        self.timer_label = tk.Label(self.stats_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.pack(side="left", padx=20)
        
        self.wpm_label = tk.Label(self.stats_frame, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.pack(side="left", padx=20)
        
        self.accuracy_label = tk.Label(self.stats_frame, text="Accuracy: 0%", font=("Arial", 12))
        self.accuracy_label.pack(side="left", padx=20)
        
        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        
        self.start_button = tk.Button(self.button_frame, text="Start Test", 
                                     command=self.start_test, font=("Arial", 12))
        self.start_button.pack(side="left", padx=10)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset", 
                                    command=self.reset_test, font=("Arial", 12))
        self.reset_button.pack(side="left", padx=10)
        
        # Initialize with a random passage
        self.new_passage()
    
    def new_passage(self):
        self.current_passage = random.choice(self.passages)
        self.text_to_type.config(state="normal")
        self.text_to_type.delete("1.0", tk.END)
        self.text_to_type.insert("1.0", self.current_passage)
        self.text_to_type.config(state="disabled")
    
    def start_test(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.user_input.config(state="normal")
            self.user_input.delete("1.0", tk.END)
            self.start_button.config(state="disabled")
            self.update_timer()
    
    def update_timer(self):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            
            # Calculate WPM every second
            typed_text = self.user_input.get("1.0", "end-1c")
            word_count = len(typed_text.split())
            minutes = elapsed / 60
            wpm = int(word_count / minutes) if minutes > 0 else 0
            self.wpm_label.config(text=f"WPM: {wpm}")
            
            # Calculate accuracy
            correct = 0
            for i, (typed_char, actual_char) in enumerate(zip(typed_text, self.current_passage)):
                if typed_char == actual_char:
                    correct += 1
            
            accuracy = (correct / len(self.current_passage)) * 100 if len(typed_text) > 0 else 0
            self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
            
            # Check if user has finished typing
            if len(typed_text) >= len(self.current_passage):
                self.finish_test()
            else:
                self.root.after(1000, self.update_timer)
    
    def finish_test(self):
        self.running = False
        self.user_input.config(state="disabled")
        
        # Final calculations
        typed_text = self.user_input.get("1.0", "end-1c")
        elapsed = time.time() - self.start_time
        word_count = len(typed_text.split())
        wpm = int(word_count / (elapsed / 60)) if elapsed > 0 else 0
        
        correct = 0
        for i, (typed_char, actual_char) in enumerate(zip(typed_text, self.current_passage)):
            if typed_char == actual_char:
                correct += 1
        
        accuracy = (correct / len(self.current_passage)) * 100 if len(typed_text) > 0 else 0
        
        # Show results
        messagebox.showinfo("Test Complete", 
                           f"Test completed!\n\nWPM: {wpm}\nAccuracy: {accuracy:.1f}%\nTime: {int(elapsed)} seconds")
    
    def reset_test(self):
        self.running = False
        self.new_passage()
        self.user_input.config(state="normal")
        self.user_input.delete("1.0", tk.END)
        self.user_input.config(state="disabled")
        self.start_button.config(state="normal")
        self.timer_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")

if __name__ == "__main__":
    root = tk.Tk()
    app = HinglishTypingTestApp(root)
    root.mainloop()