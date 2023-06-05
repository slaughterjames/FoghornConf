#! /usr/bin/env python3

'''
FoghornConf v0.1 - Copyright 2023 James Slaughter,
This file is part of Foghorn v0.1.

FoghornConf v0.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FoghornConf v0.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FoghornConf v0.1.  If not, see <http://www.gnu.org/licenses/>.
'''

#python import
import sys
import os
import argparse
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd 

#programmer generated imports
from controller import controller

'''
JsonHandler
Class: This class is responsible for the initial handling of JSON data
'''
class JsonHandler:
    '''
    __init__()
    Function: init function for the MainWindow class
    '''    
    def __init__(self, json_file):
        self.json_file = json_file

    '''
    load_json()
    Function: Loads our JSON file
    '''
    def load_json(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    '''
    save_json()
    Function: Saves our JSON file
    '''
    def save_json(self, data):
        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=4)

'''
MainWindow
Class: This class is responsible for drawing the initial window and populating it
'''
class MainWindow:
    '''
    __init__()
    Function: init function for the MainWindow class
    '''
    def __init__(self, root, json_file, jsonhandler):
        self.root = root
        self.jsonhandler = jsonhandler
        self.json_data = self.jsonhandler.load_json()
        self.root.title('FoghornConf')
        self.create_gui()

    '''
    create_gui()
    Function: Draws the initial window and populates it
    '''
    def create_gui(self):
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(fill='both', expand=True)
        self.text_widget.insert('1.0', json.dumps(self.json_data, indent=4))
        #self.save_button = tk.Button(self.root, text="Save JSON", command=self.save_json)
        #self.save_button.pack(pady=10)
        self.addins_button = tk.Button(self.root, text="View Addins", command=self.view_addins)
        self.addins_button.pack(pady=10)

    #def save_json(self):
    #    try:
    #        updated_data = json.loads(self.text_widget.get('1.0', 'end-1c'))
    #        self.jsonhandler.save_json(updated_data)
    #        messagebox.showinfo("Success", "JSON Saved Successfully")
    #    except json.JSONDecodeError:
    #        messagebox.showerror("Error", "Invalid JSON")

    #    if not json_file or not updated_data:
    #        messagebox.showwarning('Save Error', 'No configuration file loaded!')
    #        return

    #    with open(self.json_file, 'w') as file:
    #        json.dump(updated_data, file, indent=4)

    #    messagebox.showinfo('Saved JSON', 'JSON configuration file saved successfully!')            
    
    '''
    view_addins()
    Function: Display the addins section of the Foghorn Conf file
    '''    
    def view_addins(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title('Addins')
        self.new_window.geometry("400x700")
        self.listbox = tk.Listbox(self.new_window)
        self.listbox.configure(height=30,width=0)
        for addin in self.json_data['addins']:
            self.listbox.insert(tk.END, addin)
        self.listbox.pack()

        delete_button = tk.Button(self.new_window, text="Delete Addin", command=self.delete_addin)
        delete_button.pack(pady=10)
        
        save_button = tk.Button(self.new_window, text="Save JSON", command=self.save_json_from_addins)
        save_button.pack(pady=10)

        insert_button = tk.Button(self.new_window, text="Insert Addin", command=self.insert_addin)
        insert_button.pack(pady=10)    

    '''
    delete_addin()
    Function: Code executed by the delete_button in view_addins
    '''
    def delete_addin(self):
        confirm = messagebox.askokcancel('Confirmation', 'Are you sure you want to delete this addin?')
        if confirm:
            index = self.listbox.curselection() 
            del self.json_data['addins'][index[0]]
            self.listbox.delete(index)

    '''
    save_json_from_addins()
    Function: Code executed by the save_button in view_addins
    '''
    def save_json_from_addins(self):
        self.jsonhandler.save_json(self.json_data)
        messagebox.showinfo("Success", "JSON Saved Successfully")

        # Close the add addin window
        self.new_window.destroy()

    '''
    insert_addin()
    Function: Code executed by the insert_button in view_addins
    '''
    def insert_addin(self):
        self.insert_window = tk.Toplevel(self.root)
        self.insert_window.title('Insert Addin')
        
        self.insert_entry = tk.Entry(self.insert_window)
        self.insert_entry.pack(pady=10)
                
        confirm_button = tk.Button(self.insert_window, text="Insert", command=self.confirm_insert)
        confirm_button.pack(pady=10)

    '''
    confirm_insert()
    Function: Code executed by the confirm_button in insert_addin()
    '''
    def confirm_insert(self):
        new_addin = self.insert_entry.get()
        if not new_addin:
            messagebox.showwarning('Insert Error', 'No addin entered!')
            return        
        new_addin_dict = {"vt": new_addin}

        try:            
            self.json_data['addins'].append(new_addin_dict)
            self.listbox.insert(tk.END, new_addin_dict)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON")

        # Close the add addin window
        self.insert_window.destroy()            

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    print ('Usage: [required] [optional] --debug --usage --help')
    print ('Example: ./foghornconf.py --debug')
    print ('Required Arguments:')
    print ('Optional Arguments:')
    print ('--debug - Prints verbose logging to the screen to troubleshoot issues.')    
    print ('--usage - You\'re looking at it!')
    sys.exit(-1)

'''
parse_args() - Parses program arguments
'''
def parse_args():
    parser = argparse.ArgumentParser(description='Process some program arguments.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    parser.add_argument('--usage', action='store_true', help='Display program usage.')

    args = parser.parse_args()

    if args.debug:
        CON.debug = True
        print('debug: ', CON.debug)

    if args.usage:
        Usage()        

    return args

'''
This is the mainline section of the program and makes calls to the 
various other sections of the code
'''
if __name__ == "__main__":
    json_file = fd.askopenfilename(filetypes=[('CONF Files', '*.conf'),('JSON Files', '*.json')])
    if json_file:
        root = tk.Tk()
        jsonhandler = JsonHandler(json_file)
        MainWindow(root, json_file, jsonhandler)
        root.mainloop()
    else:
        print("No file selected.")