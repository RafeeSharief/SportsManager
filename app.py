import os
from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sports-demo-key")

# Organizer login
ADMIN = {"username": "organizer", "password": "admin123"}

# In-memory data
teams = ["Team A", "Team B", "Team C"]
matches = [
    {"team1": "Team A", "team2": "Team B", "date": "2026-10-01", "score": "Not played"},
    {"team1": "Team B", "team2": "Team C", "date": "2026-10-03", "score": "Not played"},
]

def logged_in():
    return session.get("logged_in", False)

@app.route("/")
def home():
    rows = "".join(
        f"<tr><td>{m['team1']}</td><td>{m['team2']}</td><td>{m['date']}</td><td>{m['score']}</td></tr>"
        for m in matches
    )
    return f"""
    <h1>Sports Tournament Manager</h1>
    <h2>Match Schedule & Results</h2>
    <table border="1" cellpadding="8">
      <tr><th>Team 1</th><th>Team 2</th><th>Date</th><th>Score</th></tr>
      {rows}
    </table>
    <p><a href="/login">Organizer Login</a></p>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == ADMIN["username"] and request.form["password"] == ADMIN["password"]:
            session["logged_in"] = True
            return redirect("/admin")
        error = "Invalid credentials"
    return f"""
    <h2>Organizer Login</h2>
    {"<p style='color:red'>" + error + "</p>" if error else ""}
    <form method="post">
      Username: <input name="username"><br>
      Password: <input type="password" name="password"><br>
      <button type="submit">Login</button>
    </form>
    """

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not logged_in():
        return redirect("/login")

    if request.method == "POST":
        # Add a new match
        matches.append({
            "team1": request.form["team1"],
            "team2": request.form["team2"],
            "date": request.form["date"],
            "score": "Not played"
        })

    rows = "".join(f"<li>{m['team1']} vs {m['team2']} ({m['date']}) - {m['score']}</li>" for m in matches)
    return f"""
    <h1>Organizer Dashboard</h1>
    <h3>Add New Match</h3>
    <form method="post">
      Team 1: <input name="team1"><br>
      Team 2: <input name="team2"><br>
      Date: <input name="date" placeholder="YYYY-MM-DD"><br>
      <button type="submit">Add Match</button>
    </form>
    <h3>All Matches</h3>
    <ul>{rows}</ul>
    <p><a href="/logout">Logout</a> | <a href="/">View Public Page</a></p>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
