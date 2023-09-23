from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        title = request.form['title']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes (title, description) VALUES (%s, %s)", (title, description))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        title = request.form['title']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE notes SET title=%s, description=%s
        WHERE id=%s
        """, (title, description, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes")
    data = cur.fetchall()
    cur.close()


    return render_template('index.html', notes=data)

if __name__ == "__main__":
    app.run(debug=True)