from nltk.corpus import words
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re
from textblob import TextBlob
from spellchecker import SpellChecker
import customtkinter
import Levenshtein 
from tkinter import ttk
    
class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []
        
class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        self.title("CTk example")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.old_spaces = 0
        
        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.configure(width=400, height=100, corner_radius=0,
                               wrap="word",border_spacing=20,font=("Arial",14),text_color = "white")
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=20, pady=50)
        self.textbox.insert("0.0", "")
        self.textbox.bind("<KeyRelease>",self.check)
        # If want to add new binding events, put add='+', if not it will replaced by it
        # self.textbox.bind('<Double-1>',self.double_click, add='+') 
        
        self.lableCount = customtkinter.CTkLabel(self,text="Word Count: 0")
        self.lableCount.grid(row=2, column=0)  
        
        self.button = customtkinter.CTkButton(self, text="Show Candidates", command=self.show_candidate_event, width=35, height=20)  
        self.button.grid(row=1, column=0)

        # self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=300, command=self.label_button_frame_event, corner_radius=0)
        # self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        # self.scrollable_label_button_frame.grid(row=0, column=1)

        # Create a themed style
        self.style = ttk.Style()

        # Configure the style for the Listbox
        self.style.configure("DarkListbox.TListbox", background="#2E2E2E", foreground="white", selectbackground="white", selectforeground="white")
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE,background="#2E2E2E",foreground="white")
        self.listbox.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

    def select_candidate_event(self,t):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index)
            print(f"Listbox item clicked: {selected_text}")

    def show_candidate_event(self):
    
        # error if no selected words
        self.listbox.delete(0, tk.END)
        print("button pressed")

        try:
            # to get highlight cursor text
            selection_indices = self.textbox.index(tk.SEL_FIRST), self.textbox.index(tk.SEL_LAST)
            print("Selection indices:", selection_indices)
            selected_word = self.textbox.get(selection_indices[0],selection_indices[1])
            print("Selection word:", selected_word)
            #limit to the incorrect word only (added 'clickable' tag)
            tags_at_cursor = self.textbox.tag_names(selection_indices[0])
            if "clickable" in tags_at_cursor:
                print("Clickable tag is present at the cursor position")
                candidate_list = self.find_top_k_nearest_words(selected_word,words.words(),5)
                for candidate in candidate_list:
                    self.listbox.insert(tk.END,candidate)
                
                
            self.listbox.bind("<ButtonRelease-1>", self.select_candidate_event)
        except:
            print("No word selected")
        
            
    def label_button_frame_event(self, item):
        print(f"label button frame clicked: {item}")

    def find_top_k_nearest_words(self,query_input, words_list, k): 
            distances = [] 
            for word in words_list: 
                distance = Levenshtein.distance(query_input, word) 
                distances.append((word, distance)) 
            sorted_distances = sorted(distances, key=lambda x: x[1]) 
            return [d[0] for d in sorted_distances[:k]] 
    
    def find_all_indices(self, main_string, substring):
        indices = []
        index = main_string.find(substring)

        while index != -1:
            indices.append(index)
            index = main_string.find(substring, index + 1)

        return indices
    
    
    
    #TODO: Fix the bugggg, If applied the find all index, When manual fix the typo, other typo cannot generate candidate. 
    
    
    def check(self,event):
        #content = self.textbox.get("1.0",tk.END) #1.0 the first char, 1.1 the second..
        content = self.textbox.get("1.0","end-1c") #1.0 the first char, 1.1 the second..
        wordCount = re.findall(r'\b\w+\b', content) 
    
        # Character Count + Word Count
        self.lableCount.configure(text = "Character Count: " + str(len(content)) + "\n" + "Word Count: " + str(len(wordCount)))
        
        spell = SpellChecker()
        space_count = content.count(" ")
        
        if space_count != self.old_spaces:
            self.old_spaces = space_count
            
            for tag in self.textbox.tag_names():
                print("tag :", tag)
                self.textbox.tag_delete(tag)


        # Non-word Errors Detection : 
        # Check whether word is in the corpus.
        
        # Real-Word Errors Detection:
        # The word is in the corpus, but wrong context. I.e. :
        # Typo : Three - There
        


            for word in content.split(" "):
                print(re.sub(r"[^\w]","",word.lower()))
                if re.sub(r"[^\w]","",word.lower()) not in words.words() and not word.isspace():# check is character and not in the corpus
                    # position = self.find_all_indices(content,word)
                    # print(position)
                    # for index in position:
                    position = content.find(word)
                    self.textbox.tag_add(word, f"1.{position}",f"1.{position+len(word)}")
                    self.textbox.tag_config(word, foreground="red")
                    
                    new_start = "1." + str(position)
                    new_end = "1." + str(position+len(word))
                    print(f"1.{position}",f"1.{position+len(word)}")
                    self.textbox.tag_add("clickable",float(new_start), float(new_end))

                        # print("Original word: ", word)
                        # print("Correction:", spell.correction(word))
                        # print(spell.candidates(word))

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
    

    # def check(self,event):
    #     spell = SpellChecker()
    #     content = self.textbox.get("1.0",tk.END) #1.0 the first char, 1.1 the second..
    #     space_count = content.count(" ")
        
    #     if space_count != self.old_spaces:
    #         self.old_spaces = space_count # old_spaces = 1
            
    #         for tag in self.textbox.tag_names():
    #             self.textbox.tag_delete(tag)
            
    #         for word in content.split(" "):
                
    #             if re.sub(r'\b\w+\b',"",word.lower()) not in words.words(): # check is character
    #                 position = content.find(word)
    #                 self.textbox.tag_add(word, f"1.{position}",f"1.{position+len(word)}")
    #                 self.textbox.tag_config(word, foreground="red")
    #                 print("Original word: ", word)
                    
    #                 correction_list = spell.correction(word)
    #                 print("Correction:", correction_list)
    #                 print(spell.candidates(word))
    #                 # for correction in correction_list:
    #                     # self.scrollable_label_button_frame.add_item(correction)
                        


# window.text = ScrolledText(window, font =("Arial",14))
# window.text.bind("<KeyRelease>",window.check)
# window.text.pack()
# window.old_spaces = 0
# window.mainloop()

# SpellingCheck()