#Import time for sleeping during text change
import time
#Import tkinter for ui
from tkinter import *
#Import random for temporary file name setting
from random import *
#Import themed tk for the file menu
from tkinter import ttk
#Import file dialog for file opening
from tkinter.filedialog import askopenfilename, asksaveasfilename
#Import standard python utils
import sys, os, datetime, random
#Import the status bar
from utils.statusbar import StatusBar

class Application:

	def __init__(self, title, path=None, show_tabs=True, key_down=None, key_up=None):
		self.__temp_dir = os.path.expanduser("~") + "/TempDir"

		self.__title = title
		self.__app = Tk()
		self.__app.title(self.__title)
		if(key_down is None):
			self.__app.bind("<KeyPress>", self.on_key_down)
		else:
			self.__app.bind("<KeyPress>", key_down)
		if(key_up is None):
			self.__app.bind("<KeyRelease>", self.on_key_up)
		else:
			self.__app.bind("<KeyRelease>", key_up)
		self.__file_content = ""
		self.__app.geometry("100x100")
		self.__show_tabs = show_tabs
		#Create the temporary directory
		self.__instantiate_temporary_directory(path=path)
		#Add the menus
		self.__create_toolbar()
		#Add the entry box
		self.__instantiate_views()
		self.__instantiate_settings()

	def on_key_down(self, key):
		self.__status_bar.set_text("User is typing")
		keycode = key.keycode
		if(keycode == 37):
			self.__control_pressed = True
		if(self.__control_pressed):
			if(keycode == 39):
				self.save()
			if(keycode == 32):
				self.open_file(askopenfilename())
				self.__control_pressed = False
		print(str(keycode))

	def on_key_up(self, key):
		self.__status_bar.set_text("User is done typing")

	def __instantiate_settings(self):
		self.__control_pressed = False
		self.__alt_pressed = False
	def __instantiate_views(self):
		if(self.__show_tabs is True):
			self.__tab_default_background = "#282828"
			self.__tab_click_background = "#282828"

			self.__style = ttk.Style()
			self.__style.theme_create("Slime", parent="alt",
				settings={
				"TNotebook": {"configure": {"tabmargins": [0,0,0,0], "background": self.__tab_default_background}},
				"TNotebook.Tab": {
				"configure" : {"padding": [0,0], "background": self.__tab_default_background, "foreground": "#FFFFFF"},
				"map": {"background": [("selected", self.__tab_click_background)],
				"expand": [("selected", [0,0,0,0])]}
				}
				})

			self.__style.theme_use("Slime")
			self.__tab_control = ttk.Notebook(self.__app)
			#Create a text box
			self.__entry_box = Text(self.__app)
			#Set its background to #282828
			self.__entry_box["bg"] = "#282828"
			#Set the foreground to #FFFFFF
			self.__entry_box["fg"] = "#FFFFFF"
			#Pack the entry box
			self.__entry_box.pack(fill=BOTH, expand=1, side=TOP)
			self.__tab_control.add(self.__entry_box, text=self.get_file_name())
			#self.__tab_control["backgroundcolor"] = "#282828"
			self.__tab_control.pack(expand=1, fill=BOTH)
		else:
			#Create a text box
			self.__entry_box = Text(self.__app)
			#Set its background to #282828
			self.__entry_box["bg"] = "#282828"
			#Set the foreground to #FFFFFF
			self.__entry_box["fg"] = "#FFFFFF"
			#Pack the entry box
			self.__entry_box.pack(fill=BOTH, expand=1, side=TOP)
		self.__status_bar = StatusBar(self.__app)
		self.__status_bar.set_text("No changes to report")

	def __create_toolbar(self):
		#Create the toolbar
		self.__toolbar = Menu(self.__app)
		#Create the file menu
		self.__file_menu = Menu(self.__toolbar)
		#self.__list_files(os.path.expanduser("~") + "/TempDir", self.__file_menu)
		#Add the save command
		self.__file_menu.add_command(label="Save", command=self.save)
		#Set the background to white
		self.__file_menu.config(bg='#FFFFFF')
		#Set the file menu's border to zero
		self.__file_menu["borderwidth"] = 0
		self.__file_menu["bg"] = "#FFFFFF"
		#Add the file button to the toolbar
		self.__toolbar.add_cascade(label="File", menu=self.__file_menu)
		#Set the toolbar to white
		self.__toolbar.config(bg = '#FFFFFF')
		#Set the border width of the toolbar to zero
		self.__toolbar["borderwidth"] = 0
		#Add the toolbar as the default toolbar, and set the app's background to white
		self.__app.config(bg='#282828',menu=self.__toolbar)

		#Return the toolbar
		return self.__toolbar

	def __list_files(self, directory, root_menu):
		for item in os.listdir(directory):
			item_path = directory + "/" + item
			if(os.path.isfile(item_path)):
				#print("FILE: " + item)
				root_menu.add_command(label=item, command=self.open_file(item_path))
			else:
				#print("DIRECTORY: " + item)
				self.__list_files(item_path, root_menu)

	def __instantiate_temporary_directory(self, path=None):
		#Create a random string for a path
		alphabet_numerics_string = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
		if(path is None):
			#Set the base path as ~/TempDir
			self.__path = os.path.expanduser("~") + "/TempDir"
			#Check if the base directory does not exist
			if(os.path.exists(self.__path) is False):
				#Since it does not, we create it
				os.mkdir(self.__path)
			#Add the current date and time in the base path
			self.__path = self.__path + "/" + str(datetime.datetime.now().year) + "_" + str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().day) + "/"
			#Check if the path exists
			if(os.path.exists(self.__path)):
				#Add the current hour, minute, and second to the directory
				self.__path = self.__path + str(datetime.datetime.now().hour) + "_" + str(datetime.datetime.now().minute) + "_" + str(datetime.datetime.now().second) + "/"
			#Create the path
			os.mkdir(self.__path)

			#Loop through a range between 0 and 10
			for range_number in range(0, 10):
				#Get a random index from 0 to the range_number
				index = random.randint(0, range_number)
				#Append the path
				self.__path = self.__path + alphabet_numerics_string[index]
			#Set the path with the extension .tmp
			self.__path = self.__path + ".tmp"
			self.__app.title(self.__title + " : " + self.__path)
		else:
			self.__path = path
			#Open the file for reading
			__file = open(self.__path, "r")
			#Read the file by looping through it
			for text in __file.readlines():
				#Append the file content
				self.__file_content += text
			#Close the file
			__file.close()

	def set_text(self, text):
		self.__file_content = ""
		#Update the file content text
		self.__file_content = text
		#Update the entry
		self.__update_entry(text)

	def __update_entry(self, text):
		try:
			self.__entry_box.delete("0.0", END)
			self.__entry_box.update()
			time.sleep(0.5)
			self.__entry_box.insert("0.0", text)
		except AttributeError as error:
			pass
	def run(self):
		#Start the application
		self.__app.mainloop()

	def save(self, ask=False):
		if(self.__path.endswith(".tmp")):
			self.__temp_path = self.__path
			self.__path = asksaveasfilename()
		#Set the file content to the text box content
		self.__file_content = self.__entry_box.get("1.0", END)
		#Open the file as writable
		__file = open(self.__path, "w")
		#Write the file content to the file
		__file.writelines(self.__file_content)
		#Flush the file
		__file.flush()
		#Close the file
		__file.close()

		#Open the temp file
		__temp = open(self.__temp_path, "w")
		#Write the text to the temp file
		__temp.writelines(self.__file_content)
		#Flush the temp file
		__temp.flush()
		#Close the temp file
		__temp.close()
		print("Saved file")

	def open_file(self, path):
		__file = open(path, "r")
		for line in __file.readlines():
			self.__file_content += line
		__file.close()
		self.set_text(self.__file_content)


	def get_entry(self):
		return self.__entry_box

	def get_toolbar(self):
		return self.__toolbar

	def get_tab_control(self):
		return self.__tab_control

	def get_tab_control_style(self):
		return self.__style

	def get_file_name(self):
		path_list = str(self.__path).split("/")
		path_list_final_index = len(path_list) - 1
		file_name = str(path_list[path_list_final_index])
		return file_name