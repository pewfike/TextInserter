import keyboard
import time
import threading
import os
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import pyperclip
import json

# Function to get the correct base path whether running as script or executable
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as executable - use the directory containing the executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

exit_flag = False

def read_text_from_file(file_path):
    try:
        # Get the base path
        base_path = get_base_path()
        # Create the full path
        full_path = os.path.join(base_path, file_path)
        
        with open(full_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        messagebox.showwarning("Warning", f"File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return ""

def write_text_to_file(file_path, text):
    try:
        # Get the base path for writing files
        base_path = get_base_path()
        # Create the full path by joining with the relative path
        full_path = os.path.join(base_path, file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the file
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(text)
        return True
    except Exception as e:
        print(f"Error in write_text_to_file: {str(e)}")  # Debug print
        print(f"Attempted path: {full_path}")  # Debug print
        messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        return False

def delete_file(file_path):
    try:
        # Get the base path
        base_path = get_base_path()
        # Create the full path by joining with the relative path
        full_path = os.path.join(base_path, file_path)
        
        os.remove(full_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
        return False

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
                base_path = get_base_path()
                abs_path = os.path.join(base_path, rel_path)
                insert_text(read_text_from_file(abs_path))
        time.sleep(0.1)

def update_text_box(selection, file_paths, text_box, notification_title_box=None):
    # Handle both StringVar and string inputs
    selected_file = selection.get() if hasattr(selection, 'get') else selection
    
    base_path = get_base_path()
    abs_path = os.path.join(base_path, file_paths[selected_file])
    text = read_text_from_file(abs_path)
    
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text)

def copy_to_clipboard(text_box):
    text = text_box.get(1.0, tk.END)
    pyperclip.copy(text)

def update_dropdowns(dropdowns, file_paths):
    chat_dropdown, notification_dropdown = dropdowns
    
    # Separate templates by type
    chat_templates = {k: v for k, v in file_paths.items() if 'ChatTemplates' in v}
    notification_templates = {k: v for k, v in file_paths.items() if 'TicketNotifications' in v}
    
    # Update Chat dropdown
    chat_menu = chat_dropdown['menu']
    chat_menu.delete(0, 'end')
    chat_menu.add_command(label="", command=lambda: chat_dropdown.setvar(chat_dropdown.cget("textvariable"), ""))
    for key in sorted(chat_templates.keys()):
        chat_menu.add_command(label=key, command=lambda k=key: chat_dropdown.setvar(chat_dropdown.cget("textvariable"), k))
    
    # Update Notification dropdown
    notification_menu = notification_dropdown['menu']
    notification_menu.delete(0, 'end')
    notification_menu.add_command(label="", command=lambda: notification_dropdown.setvar(notification_dropdown.cget("textvariable"), ""))
    for key in sorted(notification_templates.keys()):
        notification_menu.add_command(label=key, command=lambda k=key: notification_dropdown.setvar(notification_dropdown.cget("textvariable"), k))

def create_new_template(file_paths, dropdowns, text_box, selected_option):
    # Create new template window
    new_window = tk.Toplevel()
    new_window.title("Create New Template")
    new_window.geometry("800x600")
    
    # Center the window on the screen
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = (screen_width - 800) // 2
    y = (screen_height - 600) // 2
    new_window.geometry(f"800x600+{x}+{y}")
    
    # Create main frame
    main_frame = tk.Frame(new_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Template name frame
    name_frame = tk.Frame(main_frame)
    name_frame.pack(fill=tk.X, pady=5)
    name_label = tk.Label(name_frame, text="Template Name:")
    name_label.pack(side=tk.LEFT)
    name_entry = tk.Entry(name_frame, width=30)
    name_entry.pack(side=tk.LEFT, padx=5)
    
    # Template type frame with checkboxes
    type_frame = tk.Frame(main_frame)
    type_frame.pack(fill=tk.X, pady=10)
    type_label = tk.Label(type_frame, text="Template Type:")
    type_label.pack(side=tk.LEFT)
    
    # Create variables for checkboxes
    notification_var = tk.BooleanVar()
    chat_var = tk.BooleanVar()
    
    # Create checkboxes
    notification_check = tk.Checkbutton(type_frame, text="Notification", variable=notification_var)
    chat_check = tk.Checkbutton(type_frame, text="Chat", variable=chat_var)
    notification_check.pack(side=tk.LEFT, padx=5)
    chat_check.pack(side=tk.LEFT, padx=5)
    
    # Create text box for template content
    content_label = tk.Label(main_frame, text="Template Content:")
    content_label.pack(anchor=tk.W)
    edit_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=40, height=5)
    edit_text.pack(pady=5)
    
    # Create frame for buttons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    def save_template():
        try:
            # Get the template name
            template_name = name_entry.get().strip()
            if not template_name:
                messagebox.showerror("Error", "Template name cannot be empty")
                return
            
            # Check template type
            if not notification_var.get() and not chat_var.get():
                messagebox.showerror("Error", "Please select at least one template type")
                return
            
            # Get the content
            template_content = edit_text.get(1.0, tk.END).strip()
            
            # For notifications, prepend the title
            if notification_var.get():
                title = simpledialog.askstring("Notification Title", "Enter notification title:")
                if not title:
                    messagebox.showerror("Error", "Notification title cannot be empty")
                    return
                template_content = f"{title}\n{template_content}"
            
            # Determine the file path based on template type
            base_dir = 'Files/TicketNotifications' if notification_var.get() else 'Files/ChatTemplates'
            file_name = f"{template_name.lower().replace(' ', '_')}.txt"
            file_path = os.path.join(base_dir, file_name)
            
            # Save the template
            if write_text_to_file(file_path, template_content):
                # Update file_paths
                file_paths[template_name] = file_path
                
                # Update dropdowns
                update_dropdowns(dropdowns, file_paths)
                
                # Select the new template
                selected_option.set(template_name)
                update_text_box(template_name, file_paths, text_box)
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save the template file")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
    
    def cancel_template():
        new_window.destroy()
    
    # Add buttons
    save_button = tk.Button(button_frame, text="Save", command=save_template)
    save_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_template)
    cancel_button.pack(side=tk.LEFT, padx=5)

def edit_template(file_paths, dropdowns, text_box, selected_option):
    selected_template = selected_option.get()
    if not selected_template:
        messagebox.showwarning("Warning", "Please select a template to edit")
        return

    # Get the current template content
    base_path = get_base_path()
    abs_path = os.path.join(base_path, file_paths[selected_template])
    current_text = read_text_from_file(abs_path)
    
    # Create edit window
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Template: {selected_template}")
    edit_window.geometry("800x600")
    
    # Center the window on the screen
    screen_width = edit_window.winfo_screenwidth()
    screen_height = edit_window.winfo_screenheight()
    x = (screen_width - 800) // 2
    y = (screen_height - 600) // 2
    edit_window.geometry(f"800x600+{x}+{y}")
    
    # Create main frame
    main_frame = tk.Frame(edit_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Template name frame
    name_frame = tk.Frame(main_frame)
    name_frame.pack(fill=tk.X, pady=5)
    name_label = tk.Label(name_frame, text="Template Name:")
    name_label.pack(side=tk.LEFT)
    name_entry = tk.Entry(name_frame, width=30)
    name_entry.insert(0, selected_template)
    name_entry.pack(side=tk.LEFT, padx=5)
    
    # Add title field for notification type
    if "notification" in selected_template.lower():
        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        title_label = tk.Label(title_frame, text="Notification Title:")
        title_label.pack(side=tk.LEFT)
        title_entry = tk.Entry(title_frame, width=50)
        title_entry.pack(side=tk.LEFT, padx=5)
        
        # Split the content to get title and body
        lines = current_text.split('\n')
        if lines:
            title_entry.insert(0, lines[0])
            current_text = '\n'.join(lines[1:])
    
    # Create text box for template content
    content_label = tk.Label(main_frame, text="Template Content:")
    content_label.pack(anchor=tk.W)
    edit_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=20)
    edit_text.pack(pady=5)
    edit_text.insert(tk.END, current_text)
    
    # Create frame for buttons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    def save_changes():
        try:
            # Get the new template name
            new_template_name = name_entry.get().strip()
            if not new_template_name:
                messagebox.showerror("Error", "Template name cannot be empty")
                return
            
            # Get the content
            template_content = edit_text.get(1.0, tk.END).strip()
            
            # For notifications, prepend the title
            if "notification" in selected_template.lower():
                title = title_entry.get().strip()
                if not title:
                    messagebox.showerror("Error", "Notification title cannot be empty")
                    return
                template_content = f"{title}\n{template_content}"
            
            # Determine if the template type changed
            is_notification = "notification" in selected_template.lower()
            new_is_notification = "notification" in new_template_name.lower()
            
            # If template type changed, we need to move the file
            if is_notification != new_is_notification:
                # Delete the old file
                if delete_file(abs_path):
                    # Update the file path
                    base_dir = 'Files/TicketNotifications' if new_is_notification else 'Files/ChatTemplates'
                    file_name = f"{new_template_name.lower().replace(' ', '_')}.txt"
                    new_file_path = os.path.join(base_dir, file_name)
                    
                    # Update file_paths
                    del file_paths[selected_template]
                    file_paths[new_template_name] = new_file_path
                    
                    # Save the new file
                    if write_text_to_file(new_file_path, template_content):
                        # Update dropdowns
                        update_dropdowns(dropdowns, file_paths)
                        
                        # Select the new template
                        selected_option.set(new_template_name)
                        update_text_box(new_template_name, file_paths, text_box)
                        edit_window.destroy()
                        messagebox.showinfo("Success", "Template updated successfully")
                    else:
                        messagebox.showerror("Error", "Failed to update the template")
                else:
                    messagebox.showerror("Error", "Failed to delete the old template file")
            else:
                # Just update the content
                if write_text_to_file(abs_path, template_content):
                    # Update file_paths if name changed
                    if new_template_name != selected_template:
                        del file_paths[selected_template]
                        file_paths[new_template_name] = abs_path
                        
                        # Update dropdowns
                        update_dropdowns(dropdowns, file_paths)
                        
                        # Select the new template
                        selected_option.set(new_template_name)
                    
                    update_text_box(new_template_name, file_paths, text_box)
                    edit_window.destroy()
                    messagebox.showinfo("Success", "Template updated successfully")
                else:
                    messagebox.showerror("Error", "Failed to update the template")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating: {str(e)}")
    
    def cancel():
        edit_window.destroy()
    
    # Add buttons
    save_button = tk.Button(button_frame, text="Save Changes", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel)
    cancel_button.pack(side=tk.LEFT, padx=5)

def delete_template(file_paths, dropdowns, text_box, selected_option):
    # Create delete window
    delete_window = tk.Toplevel()
    delete_window.title("Delete Templates")
    delete_window.geometry("400x500")
    
    # Center the window on screen
    screen_width = delete_window.winfo_screenwidth()
    screen_height = delete_window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 500) // 2
    delete_window.geometry(f"400x500+{x}+{y}")
    
    # Create main frame
    main_frame = tk.Frame(delete_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Add title label
    title_label = tk.Label(main_frame, text="Select templates to delete:", font=("Arial", 12, "bold"))
    title_label.pack(pady=(0, 10))
    
    # Create frame for the list with scrollbar
    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    # Create scrollbar
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Create canvas with fixed width
    canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set, width=340)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure scrollbar
    scrollbar.config(command=canvas.yview)
    
    # Create frame for checkboxes
    checkbox_frame = tk.Frame(canvas)
    
    # Dictionary to store checkboxes variables
    checkbox_vars = {}
    
    # Create checkboxes for each template with improved styling
    for template_name in sorted(file_paths.keys()):
        var = tk.BooleanVar()
        checkbox_vars[template_name] = var
        cb = tk.Checkbutton(checkbox_frame, text=template_name, variable=var, 
                           font=("Arial", 10), pady=2, anchor="w", width=40)
        cb.pack(fill=tk.X, pady=3)
    
    # Add the checkbox frame to the canvas
    canvas_window = canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")
    
    # Update canvas scroll region when checkbox frame changes size
    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Make sure the window width matches the canvas width
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    
    checkbox_frame.bind('<Configure>', on_frame_configure)
    canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    # Create button frame with padding
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.BOTTOM, pady=(10, 0))
    
    def delete_selected():
        selected_templates = [name for name, var in checkbox_vars.items() if var.get()]
        
        if not selected_templates:
            messagebox.showwarning("Warning", "Please select at least one template to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_templates)} template(s)?"):
            success_count = 0
            for template_name in selected_templates:
                base_path = get_base_path()
                abs_path = os.path.join(base_path, file_paths[template_name])
                if delete_file(abs_path):
                    # Remove from file_paths
                    del file_paths[template_name]
                    success_count += 1
            
            # Update dropdowns
            update_dropdowns(dropdowns, file_paths)
            
            # Clear selection and text box if current template was deleted
            if selected_option.get() in selected_templates:
                selected_option.set('')
                text_box.delete(1.0, tk.END)
            
            # Show success message and close window
            messagebox.showinfo("Success", f"Successfully deleted {success_count} template(s)")
            delete_window.destroy()
    
    def cancel():
        delete_window.destroy()
    
    # Add buttons with improved styling
    delete_button = tk.Button(button_frame, text="Delete Selected", command=delete_selected,
                            font=("Arial", 10, "bold"), width=15, bg="#ff4d4d", fg="white",
                            activebackground="#ff6666")
    delete_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel,
                            font=("Arial", 10), width=15)
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    # Unbind mousewheel when window is destroyed
    def on_closing():
        canvas.unbind_all("<MouseWheel>")
        delete_window.destroy()
    
    delete_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Initial update of the canvas scroll region
    on_frame_configure()

def update_template(file_paths, dropdowns, text_box):
    # Get the selected template from the dropdown
    selected_template = dropdowns[0].cget("textvariable").get()
    if not selected_template:
        messagebox.showwarning("Warning", "Please select a template to update")
        return

    # Get the current template content
    abs_path = os.path.join(os.path.dirname(__file__), file_paths[selected_template])
    current_text = read_text_from_file(abs_path)
    
    # Create update window
    update_window = tk.Toplevel()
    update_window.title(f"Update Template: {selected_template}")
    update_window.geometry("600x500")

    # Create main frame
    main_frame = tk.Frame(update_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add title field for notification type
    if "notification" in selected_template.lower():
        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        title_label = tk.Label(title_frame, text="Notification Title:")
        title_label.pack(side=tk.LEFT)
        title_entry = tk.Entry(title_frame, width=50)
        title_entry.pack(side=tk.LEFT, padx=5)
        
        # Split the content to get title and body
        lines = current_text.split('\n')
        if lines:
            title_entry.insert(0, lines[0])
            current_text = '\n'.join(lines[1:])
    
    # Create text box for template content
    content_label = tk.Label(main_frame, text="Template Content:")
    content_label.pack(anchor=tk.W)
    edit_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=20)
    edit_text.pack(pady=5)
    edit_text.insert(tk.END, current_text)
    
    # Create frame for buttons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    def save_changes():
        try:
            # Get the content
            template_content = edit_text.get(1.0, tk.END).strip()
            
            # For notifications, prepend the title
            if "notification" in selected_template.lower():
                title = title_entry.get().strip()
                if not title:
                    messagebox.showerror("Error", "Notification title cannot be empty")
                    return
                template_content = f"{title}\n{template_content}"
            
            # Save the template
            if write_text_to_file(abs_path, template_content):
                # Update the text box with new content
                update_text_box(selected_template, file_paths, text_box)
                update_window.destroy()
                messagebox.showinfo("Success", "Template updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update the template")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating: {str(e)}")
    
    def cancel():
        update_window.destroy()
    
    # Add buttons
    save_button = tk.Button(button_frame, text="Save Changes", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel)
    cancel_button.pack(side=tk.LEFT, padx=5)

def create_ui(file_paths):
    root = tk.Tk()
    root.title("Text Inserter")

    # Set window size and position
    window_width = 1280
    window_height = 720
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create main container
    main_container = tk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create left frame for buttons
    left_frame = tk.Frame(main_container)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

    # Create right frame for text box and other controls
    right_frame = tk.Frame(main_container)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create dropdown frame
    dropdown_frame = tk.Frame(right_frame)
    dropdown_frame.pack(fill=tk.X, pady=(0, 10))

    # Create text box (larger)
    text_box = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=80, height=40, font=("Arial", 16))
    text_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    # Create template management buttons with larger font and square shape
    button_font = ("Arial", 12, "bold")
    button_width = 15
    button_height = 2

    # Create variables for both dropdowns
    chat_option = tk.StringVar()
    notification_option = tk.StringVar()
    selected_option = tk.StringVar()  # This will store the currently selected template
    
    # Set initial values to empty string
    chat_option.set("")
    notification_option.set("")
    selected_option.set("")

    # Separate templates by type
    chat_templates = {k: v for k, v in file_paths.items() if 'ChatTemplates' in v}
    notification_templates = {k: v for k, v in file_paths.items() if 'TicketNotifications' in v}

    # Create label and dropdown for Chat templates
    chat_label = tk.Label(dropdown_frame, text="Chat Templates:", font=("Arial", 10, "bold"))
    chat_label.pack(side=tk.LEFT, padx=(0, 5))
    
    chat_dropdown = tk.OptionMenu(dropdown_frame, chat_option, "", *sorted(chat_templates.keys()))
    chat_dropdown.config(font=("Arial", 10), width=30)
    chat_dropdown.pack(side=tk.LEFT, padx=5)

    # Create label and dropdown for Notification templates
    notification_label = tk.Label(dropdown_frame, text="Notifications/Tickets:", font=("Arial", 10, "bold"))
    notification_label.pack(side=tk.LEFT, padx=(20, 5))
    
    notification_dropdown = tk.OptionMenu(dropdown_frame, notification_option, "", *sorted(notification_templates.keys()))
    notification_dropdown.config(font=("Arial", 10), width=30)
    notification_dropdown.pack(side=tk.LEFT, padx=5)

    # Function to handle template selection from either dropdown
    def on_template_selected(*args):
        # Get the current values from both dropdowns
        chat_value = chat_option.get()
        notification_value = notification_option.get()
        
        # Determine which variable was changed by checking the args
        changed_var = args[0]
        
        if changed_var == chat_option._name:
            # Chat dropdown was changed
            if chat_value:
                notification_option.set("")  # Clear notification dropdown
                selected_option.set(chat_value)
                update_text_box(chat_value, file_paths, text_box)
        elif changed_var == notification_option._name:
            # Notification dropdown was changed
            if notification_value:
                chat_option.set("")  # Clear chat dropdown
                selected_option.set(notification_value)
                update_text_box(notification_value, file_paths, text_box)
        
        # If both are empty, clear everything
        if not chat_value and not notification_value:
            selected_option.set("")
            text_box.delete(1.0, tk.END)

    # Bind the dropdowns to the selection handler
    chat_option.trace('w', on_template_selected)
    notification_option.trace('w', on_template_selected)

    # Clear the text box initially
    text_box.delete(1.0, tk.END)

    new_button = tk.Button(left_frame, text="New Template", 
                         command=lambda: create_new_template(file_paths, [chat_dropdown, notification_dropdown], text_box, selected_option),
                         font=button_font, width=button_width, height=button_height)
    new_button.pack(pady=5)

    edit_button = tk.Button(left_frame, text="Edit Template", 
                          command=lambda: edit_template(file_paths, [chat_dropdown, notification_dropdown], text_box, selected_option),
                          font=button_font, width=button_width, height=button_height)
    edit_button.pack(pady=5)

    delete_button = tk.Button(left_frame, text="Delete Template", 
                            command=lambda: delete_template(file_paths, [chat_dropdown, notification_dropdown], text_box, selected_option),
                            font=button_font, width=button_width, height=button_height)
    delete_button.pack(pady=5)

    # Copy to clipboard button (dark red)
    copy_button = tk.Button(left_frame, text="Copy to Clipboard", 
                          command=lambda: copy_to_clipboard(text_box),
                          font=button_font, width=button_width, height=button_height,
                          bg="#8B0000", fg="white", activebackground="#A52A2A")
    copy_button.pack(pady=5)

    # Add version label above Exit button
    version_label = tk.Label(left_frame, text="Version 2.0", fg="gray", font=("Arial", 10, "italic"))
    version_label.pack(side=tk.BOTTOM, pady=(0, 5))

    # Add Exit button at the bottom of left frame
    exit_button = tk.Button(left_frame, text="Exit", 
                          command=root.quit,
                          font=button_font, width=button_width, height=button_height)
    exit_button.pack(side=tk.BOTTOM, pady=5)

    # Set up the initial dropdown menus
    update_dropdowns([chat_dropdown, notification_dropdown], file_paths)

    # Watermark label
    watermark_label = tk.Label(root, text="Made by @Dobrin Mihai-Alexandru", fg="gray", font=("Arial", 10, "italic"))
    watermark_label.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()

def main():
    # Initialize empty dictionary for file paths
    file_paths = {}
    
    # Define the base directories
    notification_dir = 'Files/TicketNotifications'
    chat_dir = 'Files/ChatTemplates'
    
    # Get the base path (works for both script and executable)
    base_path = get_base_path()
    
    # Load notification templates
    notification_path = os.path.join(base_path, notification_dir)
    if os.path.exists(notification_path):
        for file in os.listdir(notification_path):
            if file.endswith('.txt'):
                template_name = file.replace('.txt', '').replace('_', ' ').title()
                file_paths[template_name] = os.path.join(notification_dir, file)
    
    # Load chat templates
    chat_path = os.path.join(base_path, chat_dir)
    if os.path.exists(chat_path):
        for file in os.listdir(chat_path):
            if file.endswith('.txt'):
                template_name = file.replace('.txt', '').replace('_', ' ').title()
                file_paths[template_name] = os.path.join(chat_dir, file)

    keyboard_thread = threading.Thread(target=on_key_event, args=(file_paths,))
    keyboard_thread.start()

    create_ui(file_paths)

    global exit_flag
    exit_flag = True
    keyboard_thread.join()

if __name__ == "__main__":
    main()
