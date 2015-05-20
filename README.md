# speakUp
gTTS (google Text-To-Speak) interface via CGI

=== Usage ===
open a terminal
git https://github.com/fgrando/speakUp.git
cd speakUp
./server.py

open a web browser and go to http://localhost:8000/say to type your message
 _OR_
directly access http://localhost:8000/speakUp.py?msg=hello+world

=== Insatalation ===
1 - Linux only (for now)
2 - sudo apt-get install python-pip # to install gTTS
3 - sudo pip install gTTS           # the text to speak engine
4 - sudo apt-get install mplayer    # to play the songs
