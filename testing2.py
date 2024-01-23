from nltk.corpus import words
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re
from textblob import TextBlob
from spellchecker import SpellChecker
import customtkinter
import Levenshtein 
from tkinter import ttk
    
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
                               wrap="word",border_spacing=20,font=("Arial",14))
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=20, pady=50)
        self.textbox.insert("0.0", "")
        self.textbox.bind("<KeyRelease>",self.check)

        self.lableCount = customtkinter.CTkLabel(self,text="Word Count: 0")
        self.lableCount.grid(row=2, column=0,pady=10)  
        
        self.button = customtkinter.CTkButton(self, text="Show Candidates",
                                            command=self.show_candidate_event, 
                                            width=35, 
                                            height=20,
                                            border_width=10,
                                            border_color="hotpink3",
                                            fg_color="hotpink3",
                                            hover_color="hotpink3")  
        self.button.grid(row=1, column=0,padx=0,pady=0)

        # Configure the style for the Listbox
        self.style = ttk.Style()
        self.listbox = tk.Listbox(self, 
                                  selectmode=tk.SINGLE,
                                  activestyle="none",
                                  selectbackground="pink",
                                  selectforeground="black",
                                  background="#2E2E2E",
                                  foreground="white",
                                  font=("Helvetica", 12),
                                  borderwidth=0, 
                                  highlightthickness=20,
                                  highlightbackground="#2E2E2E",
                                  highlightcolor="#2E2E2E")
        self.listbox.grid(row=0, column=1,rowspan=3, padx=20, pady=20, sticky="nsew")


    def select_candidate_event(self,t):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_candidate = self.listbox.get(selected_index)
            candidate_without_distance = re.sub(r'\(Edit Distance: \d+\)', '', selected_candidate)
            self.textbox.delete(self.selection_indices[0], self.selection_indices[1])
            self.textbox.insert(self.selection_indices[0], candidate_without_distance.strip())
            self.listbox.delete(0,tk.END)
    
    # global variable - to store selected text's start and end indices
    selection_indices = []

    def show_candidate_event(self):
        # error if no selected words
        self.listbox.delete(0, tk.END)
        print("button pressed")
        self.selection_indices = []
        try:
            # to get highlight cursor text and its start and end indices
            self.selection_indices = self.textbox.index(tk.SEL_FIRST), self.textbox.index(tk.SEL_LAST)
            selected_word = self.textbox.get(self.selection_indices[0],self.selection_indices[1])

            #limit to the incorrect word only (added 'clickable' tag)
            tags_at_cursor = self.textbox.tag_names(self.selection_indices[0])
            
            if "clickable" in tags_at_cursor:
                print("clickable: ",self.textbox.tag_names(self.selection_indices[0]))
                print("Clickable tag is present at the cursor position")
                candidate_list = self.find_top_k_nearest_words(selected_word,words.words(),10)
                for candidate, distance in candidate_list:
                    list_label = f"{candidate} (Edit Distance: {distance})"
                    self.listbox.insert(tk.END,list_label)
            self.listbox.bind("<Double-1>", self.select_candidate_event)
        except:
            print("No word selected")
        

    def find_top_k_nearest_words(self,query_input, words_list, k): 
            distances = [] 
            for word in words_list: 
                distance = Levenshtein.distance(query_input, word) 
                distances.append((word, distance))
            sorted_distances = sorted(distances, key=lambda x: x[1]) 
            print("Distances: ",[d for d in sorted_distances[:k]])
            return [d for d in sorted_distances[:k]] 
    
        
    def check(self,event):
        # Character Count
        self.lableCount.configure(text = "Character Count: " + str(len(self.textbox.get("1.0", "end-1c"))))
        
        spell = SpellChecker()
        
        content = self.textbox.get("1.0",tk.END) #1.0 the first char, 1.1 the second..
        space_count = content.count(" ")
        
        if space_count != self.old_spaces:
            self.old_spaces = space_count
            
            for tag in self.textbox.tag_names():
                self.textbox.tag_delete(tag)

            for word in content.split(" "):
                # check if character not in the corpus amd not spaces
                if re.sub(r"[^\w]","",word.lower()) not in words.words() and not word.isspace():
                    position = content.find(word)
                    self.textbox.tag_add(word, f"1.{position}",f"1.{position+len(word)}")
                    new_start = "1." + str(position)
                    new_end = "1." + str(position+len(word))
                    print(f"1.{position}",f"1.{position+len(word)}")
                    self.textbox.tag_add("clickable",float(new_start), float(new_end))

                    print("Original word: ", word)
                    print("Correction:", spell.correction(word))
                    print(spell.candidates(word))
                    self.textbox.tag_config(word, foreground="red")
    
if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()

