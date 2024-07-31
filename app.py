from flask import Flask, request, render_template
from flask_cors import CORS
from flask_mysqldb import MySQL
from static.dbti.DBTIDB_conn import save_result

app = Flask(__name__)
CORS(app)  # CORS 설정

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'easygymdb'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/saveResult', methods=['POST'])
def handle_save_result():
    return save_result(request, mysql)


if __name__ == '__main__':
    app.run()
