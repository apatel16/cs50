import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    stocks_list = []
    total = 0.0

    # get stock symbol, shares
    result1 = db.execute("SELECT stock_symbol, SUM(shares) from purchases WHERE user_id = :user_id GROUP BY stock_symbol HAVING SUM(shares)>0",
                         user_id=session["user_id"])

    # get current stock price
    for stock in result1:
        templist = []
        temp = 0.0

        quote = lookup(stock["stock_symbol"])
        templist.append(quote["symbol"])  # Symbol
        templist.append(quote["name"])  # Name
        templist.append(stock["SUM(shares)"])  # Shares
        templist.append(quote["price"])  # Price

        temp = round(quote["price"] * stock["SUM(shares)"], 2)
        templist.append(temp)  # total

        total = total + temp

        stocks_list.append(templist)

    # get cash of user
    result2 = db.execute("SELECT cash from users WHERE id = :user_id", user_id=session["user_id"])
    cash = result2[0]["cash"]
    total = total + cash

    return render_template("index.html", stocks=stocks_list, cash=round(cash, 2), total=round(total, 2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Invalid symbol!", 400)

        if not request.form.get("shares"):
            return apology("Missing number of shares", 400)

        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("Enter positive number", 400)
        except ValueError:
            return apology("That's not an int!", 400)

        quote = lookup(request.form.get("symbol"))

        try:
            stock_name = quote["name"]
            stock_price = quote["price"]
            stock_symbol = quote["symbol"]
        except Exception:
            return apology("Stock lookup error", 400)

        cash = db.execute("SELECT cash from users WHERE id = :user_id", user_id=session["user_id"])

        if cash[0]["cash"] < (stock_price * shares):
            return apology("Sorry! You don't have enough cash", 400)

        result = db.execute("INSERT INTO purchases (stock_symbol, price, user_id, shares) VALUES (:stock_symbol, :stock_price, :user_id, :shares)",
                            stock_symbol=request.form.get("symbol"),
                            stock_price=stock_price,
                            user_id=session["user_id"],
                            shares=shares)

        if not result:
            return apology("Transaction incompete", 400)

        result2 = db.execute("UPDATE users SET cash = cash - :purchase where id = :user_id",
                             purchase=round(stock_price * shares, 2),
                             user_id=session["user_id"])

        if not result2:
            return apology("Cash not updated", 400)

        result3 = db.execute("")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transaction_list = []

    transactions = db.execute("SELECT stock_symbol, price, shares, timestamp from purchases WHERE user_id = :user_id",
                              user_id=session["user_id"])

    for transaction in transactions:
        templist = []
        templist.append(transaction["stock_symbol"])
        templist.append(transaction["price"])
        templist.append(transaction["shares"])
        templist.append(transaction["timestamp"])

        transaction_list.append(templist)

    return render_template("history.html", transactions=transaction_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Symbol Error!", 400)

        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Stock is not valid!", 400)

        name_ = quote["name"]
        price_ = quote["price"]
        symbol_ = quote["symbol"]

        return render_template("/quoted.html", s_name=name_, s_price=price_, s_symbol=symbol_)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Must provide username", 400)

        if not request.form.get("password"):
            return apology("Must provide password", 400)

        if not request.form.get("confirmation"):
            return apology("Please confirm password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        password_hash = generate_password_hash(request.form.get("password"))

        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"),
                            hash=password_hash)

        if not result:
            return apology("user already exist", 400)

        session["user_id"] = result

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stock_symbol_list = []

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Symbol Error", 400)

        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Stock is not valid!", 400)

        stock_price = quote["price"]

        if not request.form.get("shares"):
            return apology("Enter valid number of shares", 400)

        shares = int(request.form.get("shares"))
        if shares < 0:
            return apology("Enter positive number", 400)

        result = db.execute("SELECT stock_symbol, SUM(shares) from purchases WHERE user_id=:user_id and stock_symbol=:stock_symbol",
                            user_id = session["user_id"],
                            stock_symbol = request.form.get("symbol"))
        if not result:
            return apology("Can't sell shares", 400)

        if int(result[0]["SUM(shares)"]) < shares:
            return apology("Don't have enough shares to sell", 400)

        results1 = db.execute("INSERT INTO purchases (stock_symbol, price, user_id, shares) VALUES (:stock_symbol, :stock_price, :user_id, :shares)",
                              stock_symbol=request.form.get("symbol"),
                              stock_price=stock_price,
                              user_id=session["user_id"],
                              shares=shares * -1)
        if not results1:
            return apology("Stock not sold", 400)

        results2 = db.execute("UPDATE users SET cash = cash + :sold where id = :user_id",
                              sold=round(stock_price * shares, 2),
                              user_id=session["user_id"])
        if not results2:
            return apology("Cash transaction Error", 400)

        return redirect("/")

    else:
        results3 = db.execute("SELECT stock_symbol from purchases WHERE user_id=:user_id GROUP BY stock_symbol HAVING SUM(shares)>0",
                              user_id=session["user_id"])

        for result in results3:
            stock_symbol_list.append(result["stock_symbol"])

        return render_template("sell.html", symbols_list=stock_symbol_list)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def addCash():

    if request.method == "POST":

        if not request.form.get("cash"):
            return apology("Enter valid amount", 400)

        cash_ = int(request.form.get("cash"))
        if cash_ < 0 :
            return apology("Enter valid amount", 400)

        result = db.execute("UPDATE users SET cash = cash + :cash where id = :user_id",
                            cash = cash_,
                            user_id = session["user_id"])
        if not result:
            return apology("Transaction cancelled", 400)

        return redirect("/")

    else:
        return render_template("cash.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
