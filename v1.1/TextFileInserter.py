import keyboard
import time
import threading

exit_flag = False


print("Tickets + Notifications macros:\n")
print("If CTRL + 1 = Notification for NJ studio")
print("If CTRL + 2 = Incorrectly Finished Round ticket format")
print("If CTRL + 4 = Base ticket format")
print("If CTRL + 5 = Base ticket format")
print("If CTRL + 6 = Base ticket format")
print("If CTRL + 7 = Base ticket format")
print("If CTRL + 8 = Base ticket format")
print("If CTRL + 9 = Base ticket format")
print("If CTRL + 0 = Base ticket format\n")
print("Chat Macros:\n")
print("If ALT + 1 = Hello, thank you for contacting support, how can I assist you today?")
print("If ALT + 2 = Hello, thank you for contacting support, how can I assist you today? Dear player, for a better assistance regarding any issues please use a translator for English. Thank you for understanding.")
print("If ALT + 3 = Hello, thank you for contacting support, dear player can you please provide more details regarding your request, Game ID, Table, Dealer name. ")
print("If ALT + 6 = Dear player, unfortunately these issues cannot be solved on our end. Please contact your operator for further assistance.  We apologize for any inconvenience this situation may have created.")
print("If ALT + 7 = Dear player, this type of behavior is not acceptable in the chat room and if this behavior persists, we will be forced to disable your chat system. Thank you for understanding.")
print("If ALT + 8 = Dear player, your chat system was temporarily disabled. If this behavior persists, we will be forced to disable your chat system permanently.")
print("If ALT + 9 = Dear player, your chat system was permanently disabled due bad behavior.")
print("If ALT + 0 = Dear player, you chat will be suspended for the next 12 hours due bad behavior.")

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
        elif keyboard.is_pressed('alt+1'):
            insert_text(read_text_from_file(file_path['F1']))
        elif keyboard.is_pressed('alt+2'):
            insert_text(read_text_from_file(file_path['F2']))
        elif keyboard.is_pressed('alt+3'):
            insert_text(read_text_from_file(file_path['F3']))
        elif keyboard.is_pressed('alt+6'):
            insert_text(read_text_from_file(file_path['F6']))
        elif keyboard.is_pressed('alt+7'):
            insert_text(read_text_from_file(file_path['F7']))
        elif keyboard.is_pressed('alt+8'):
            insert_text(read_text_from_file(file_path['F8']))
        elif keyboard.is_pressed('alt+9'):
            insert_text(read_text_from_file(file_path['F9']))
        elif keyboard.is_pressed('alt+0'):
            insert_text(read_text_from_file(file_path['F10']))
        time.sleep(0.1)

def main():
    file_paths = {
        'CTRL+1': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\TicketNotifications\Nj_notification.txt',
        'CTRL+2': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\TicketNotifications\inc_finished.txt',
        'CTRL+3': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\TicketNotifications\base_ticket.txt',
        'CTRL+4': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\TicketNotifications\Nj_notification.txt',
        'F1': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_1.txt',
        'F2': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_2.txt',
        'F3': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_3.txt',
        'F6': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_4.txt',
        'F7': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_5.txt',
        'F8': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_6.txt',
        'F9': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_7.txt',
        'F10': r'C:\Users\mihai.dobrin\Documents\GitHub\TextInserter\v1.1\Files\ChatTemplates\chat_8.txt',
        
        # Add more hotkeys and corresponding file paths as needed
    }
    keyboard.add_hotkey('F1', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F2', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F3', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F6', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F7', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F8', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F9', lambda: insert_text(read_text_from_file(file_paths)))
    keyboard.add_hotkey('F10', lambda: insert_text(read_text_from_file(file_paths)))

    keyboard_thread = threading.Thread(target=on_key_event, args=(file_paths,))
    keyboard_thread.start()

    keyboard.wait('esc')

    global exit_flag
    exit_flag = True
    keyboard_thread.join()

if __name__ == "__main__":
    main()