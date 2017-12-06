SpoonTune: A Sound Bite
=========================================================================================================================
Introduction-


SpoonTune is a lightweight melody generation app built on a flask server. It is designed for a musician to be able to
input a set of paramaters, and recieve back a radomly generated melody. If the user likes the melody, they can download
it in either a .wav format or .midi format. The former is better for composers, while the latter is more useful for music
producers working in a DAW (such as Garageband of Fruityloops). The website allows for users to create an account, with
which they can save their favorite presets.

========================================================================================================================
Parameters-


Key - Sets the tonic note of the song

Scale - 5 different scales to choose from, depending on desired output

Tonality - Tonality is the frequency of the key's primary chord tones to it's complimentary notes in the song.

Energy - Energy is the speed of the notes in a song.

Measures - How many measures there are

Time Signature - The time signature of the song

=======================================================================================================================
Libraries used-


music21 - Allowed for the conversion of randomly generated notes and rythyms into midi files. Dowload information
be found at http://web.mit.edu/music21/doc/installing/installLinux.html. Basically, you just need to run...

pip3 install –upgrade music21

midi2audio - A library that allows for the conversion of a midi file to a wav file, using the audio synthesizer Fluid
Synth. Install using the command...

pip install midi2audio

midi2audio also requires a song font, "GeneralUserGS.sf2", which can be downloaded at
http://schristiancollins.com/generaluser.php
=======================================================================================================================