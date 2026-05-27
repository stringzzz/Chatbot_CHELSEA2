#Here are the list of dependencies so far and how to install them:

#These are needed for the text-to-speech setup:
sudo apt install sox;

#Need virtual envrionment for installing certain python modules:
python3 -m venv myenv;
source myenv/bin/activate;

pip3 install piper-tts;

#Download a voice model from here: https://rhasspy.github.io/piper-samples/
#The code is setup to use this one 'en_US-amy-low'
#Other voices may require some adjustments on pitch and speed!
# ! Refer to this line in 'chelsea_class.py':
#self.MODEL_PATH = "/YOUR_DIRECTORY_HERE/.local/share/piper-tts/piper-voices/en_US-amy-low.onnx"
mkdir -p ~/.local/share/piper-tts/piper-voices;
sudo mv /[DOWNLOAD PATH]/en_US-amy-low.onnx ~/.local/share/piper-tts/piper-voices/;
sudo mv /[DOWNLOAD PATH]/en_US-amy-low.onnx.json ~/.local/share/piper-tts/piper-voices/;
#Edit the path in 'chelsea_class.py' to where you place this voice file.

#These are for the speech recognition capabilities:
pip3 install speechRecognition;
sudo apt-get update;
sudo apt-get install python3-pyaudio portaudio19-dev;
pip3 install PyAudio;

#Offline speech recognition:
pip3 install Vosk;
sprc download vosk;
