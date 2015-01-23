#!/usr/bin/env python
from __future__ import print_function

ESOCAND_VERSION='2015.01.23_build001'


def get_list_randomized_from_content(objects_container, random_seed=''):
	import hashlib
	import random
	
	objects_container_aslist = list( objects_container )
	objects_container_aslist.sort()
	
	hasher = hashlib.sha256()
	for element in objects_container_aslist:
		hasher.update( element )
	hasher.update( random_seed )
	
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
		
		label_text_seed       = Tk.Label(master, height=1, relief=Tk.SUNKEN, text="Seed di estrazione")
		label_text_add_name   = Tk.Label(master, height=1, relief=Tk.SUNKEN, text="Nome da aggiungere")
		label_input_namelist  = Tk.Label(master, height=1, relief=Tk.SUNKEN, text="Lista inserita"    )
		label_output_namelist = Tk.Label(master, height=1, relief=Tk.SUNKEN, text="Lista riordinata"  )
		
		scrollbar_input_namelist   = Tk.Scrollbar(master, orient=Tk.VERTICAL)
		scrollbar_output_namelist  = Tk.Scrollbar(master, orient=Tk.VERTICAL)
		
		input_namelist = Tk.Listbox(master, width = 40, height = 30, yscrollcommand=scrollbar_input_namelist.set)
		output_namelist = Tk.Listbox(master, width = 40, height = 30, yscrollcommand=scrollbar_output_namelist.set)
		
		
		# Helpers
		
		def insert_single(to_insert):
			# Strip the newline at the end
			if to_insert[-1] == u'\n':
				to_insert = to_insert[:-1]
			
			# Prevent whitespace from being inserted
			if len(to_insert.strip()) == 0:
				return
			
			already_inserted = input_namelist.get(0, Tk.END)
			
			# Prevent inserting duplicate names
			if to_insert in already_inserted:
				return
			
			import bisect
			ins_pos = bisect.bisect(already_inserted, to_insert)
			print('adding '+repr(to_insert))
			input_namelist.insert(ins_pos, to_insert)
		
		
		def insert_multiple(iterable):
			already_inserted = input_namelist.get(0, Tk.END)
			
			for to_insert in iterable:
				# Strip the newline at the end
				if to_insert[-1] == u'\n':
					to_insert = to_insert[:-1]
				
				# Prevent whitespace from being inserted
				if len(to_insert.strip()) == 0:
					return
				
				# Prevent inserting duplicate names
				if to_insert in already_inserted:
					return
				
				import bisect
				ins_pos = bisect.bisect(already_inserted, to_insert)
				print('adding '+repr(to_insert))
				input_namelist.insert(ins_pos, to_insert)
		
		
		# Button callables
		def insert_from_textbox():
			to_insert = text_add_name.get(1.0, Tk.END)
			insert_single(to_insert)
			text_add_name.delete(1.0, Tk.END)
		
		
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
		
		
		def reset_list():
			input_namelist.delete(0, Tk.END)
		
		
		def shuffle_list():
			already_inserted = input_namelist.get(0, Tk.END)
			seed = text_seed.get(1.0, Tk.END)
			
			if seed[-1] == u'\n':
				seed = seed[:-1]
			
			shuffled_list = get_list_randomized_from_content(already_inserted, random_seed=seed)
			
			output_namelist.delete(0, Tk.END)
			
			for element in shuffled_list:
				output_namelist.insert(Tk.END, element)
			
		
		def write_output_list():
			shuffled_list = output_namelist.get(0, Tk.END)
			
			dialogoptions = {}
			dialogoptions['title'] = 'Scegli il nome del file da salvare'
			f = tkFileDialog.asksaveasfile(mode='w', **dialogoptions)
			
			write_iterable_to_file_line_by_line(shuffled_list, f)
		
		
		
		button_add_names_from_textbox = Tk.Button(master, bg='LightSkyBlue', activebackground='LightSkyBlue', text='Aggiungi nome'          , command=insert_from_textbox)
		button_add_names_from_file    = Tk.Button(master, bg='LightSkyBlue', activebackground='LightSkyBlue', text='Aggiungi nomi da file'  , command=insert_from_file)
		button_reset_list             = Tk.Button(master, bg='orange red'  , activebackground='orange red'  , text='Cancella lista inserita', command=reset_list)
		button_shuffle_list           = Tk.Button(master, bg='yellow'      , activebackground='yellow'      , text='Calcola nuova lista'    , command=shuffle_list)
		button_save_names_to_file     = Tk.Button(master, bg='pale green'  , activebackground='pale green'  , text='Salva nomi in file'     , command=write_output_list)
		
		
		
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
	def __init__(self):
		import Tkinter as Tk
		rootwidget = Tk.Tk()
		app = Gui(master=rootwidget)
		rootwidget.mainloop()

def run_gui():
	a = GuiCore()


run_gui()

a = set(['alfa alfa','beta beta','gamma gamma','delta delta'])
print('unsorted                 : ' + str( repr( a ) ) )
print('sorted                   : ' + str( repr( sorted(a) ) ) )
print('shuffled (default seed)  : ' + str( repr( get_list_randomized_from_content(a) ) ) )
print('shuffled (default seed)  : ' + str( repr( get_list_randomized_from_content(a) ) ) )
print('shuffled (\'gommo\' seed): ' + str( repr( get_list_randomized_from_content(a,'gommo') ) ) )
print('shuffled (\'gommo\' seed): ' + str( repr( get_list_randomized_from_content(a,'gommo') ) ) )


#def get_randomized_list

#if __name__ == "__main__":

