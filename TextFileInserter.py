import keyboard
import time
import threading

exit_flag = False

print("If CTRL + 1 = Notification for NJ studio")
print("If CTRL + 2 = Incorrectly Finished Round ticket format")
print("If CTRL + 3 = Base ticket format")

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def insert_text(text):
    keyboard.write(text)
    time.sleep(0.2)

def on_key_event(file_path):
    global exit_flag

    while not exit_flag:
        if keyboard.is_pressed('CTRL+1'):
            insert_text(read_text_from_file(file_path['CTRL+1']))
        elif keyboard.is_pressed('CTRL+2'):
            insert_text(read_text_from_file(file_path['CTRL+2']))
        elif keyboard.is_pressed('CTRL+3'):
            insert_text(read_text_from_file(file_path['CTRL+3']))
        elif keyboard.is_pressed('CTRL+4'):
            insert_text(read_text_from_file(file_path['CTRL+4']))
        time.sleep(0.1)

def main():
    file_paths = {
        'CTRL+1': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\Files\Nj_notification.txt',
        'CTRL+2': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\Files\inc_finished.txt',
        'CTRL+3': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\Files\base_ticket.txt',
        'CTRL+4': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\Files\Nj_notification.txt',
        # Add more hotkeys and corresponding file paths as needed
    }

    keyboard_thread = threading.Thread(target=on_key_event, args=(file_paths,))
    keyboard_thread.start()

    keyboard.wait('esc')

    global exit_flag
    exit_flag = True
    keyboard_thread.join()

if __name__ == "__main__":
    main()