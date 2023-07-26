import logging
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from Scraping_Yahoo_Finance import Scraping_Data
import datetime

logging.basicConfig(filename='app.log', filemode='w',level=logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')

app = Flask(__name__)

#MySQL Database connection using SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Talha1234@localhost/finance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#This is a model class of finance_data table in database
class finance_data(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Symbol = db.Column(db.String(50))
    Name = db.Column(db.String(200))
    URL = db.Column(db.String(500))
    Last_Price = db.Column(db.String(50))
    Change_ = db.Column(db.String(50))
    Percentage_Change = db.Column(db.String(50))
    Timestamp = db.Column(db.DateTime)

def create_or_recreate_table():
    '''This function is for table creation in database, it will check if the table is not exist then create it.
    And if table exist first it will drop the table and then create the table
    '''
    with app.app_context():
        try:
            insp = inspect(db.engine)
            if insp.has_table(finance_data.__tablename__):
                finance_data.__table__.drop(db.engine)
            db.create_all()
        except Exception as e:
            logging.error(f"Error creating or recreating table: {str(e)}")


@app.route('/fetch-data/', methods=['POST'])
def fetch_data_and_store():
    try:
        create_or_recreate_table()
        data = Scraping_Data()
        for item in data:
            finance_item = finance_data(
                Symbol=item['Symbol'],
                Name=item['Name'],
                URL=item['URL'],
                Last_Price=item['Last_Price'],
                Change_=item['Change_'],
                Percentage_Change=item['Percentage_Change'],
                Timestamp = item['TimeStamp']
            )
            db.session.add(finance_item)

        db.session.commit()
        return jsonify({'message': 'Data fetched and stored successfully','data':data})
    except Exception as e:
        logging.error(f"Error fetching data and storing: {str(e)}")
        return jsonify({'error': 'Something went wrong.'}), 500
    
# Endpoint to get all books from the database
@app.route('/get-all-data/', methods=['GET'])
def get_all_data():
    try:
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
                'percentage_change': row.Percentage_Change,
                'Timestamp': row.Timestamp
            }
            Finance_data.append(data)
        return jsonify(Finance_data)
    except Exception as e:
        logging.error(f"Error getting all data: {str(e)}")
        return jsonify({'error': 'Something went wrong.'}), 500
    
@app.route('/get-specific-record/<int:record_id>/', methods=['GET'])
def get_specific_record(record_id):
    try:
        record = db.session.query(finance_data).filter_by(Id=record_id).first()
        if not record:
            return jsonify({'message': 'Record not found'}), 404

        data = {
            'Id': record.Id,
            'Symbol': record.Symbol,
            'Name': record.Name,
            'URL': record.URL,
            'Last_Price': record.Last_Price,
            'Change_': record.Change_,
            'Percentage_Change': record.Percentage_Change,
            'Timestamp': record.Timestamp
        }
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting all data: {str(e)}")
        return jsonify({'error': 'Something went wrong.'}), 500

@app.route('/add-data/', methods=['POST'])
def add_data():
    try:
        data = finance_data(
            Symbol=request.json['symbol'],
            Name=request.json['name'],
            URL=request.json['url'],
            Last_Price=request.json['last_price'],
            Change_=request.json['change_'],
            Percentage_Change=request.json['percentage_change'],
            Timestamp = request.json['timestamp'])
        db.session.add(data)
        db.session.commit()
        return {'id': data.Id}
    except KeyError as ke:
        logging.error(f"KeyError in add_data: {str(ke)}")
        return jsonify({'error': 'One or more required fields are missing.'}), 400
    except Exception as e:
        logging.error(f"Error adding data: {str(e)}")
        return jsonify({'error': 'Something went wrong.'}), 500

@app.route('/update-record/<int:record_id>/', methods=['PUT'])
def update_record(record_id):
    try:
        record = db.session.query(finance_data).filter_by(Id=record_id).first()
        if not record:
            return jsonify({'message': 'Record not found'}), 404

        record.Symbol = request.json['symbol']
        record.Name = request.json['name']
        record.URL = request.json['url']
        record.Last_Price = request.json['last_price']
        record.Change_ = request.json['change_']
        record.Percentage_Change = request.json['percentage_change']
        record.Timestamp = request.json['timestamp']

        db.session.commit()
        return jsonify({'message': 'Record updated successfully'})
    except KeyError as ke:
        logging.error(f"KeyError in update_record: {str(ke)}")
        return jsonify({'error': 'One or more required fields are missing.'}), 400
    except Exception as e:
        logging.error(f"Error updating record: {str(e)}")
        return jsonify({'error': 'Something went wrong.'}), 500

@app.route('/delete-record/<int:record_id>/', methods=['DELETE'])
def delete_record(record_id):
    try:
        record = db.session.query(finance_data).filter_by(Id=record_id).first()
        if not record:
            return jsonify({'message': 'Record not found'}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully'})
    except Exception as e:
        logging.error(f"Error deleting record: {str(e)}")
        return jsonify({'error': 'Something went wrong.'}), 500
    
if __name__ == "__main__":
    app.run()