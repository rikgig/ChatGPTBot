from tkinter import *
import customtkinter
import openai
import os
import pickle


root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry('600x520')
filename = "api_key"

# only for windows
#root.iconbitmap('ai_lt.ico') # https://tkinter.com/ai_lt.ico

# Set the Color Schem

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Submit to ChatGPT

def speak():
	if chat_entry.get():
		# Send to ChatGPT
		key = read_key(filename)
		if key:
			# Query ChatGPT
			my_text.insert(END,"\n\nworking with key:" +key + "\n\n")
			my_text.insert(END,"Sending text: "+ chat_entry.get()+"\n\n")
			openai.api_key = key
			openai.Model.list()
			response = openai.Completion.create(
				model = "text-davinci-003",
				prompt = chat_entry.get(),
				temperature = 0,
				max_tokens = 60,
				top_p = 1.0,
				frequency_penalty=0.0,
				presence_penalty=0.0,
				)
			my_text.insert(END, response)

			text_response = (response["choices"][0]["text"].strip())
			my_text.insert(END,text_response)
			my_text.insert(END, "\n\n")
		else:
			my_test.insert(END, "\n\nNo API key available\n\n")
		return
	else:
		my_text.insert(END, "\n\nNothing to send\n\n")


# Clear the Screens
def clear():
	my_text.delete(1.0,END)
	chat_entry.delete(0,END)



# Do API stuff
def key():

	try:
		if (os.path.isfile(filename)):
			# Open the file
			input_file = open(filename,'rb')
			# Load data from file
			keyfileContent = pickle.load(input_file)
			# output this in entry box
			api_entry.insert(END, keyfileContent)
		else:
			# Create the file
			input_file = open(filename,'wb')
			# Close the file
			input_file.close()
	except Exception as e:
		exceptionMessage = str(e)
		my_text.insert(END, "\n\nThere was an error writing the key file\n\n"+exceptionMessage)

	# Resize the frame
	root.geometry('600x650')
	api_frame.pack(pady=30)


# Do Save API key
def save_key():
	try:
		# Open the file	
		output_file = open(filename,'wb')
		pickle.dump(api_entry.get(),output_file)
		output_file.close()
		# Empty the box to prevent saving many times
		api_entry.delete(0,END)

		api_frame.pack_forget()
		root.geometry('600x520')
	except Exception as e:
		exceptionMessage = str(e)
		my_text.insert(END, "\n\nThere was an error reading the key file\n\n"+exceptionMessage)

def read_key(keyfileName):
	try:
		if (os.path.isfile(keyfileName)):
			# Open the file
			input_file = open(keyfileName,'rb')
			# Load data from file
			keyfileContent = pickle.load(input_file)
			# output this in entry box
			return keyfileContent
		else:
			return
	except Exception as e:
		exceptionMessage = str(e)
		my_text.insert(END, "\n\nThere was an error reading the key file\n\n"+exceptionMessage)
		return


# Main program commands
# Create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add text widget for responses
my_text = Text(text_frame,
	bg="#343638",
	width=73,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1f538d");
my_text.grid(row=0,column=0)

# Scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

my_text.configure(yscrollcommand=text_scroll.set)

# Entry Widget for sending text to ChatGPT

chat_entry= customtkinter.CTkEntry(root,
	placeholder_text="Type Something to ChatGPT",
	width=535, 
	height=50,
	border_width=1)

chat_entry.pack(pady=10)

# Button frame

button_frame = customtkinter.CTkFrame(root,
	fg_color="#242424")
button_frame.pack(pady=10)

# Add buttons: submit, clear, open API screen

submit_button = customtkinter.CTkButton(button_frame,
	text="Speak to ChatGPT",
	command=speak)

submit_button.grid(row=0, column=0, padx=25)


clear_button = customtkinter.CTkButton(button_frame,
	text="Clear screen",
	command=clear)

clear_button.grid(row=0, column=1, padx=35)

api_button = customtkinter.CTkButton(button_frame,
	text="Update API key",
	command=key)

api_button.grid(row=0, column=2, padx=25)

# Add API Key Frame

api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget

api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter your API key",
	width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)




root.mainloop()

