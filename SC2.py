
import tkinter as tk

class RichTextRenderer:
    def __init__(self, canvas_width=600, canvas_height=400, font=('Arial', 12)):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.font = font

    def render(self, text, tags):
        # Create the root window and the canvas widget
        root = tk.Tk()
        root.geometry(f'{self.canvas_width}x{self.canvas_height}')
        canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        canvas.pack()

        # Set up the tags in the text widget
        text_widget = tk.Text(root, wrap='word', font=self.font, width=self.canvas_width//10, height=self.canvas_height//20)
        text_widget.pack_forget()  # Pack and immediately forget to avoid the widget being seen
        for tag_name, tag_positions in tags.items():
            for pos in tag_positions:
                start = f'1.0 + {pos[0]}c'
                end = f'1.0 + {pos[1]}c'
                text_widget.tag_add(tag_name, start, end)

        # Insert the text into the text widget
        text_widget.insert('end', text)

        # Get the lines of text in the widget
        lines = text_widget.get('1.0', 'end').split('\n')

        # Get the tag positions for each line
        line_tags = {}
        for tag_name, tag_positions in tags.items():
            for pos in tag_positions:
                start, end = pos
                for i, line in enumerate(lines):
                    if start < len(line):
                        if i not in line_tags:
                            line_tags[i] = {}
                        if tag_name not in line_tags[i]:
                            line_tags[i][tag_name] = []
                        if end <= len(line):
                            line_tags[i][tag_name].append((start, end))
                            break
                        else:
                            line_tags[i][tag_name].append((start, len(line)))
                            start = 0
                            end -= len(line) + 1

        # Draw the text and tags in the canvas widget
        for i, line in enumerate(lines):
            y = i * self.font[1] + 5
            x = 5
            for tag_name, tag_positions in line_tags.get(i, {}).items():
                for pos in tag_positions:
                    start, end = pos
                    s = f'{i+1}.{start}'
                    e = f'{i+1}.{end}'
                    b1 = text_widget.bbox("1.5")
                    b2=text_widget.bbox(e)
                    print(b1,b2)
                    if b1!=None and b2!=None:
                        x0, y0,_,__ = b1
                        x1,y1,w1,h1= b2
                        x1+=w1
                        y1+=h1
                        canvas.create_rectangle(x0, y0, x1, y1, outline='red')
            canvas.create_text(x, y, text=line, anchor='nw', font=self.font)

        # Start the main loop
        root.mainloop()
renderer = RichTextRenderer()
text = 'This is a test sentence. It contains two tags: the first tag and the second tag.'
tags = {
    'first_tag': [(25, 34)],
    'second_tag': [(48, 59)]
}
renderer.render(text, tags)



"""
import tkinter as tk

root = tk.Tk()

text = tk.Text(root, width=30, height=10)
text.pack()

text.insert('0.0', 'Hello, world! This is some rich text.')
text.tag_add('bold', '1.0', '6.0')  # Tag the first word
text.tag_add('tag1', '8.0', '13.0')  # Tag the second word
text.tag_add('tag1', '14.0', '30.0')  # Tag the rest of the sentence

for tag in text.tag_names():
    indices = text.tag_ranges(tag)
    for i in indices:
        print(i)

root.mainloop()
"""

"""
import tkinter as tk

def display_rich_text(canvas, text, tags):
    canvas.create_text()
    for tag in tags:
        canvas.create_text(tag['x'], tag['y'], text=text[tag['start']:tag['end']], font=tag['font'], fill=tag['color'], anchor=tag['anchor'])

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

text = 'Hello, world! This is some rich text.'
tags = [
    {'start': 0, 'end': 6, 'font': 'Arial 24 bold', 'color': 'black', 'x': 50, 'y': 50, 'anchor': 'nw'},
    {'start': 4, 'end': 13, 'font': 'Arial 24 bold', 'color': 'blue', 'x': 100, 'y': 100, 'anchor': 'nw'},
    {'start': 14, 'end': 30, 'font': 'Verdana 18 underline', 'color': 'red', 'x': 150, 'y': 150, 'anchor': 'nw'},
]

display_rich_text(canvas, text, tags)

root.mainloop()






"""
"""
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import ctypes
from functools import partial
from json import loads, dumps

ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup
root = Tk()
root.geometry('600x600')

# Used to make title of the application
applicationName = 'Rich Text Editor'
root.title(applicationName)

# Current File Path
filePath = None

# initial directory to be the current directory
initialdir = '.'

# Define File Types that can be choosen
validFileTypes = (
    ("Rich Text File","*.rte"),
    ("all files","*.*")
)

# Setting the font and Padding for the Text Area
fontName = 'Bahnschrift'
padding = 60

# Infos about the Document are stored here
document = None

# Default content of the File
defaultContent = {
    "content": "",
    "tags": {
        'bold': [(), ()]
    },
}

# Transform rgb to hex
def rgbToHex(rgb):
    return "#%02x%02x%02x" % rgb  

# Add Different Types of Tags that can be added to the document.
tagTypes = {
    # Font Settings
    'Bold': {'font': f'{fontName} 15 bold'},
    'Italic': {'font': f'{fontName} 15 italic'},
    'Code': {'font': 'Consolas 15', 'background': rgbToHex((200, 200, 200))},

    # Sizes
    'Normal Size': {'font': f'{fontName} 15'},
    'Larger Size': {'font': f'{fontName} 25'},
    'Largest Size': {'font': f'{fontName} 35'},

    # Background Colors
    'Highlight': {'background': rgbToHex((255, 255, 0))},
    'Highlight Red': {'background': rgbToHex((255, 0, 0))},
    'Highlight Green': {'background': rgbToHex((0, 255, 0))},
    'Highlight Black': {'background': rgbToHex((0, 0, 0))},

    # Foreground /  Text Colors
    'Text White': {'foreground': rgbToHex((255, 255, 255))},
    'Text Grey': {'foreground': rgbToHex((200, 200, 200))},
    'Text Blue': {'foreground': rgbToHex((0, 0, 255))},
    'Text green': {'foreground': rgbToHex((0, 255, 0))},
    'Text Red': {'foreground': rgbToHex((255, 0, 0))},
}

# Handle File Events
def fileManager(event=None, action=None):
    global document, filePath

    # Open
    if action == 'open':
        # ask the user for a filename with the native file explorer.
        filePath = askopenfilename(filetypes=validFileTypes, initialdir=initialdir)


        with open(filePath, 'r') as f:
            document = loads(f.read())

        # Delete Content
        textArea.delete('1.0', END)
        
        # Set Content
        textArea.insert('1.0', document['content'])

        # Set Title
        root.title(f'{applicationName} - {filePath}')

        # Reset all tags
        resetTags()

        # Add To the Document
        for tagName in document['tags']:
            for tagStart, tagEnd in document['tags'][tagName]:
                textArea.tag_add(tagName, tagStart, tagEnd)
                print(tagName, tagStart, tagEnd)

    elif action == 'save':
        document = defaultContent
        document['content'] = textArea.get('1.0', END)

        for tagName in textArea.tag_names():
            if tagName == 'sel': continue

            document['tags'][tagName] = []

            ranges = textArea.tag_ranges(tagName)

            for i, tagRange in enumerate(ranges[::2]):
                document['tags'][tagName].append([str(tagRange), str(ranges[i+1])])

        if not filePath:
            # ask the user for a filename with the native file explorer.
            newfilePath = asksaveasfilename(filetypes=validFileTypes, initialdir=initialdir)
    
            # Return in case the User Leaves the Window without
            # choosing a file to save
            if newfilePath is None: return

            filePath = newfilePath

        if not filePath.endswith('.rte'):
            filePath += '.rte'

        with open(filePath, 'w') as f:
            print('Saving at: ', filePath)  
            f.write(dumps(document))

        root.title(f'{applicationName} - {filePath}')


def resetTags():
    for tag in textArea.tag_names():
        textArea.tag_remove(tag, "1.0", "end")

    for tagType in tagTypes:
        textArea.tag_configure(tagType.lower(), tagTypes[tagType])


def keyDown(event=None):
    root.title(f'{applicationName} - *{filePath}')


def tagToggle(tagName):
    start, end = "sel.first", "sel.last"

    if tagName in textArea.tag_names('sel.first'):
        textArea.tag_remove(tagName, start, end)
    else:
        textArea.tag_add(tagName, start, end)


textArea = Text(root, font=f'{fontName} 15', relief=FLAT)
textArea.pack(fill=BOTH, expand=TRUE, padx=padding, pady=padding)
textArea.bind("<Key>", keyDown)

resetTags()


menu = Menu(root)
root.config(menu=menu)

fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=fileMenu)

fileMenu.add_command(label="Open", command=partial(fileManager, action='open'), accelerator='Ctrl+O')
root.bind_all('<Control-o>', partial(fileManager, action='open'))

fileMenu.add_command(label="Save", command=partial(fileManager, action='save'), accelerator='Ctrl+S')
root.bind_all('<Control-s>', partial(fileManager, action='save'))

fileMenu.add_command(label="Exit", command=root.quit)


formatMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Format", menu=formatMenu)

for tagType in tagTypes:
    formatMenu.add_command(label=tagType, command=partial(tagToggle, tagName=tagType.lower()))


root.mainloop()
"""