from flask import Flask, render_template, request, redirect, url_for, make_response, json
import sqlite3
import datetime
import pandas as pd
from flask_mail import Mail, Message

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

from core_functions import hash_string, check_string
from mail_functions import order_conf, registration_conf
########################################################################################################################

app = Flask(__name__)
#application = app

db = 'uAiYPtSRGHGzIrWe.db'

f = open("access.txt", "r")
acc = f.readline()
m, p =  acc.split(" ", 1)
f.close()

app.config.update(
	DEBUG=True,
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = m,
	MAIL_PASSWORD = p
	)

mail = Mail(app)

f = open("api.txt", "r")
api_key = f.readline()
f.close()

GoogleMaps(app, key = api_key)

########################################################################################################################

@app.route('/signup', methods = ['GET','POST'])
def registration():
    if request.method == 'POST':
        ProvidedName = request.form.get('name')
        ProvidedLogin = request.form.get('login')
        ProvidedMail = request.form.get('mail')
        HashedPassword = hash_string(request.form.get('password'))
        now = datetime.datetime.now()
        CurrTime = now.strftime("%Y-%m-%d %H:%M:%s")
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, login, mail, password, rank, reg_time) VALUES (?,?,?,?,?,?)",
                  (ProvidedName, ProvidedLogin, ProvidedMail, HashedPassword, 'user', CurrTime))
        conn.commit()
        c.close()

        msg = Message("Welcome on eBookStore " + ProvidedName,
                      sender = "yoursendingemail@gmail.com",
                      recipients = [ProvidedMail])
        msg.body = registration_conf(ProvidedName)
        mail.send(msg)

        return redirect('/login')
    return render_template('registration.html', page_title="Register Now!")



@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        ProvidedLogin = request.form.get('login')
        ProvidedPassword = request.form.get('password')
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('SELECT password, rank FROM users WHERE login LIKE ?', [ProvidedLogin])
        result = c.fetchone()

        if result is not None:
            if check_string(result[0], ProvidedPassword):
                resp = make_response(redirect('/index'))
                resp.set_cookie("user", ProvidedLogin)
                resp.set_cookie("rank", result[1])
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
                c.execute("INSERT INTO logs (login, dt) VALUES (?,?)", [ProvidedLogin, dt])
                conn.commit()
                c.close()
                return resp
            else:
                error = "Wrong password!"
                return render_template('login.html', page_title="Let's Log In!", error = error)
        else:
            error = "Wrong login!"
            return render_template('login.html', page_title="Let's Log In!", error = error)
    return render_template('login.html', page_title="Let's Log In!", error = error)



@app.route('/logout')
def logout():
    resp = make_response(redirect('/index'))
    resp.set_cookie("user", expires = 0)
    resp.set_cookie("rank", expires = 0)
    return resp



@app.route('/')
@app.route('/index')
def index():
    #localtime = now.strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id, title, author, price FROM ebooks_storage ORDER BY id desc LIMIT 5")
    last = c.fetchall()

    c.execute("SELECT book_id, count(*), title, author, price FROM sales LEFT JOIN ebooks_storage ON sales.book_id = ebooks_storage.id GROUP BY book_id HAVING title != 'None' ORDER BY count(*) desc, sales.id desc LIMIT 5")
    best = c.fetchall()



    return render_template('index.html', page_title = "Index",
                           user = request.cookies.get("user"), rank = request.cookies.get("rank"),
                           last = last, best = best)



@app.route('/search', methods = ['GET','POST'])
def search():
        find = request.form.get('search_value')
        conn = sqlite3.connect(db)
        c = conn.cursor()
        if find is not None:
            c.execute("SELECT id, title, author, year, price FROM ebooks_storage WHERE title LIKE ('%' || ? || '%') OR author LIKE ('%' || ? || '%') ORDER BY title",
                  (find, find))
        else:
            c.execute("SELECT id, title, author, year, price FROM ebooks_storage ORDER BY title")
        results = c.fetchall()
        c.close()
        return render_template('search.html', page_title="Find interesting book!", rows = results)



@app.route('/details/<int:book_id>')
def details(book_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id, title, author, isbn, year, publisher, price, details FROM ebooks_storage WHERE id LIKE ?", [book_id])
    results = c.fetchall()
    c.execute("SELECT id FROM users WHERE login LIKE ?", [request.cookies.get("user")])
    try:
        user_id = c.fetchone()[0]
        c.execute("SELECT user_id, book_id FROM wishlist WHERE book_id LIKE ? AND user_id LIKE ?", [book_id, user_id])
        wished = len(c.fetchall())
    except:
        wished = 0
    c.close()
    return render_template('details.html', details = results[0], wished = wished)



@app.route('/order/<int:book_id>', methods = ['GET','POST'])
def order_book(book_id):
    if request.method == 'POST':
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%s")
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT id, mail FROM users WHERE login LIKE ?", [request.cookies.get("user")])
        try:
            query_result = c.fetchone()
            user_id = query_result[0]
            user_mail = query_result[1]

        except:
            return redirect('/login')
        c.execute("SELECT title, author, isbn, publisher, price  FROM ebooks_storage WHERE id LIKE ?", [book_id])
        book_data = c.fetchone()
        print(book_data)
        current_price = book_data[4]
        c.execute("INSERT INTO sales (user_id, book_id, dt, cost) VALUES (?, ?, ?, ?)", (user_id, book_id, dt, current_price))
        conn.commit()
        c.close()

        msg = Message("Thanks for the order " + request.cookies.get("user") + "!",
                      sender="yoursendingemail@gmail.com",
                      recipients = [user_mail])

        msg.body = order_conf(request.cookies.get("user"), book_data)
        mail.send(msg)

        return redirect('/history')
    else:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT id, title, author, isbn, publisher, price FROM ebooks_storage WHERE id LIKE ?", [book_id])
        results = c.fetchall()
        c.close()
        return render_template('order.html', details=results[0])



@app.route('/history')
def history():
    user_name = request.cookies.get("user")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT book_id, dt, title, author, cost, login FROM sales LEFT JOIN ebooks_storage ON sales.book_id = ebooks_storage.id LEFT JOIN users ON sales.user_id = users.id WHERE login LIKE ?",
              [user_name])
    results = c.fetchall()
    total_spendings = sum([row[4] for row in results])
    c.close()
    return render_template('history.html', data = results, login = user_name, total_spendings = total_spendings)



@app.route('/profile')
def user_profile():
    user_name = request.cookies.get("user")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        "SELECT id, name, login, mail, spendings FROM users LEFT JOIN (SELECT user_id, SUM(cost) as spendings FROM sales GROUP BY user_id) B ON users.id = B.user_id WHERE users.login LIKE ?",
        [user_name])
    result = c.fetchone()
    c.execute(
        "SELECT book_id, title, author FROM wishlist LEFT JOIN ebooks_storage ON wishlist.book_id = ebooks_storage.id LEFT JOIN users ON wishlist.user_id = users.id WHERE login LIKE ?",
        [user_name])
    wishlist = c.fetchall()
    c.close()
    return render_template('profile.html', name = result[1], login = result[2], mail = result[3], spendings = result[4], wishlist = wishlist)



@app.route('/all_ebooks')
def all_ebooks():
    find = request.form.get('search_value')
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if find is not None:
        c.execute(
            "SELECT id, title, author, year, price FROM ebooks_storage WHERE title LIKE ('%' || ? || '%') OR author LIKE ('%' || ? || '%') ORDER BY title",
            (find, find))
    else:
        c.execute("SELECT id, title, author, year, price FROM ebooks_storage ORDER BY title")
    results = c.fetchall()
    c.close()
    return render_template('all_ebooks.html', rows=results)




@app.route('/edit_ebook/<int:book_id>', methods = ['GET','POST'])
def edit_ebook(book_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_author = request.form.get('author')
        new_year = request.form.get('year')
        new_price = request.form.get('price')
        new_isbn = request.form.get('isbn')
        new_publisher  = request.form.get('publisher')
        new_details = request.form.get('details')
        c.execute("UPDATE ebooks_storage SET title = ?, author = ?, year = ?, price = ?, isbn = ?, publisher = ?, details = ? WHERE id LIKE ?",
                  [new_title, new_author, new_year, new_price, new_isbn, new_publisher, new_details, book_id])
        conn.commit()
        c.close()
        return redirect('/all_ebooks')
    else:
        c.execute("SELECT * FROM ebooks_storage WHERE id LIKE ?", [book_id])
        result = c.fetchone()
        c.close()
        return render_template('edit_ebook.html', result = result)



@app.route('/new_ebook', methods = ['GET','POST'])
def add_ebook():
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_author = request.form.get('author')
        new_year = request.form.get('year')
        new_price = request.form.get('price')
        new_isbn = request.form.get('isbn')
        new_publisher = request.form.get('publisher')
        new_details = request.form.get('details')

        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(
            "INSERT INTO ebooks_storage (title, author, year, price, isbn, publisher, details) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [new_title, new_author, new_year, new_price, new_isbn, new_publisher, new_details])
        conn.commit()
        c.close()
        return redirect('/all_ebooks')
    return render_template('new_ebook.html')



@app.route('/delete_ebook/<int:book_id>', methods = ['GET','POST'])
def delete_ebooks(book_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    if request.method == 'POST':
        c.execute("DELETE FROM ebooks_storage WHERE id LIKE ? ", [book_id])
        conn.commit()
        c.close()
        return redirect('/all_ebooks')
    else:
        c.execute("SELECT * FROM ebooks_storage WHERE id LIKE ?", [book_id])
        results = c.fetchone()
        c.close()
        return render_template('delete_ebook.html', results =results)



@app.route('/sales')
def sales():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT sales.id, sales.dt, users.login, title, author, sales.cost FROM sales LEFT JOIN users ON sales.user_id = users.id LEFT JOIN ebooks_storage ON sales.book_id = ebooks_storage.id order by sales.dt DESC")
    results = c.fetchall()
    c.close()
    now = datetime.datetime.now()
    TRmonth = sum([row[-1] for row in results if (int(row[1][:4]) == now.year) & (int(row[1][5:7]) == now.month)])
    TRyear = sum([row[-1] for row in results if int(row[1][:4]) == now.year])
    total_revenues = sum([row[-1] for row in results])

    gr = pd.DataFrame([[datetime.date( int(x[1][:4]), int(x[1][5:7]), 1), x[-1]] for x in results], columns = ["YYYYMM", "PLN"])
    gr = gr.groupby(["YYYYMM"], as_index=False)["PLN"].agg({"value": sum, "volume": "count"}).sort_values(by=["YYYYMM"])

    value = list(gr["value"])
    volume = list(gr["volume"])
    labels = list(gr["YYYYMM"])

    return render_template('sales.html', results = results[:10], TR = total_revenues, TR_year = TRyear, TR_mth = TRmonth,
                           year = now.year, month = now.strftime("%Y-%m"), labels = labels, volume = volume, value = value)


@app.route('/users', methods = ['GET','POST'])
def users():
    find = request.form.get('search_value')
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if find is not None:
        c.execute(
            "SELECT name, users.login, mail, rank, reg_time, case when max(logs.dt) != 'None' then max(logs.dt) else reg_time end as last_log "
            "FROM users LEFT JOIN logs on users.login = logs.login "
            "WHERE users.login LIKE ('%' || ? || '%') OR name LIKE ('%' || ? || '%') GROUP BY users.login ORDER BY reg_time", (find, find))
    else:
        c.execute("SELECT name, users.login, mail, rank, reg_time, case when max(logs.dt) != 'None' then max(logs.dt) else reg_time end as last_log "
              "FROM users LEFT JOIN logs on users.login = logs.login GROUP BY users.login ORDER BY reg_time")
    results = c.fetchall()
    c.close()
    return render_template('users.html', results = results)



@app.route('/edit_user/<string:login>', methods = ['GET','POST'])
def edit_user(login):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if request.method == 'POST':

        new_login = request.form.get('login')
        new_name = request.form.get('name')
        new_mail = request.form.get('mail')
        new_rank = request.form.get('rank')
        c.execute(
            "UPDATE users SET name = ?, login = ?, mail = ?, rank = ? WHERE login LIKE ?",
            [new_name, new_login, new_mail, new_rank, login])
        conn.commit()
        c.close()
        return redirect('/users')
    else:
        c.execute("SELECT login, name, mail, rank, reg_time FROM users WHERE login LIKE ?", [login])
        result = c.fetchone()
        c.close()
        return render_template('edit_user.html', result=result)


@app.route('/delete_user/<string:login>', methods = ['GET','POST'])
def delete_user(login):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    if request.method == 'POST':
        c.execute("DELETE FROM users WHERE login LIKE ? ", [login])
        conn.commit()
        c.close()
        return redirect('/users')
    else:
        c.execute("SELECT login, name, mail, rank, reg_time FROM users WHERE login LIKE ?", [login])
        results = c.fetchone()
        c.close()
        return render_template('delete_user.html', results =results)



@app.route('/wish/<int:book_id>')
def wish(book_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE login LIKE ?", [request.cookies.get("user")])
    try:
        user_id = c.fetchone()[0]
    except:
        return redirect('/login')
    now = datetime.datetime.now()
    c.execute("INSERT INTO wishlist (user_id, book_id, dt) VALUES (?, ?, ?)", [user_id, book_id, now.strftime("%Y-%m-%d %H:%M:%s")])
    conn.commit()
    c.close()
    return redirect('/profile')



@app.route('/unwish/<int:book_id>')
def unwish(book_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE login LIKE ?", [request.cookies.get("user")])
    user_id = c.fetchone()[0]
    c.execute("DELETE FROM wishlist WHERE book_id LIKE ? AND user_id LIKE ?", [book_id, user_id])
    conn.commit()
    c.close()
    return redirect('/details/' + str(book_id))


@app.route('/about')
def about():

    return render_template('about.html', page_title = "About eBook Store")

@app.route('/contact')
def contact():
    map = Map(
        identifier = 'mapa_wne',
        lat= 52.247186,
        lng= 21.003806,
        markers=[(52.247186, 21.003806)],
        fit_markers_to_bounds = False,
        style = "height: 400px; width: 90%; margin-left: 5%;"
    )

    return render_template('contact.html', page_title = "Contact", mapa_wne = map)



########################################################################################################################

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug = False)
