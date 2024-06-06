import keyboard
import time
import threading
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

exit_flag = False

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        messagebox.showwarning("Warning", f"File not found at {file_path}")
        return ""

def insert_text(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        keyboard.write(line.strip())
        keyboard.press_and_release('ctrl+enter')

def on_key_event(file_paths):
    global exit_flag

    while not exit_flag:
        for hotkey, rel_path in file_paths.items():
            if keyboard.is_pressed(hotkey):
                abs_path = os.path.join(os.path.dirname(__file__), rel_path)
                insert_text(read_text_from_file(abs_path))
        time.sleep(0.1)

def trigger_macro(file_path, text_box):
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    text = read_text_from_file(abs_path)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text)

def create_ui(file_paths):
    root = tk.Tk()
    root.title("Chat Macros & Slack")

    text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_box.pack(pady=10)

    for hotkey, rel_path in file_paths.items():
        # Customizing the button text here
        button_text = f"{hotkey}"  # Customize this text as needed
        button = tk.Button(root, text=button_text, command=lambda rp=rel_path: trigger_macro(rp, text_box))
        button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=20)

    root.mainloop()

def main():
    file_paths = {
        'NJ Notification': 'v1.1/Files/TicketNotifications/Nj_notification.txt',
        'Internal Notification': 'v1.1/Files/TicketNotifications/internal_notification.txt',
        'Base ticket': 'v1.1/Files/TicketNotifications/base_ticket.txt',
        'Ultimate Roulette Template': 'v1.1/Files/TicketNotifications/ultimate_roulette.txt',
        'Mail Validation': 'v1.1/Files/TicketNotifications/mail_validation.txt',
        'General Error Template': 'v1.1/Files/TicketNotifications/general_error.txt',
        'Incorrectly Finished Template': 'v1.1/Files/TicketNotifications/inc_finished.txt',
        'Chat 1': 'v1.1/Files/ChatTemplates/chat_1.txt',
        'Chat 2': 'v1.1/Files/ChatTemplates/chat_2.txt',
        'Chat 3': 'v1.1/Files/ChatTemplates/chat_3.txt',
        'Chat 4': 'v1.1/Files/ChatTemplates/chat_4.txt',
        'Chat 5': 'v1.1/Files/ChatTemplates/chat_5.txt',
        'Chat 6': 'v1.1/Files/ChatTemplates/chat_6.txt',
        'Chat 7': 'v1.1/Files/ChatTemplates/chat_7.txt',
        'Chat 8': 'v1.1/Files/ChatTemplates/chat_8.txt',
        # Add more hotkeys and paths as needed
    }

    keyboard_thread = threading.Thread(target=on_key_event, args=(file_paths,))
    keyboard_thread.start()

    create_ui(file_paths)

    global exit_flag
    exit_flag = True
    keyboard_thread.join()

if __name__ == "__main__":
    main()
