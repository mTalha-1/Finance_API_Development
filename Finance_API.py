from flask import Flask,jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Talha1234',
    database='finance'
)

def execute_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


# Endpoint to get all books from the database
@app.route('/api/finance', methods=['GET'])
def get_all_data():
    query = 'SELECT * FROM finance_data;'
    result = execute_query(query)
    Finance_data = []
    for row in result:
        data = {
            'id': row[0],
            'symbol': row[1],
            'name': row[2],
            'url': row[3],
            'last_price': row[4],
            'change_': row[5],
            'percentage_change': row[6]
        }
        Finance_data.append(data)
    return jsonify(Finance_data)

# # Endpoint to get a specific book by its ID from the database
# @app.route('/api/books/<int:Id>', methods=['GET'])
# def get_book_by_id(Id):
#     cursor = get_db_connection()
#     cursor.execute('SELECT * FROM finance_data WHERE id = ?', (Id,))
#     row = cursor.fetchone()
#     cursor.close()
#     if row:
#         return jsonify(dict(row))
#     else:
#         return jsonify({'message': 'Book not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)