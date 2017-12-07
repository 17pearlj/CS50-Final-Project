SpoonTune: A sound bite

======================================================================================================================
Methodology-


The song input form allows the user to choose particular parameters that ultimately alter the song. These
parameters are defined in README.txt, and these different factors are inserted into an algorithm.

The randomly generated song is then saved as a static file within the website that can be accessed
via randomly generated links (for example, /static/12345.wav or /static/12345.midi). This allows the website
to not only display the song but also provide the option to download it as either a .wav or .midi.

Should the user decide to save the presets (the parameters used to generate a song), these presets are
then saved into a new SQL table, which is then displayed under the page "My Presets". Using SQL functions,
we've allowed the user to choose to delete presets or generate new songs using the saved parameters.
=====================================================================================================================
Design-


The website is initially derived from the C$50 Finance website, so Bootstrap is utilized in the website.
The same menu bar along with background is displayed throughout the entire website, while black
transparent boxes serve as the backdrops to whatever information is displayed on each page.

The style sheet is found in /static/style.css.

Outside sources were used for particular elements, all of them being free to the public and open-sourced.
These particular elements are the moving buttons (submit buttons and download buttons), along with the
radio buttons which were used in the "Song Input" page. The background image was also captured from an
outside source that provides royalty-free images labeled for free use with modification.
=====================================================================================================================
Function Data Storage

The data tables are located in tunes.db. There are three data tables.

Users: the user data such as id, username, and password hash are stored just like in C$50 Finance.

Active: the data that the user put into the song input form is stored in the table active.
Each user has a row in active that is continually updated with new form generations.

Favs: the list of favorite presets that the user has chosen that can be copied into active and regenerated.

When tonic and style, two of the parameters of the createTune method from the helpers.py, are displayed to the user,
their values are displayed to the user as new dictionary values key and read.

=====================================================================================================================
Random Algorithm Design -


The random music algorithm is found in helpers.py

The first step is to generate the scale of the song. This is done by generateScale, which takes in a scale and a
style, and outputs one octave of the correct scale int the form of a list. All scales follow a unique pattern of
"steps", so generation of them is done in a for loop. The loop runs as many times as there are notes in the scale,
and calculates the number of musical steps to the next note by looking at the current index of the for loop.

The next step is to create a sample of notes that the algorithm will randomly select from to get the randomly
note. This is done in generateSampleNotes, which takes in the tonic note, style, and tonality. It first gets the
scale from generateScale. In music, chord tones help define what notes sond "in the key of the song". For example,
for a song in C Major, C E and G sound the best. Tonality is the relative frequency of these notes in the song to
the other notes in the scale. When tonality is 100 generateSampleNotes creates an list of from the scale comprised
entirely of chord tones. When Tonality is 0, all notes are represented equally. generateSample notes returns a list
of the notes that the random generator will sample from, in the proper frequencies that they should appear in the
song.

In order to generate the lengths of the notes, you use generateSampleLengths. This function takes in energy, which is
thevspeed of the notes in the song, and outputs a list of the rythms, in the relative frequency that they should
appear in the song. An energy level of 100 means that all of the notes in the song will be 16th notes, while an
energy level of 0 means it will be all whole notes.

createTune takes in all of the parameters in the form of song_input.html, and returns the song in the form of a
music21 object. It does so by generating the sample notes and the sample rhythms, randomly selecting an element from
each of them, using the randomly selected note and rhythm to create a music21 note object, and appending that note
object to the end of a stream. It keeps track of the length of the notes appended to the stream, then stops when it
reaches the desired number of measures.
=====================================================================================================================
Design Credits-


Submit buttons are credited to https://codepen.io/anon/pen/ZaqeRQ
Radio buttons are credited to https://codepen.io/raubaca/pen/ONzBxP
Download buttons are credited to https://codepen.io/nw/pen/udkIB
Background image is credited to http://maxpixel.freegreatpicture.com/Musical-Note-Music-Melody-1608492
======================================================================================================================