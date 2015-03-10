# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#!/usr/bin/env python
from __future__ import print_function

ESOCAND_VERSION='0.1 beta'


def get_list_randomized_from_content(objects_container, random_seed=u''):
	import hashlib
	import random
	
	objects_container_aslist = list( objects_container )
	objects_container_aslist.sort()
	
	hasher = hashlib.sha256()
	for element in objects_container_aslist:
		hasher.update( element.encode('utf-8') )
	hasher.update( random_seed.encode('utf-8') )
	
	random.seed( hasher.hexdigest() )
	
	return random.sample( objects_container_aslist, len( objects_container_aslist ) )


def get_list_from_file_line_by_line(f):
	names = []
	for line in f:
		names.append(line)
	return names

def write_iterable_to_file_line_by_line(iterable, f):
	for line in iterable:
		print_function(line, file=f)


import Tkinter as Tk

class Gui(Tk.Frame):
	def __init__(self, master=None):
		import Tkconstants as Tkc
		import tkFileDialog
		
		Tk.Frame.__init__(self, master)
		
		def noop():
			pass
		
		
		self.grid()
		self.master.title("ESOCAND - Estrazione a SOrte dei CANdidati, ver. " + ESOCAND_VERSION)
		
		text_seed                     = Tk.Text(master, height=1, width=30, bg='white')
		text_add_name                 = Tk.Text(master, height=1, width=30, bg='white')
		
		separator_col0_0 = Tk.Frame(master, height= 1, bd=1, relief=Tk.FLAT )
		separator_col0_1 = Tk.Frame(master, height= 1, bd=1, relief=Tk.FLAT )
		separator_col0_2 = Tk.Frame(master, height= 1, bd=1, relief=Tk.FLAT )
		separator_col0_3 = Tk.Frame(master, height= 1, bd=1, relief=Tk.FLAT )
		
		separator_vert_1 = Tk.Frame(master, width=10, bd=1, relief=Tk.FLAT)
		separator_vert_2 = Tk.Frame(master, width=10, bd=1, relief=Tk.FLAT)
		
		buffer_label_input_namelist  = Tk.StringVar()
		buffer_label_output_namelist = Tk.StringVar()
		
		buffer_label_input_namelist .set("Lista inserita"  )
		buffer_label_output_namelist.set("Lista riordinata")
		
		label_text_seed       = Tk.Label(master, height=1, relief=Tk.SUNKEN, text="Seed di estrazione")
		label_text_add_name   = Tk.Label(master, height=1, relief=Tk.SUNKEN, text="Nomi da aggiungere (1 per linea)")
		label_input_namelist  = Tk.Label(master, height=1, relief=Tk.SUNKEN, textvariable=buffer_label_input_namelist   )
		label_output_namelist = Tk.Label(master, height=1, relief=Tk.SUNKEN, textvariable=buffer_label_output_namelist  )
		
		scrollbar_input_namelist   = Tk.Scrollbar(master, orient=Tk.VERTICAL)
		scrollbar_output_namelist  = Tk.Scrollbar(master, orient=Tk.VERTICAL)
		
		input_namelist = Tk.Listbox(master, width = 40, height = 30, yscrollcommand=scrollbar_input_namelist.set)
		output_namelist = Tk.Listbox(master, width = 40, height = 30, yscrollcommand=scrollbar_output_namelist.set)
		
		
		# Helpers
		def parse_multiline(multiline_text):
			return multiline_text.split(u'\n')
		
		def strip_newlines(mystring):
			import os
			if mystring[-1] == u'\n':
				return mystring[:-1]
			else:
				return mystring
		
		def name_is_valid(mystring):
			# Prevent whitespace from being inserted
			if len(mystring) == 0 or len(mystring.strip()) == 0:
				return False
			
			# String survived cuts
			return True
		
		def filter_invalid_names(iterable):
			return [ strip_newlines(s) for s in iterable if name_is_valid(s) ]
		
		def insert_multiple(iterable):
			import os
			import heapq
			
			already_inserted = list( input_namelist.get(0, Tk.END) )
			input_namelist.delete(0, Tk.END)
			
			merged_list = sorted( list( set( already_inserted + filter_invalid_names(iterable) ) ) )
			
			print('Merged list content follows:')
			print(repr(merged_list))
			
			for to_insert in merged_list:
				input_namelist.insert(Tk.END, to_insert)
		
		
		def update_label_input_namelist():
			buffer_label_input_namelist .set('Lista inserita ('   + str(input_namelist .size()) + ' elementi)' )
			
		def update_label_output_namelist():
			buffer_label_output_namelist.set('Lista riordinata (' + str(output_namelist.size()) + ' elementi)' )
		
		
		
		
		
		# Button callables
		def insert_from_textbox():
			to_insert = text_add_name.get(1.0, Tk.END)
			insert_multiple( parse_multiline(to_insert) )
			text_add_name.delete(1.0, Tk.END)
			update_label_input_namelist()
		
		
		def insert_from_file():
			dialogoptions = {}
			dialogoptions['title'] = 'Scegli un file da aprire'
			f = tkFileDialog.askopenfile(mode='r', **dialogoptions)
			
			names = get_list_from_file_line_by_line(f)
			names_set = set(names)
			
			if len(names_set) != len(names):
				print('Warning: there are duplicate names in the file you provided, discarding duplicates')
			
			names = list(names_set)
			
			insert_multiple(names)
			update_label_input_namelist()
		
		
		def reset_list():
			input_namelist.delete(0, Tk.END)
			update_label_input_namelist()
		
		
		def shuffle_list():
			already_inserted = input_namelist.get(0, Tk.END)
			seed = text_seed.get(1.0, Tk.END)
			
			if seed[-1] == u'\n':
				seed = seed[:-1]
			
			shuffled_list = get_list_randomized_from_content(already_inserted, random_seed=seed)
			
			output_namelist.delete(0, Tk.END)
			
			for element in shuffled_list:
				output_namelist.insert(Tk.END, element)
			update_label_output_namelist()
			
		
		def write_output_list():
			shuffled_list = output_namelist.get(0, Tk.END)
			
			dialogoptions = {}
			dialogoptions['title'] = 'Scegli il nome del file da salvare'
			f = tkFileDialog.asksaveasfile(mode='w', **dialogoptions)
			
			write_iterable_to_file_line_by_line(shuffled_list, f)
		
		
		
		button_add_names_from_textbox = Tk.Button(master, bg='LightSkyBlue', activebackground='LightSkyBlue', text='Aggiungi nomi'          , command=insert_from_textbox)
		button_add_names_from_file    = Tk.Button(master, bg='LightSkyBlue', activebackground='LightSkyBlue', text='Aggiungi nomi da file'  , command=insert_from_file)
		button_reset_list             = Tk.Button(master, bg='orange red'  , activebackground='orange red'  , text='Cancella lista inserita', command=reset_list)
		button_shuffle_list           = Tk.Button(master, bg='yellow'      , activebackground='yellow'      , text='Calcola nuova lista'    , command=shuffle_list)
		button_save_names_to_file     = Tk.Button(master, bg='pale green'  , activebackground='pale green'  , text='Salva nomi in file (1 per linea)'     , command=write_output_list)
		
		
		
		scrollbar_input_namelist .config( command = input_namelist .yview )
		scrollbar_output_namelist.config( command = output_namelist.yview )
		
		
		
		separator_col0_0             .grid(row =  0, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		label_text_seed              .grid(row =  1, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S, ipadx=0, ipady=0)
		text_seed                    .grid(row =  2, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S, ipadx=0, ipady=0)
		
		separator_col0_1             .grid(row =  3, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		label_text_add_name          .grid(row =  4, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		text_add_name                .grid(row =  5, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		button_add_names_from_textbox.grid(row =  6, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		separator_col0_2             .grid(row =  7, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		button_add_names_from_file    .grid(row =  8, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		separator_col0_3             .grid(row =  9, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		button_shuffle_list          .grid(row = 10, column = 0, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		
		
		
		separator_vert_1             .grid(row =  0, column = 1, rowspan = 11, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		label_input_namelist         .grid(row =  0, column = 2, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		input_namelist               .grid(row =  1, column = 2, rowspan = 10, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		button_reset_list            .grid(row = 11, column = 2, rowspan =  2, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		scrollbar_input_namelist     .grid(row =  1, column = 3, rowspan = 10, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		separator_vert_2             .grid(row =  0, column = 4, rowspan = 11, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		label_output_namelist        .grid(row =  0, column = 5, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		output_namelist              .grid(row =  1, column = 5, rowspan = 10, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		button_save_names_to_file     .grid(row = 11, column = 5, rowspan =  1, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		scrollbar_output_namelist    .grid(row =  1, column = 6, rowspan = 11, columnspan = 1, sticky = Tk.W+Tk.E+Tk.N+Tk.S)
		
		

class GuiCore:
	def poll(self):
		self.root.after(1000, self.poll)
	
	def quit_KeyboardInterrupt(event):
		self.root.quit()
		raise KeyboardInterrupt()
	
	def __init__(self):
		import Tkinter as Tk
		self.root = Tk.Tk()
		self.root.bind('<Control-c>', self.quit_KeyboardInterrupt)
		self.app = Gui(master=self.root)
		self.poll()
		self.root.mainloop()

def run_gui():
	a = GuiCore()


# If executed as main
if __name__ == "__main__":
	run_gui()

