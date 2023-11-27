import keyboard
import time
import threading

feedback_text = "Text inserted!"
text_hello = "Hello,\nHope you're doing fine."
text_signature = "If you require further assistance or if you have any questions, please do not hesitate to contact us.\n\nBest regards,\nMihai Dobrin | Global CS Representative"
text_transaction = "Transaction"
exit_flag = False

def on_key_event():
    global exit_flag

    while not exit_flag:
        if keyboard.is_pressed('F2'):
            keyboard.write(text_hello)
            time.sleep(0.2)
            print(feedback_text)
        elif keyboard.is_pressed('F4'):
            keyboard.write(text_signature)
            time.sleep(0.2) 
            print(feedback_text)
        elif keyboard.is_pressed('F8'):
            keyboard.write(text_transaction)
            time.sleep(0.2)
            print(feedback_text)
        time.sleep(0.1)

keyboard_thread = threading.Thread(target=on_key_event)
keyboard_thread.start()

keyboard.wait('esc')

exit_flag = True
keyboard_thread.join()  
