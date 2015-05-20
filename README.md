# speakUp v1.0
HTTP CGI interface to gTTS (google Text-To-Speak)

You can type the URL directly with the message and it is converted to sound instantaneously! You sounds are kept in a local cache, which is useful when you need the same messages again and again (home automation in my case...)

![Demo Picture](./demo.png?raw=true "In use:")

# Usage
After the simple install procedure, you just need open a terminal and type
```sh
cd speakUp
./server.py
```
Then open a web browser and go to http://localhost:8000/say to type your message

 _OR_

directly access http://localhost:8000/speakUp.py?msg=hello+world

# Instalation
I'm working in a better way to do it, but this is what we have now (Linux only):
```sh
sudo apt-get install python-pip # to install gTTS
sudo pip install gTTS           # the text to speak engine
sudo apt-get install mplayer    # to play the sounds
git clone https://github.com/fgrando/speakUp.git
```
And, finally follow usage instructions =)

# Bonus
If you have read until this line you will know that speakUp.py can be run from command line! Explore the options running ./speakUp.py --help .

# Thanks area
Special thanks to Google by the nice API & free translation service.
And to Python, a such lovely language.


