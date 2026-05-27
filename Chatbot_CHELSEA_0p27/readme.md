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


Important! This program requires several dependencies. 
Refer to 'dependency_installations.sh' to view them, and it can also be run to install all of them in one script.
In order to run CHELSEA after that likely need to 'source myenv/bin/activate' first.


(05-12-2026)
Now comes with a tool to expand her memory by answering her many 'what is/are' questions automatically using the nltk module.
Refer to directory 'memory_expansion_tool02' for details.


####################################################


#################### (05-27-2026) ##################


####################################################


There have been many changes including to CHELSEA's and the user's memory files. 
If you happen to have been using an older version and want to keep the same set of memory, it can be converted. 
If you are just starting out and are using one of the 2 sets of memory files this code comes with, 
you don't need to worry about any of the converting stuff. 
Honestly, I would recommend just using the new files, but... Otherwise:


Steps to convert memory files from Version 0.26 to 0.27:


1. Place both the 'bigram' and 'trigram' memory files in the same directory as 'ngram_conversion01.py' and run it. 
You will get 2 pairs of both bigram and trigram files, all ending in '2'. 
These are the new files, they can then be copied into the same directory that you have CHELSEA's scripts in.


2. (Optional) Place 'dictionary.json' into the same directory as 'learn_stop_words.py' and run it. 
Having certain words marked as 'permanent neutral' (stop words) helps one of her methods (use_imagination2) to work a bit better. 
You can now move the file back into where your CHELSEA scripts are at.


3. Finally, place your user file (_YOUR_USERNAME_.json) in the same directory as 'user_file_conversion01.py' and run it. 
Now this file can be moved back to the same directory where you keep CHELSEA's code, and you are done converting.


#######################################


Known issue: After working on this latest version, there was something bothering me more and more. 
All the regular expression patterns in the code are a massive mess, they are hard to work with because of this.
I was unaware of how VERBOSE worked until recently, so now I know I need to go in and apply that to separate all
the parts of the regexes and put comments on them for much more clarity. 
This will be done within the next version.


#######################################

To run CHELSEA, enter (Likely need to 'source myenv/bin/activate;' first):
python3 chatbotCHELSEA.py


This enables text entry mode by default, so you type all of your replies in the command line. 


If you are in text mode, you can activate speech recognition mode by entering 'enable speech'.
Likewise, you can switch to text mode by saying 'disable speech' when it is listening.
That's about it for now. You can virtually teach CHELSEA whatever you want, there is no filter.


Command line arguments (Can use in any order):


'sr': Enables speech recognition mode, so you speak your replies instead.


'nouser': Acts as if you are a brand new user that it makes a new set of information for, 
AND it won't output that information to the user file after exiting the chat.


'nomem': Inputs CHELSEA's memory files, but doesn't output the newly gathered memory back into them when the chat ends. 
It still always outputs the chatlogs, and unless 'nouser' is active it will still output the user file.
