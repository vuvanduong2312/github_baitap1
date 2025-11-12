from app import create_app, db
from app.models import User, Book, Category, Author, Order, OrderDetail

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
