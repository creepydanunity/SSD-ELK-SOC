import ctypes
from logging.handlers import RotatingFileHandler
import time
from flask import Flask, has_request_context, jsonify, request
from sqlalchemy import create_engine, text
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from flask_cors import CORS
from sqlalchemy.exc import OperationalError


class RequestIPFilter(logging.Filter):
    def filter(self, record):
        record.client_ip = request.remote_addr if has_request_context() else '-'
        return True


app = Flask(__name__)

log_directory = '/var/log/backend_logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

if not os.path.exists("/var/log/test_logs"):
    os.makedirs("/var/log/test_logs")

if not os.path.exists("/var/log/test_logs/test.log"):
    open("/var/log/test_logs/test.log", "a").close()

handler = RotatingFileHandler(os.path.join(log_directory, 'app.log'), maxBytes=10000000, backupCount=3)
handler.setLevel(logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(client_ip)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.addFilter(RequestIPFilter())

app.logger.addHandler(handler)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vuln_app:vuln_app@db/onlinestore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

vulnerable_lib = ctypes.CDLL('./libvulnerable.so')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)

@app.route('/')
def home():
    return 'Welcome to the Online Store API!'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')

    app.logger.info(f"Login attempt with username: {username}, password: {password}")

    try:
        query = text(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        result = db.session.execute(query).fetchone()

        if result:
            app.logger.info(f"Login successful for user: {username}")
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            app.logger.warning(f"Invalid login attempt for user: {username}")
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    except Exception as e:
        app.logger.error(f"Error in login attempt for user {username}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        app.logger.info("Fetching all products")
        products = Product.query.all()
        return jsonify([{
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        } for product in products])
    except Exception as e:
        app.logger.error(f"Error fetching products: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if not product:
        app.logger.warning(f"Product not found with ID: {product_id}")
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description
    })

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(
        name=data.get('name'),
        price=data.get('price'),
        description=data.get('description')
    )
    try:
        db.session.add(new_product)
        db.session.commit()
        app.logger.info(f"Product created successfully: {new_product.name}")
        return jsonify({'message': 'Product created successfully'}), 201
    except Exception as e:
        app.logger.error(f"Error creating product: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        app.logger.warning(f"Product not found with ID: {product_id}")
        return jsonify({'error': 'Product not found'}), 404

    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.description = data.get('description', product.description)

    try:
        db.session.commit()
        app.logger.info(f"Product updated successfully: {product.name}")
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating product: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        app.logger.warning(f"Product not found with ID: {product_id}")
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    try:
        db.session.commit()
        app.logger.info(f"Product deleted successfully: {product.name}")
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting product: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/search', methods=['GET'])
def search_products():
    search_query = request.args.get('q', '')
    app.logger.info(f"Search query: {search_query}")

    try:
        query = text(f"SELECT * FROM products WHERE name LIKE '%{search_query}%'")
        result = db.session.execute(query).fetchall()
        products = [{"id": row[0], "name": row[1], "price": row[2], "description": row[3]} for row in result]
        return jsonify(products)
    except Exception as e:
        app.logger.error(f"Error searching products: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/support', methods=['POST'])
def vulnerable_c():
    user_input = request.json.get('input', '')
    app.logger.info(f"Vulnerable C function called with input: {user_input}")

    try:
        c_input = ctypes.create_string_buffer(user_input.encode('utf-8'))
        vulnerable_lib.vulnerable_function(c_input)
        return jsonify({'message': 'Function executed successfully'})
    except Exception as e:
        app.logger.error(f"Error executing vulnerable function: {str(e)}")
        return jsonify({'error': str(e)}), 500

def wait_for_db():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    attempts = 0
    while attempts < 5:
        try:
            with engine.connect() as conn:
                return True
        except OperationalError:
            attempts += 1
            time.sleep(2)
    raise Exception("Failed to connect to database")

if __name__ == '__main__':
    with app.app_context():
        wait_for_db()
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
