import keyboard
import time
import threading
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyperclip

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

def update_text_box(selection, file_paths, text_box, notification_title_box=None):
    selected_file = selection.get()
    abs_path = os.path.join(os.path.dirname(__file__), file_paths[selected_file])
    text = read_text_from_file(abs_path)
    
    if notification_title_box:
        if "notification" in selected_file.lower():
            lines = text.split('\n')
            notification_title_box.delete(1.0, tk.END)
            notification_title_box.insert(tk.END, lines[0])  # Display the first line (title) in the title box
            text = '\n'.join(lines[1:])  # Exclude the title from the main text
        else:
            notification_title_box.delete(1.0, tk.END)  # Clear the title box
    
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text)

def copy_to_clipboard(text_box):
    text = text_box.get(1.0, tk.END)
    pyperclip.copy(text)

def create_ui(file_paths):
    root = tk.Tk()
    root.title("Text Inserter")

    text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_box.pack(pady=10)

    # Create dropdown list for buttons
    selected_option = tk.StringVar()
    dropdown = tk.OptionMenu(root, selected_option, *file_paths.keys(), command=lambda _: update_text_box(selected_option, file_paths, text_box, notification_title_box))
    dropdown.config(font=("Arial", 10))  # Customize font
    dropdown.pack(pady=10)

    # Create title box for notification files
    notification_files = [key for key in file_paths.keys() if "notification" in key.lower()]
    if notification_files:
        notification_frame = tk.Frame(root)
        notification_frame.pack(pady=10)
        notification_title_label = tk.Label(notification_frame, text="Notification Title:")
        notification_title_label.pack(side=tk.LEFT)
        notification_title_box = tk.Text(notification_frame, wrap=tk.WORD, width=30, height=1)
        notification_title_box.pack(side=tk.LEFT)

    # Copy to clipboard button
    copy_button = tk.Button(root, text="Copy to Clipboard", command=lambda: copy_to_clipboard(text_box))
    copy_button.pack(pady=10)

    # Watermark label
    watermark_label = tk.Label(root, text="Made by @Dobrin Mihai-Alexandru", fg="gray", font=("Arial", 10, "italic"))
    watermark_label.pack(side=tk.BOTTOM, pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=20)

    root.mainloop()


def main():
    file_paths = {
        'NJ Notification': 'v1.2/Files/TicketNotifications/Nj_notification.txt',
        'Internal Notification': 'v1.2/Files/TicketNotifications/internal_notification.txt',
        'Base ticket': 'v1.2/Files/TicketNotifications/base_ticket.txt',
        'Ultimate Roulette Template': 'v1.2/Files/TicketNotifications/ultimate_roulette.txt',
        'Mail Validation': 'v1.2/Files/TicketNotifications/mail_validation.txt',
        'General Error Template': 'v1.2/Files/TicketNotifications/general_error.txt',
        'Incorrectly Finished Template': 'v1.2/Files/TicketNotifications/inc_finished.txt',
        'Chat 1': 'v1.2/Files/ChatTemplates/chat_1.txt',
        'Chat 2': 'v1.2/Files/ChatTemplates/chat_2.txt',
        'Chat 3': 'v1.2/Files/ChatTemplates/chat_3.txt',
        'Chat 4': 'v1.2/Files/ChatTemplates/chat_4.txt',
        'Chat 5': 'v1.2/Files/ChatTemplates/chat_5.txt',
        'Chat 6': 'v1.2/Files/ChatTemplates/chat_6.txt',
        'Chat 7': 'v1.2/Files/ChatTemplates/chat_7.txt',
        'Chat 8': 'v1.2/Files/ChatTemplates/chat_8.txt',
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
