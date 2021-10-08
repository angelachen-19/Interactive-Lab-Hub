#arecord -f cd -r 16000 -d 5 -t wav recorded.wav && sox recorded.wav recorded_mono.wav remix 1,2

espeak -ven+f2 -k5 -s150 --stdout  "What is your phone number?" | aplay

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
python3 test_words.py recorded_mono.wav
