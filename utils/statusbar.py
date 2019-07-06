#Import tkinter for UI
from tkinter import *
import time

class StatusBar(Frame):

	def __init__(self, master_view):
		Frame.__init__(self, master_view)

		self.variable = StringVar()
		self.label = Label(self, bd=1, relief=SUNKEN, anchor=W, textvariable=self.variable, font=('arial', 10, 'normal'))
		self.variable.set('Status Bar')
		self.label.pack(fill=X, side=LEFT)
		self.pack(fill=X, side=BOTTOM)
		self.label['bg'] = self['bg']
		#Configure the interface to make it blend
		#Set the border width for the frame to zero
		self.configure(borderwidth=0)
		#Set the border width for the label to zero
		self.label.configure(borderwidth=0)
		#Set the highlight thickness for the frame to zero
		self.configure(highlightthickness=0)
		#Set the highlight thickness for the label to zero
		self.label.configure(highlightthickness=0)

	def set_text(self, text, time_slept_before_change=0):
		#Sleep for the requested amount
		time.sleep(time_slept_before_change)
		#Change the variable text
		self.variable.set(text)
		#Update the label
		self.label.update()

	def word_by_word_timed_text_change(self, text, time_slept_before_change):
		full_text = ""
		for line in text.split(" "):
			full_text += line + " "
			self.set_text(full_text, time_slept_before_change=time_slept_before_change)
	def letter_by_letter_timed_text_change(self, text, time_slept_before_change):
		full_text = ""
		for line in text.split(" "):
			for letter in line:
				full_text += letter
				self.set_text(full_text, time_slept_before_change=time_slept_before_change)
			full_text += " "