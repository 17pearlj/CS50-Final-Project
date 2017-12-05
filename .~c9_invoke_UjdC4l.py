from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import generateScale, generateSampleNotes, generateSampleLengths, createNote, createTune, generateOutputString
import pysynth
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

#Empty local variables
#tonic = ""
#style = ""
#timeSignature = ""
#tonality = ""
#energy = ""
#tempo = ""
#measures = ""


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
        return render_template("login.html", apology="")



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

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", apology="")


@app.route("/song_input", methods=["GET", "POST"])
@login_required
def song_input():
    if request.method == "POST":

        tonic = str(request.form.get("key"))
        style = str(request.form.get("style"))
        timeSignature = str(request.form.get("timeSignature"))
        tonality = int(request.form.get("tonality"))
        energy = int(request.form.get("energy"))
        tempo = int(request.form.get("tempo"))
        measures = int(request.form.get("measures"))
        print(tonic)
        print(style)
        print(timeSignature)
        print(tonality)
        print(energy)
        print(tempo)
        print(measures)
        output = db.execute("SELECT * from active WHERE userid = :userid", userid = session["user_id"])
        print(output)
        if (output == []):
            print(empty)
            db.execute("INSERT INTO active (userid, tonic, style, timeSignature, tonality, energy, tempo, measures) VALUES (:userid,:tonic,:style, :timeSignature, :tonality, :energy, :tempo, :measures)",
                userid=session["user_id"], tonic=tonic, style=style, timeSignature=timeSignature, tonality=tonality, energy=energy, tempo=tempo, measures=measures)

        else:
            db.execute("UPDATE active SET tonic = tonic, style = style, timeSignature = timeSignature, tonality = tonality, energy=energy, tempo=tempo, measures=measures WHERE userid = :userid", userid = session["user_id"])

        return redirect("/song")
    else:
        return render_template("song_input.html")

@app.route("/song")
@login_required
def song():
    output = db.execute("SELECT * FROM active WHERE userid = :userid", userid=session["user_id"])
    print(output)
    print(output[0]["tonic"])
    song = createTune(output[0]["tonic"], output[0]["style"], output[0]["tonality"], output[0]["energy"], output[0]["tempo"], output[0]["timeSignature"], output[0]["measures"])
    songMidi = song.write("midi")
    songFileLocation = generateOutputString()
    FluidSynth('GeneralUserGS.sf2').midi_to_audio(songMidi, songFileLocation)
    return render_template("song.html", tonic = output[0]["tonic"], style = output[0]["style"], timeSignature = output[0]["timeSignature"], tonality = output[0]["tonality"], energy = output[0]["energy"], tempo = output[0]["tempo"], measures = output[0]["measures"], songFileLocation=songFileLocation)

@app.route("/library", methods=["GET"])
@login_required
def library():
    favs = db.execute("SELECT * FROM favs WHERE userid = :userid", userid=session["user_id"])
    return render_template("library.html", favs=favs)

@app.route("/save", methods=["GET", "POST"])
@login_required
def save():
    output = db.execute("SELECT * FROM active WHERE userid = :userid", userid=session["user_id"])
    if request.method == "POST":
        
        db.execute("INSERT INTO favs (userid, tonic, style, timeSignature, tonality, energy, tempo, measures) VALUES (:userid, :name, tonic, style, timeSignature, tonality, energy, tempo, measures)", userid=session["user_id"], name=name)
        redirect("/library")
    else:
        return render_template("save.html", tonic = output[0]["tonic"], style = output[0]["style"], timeSignature = output[0]["timeSignature"], tonality = output[0]["tonality"], energy = output[0]["energy"], tempo = output[0]["tempo"], measures = output[0]["measures"])



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

