import json
import urllib.request

class UpdateChecker:
	def __init__(self, status_bar, url="https://raw.github.com/UltraTextEditor/app/master/info/info.json"):
		if(url is "info/info.json"):
			url = "https://raw.github.com/UltraTextEditor/app/master/info/info.json"
		#Set the status bar
		self.__status_bar = status_bar
		#Set the url
		self.__url = url

	def check_for_updates(self):
		#Notify that we are checking for updates
		self.__status_bar.set_text("Checking for updates")
		#Get the response from the github page
		response = urllib.request.urlopen(self.__url)
		#Update the status of our update checking
		self.__status_bar.set_text("Checking for updates.", time_slept_before_change=0.5)
		#Set json to the string grabbed from the github page
		__github = json.loads(str(response.read().decode()))
		#Notify of our current status
		self.__status_bar.set_text("Checking for updates..", time_slept_before_change=0.5)
		#Set the update version variable
		__update_version = __github['current_version']
		self.__status_bar.set_text("Checking for updates...", time_slept_before_change=0.5)

		#Get the local version
		#Read the file stored locally
		__local_file = open("info/info.json", "r")
		self.__status_bar.set_text("Checking for updates....", time_slept_before_change=0.5)
		#Get the list of text
		__local_json_lines = __local_file.readlines()
		self.__status_bar.set_text("Checking for updates.....", time_slept_before_change=0.5)
		#Use full text for json loading
		__full_text = ""
		#Loop through and add lines to full text variable
		for line in __local_json_lines:
			#Append the full text
			__full_text += line + " "
		self.__status_bar.set_text("Checking for updates......", time_slept_before_change=0.5)
		#Tell the json library to load the text we appended
		__local_json = json.loads(__full_text)
		self.__status_bar.set_text("Checking for updates.......", time_slept_before_change=0.5)
		#Get the local version
		__local_version = __local_json["current_version"]

		#Check if the local version and the github version are not the same
		if(__local_version != __update_version):
			#Notify that an update is available
			self.__status_bar.set_text("Update available!")
		else:
			#Notify that the user is running the latest version
			self.__status_bar.set_text("You are running the latest version!")