from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import generateScale, generateSampleNotes, generateSampleLengths, createNote, createTune, generateOutputString, songMidiLocation
import pysynth
import random
from midi2audio import FluidSynth
from extra import login_required



# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tunes.db")



@app.route("/")
@login_required
def index():
        user = db.execute("SELECT username FROM users WHERE id = :id", id = session["user_id"])
        return render_template("home.html", user=user[0]["username"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", apology="Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", apology=" ")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("register.html", apology="Must provide username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", apology="Must provide password.")

        # Query database for username

        rows = db.execute("SELECT username FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if rows != []:
            return render_template("register.html", apology="Username taken.")

        if request.form.get("confirmation") != request.form.get("password"):
            return render_template("register.html", apology="Passwords don't match.")

        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=hash)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to instructions page
        return redirect("/instructions")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", apology="")


@app.route("/song_input", methods=["GET", "POST"])
@login_required
def song_input():
    if request.method == "POST":

        tonic1 = str(request.form.get("key"))
        style1 = str(request.form.get("style"))
        timeSignature1 = str(request.form.get("timeSignature"))
        tonality1 = int(request.form.get("tonality"))
        energy1 = int(request.form.get("energy"))
        measures1 = int(request.form.get("measures"))
        output = db.execute("SELECT * from active WHERE userid = :userid", userid = session["user_id"])
        if (output == []):
            db.execute("INSERT INTO active (userid, tonic, style, timeSignature, tonality, energy, measures) VALUES (:userid,:tonic,:style, :timeSignature, :tonality, :energy, :measures)",
                userid=session["user_id"], tonic=tonic1, style=style1, timeSignature=timeSignature1, tonality=tonality1, energy=energy1, measures=measures1)
        else:
            output = db.execute("UPDATE active SET tonic = :tonic, style = :style, timeSignature =:timeSignature, tonality=:tonality, energy=:energy, measures=:measures WHERE userid = :userid", userid = session["user_id"], tonic=tonic1, style=style1, timeSignature=timeSignature1, tonality=tonality1, energy=energy1, measures=measures1)
        return redirect("/song")
    else:
        return render_template("song_input.html")

@app.route("/song")
@login_required
def song():
    output = db.execute("SELECT * FROM active WHERE userid = :userid", userid=session["user_id"])
    print(output)
    song = createTune(output[0]["tonic"], output[0]["style"], output[0]["tonality"], output[0]["energy"], 120, output[0]["timeSignature"], output[0]["measures"])
    datNumber = random.randint(1,1000000)
    midiLocation = songMidiLocation(datNumber)
    songMidi = song.write("midi", midiLocation)
    songFileLocation = generateOutputString(datNumber)
    FluidSynth('GeneralUserGS.sf2').midi_to_audio(songMidi, songFileLocation)
    return render_template("song.html", tonic = output[0]["tonic"], style = output[0]["style"], timeSignature = output[0]["timeSignature"], tonality = output[0]["tonality"], energy = output[0]["energy"],  measures = output[0]["measures"], songFileLocation=songFileLocation, midiLocation=midiLocation)

@app.route("/presets", methods=["GET", "POST"])
@login_required
def presets():
    style = []
    tonic = []
    if request.method == "POST":
        option = request.form.get("option")
        print(option)
        name1 = request.form.get("name")
        print(name1)
        if (option == "delete"):
            db.execute("DELETE FROM favs WHERE (userid = :userid and name = :name)", userid=session["user_id"], name=name1)
            pre = db.execute("SELECT * FROM favs WHERE userid = :userid", userid=session["user_id"])
            zero = ""
            if (pre == []):
                zero = "No Presets Saved!"
            else:
                for p in pre:
                    style.append(p["style"])
                    tonic.append(p["tonic"])
                for i in range(0, (len(style)-1)):
                    if (style[i] == "naturalMinor"):
                        style[i] = "natural minor"
                    if (style[i] == "harmonicMinor"):
                        style[i] = "harmonic minor"
                    if (style[i] == "majorPentatonic"):
                        style[i] = "major pentatonic"
                    if (style[i] == "minorPentatonic"):
                        style[i] = "minor pentatonic"
                    if (len(tonic[i]) == 2):
                        tonic[i] = tonic[i][0]
                    if (len(tonic[i]) == 3):
                        tonic[i] = tonic[i][0:2] + " / " + chr(ord(tonic[i][0]) + 1) + "b"
            return render_template("presets.html", pre=pre, zero=zero, style=style, tonic=tonic)
        if(option == "regenerate"):
            regen = db.execute("SELECT * FROM favs WHERE (userid = :userid and name = :name)", userid=session["user_id"], name=name1)
            db.execute("UPDATE active SET tonic = :tonic, style = :style, timeSignature =:timeSignature, tonality=:tonality, energy=:energy, measures=:measures WHERE userid = :userid",
                userid = session["user_id"], tonic=regen[0]["tonic"], style=regen[0]["style"], timeSignature=regen[0]["timeSignature"], tonality=regen[0]["tonality"], energy=regen[0]["energy"], measures=regen[0]["measures"])
            return redirect("/song")
    else:
        pre = db.execute("SELECT * FROM favs WHERE userid = :userid", userid=session["user_id"])
        zero = ""
        if pre == []:
            zero = "No Presets Saved!"
        else:
            for p in pre:
                    style.append(p["style"])
                    tonic.append(p["tonic"])
            for i in range(0, (len(style)-1)):
                if (style[i] == "naturalMinor"):
                    style[i] = "natural minor"
                if (style[i] == "harmonicMinor"):
                    style[i] = "harmonic minor"
                if (style[i] == "majorPentatonic"):
                    style[i] = "major pentatonic"
                if (style[i] == "minorPentatonic"):
                    style[i] = "minor pentatonic"
                if (len(tonic[i]) == 2):
                    tonic[i] = tonic[i][0]
                if (len(tonic[i]) == 3):
                    tonic[i] = tonic[i][0:2] + " / " + chr(ord(tonic[i][0]) + 1) + "b"
        return render_template("presets.html", pre=pre, zero=zero, style=style, tonic=tonic)

@app.route("/save", methods=["GET", "POST"])
@login_required
def save():
    apology = ""
    output = db.execute("SELECT * FROM active WHERE userid = :userid", userid=session["user_id"])
    style = output[0]["style"]
    tonic = output[0]["tonic"]
    if (style == "naturalMinor"):
        style = "minor"
    if (len(tonic) == 2):
        tonic = tonic[0]
    else:
        tonic = tonic[0:2] + " / " + chr(ord(tonic[0]) + 1) + "b"
    if request.method == "POST":
        name = request.form.get("name")
        named = db.execute("SELECT * FROM favs WHERE (userid = :userid and name = :name)", userid = session["user_id"], name=name)
        if (named != []):
            apology = "You already used this name!"
            return render_template("save.html", tonic = tonic, style = style, timeSignature = output[0]["timeSignature"], tonality = output[0]["tonality"], energy = output[0]["energy"], measures = output[0]["measures"], apology = apology)
        else:
            db.execute("INSERT INTO favs (userid, name, tonic, style, timeSignature, tonality, energy, measures) VALUES (:userid, :name, :tonic, :style, :timeSignature, :tonality, :energy, :measures)", userid=session["user_id"], name=name, tonic = output[0]["tonic"], style = output[0]["style"], timeSignature = output[0]["timeSignature"], tonality = output[0]["tonality"], energy = output[0]["energy"],  measures = output[0]["measures"])
            return redirect("/presets")
    else:
        return render_template("save.html", tonic = output[0]["tonic"], style = output[0]["style"], timeSignature = output[0]["timeSignature"], tonality = output[0]["tonality"], energy = output[0]["energy"],  measures = output[0]["measures"], apology = apology)

@app.route("/instructions", methods=["GET", "POST"])
def instructions():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("instructions.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


