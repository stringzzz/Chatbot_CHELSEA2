This is a kind of continuation of an AI chatbot project I started called CHELSEA, written in Python (there will be other languages involved later on). 
I decided to leave that project as is in its repository, because it technically has no dependencies (Aside from espeak, but this can be disabled). 
I really wanted to create an AI chatbot that had little to no dependencies so anyone could download the code and run it with little setup. 
As I'm learning more, I am realizing that in order to make CHELSEA better, I have to rely on more and more python modules and external programs.
So, that's why I'm starting this new repository, to keep them separate. I will no longer work on the original, and so if you are interested in the code, 
it can be found here:


https://github.com/stringzzz/Chatbot_CHELSEA


Note that this newer project has only been tested on Ubuntu Linux, I currently have no idea if it will work on another OS.


Chatbot CHELSEA is an AI chatbot with simulated emotions that learns from you talking to her. 
If you are using the 'starter_memory_files', note that certain features will not be active until she learns a lot more.
The purpose of this is that when those features are sometimes activated, during those times CHELSEA won't learn new responses.
So, when her memory is brand new, having those features active would just cheat her out of learning experiences.
Also to note, any time CHELSEA doesn't recognize what you are saying, CHELSEA will learn from that, 
but in order to keep the conversation going CHELSEA will just choose a random response from her memory to respond with.
That means that until she learns a lot more, she can seem really random for a while, but if you keep talking to her properly she will learn.


Important! The only way CHELSEA will output and save everything she learned from the conversation is to end it by 
entering (text mode) or speaking (speech recognition mode): 'exit the chat'.


CHELSEA comes with 2 sets of memory, one under 'my_memory_files' for my own ones I've taught her. 
The other is 'starter_memory_files' which are for starting from nearly scratch (Requires a lot of teaching).
Whichever set you choose to use, just copy or move them from their directory to the same directory as the python scripts.


(05-12-2026)
Now comes with a tool to expand her memory by answering her many 'what is/are' questions automatically using the nltk module.
Refer to directory 'memory_expansion_tool01' for details.


Here are the list of dependencies so far and how to install them:


#These are needed for the text-to-speech setup:


$ sudo apt install sox


#(May need venv)


$ pip3 install piper-tts


#Download a voice model from here: https://rhasspy.github.io/piper-samples/


#The code is setup to use this one 'en_US-amy-low'


#Other voices may require some adjustments on pitch and speed!


$ mkdir -p ~/.local/share/piper-tts/piper-voices


$ sudo mv /[DOWNLOAD PATH]/en_US-amy-low.onnx ~/.local/share/piper-tts/piper-voices/


$ sudo mv /[DOWNLOAD PATH]/en_US-amy-low.onnx.json ~/.local/share/piper-tts/piper-voices/


Edit the path in 'chelsea_class.py' to where you place this voice file.


#Need virtual envrionment for installing certain python modules:


$ python3 -m venv myenv


$ source myenv/bin/activate;


#These are for the speech recognition capabilities:


$ pip3 install speechRecognition


$ sudo apt-get update


$ sudo apt-get install python3-pyaudio portaudio19-dev


$ pip3 install PyAudio


#Offline speech recognition


$ pip3 install Vosk


$ sprc download vosk


I will likely set up all of these in a bash script in the future for ease of use.


In order to run CHELSEA after that, enter (Likely need to 'source myenv/bin/activate;' first):
python3 chatbotCHELSEA.py


This enables text entry mode by default, so you type all of your replies in the command line. 
If you add 'sr' as an end argument on the command, it will enable speech recognition mode, so you speak your replies instead, like this:
python3 chatbotCHELSEA.py sr


If you are in text mode, you can activate speech recognition mode by entering 'enable speech'.
Likewise, you can switch to text mode by saying 'disable speech' when it is listening.
That's about it for now. You can virtually teach CHELSEA whatever you want, there is no filter.


