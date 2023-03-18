import os
import datetime
import pyautogui
from pynput import keyboard
from fpdf import FPDF
import tkinter as tk

# set the directory to save the screenshots
screenshots_dir = 'screenshots'

# create the screenshots directory if it doesn't exist
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)

# initialize the list of screenshots
screenshots = []

# define the function to take a screenshot
def take_screenshot():
    now = datetime.datetime.now()
    filename = os.path.join(screenshots_dir, f'screenshot_{now.strftime("%Y-%m-%d_%H-%M-%S")}.png')
    pyautogui.screenshot(filename)
    screenshots.append(filename)
    listbox.insert(tk.END, filename)
    print(f'Screenshot taken: {filename}')

# define the function to save the screenshots as a PDF file
def save_pdf():
    pdf = FPDF()
    for screenshot in screenshots:
        pdf.add_page()
        pdf.image(screenshot)
    pdf_filename = os.path.join(screenshots_dir, 'screenshots.pdf')
    pdf.output(pdf_filename, 'F')
    print(f'PDF file saved: {pdf_filename}')

# define the function to handle key presses
def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l and keyboard.KeyCode.from_char('s'):
            take_screenshot()
    except AttributeError:
        pass

# create a listener for key presses
with keyboard.Listener(on_press=on_press) as listener:
    # create the GUI
    root = tk.Tk()
    root.title('Screenshots')
    root.geometry('400x300')

    # create the listbox to display the screenshots
    listbox = tk.Listbox(root)
    listbox.pack(fill=tk.BOTH, expand=True)

    # create the "Save PDF" button
    save_button = tk.Button(root, text='Save PDF', command=save_pdf)
    save_button.pack(side=tk.BOTTOM, pady=10)

    # start the GUI main loop
    root.mainloop()

    # stop the key press listener when the GUI is closed
    listener.stop()