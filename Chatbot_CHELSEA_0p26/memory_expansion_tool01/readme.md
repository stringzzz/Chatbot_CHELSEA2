This tool is for expanding on CHELSEA's memory by answering the many 'what is/are' questions she forms when learning new words.


The tool will run through the set of her questions 10 times, as when she learns new definitions it causes her to also learn new words,
so more questions are added each time.


Here are the list of dependencies to install to use this tool (May need to use virtual environment venv):


$ pip3 install nltk


$ pip3 install inflect


Additionally, certain files need to be downloaded once for the nltk module to work in this tool.
You may install them by running 'python3 ntlk_files_setup01.py', a script that is included in this directory.


Next, you can either edit 'self.file_path' in 'chelsea_class.py' to point to the directory containing her memory files (Look for the comment '#PATH'),
or you can just put the 2 scripts in the same directory as the memory files.


Finally, use 'python3 memory_expansion_tool01.py' to run the script. If the dependencies were installed in venv, may need 'source myenv/bin/activate;' first. The script will show its progress on the command line, and it may take a while depending on how many questions she has in your particular set of memory for her.
