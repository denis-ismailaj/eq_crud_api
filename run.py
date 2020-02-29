from eq import app
from peewee import *
from instance.config import *


def init():
    mysql_db = MySQLDatabase('earthquakedb', user='root', password='my-secret-pw', host=MYSQL_IP, port=MYSQL_PORT)
    print(mysql_db.connection())


if __name__ == '__main__':
    init()


app.run(debug=True)
