This is a kind of continuation of a AI chatbot project I started called CHELSEA, written in Python (there will be other languages involved later on). 
I decided to leave that project as is in its repository, because it technically has no dependencies (Aside from espeak, but this can be disabled). 
I really wanted to create an AI chatbot that had little to no dependencies so anyone could download the code and run it will little setup. 
As I'm learning more, I am realizing that in order to make CHELSEA better, I have to rely on more and more python modules and external programs.
So, that's why I'm starting this new repository, to keep them separate. I will no longer work on the original, and so if you are interested in the code, 
it can be found here:


https://github.com/stringzzz/Chatbot_CHELSEA


Note that this newer project has only been tested on Ubuntu Linux, I currently have no idea if it will work on another OS.


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


#Need virtual envrionment for installing certain python modules:


$ python3 -m venv myenv


$ source myenv/bin/activate;


$ pip3 install speechRecognition


$ sudo apt-get update


$ sudo apt-get install python3-pyaudio portaudio19-dev


$ pip3 install PyAudio


#Offline speech recognition


$ pip3 install Vosk


$ sprc download vosk


I will likely set up all of these in a bash script in the future for ease of use.


CHELSEA comes with 2 sets of memory, one under 'my_memory_files' for my own ones I've taught her. 
The other is 'starter_memory_files' which are for starting from nearly scratch (Requires a lot of teaching).
Whichever set you choose to use, just copy or move them from their directory to the same directory as the python scripts.


In order to run CHELSEA after that, enter:
python3 chatbotCHELSEA.py


This enables text entry mode by default, so you type all of your replies in the command line. 
If you add 'sr' as an end argument on the command, it will enable speech recognition mode, so you speak your replies instead, like this:
python3 chatbotCHELSEA.py sr


If you are in text mode, you can activate speech rec mode by entering 'enable speech'.
Likewise, you can switch to text mode by saying 'disable speech' when it is listening.
That's about it for now. You can virtually teach CHELSEA whatever you want, there is no filter.


