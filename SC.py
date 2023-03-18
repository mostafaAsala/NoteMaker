import vlc
import tkinter as tk
from tkinter import filedialog as fd 
from pynput import keyboard

from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from functools import partial
import pickle
"""
# Create a VLC instance
vlc_instance = vlc.Instance()

# Create a media player
player = vlc_instance.media_player_new()
# Load the media file
media = vlc_instance.media_new('path/to/video.mp4')

# Set the media for the player
player.set_media(media)
"""

class TagTypes:
    def __init__(self) -> None:
        
        self.fontName = 'Bahnschrift'
        self.padding = 5
        self.tagTypes = {
                # Font Settings
                'Bold': {'font': f'{self.fontName} 15 bold'},
                'Italic': {'font': f'{self.fontName} 15 italic'},
                'Code': {'font': 'Consolas 15', 'background': self.rgbToHex((200, 200, 200))},

                # Sizes
                'Normal Size': {'font': f'{self.fontName} 15'},
                'Larger Size': {'font': f'{self.fontName} 25'},
                'Largest Size': {'font': f'{self.fontName} 35'},

                # Background Colors
                'No Highlight': {'background': self.rgbToHex((255, 255, 0))},
                'Highlight Red': {'background': self.rgbToHex((255, 0, 0))},
                'Highlight Green': {'background':self.rgbToHex((0, 255, 0))},
                'Highlight Black': {'background': self.rgbToHex((0, 0, 0))},

                # Foreground /  Text Colors
                'Text White': {'foreground': self.rgbToHex((255, 255, 255))},
                'Text Grey': {'foreground': self.rgbToHex((200, 200, 200))},
                'Text Blue': {'foreground': self.rgbToHex((0, 0, 255))},
                'Text green': {'foreground': self.rgbToHex((0, 255, 0))},
                'Text Red': {'foreground': self.rgbToHex((255, 0, 0))},
            }
    def rgbToHex(self,rgb):
        return "#%02x%02x%02x" % rgb  
tagtypes = TagTypes()    

class VideoData:
    def __init__(self) -> None:
        self.directory =""    
        self.name = ""
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.media =""

        pass

    def Getvideo(self):
        self.name = fd.askopenfilename() 
        print(self.name)
    def play_video(self):
        self.media = self.vlc_instance.media_new(self.name)
        self.player.set_media(self.media)
        self.player.play()
    def Select_video(self):
        self.Getvideo()
        self.play_video()
        pass

class shot:
    def __init__(self) -> None:
        self.time=None
        self.data=None
        pass
class VLC_Reader:

    def __init__(self) -> None:
        self.screenshots = []    
        self.data = VideoData()
        self.rate = 1
        pass

    def take_screenshot(self,event):
        screen = self.data.player.video_take_snapshot(0, 'screenshot.png', 0, 0)
        if(screen==0):
            image = Image.open('screenshot.png')
            return image

    def on_press(self,key):
        
        try:
            if key == keyboard.Key.ctrl_l and keyboard.KeyCode.from_char('s'):
                
                self.take_screenshot(key)
        except AttributeError:
            pass
class canvas_holder:
    def __init__(self) -> None:
        self.canvas=None
        self.img = None
        self.text=None
        self.label=None
        self.tags=None
        pass

class ListArea(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.list =[]
        # create a scrollable frame
        self.canvas = tk.Canvas(self, borderwidth=2, highlightthickness=2 ,bg='gray')
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # add the scrollable frame to the main frame
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def render_item(self,item,tags=None):
        d = canvas_holder()
        if isinstance(item, str):
            # if the item is a string, add it as rich text
            #canvas.create_text(30, 50, text=item, font=('Helvetica 15 bold'),tags= "html")
            
            label = Text(self.scrollable_frame, relief=FLAT,height=1,width=25)
            label.insert(INSERT,item)
            for tag in tagtypes.tagTypes:
                label.tag_configure(tag.lower(),tagtypes.tagTypes[tag])
            
            scaller = 1
            
            if tags !=None: 
                for tag in tags:
                    for i in range(0,len(tags[tag]),2):
                        if(tag=='bold' and scaller==1):
                            scaller=2
                        elif tag=='larger size' and scaller<3:
                            scaller=3
                        elif tag =='largest size' and scaller<4:
                            scaller=4
                        
                        label.tag_add(tag.lower(),tags[tag][i],tags[tag][i+1])
                print(label.tag_ranges('bold'))
            label.pack(padx=5,pady=5,fill='both', expand=False)
            
            width = (max(len(line) for line in item.split('\n')))*scaller
            height = (item.count('\n') + 1)*scaller
            if width>35: height*=(width//35)*0.8
            width = 35 if width>35 else width
            height = 8 if height>8 else height
             
            label.configure(width=width,height=height)
            
            
            
            d.text = item
            d.label=label
            d.tags=tags
            
        elif isinstance(item, Image.Image):
            canvas= Canvas(self.scrollable_frame, width= 200,height=50)
            canvas.pack(padx=5,pady=5)
            d.canvas = canvas    
        
            # if the item is an image, add it to the list
            img = ImageTk.PhotoImage(item)
            id = canvas.create_image(0,0,anchor=NW,image=img)
            d.img= img
        else:
            raise TypeError("Item must be either a string or a PIL image.")
        self.list.append(d)

        
        pass
    def restore(self):
        for item in self.list:
            

            if item.img!=None:
                canvas= Canvas(self.scrollable_frame, width= 200,height=50)
                canvas.pack(padx=5,pady=5)   
                canvas.create_image(0,0,anchor=NW,image=item)
                item.canvas = canvas

            elif item.text!=None:
                tags = item.tags
                string = item.text
                label = Text(self.scrollable_frame, relief=FLAT,height=1,width=25)
                label.insert(INSERT,string)
                for tag in tagtypes.tagTypes:
                    label.tag_configure(tag.lower(),tagtypes.tagTypes[tag])
                
                scaller = 1
                
                if tags !=None: 
                    for tag in tags:
                        for i in range(0,len(tags[tag]),2):
                            if(tag=='bold' and scaller==1):
                                scaller=2
                            elif tag=='larger size' and scaller<3:
                                scaller=3
                            elif tag =='largest size' and scaller<4:
                                scaller=4
                            
                            label.tag_add(tag.lower(),tags[tag][i],tags[tag][i+1])
                    print(label.tag_ranges('bold'))
                label.pack(padx=5,pady=5,fill='both', expand=False)
                
                width = (max(len(line) for line in string.split('\n')))*scaller
                height = (string.count('\n') + 1)*scaller
                if width>35: height*=(width//35)*0.8
                width = 35 if width>35 else width
                height = 8 if height>8 else height
                
                label.configure(width=width,height=height)
                item.label = label
            
            
        pass   
    def edit_item(self,index,data):
        if isinstance(data, str):
            pass
            #self.list[index].itemconfig(1, text = data)
        elif isinstance(data, ImageTk.PhotoImage):
            self.list[index].canvas.delete("all")
            self.list[index].canvas.create_image(10, 10, anchor=NW, image=data)
            self.list[index].canvas.config(height = data.height()+10,width = data.width()+10)
            self.list[index].img = data
            
            

    """
    def render_items(self):
        self.clear_items()
        
        for item in self.list:
            if isinstance(item, str):
                # if the item is a string, add it as rich text
                tk.Label(self.scrollable_frame, text=item).pack(pady=10)
                
            elif isinstance(item, Image.Image):
                # if the item is an image, add it to the list
                img = ImageTk.PhotoImage(item)
                label = tk.Label(self.scrollable_frame, image=img)
                label.image = img
                label.pack(padx=10, pady=10)
                
            else:
                raise TypeError("Item must be either a string or a PIL image.")
    
    def add_item(self, item_new):
        
        self.list.append(item_new)
        self.render_items()
    """ 
    def clear_items(self):
        # remove all items from the list
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

class TextEditor(tk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
         # Setting the font and Padding for the Text Area
        self.fontName = 'Bahnschrift'
        self.padding = 5
        # Infos about the Document are stored here
        self.document = None

        # Default content of the File
        self.defaultContent = {
            "content": "",
            "tags": {
                'bold': [(), ()]
            },
        }
        # Add Different Types of Tags that can be added to the document.
        self.tagTypes = {
            # Font Settings
            'Bold': {'font': f'{self.fontName} 15 bold'},
            'Italic': {'font': f'{self.fontName} 15 italic'},
            'Code': {'font': 'Consolas 15', 'background': self.rgbToHex((200, 200, 200))},

            # Sizes
            'Normal Size': {'font': f'{self.fontName} 15'},
            'Larger Size': {'font': f'{self.fontName} 25'},
            'Largest Size': {'font': f'{self.fontName} 35'},

            # Background Colors
            'No Highlight': {'background': self.rgbToHex((255, 255, 0))},
            'Highlight Red': {'background': self.rgbToHex((255, 0, 0))},
            'Highlight Green': {'background':self.rgbToHex((0, 255, 0))},
            'Highlight Black': {'background': self.rgbToHex((0, 0, 0))},

            # Foreground /  Text Colors
            'Text White': {'foreground': self.rgbToHex((255, 255, 255))},
            'Text Grey': {'foreground': self.rgbToHex((200, 200, 200))},
            'Text Blue': {'foreground': self.rgbToHex((0, 0, 255))},
            'Text green': {'foreground': self.rgbToHex((0, 255, 0))},
            'Text Red': {'foreground': self.rgbToHex((255, 0, 0))},
        }
        self.textsetting = {'Bold':'B','Italic':'I','Code':'C'}
        self.textSize = {'Normal Size':'normal','Larger Size':'medium','Largest Size':'large'}
        self.BC = {'Highlight':'none','Highlight Red':'red','Highlight Green':'green','Highlight Black':'black'}
        self.FC = {'Text White':'white','Text Grey':'grey','Text Blue':'blue','Text green':'green','Text Red':'red'}

        
        self.textArea = Text(self, font=f'{self.fontName} 15', relief=FLAT,height=2)
        self.textArea.pack(fill=BOTH, expand=TRUE, padx=self.padding, pady=self.padding)
        self.textArea.bind("<Key>", self.keyDown)
        self.textArea.bind('<FocusIn>',self.on_select)
        self.resetTags()
    def on_select(self,event):
        print("select")
        pass

        # Transform rgb to hex
    def rgbToHex(self,rgb):
        return "#%02x%02x%02x" % rgb  
    
    def resetTags(self):
        for tag in self.textArea.tag_names():
            self.textArea.tag_remove(tag, "1.0", "end")

        for tagType in self.tagTypes:
            self.textArea.tag_configure(tagType.lower(), self.tagTypes[tagType])


    def keyDown(self,event=None):
        return
        self.title(f'{"Editor"} - *{"filePath"}')


    def tagToggle(self,tagName):
        start, end = "sel.first", "sel.last"

        if tagName in self.textArea.tag_names('sel.first'):
            self.textArea.tag_remove(tagName, start, end)
        else:
            self.textArea.tag_add(tagName, start, end)



class TextEditorFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.user_input=""
        # Create the text field
        self.text = TextEditor(self)
        self.text.pack(side="top", fill="x")
        
        self.submit_button = ttk.Button(self, text="Enter", command=self.submit_text)
        self.submit_button.pack(side="bottom", padx=5, pady=5,expand=True)
        self.text_event = None
        # Create the formatting buttons and combobox
        comwidth =4
        self.whole = tk.Frame(self)
        self.text.textArea.bind("<FocusIn>",lambda event: self.whole.pack())

        for tagtype in self.text.textsetting:
            button = ttk.Button(self.whole, text=self.text.textsetting[tagtype], width=3, command=partial(self.text.tagToggle, tagName=tagtype.lower()))
            button.pack(side="right", padx=5, pady=5)
        
        f=tk.Frame(self.whole)
        f.pack(fill=tk.X, padx=5, pady=5,side="right")
        
        self.selected_BC = tk.StringVar()   
        l=tk.Label(f,text="size")
        l.pack(fill=tk.X, padx=0, pady=0,side="top")

        self.selected_size = tk.StringVar()   
        textSize = ttk.Combobox(f,values = [self.text.textSize[t]for t in self.text.textSize] ,width=comwidth,textvariable = self.selected_size)
        textSize.bind('<<ComboboxSelected>>', self.sel)
        textSize.current(0)
        textSize.pack(fill=tk.X, padx=0, pady=0,side="right")
        
        f=tk.Frame(self.whole)
        f.pack(fill=tk.X, padx=5, pady=5,side="right")
        self.selected_BC = tk.StringVar()   
        l=tk.Label(f,text="back")
        l.pack(fill=tk.X, padx=0, pady=0,side="top")
        
        textBC = ttk.Combobox(f,values =[self.text.BC[t]for t in self.text.BC] ,width=comwidth ,textvariable = self.selected_BC)
        textBC.bind('<<ComboboxSelected>>', self)
        textBC.current(0)
        textBC.pack(fill=tk.X, padx=0, pady=0,side="top")
        
        
        f=tk.Frame(self.whole)
        f.pack(fill=tk.X, padx=5, pady=5,side="right")
        self.selected_BC = tk.StringVar()   
        l=tk.Label(f,text="fore")
        l.pack(fill=tk.X, padx=0, pady=0,side="top")

        self.selected_FC = tk.StringVar()    
        textFC = ttk.Combobox(f,values = [self.text.FC[t]for t in self.text.FC],width=comwidth ,textvariable = self.selected_FC)
        textFC.bind('<<ComboboxSelected>>', self)
        textFC.current(0)
        textFC.pack(fill=tk.X, padx=0, pady=0,side="right")
          


    def submit_text(self):
        self.user_input = self.text.textArea.get("1.0",'end-1c')
        
        if(self.user_input==""):
            return
        self.tags = {}
        for tagname in self.text.textArea.tag_names():
            self.tags[tagname] = self.text.textArea.tag_ranges(tagname)
        self.whole.pack_forget()  
        self.text_event()
        self.text.textArea.delete('1.0','end')
        self.text.resetTags()

    def sel(self,event):
            self.text.tagToggle(event.widget.get().lower())
          
class InputFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        # Create a text field for the user input
        self.text_field = tk.Entry(self)
        self.text_field.pack(side=tk.LEFT,fill="both",expand=True)

        # Create a button to submit the user input
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_text)
        self.submit_button.pack(side=tk.LEFT)

    # Define a function to be called when the button is clicked
    def submit_text(self):
        user_input = self.text_field.get()
        user_input = self.text_field.selection_get(type="html")
        

class APP:

    def __init__(self) -> None:
        self.width = 400
        self.height = 300
        self.resize_ = False
        self.redrawFlag=False
        self.root = tk.Tk()
        self.root.minsize(200,300)
        self.reader = VLC_Reader()
        self.root.title('noteBook')
        self.root.geometry('{}x{}'.format(self.width,self.height))
        self.data = []
        self.create_widgets()
        self.root.mainloop()
        
    def create_widgets(self):
        self.listArea = ListArea(self.root)
        self.listArea.pack(side="top",fill="both",expand=True)

            # create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", fill="y")

            # create three buttons and add them to the button frame
        self.input = TextEditorFrame()
        self.input.text_event = self.get_text
        self.input.pack(side="left",pady=10)
        button1 = tk.Button(button_frame, text="select vid", padx=10,command=self.reader.data.Getvideo)
        button1.pack(side="left", padx=10)
        button2 = tk.Button(button_frame, text="Play vid", padx=10,command=self.reader.data.play_video)
        button2.pack(side="left", padx=10)
        self.root.bind("<Control-s>", self.take_screen)
        self.root.bind("<Configure>",self.resize)
        #self.root.bind("<ButtonRelease-1>",self.onrelease)
      
    def take_screen(self,event):
        image = self.reader.take_screenshot(event)
        ratio =self.width/ image.width
        self.data.append(image)
        img = image.copy()
        #img = image.resize(((int)(image.width*ratio), (int)(image.height*ratio)), Image.Resampling.LANCZOS)
        self.listArea.render_item(img)
        self.render_items()
    
    def onrelease(self,event):
        if self.resize_ == True:
            #self.render_items()
            self.resize_ = False
        pass
    def speed(self,event):
        if(self.reader.data.player.get_rate()<4):
            self.reader.data.player.set_rate(self.reader.data.player.get_rate()+0.1)
    def slow(self,event):
        if(self.reader.data.player.get_rate()>0):
            self.reader.data.player.set_rate(self.reader.data.player.get_rate()-0.1)
    def resize(self,event):
        if type(event.widget) == type(self.root):
            self.height = event.height
            if(self.width!=event.width-50):
                self.resize_ = False
                self.width = event.width-50
                self.render_items()
    def get_text(self):
        print("User input: ", self.input.user_input)
        self.data.append(self.input.user_input)
        self.listArea.render_item(self.input.user_input,self.input.tags)
        pass    
    def render_items(self):
        #self.listArea.clear_items()
        i=0
        for image in self.data:

            if(isinstance(image, Image.Image)):
                ratio =self.width/ image.width
                image = image.resize(((int)(image.width*ratio), (int)(image.height*ratio)), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(image)
                self.listArea.edit_item(i,img)
            i+=1  
    def save_list(self):
        with open("List.pickle", "wb") as f:
            pickle.dump(self.listArea.list, f)
    def load_list(self):
        with open("my_obj.pickle", "rb") as f:
            self.listArea.list = pickle.load(f)
            self.listArea.restore()

    def resize_images(self):
        for image in self.listArea.list:
            if(isinstance(image, Image.Image)):

                ratio =self.width/ image.width
                image = image.resize(((int)(image.width*ratio), (int)(image.height*ratio)), Image.Resampling.LANCZOS)
                
        self.listArea.render_items()     
     
        pass    
    def show_images(self,key):
        self.reader.take_screenshot(key)
        ''' Show the listed image names along with the images themselves. '''
        self.text.delete('1.0', END)  # Clear current contents.
        self.text.images.clear()
        # Display images in Text widget.
        for image in self.reader.screenshots:

            ratio =self.width/ image.width
            
            img = image.resize(((int)(image.width*ratio), (int)(image.height*ratio)), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            
            self.text.image_create(INSERT, padx=5, pady=5, image=img)
            self.text.images.append(img)  # Keep a reference.
            self.text.insert(INSERT, '\n')


def main():
    app = APP()
    """    reader = VLC_Reader()
    with keyboard.Listener(on_press=reader.on_press) as listener:
        
        root = tk.Tk()
        root.title('Screenshots')
        root.geometry('400x300')

        # create the listbox to display the screenshots
        listbox = tk.Listbox(root)
        reader.listbox=listbox
        listbox.pack(fill=tk.BOTH, expand=True)
        print("   cdwsde",len(reader.screenshots))
        for shot in reader.screenshots:
            print("image")
            listbox.insert(END,"")
            listbox.itemconfig(listbox.size()-1, image=shot)

            pass

        tk.Button(text='Click to Open File', 
        command=reader.data.Getvideo).pack(fill=tk.X)
        tk.Button(text='Play Video', 
        command=reader.data.play_video).pack(fill=tk.X)
        root.bind("<Control-s>", reader.on_press)

        tk.mainloop()
    pass
"""

if __name__=="__main__":
    main()