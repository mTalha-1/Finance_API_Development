from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Talha1234@localhost/finance'
db = SQLAlchemy(app)

class finance_data(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Symbol = db.Column(db.String(50))
    Name = db.Column(db.String(200))
    URL = db.Column(db.String(500))
    Last_Price = db.Column(db.String(50))
    Change_ = db.Column(db.String(50))
    Percentage_Change = db.Column(db.String(50))

# Endpoint to get all books from the database
@app.route('/api/finance', methods=['GET'])
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
    app.run(debug=True)