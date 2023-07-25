from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from Scraping_Yahoo_Finance import Scraping_Data

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Talha1234@localhost/finance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class finance_data(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Symbol = db.Column(db.String(50))
    Name = db.Column(db.String(200))
    URL = db.Column(db.String(500))
    Last_Price = db.Column(db.String(50))
    Change_ = db.Column(db.String(50))
    Percentage_Change = db.Column(db.String(50))

def create_or_recreate_table():
    with app.app_context():
        insp = inspect(db.engine)
        if insp.has_table(finance_data.__tablename__):
            finance_data.__table__.drop(db.engine)
        db.create_all()


@app.route('/fetch-data/', methods=['POST'])
def fetch_data_and_store():
    create_or_recreate_table()
    data = Scraping_Data()
    for item in data:
        finance_item = finance_data(
            Symbol=item['Symbol'],
            Name=item['Name'],
            URL=item['URL'],
            Last_Price=item['Last_Price'],
            Change_=item['Change_'],
            Percentage_Change=item['Percentage_Change']
        )
        db.session.add(finance_item)

    db.session.commit()
    return jsonify({'message': 'Data fetched and stored successfully','data':data})

# Endpoint to get all books from the database
@app.route('/get-all-data/', methods=['GET'])
def get_all_data():
    result = finance_data.query.all()
    Finance_data = []
    for row in result:
        data = {
            'id': row.Id,
            'symbol': row.Symbol,
            'name': row.Name,
            'url': row.URL,
            'last_price': row.Last_Price,
            'change_': row.Change_,
            'percentage_change': row.Percentage_Change
        }
        Finance_data.append(data)
    return jsonify(Finance_data)

if __name__ == "__main__":
    app.run()