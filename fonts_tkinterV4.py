#!/usr/bin/env python3
#
#  fonts_tkinterV4.py
#  
#  Copyright 2025 Nap0
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  This small application lists all unique font names found
#  using font.families() and lists them. 
#  the list can be filtered by typing a piece of text
#  Clicking a font name allows a sample text to be viewed
#  colors, size ans italic / bold properties can be changed
#  the font name can be cpied to clipboard 

import tkinter as tk
from tkinter import font,colorchooser

class FontViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.nameoffontviewer = "Tkinter font viewer"
        self.title(self.nameoffontviewer)
        self.geometry("1280x760")
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=0)
        self.rowconfigure(3,weight=0)
        self.rowconfigure(4,weight=0)
        
        # ---- Variables --------------------------------------------
        # size of font in label
        self.fontsize = 15   
        # whether the font is normal/bold and italic/roman
        self.fontweightslant = tk.StringVar()
        self.fontweightslant.set("normal")
        # color of font and background
        self.displaycolor="black"
        self.backgroundcolor="white"
        
        # ---- Widgets --------------------------------------------------------------
        # label to view selected font
        self.labeltext = tk.StringVar()
        self.labeltext.set("Click font name")
        self.labelfonts = tk.Label(self, textvariable=self.labeltext)
        self.labelfonts.grid(row=0, column=1, rowspan=2, sticky="WENS")
        
        # frame for filter
        self.framefilter = tk.Frame(self)
        self.framefilter.grid(row=0, column=0, sticky="EW")
        
        # controls for filter
        self.buttonclearfilter = tk.Button(self.framefilter,
            text="Clear filter", command = lambda: self.filter(clear=True) )
        self.buttonclearfilter.grid(row=0, column=0)
        self.filterstring = tk.StringVar()
        self.entryfilter = tk.Entry(self.framefilter, width = 15, 
            textvariable = self.filterstring)
        self.entryfilter.grid(row=0, column=1, sticky="EW")
        self.buttonfilter = tk.Button(self.framefilter,
            text="Filter", command = self.filter)
        self.buttonfilter.grid(row=0, column=2)
        
        #frame for listbox with font names and scrollbar
        self.framelistbox = tk.Frame(self)        
        self.framelistbox.grid(row=1, column=0, sticky="NEWS")
        self.framelistbox.rowconfigure(0,weight=1)
        self.framelistbox.columnconfigure(0,weight=1)
        self.framelistbox.columnconfigure(1,weight=0)
        
        # listbox with font names
        self.listboxfonts = tk.Listbox(self.framelistbox)
        self.listboxfonts.grid(row=0, column=0, sticky="NEWS")
        
        # scrollbar for listbox
        self.scrollbarlistbox = tk.Scrollbar(self.framelistbox)
        self.scrollbarlistbox.grid(row=0, column=1, sticky="NS")
        
        # listbox gets method of scrollbar assigned to it's yscollcommand 
        self.listboxfonts.config(yscrollcommand = self.scrollbarlistbox.set)
        
        # scrollbar gets event handler
        self.scrollbarlistbox.config(command = self.listboxfonts.yview) 
        
        # assign listboxselect to event for listbox
        self.listboxfonts.bind('<<ListboxSelect>>', self.listboxselect)
        
        # frame for controls
        self.framecontrols = tk.Frame(self)
        self.framecontrols.grid(row=2, column=0, columnspan=2, sticky="WENS")
        
        # frame to stack buttons
        self.framebuttons = tk.Frame(self.framecontrols)
        self.framebuttons.grid(row=0, column=0, sticky="WES", padx=10)
        
        # button to copy font name to clipboard
        self.buttoncopyname = tk.Button(self.framebuttons, text = "Copy Font Name", 
            command = self.copyname)
        self.buttoncopyname.grid(row=0, column=0, sticky="NEWS") 
        
        # button to set font color
        self.buttonfontcolor = tk.Button(self.framebuttons, text = "Set font color", 
            command = self.setdisplaycolor)
        self.buttonfontcolor.grid(row=1, column=0, sticky="NEWS") 
        
        # button to set background color
        self.buttonbackgroundcolor = tk.Button(self.framebuttons, text = "Set background color", 
            command = self.setbackgroundcolor)
        self.buttonbackgroundcolor.grid(row=2, column=0, sticky="NEWS") 
        
        # scale to set font size       
        self.scalefontsize = tk.Scale(self.framecontrols, from_=5, to=50, orient = tk.HORIZONTAL,
            label="Font size", length=200, tickinterval=10, resolution=1,
            command= self.changefontsize)
        self.scalefontsize.set(self.fontsize)
        self.scalefontsize.grid(row=0, column=1, padx=10) 
        
        # frame to group radiobuttons
        self.frameradiobuttons = tk.Frame(self.framecontrols)
        self.frameradiobuttons.grid(row=0, column=2, padx=10)
        
        # radiobuttons to select normal / bold / italic
        self.radiobuttonfntnormal = tk.Radiobutton(self.frameradiobuttons, text="Normal", 
            value="normal", variable=self.fontweightslant, command=self.changefontweightslant)
        self.radiobuttonfntnormal.grid(row=0,column=0, sticky="W")
        self.radiobuttonfntbold = tk.Radiobutton(self.frameradiobuttons, text="Bold", 
            value="bold", variable=self.fontweightslant, command=self.changefontweightslant)
        self.radiobuttonfntbold.grid(row=1,column=0, sticky="W")
        self.radiobuttonfntitalic = tk.Radiobutton(self.frameradiobuttons, text="Italic", 
            value="normal italic", variable=self.fontweightslant, command=self.changefontweightslant)
        self.radiobuttonfntitalic.grid(row=2,column=0, sticky="W")
        self.radiobuttonfntbolditalic = tk.Radiobutton(self.frameradiobuttons, text="Bold Italic", 
            value="bold italic", variable=self.fontweightslant, command=self.changefontweightslant)
        self.radiobuttonfntbolditalic.grid(row=3,column=0, sticky="W")
        
        # status label
        self.statustext = tk.StringVar()
        self.labelstatus = tk.Label(self, textvariable = self.statustext, anchor="w")
        self.labelstatus.grid(row=3, column=0, columnspan=2, sticky="EW")    
        
        # --- initialisation -------------------------------------------
        
        # generate alphanumeric characters for label
        self.generatecharacters()
        
        # fill listbox wth font names
        self.filllistbox()
       
        # characters in label
        self.updatelabel(self.listboxfonts.get(0)) 
        
        # update status
        self.updatestatus()
        
        # maximize window on linux machine
        #self.wm_attributes('-zoomed', True)
        
    # generate a string with the sample text for viewing a font    
    def generatecharacters(self):
        
        # generator comprehension for capital letters A..Z
        charactergen = ( chr(a) for a in range(65,91) )
        
        # use generator to make string
        self.characters = "".join( charactergen )
        
        # add lower case letters
        self.characters += "\n" + self.characters.lower()
        
        # generator for numbers 0..9 used to add numbers
        # to string
        charactergen = ( str(a) for a in range(0,10) )
        self.characters += "\n" + "".join( charactergen )
        self.characters += "\n  + - * / . , ; :"
        
    
    # sort the font names, remove duplicates and optionally apply filter
    def sortandfilter(self, listofstrings, filtertxt = ""):
        
        # convert to set to remove duplicates
        setofstrings = set( listofstrings )
        
        # the key fuction str.casefold lets sorted() sort on lower case strings
        # to sort string purely alphabetically taking not into account whether
        # they start with a capital or small character
        # the strings in the set remain unchanged, sorted() returns a list
        listofstrings = sorted( setofstrings, key=str.casefold )
        
        # define function for use with the filter() statement
        # it returns True if it finds filtertxt in the given string txt
        # works case-insensitive
        def comparetxt(txt):
            return filtertxt.casefold() in txt.casefold()            
        
        # apply filter if filter exists
        # the Python function filter() applies function comparetxt 
        # to all elements in listofstrings, it only retains the elements
        # for which function comparetxt returns True
        if filtertxt != "":
            newlist = list( filter(comparetxt, listofstrings) )
            return newlist
        else:
            return listofstrings
    
    # get font names and add sorted, filtered list to listbox
    def filllistbox(self):
        
        # font.families() gives a tuple of strings with the font names
        # convert to set to remove duplicates
        self.setfontnames = set( font.families() )
        
        # the key function str.casefold makes sorted() sort on lower case strings
        # to sort strings starting with lower or upper case letters purely alfabetically
        # strings in result remain unchanged 
        self.setfontnames = sorted( self.setfontnames, key=str.casefold )
        
        # get text for filter if any
        filtertxt = self.filterstring.get()
        filtertxt = filtertxt.casefold()
        
        # apply filter if filter exists
        self.setfontnames = self.sortandfilter(self.setfontnames, filtertxt) 
        
        # clear listbox
        self.listboxfonts.delete(0, tk.END)   
        
        # add fontnames to list
        for fontname in self.setfontnames:            
            self.listboxfonts.insert(tk.END, fontname) 
        
        # select first element in listbox
        if self.listboxfonts.size() > 0:
            self.listboxfonts.select_set(0)

            
    # event handler when listbox item is selected    
    def listboxselect(self, anevent):
        
        # anevent is an event object thewidget is here the listbox
        thewidget = anevent.widget
        
        # continue if listbox has items
        if (thewidget.size() > 0):
            
            # get index of selected item
            if len(thewidget.curselection()) > 0:
                index = int(thewidget.curselection()[0])
                
                # get fontname with index
                value = thewidget.get(index)
                
                # use font for label
                self.updatelabel(value)
                
                # update status
                self.updatestatus()
        
    # returns fontname currently selected in listbox    
    def getselectedfontname(self):
        if self.listboxfonts.size() > 0:
            index = self.listboxfonts.curselection()[0]
            fontname = self.listboxfonts.get( index )
        else:
            fontname = ""
        return(fontname)
        

    # change font of label to fontname   
    def updatelabel(self, fontname):
        if fontname == "":
            self.labeltext.set( "" )
        else:
            self.labeltext.set( self.characters )
            self.labelfonts.config( font = (fontname, self.fontsize, self.fontweightslant.get()) )
            self.labelfonts.config( foreground = self.displaycolor, background = self.backgroundcolor )
        self.updatestatus()
        
    # update the status line        
    def updatestatus(self):
        if self.listboxfonts.size() > 0:
            fontname = self.getselectedfontname()
            # update status label
            status = f"{self.listboxfonts.size()} fonts found,  "
            status += f"font selected: {fontname},  "
            status += f"font size = {self.fontsize},  "
            status += f"{self.fontweightslant.get()},  "
            status += f"font color = {self.displaycolor},  "
            status += f"background color = {self.backgroundcolor}"
            self.statustext.set(status)
        else:
            status = f"{self.listboxfonts.size()} fonts found,  "
        self.statustext.set(status)

        
     # copy fontname to clipboard   
    def copyname(self):
        fontname = self.getselectedfontname()        
        self.clipboard_clear()
        self.clipboard_append(fontname)
        
        
    # change the size of the label's font    
    def changefontsize(self, value):
        self.fontsize = int(value)
        fontname = self.getselectedfontname()        
        self.updatelabel( fontname )
        
        # update status
        self.updatestatus()
        
    # change font properties: italic, bold  
    def changefontweightslant(self):
        fontname = self.getselectedfontname()        
        self.updatelabel( fontname )
        
        # update status
        self.updatestatus()
        
        
    # change color of font using colorchooser dialogbox    
    def setdisplaycolor(self):
        answer=colorchooser.askcolor(self.displaycolor)
        if not(answer[1] is None):
            self.displaycolor=answer[1]
            fontname = self.getselectedfontname()   
            self.updatelabel( fontname )
            
            # update status
            self.updatestatus()
            
            
    # change color of background using colorchooser dialogbox    
    def setbackgroundcolor(self):
        answer=colorchooser.askcolor(self.backgroundcolor)
        if not(answer[1] is None):
            self.backgroundcolor=answer[1]
            fontname = self.getselectedfontname()   
            self.updatelabel( fontname )
            
            # update status
            self.updatestatus()
            
            
    # clear filter update listbox, label and statusline     
    def filter(self, clear=False):
        if clear:
            self.filterstring.set("")
        self.filllistbox()
        self.updatelabel(self.listboxfonts.get(0)) 
        self.updatestatus()


        
        
        

toepassing=FontViewer()
toepassing.mainloop()
