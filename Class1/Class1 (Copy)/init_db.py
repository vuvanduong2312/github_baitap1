from app import create_app, db
from app.models import User, Book, Category, Author
from datetime import datetime

def init_db():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("Database tables created!")
        
        # Create admin user
        admin = User(
            name='Admin',
            email='admin@bookstore.com',
            phone='0123456789',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create test user
        user = User(
            name='Nguyễn Văn A',
            email='user@example.com',
            phone='0987654321',
            is_admin=False
        )
        user.set_password('user123')
        db.session.add(user)
        
        print("Admin and test user created!")
        
        # Create categories
        categories_data = [
            {'name': 'Văn học', 'description': 'Sách văn học trong và ngoài nước'},
            {'name': 'Kinh tế', 'description': 'Sách về kinh tế, kinh doanh'},
            {'name': 'Kỹ năng sống', 'description': 'Sách phát triển bản thân'},
            {'name': 'Thiếu nhi', 'description': 'Sách dành cho trẻ em'},
            {'name': 'Khoa học', 'description': 'Sách khoa học, công nghệ'},
            {'name': 'Lịch sử', 'description': 'Sách lịch sử Việt Nam và thế giới'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat = Category(**cat_data)
            db.session.add(cat)
            categories.append(cat)
        
        db.session.flush()
        print(f"Created {len(categories)} categories!")
        
        # Create authors
        authors_data = [
            {'name': 'Nguyễn Nhật Ánh', 'bio': 'Nhà văn nổi tiếng Việt Nam'},
            {'name': 'Paulo Coelho', 'bio': 'Nhà văn Brazil nổi tiếng'},
            {'name': 'Dale Carnegie', 'bio': 'Chuyên gia về phát triển bản thân'},
            {'name': 'Haruki Murakami', 'bio': 'Nhà văn Nhật Bản'},
            {'name': 'Tô Hoài', 'bio': 'Nhà văn Việt Nam'},
            {'name': 'Napoleon Hill', 'bio': 'Tác giả về thành công'},
            {'name': 'Yuval Noah Harari', 'bio': 'Nhà sử học người Israel'},
            {'name': 'Robert Kiyosaki', 'bio': 'Doanh nhân và nhà đầu tư'},
        ]
        
        authors = []
        for author_data in authors_data:
            author = Author(**author_data)
            db.session.add(author)
            authors.append(author)
        
        db.session.flush()
        print(f"Created {len(authors)} authors!")
        
        # Create books
        books_data = [
            {
                'title': 'Mắt Biếc',
                'author_id': 1,
                'category_id': 1,
                'publisher': 'NXB Trẻ',
                'year': 2020,
                'price': 95000,
                'stock': 50,
                'description': 'Mắt biếc là một truyện ngắn nổi tiếng của nhà văn Nguyễn Nhật Ánh.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/5e/18/24/2a6154ba3e93db9a0c60766e8e5f4973.jpg'
            },
            {
                'title': 'Cho Tôi Xin Một Vé Đi Tuổi Thơ',
                'author_id': 1,
                'category_id': 1,
                'publisher': 'NXB Trẻ',
                'year': 2018,
                'price': 82000,
                'stock': 30,
                'description': 'Truyện kể về những kỷ niệm tuổi thơ dữ dội, với vô số trò tinh nghịch.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/31/1d/b6/6f3666c42c6bd6b991ce5c2dbdaa6b74.jpg'
            },
            {
                'title': 'Nhà Giả Kim',
                'author_id': 2,
                'category_id': 3,
                'publisher': 'NXB Hội Nhà Văn',
                'year': 2019,
                'price': 79000,
                'stock': 45,
                'description': 'Cuốn sách nổi tiếng của Paulo Coelho về hành trình tìm kiếm ước mơ.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/45/3b/fc/aa81d0a534b45706ae1eee1e344e80d9.jpg'
            },
            {
                'title': 'Đắc Nhân Tâm',
                'author_id': 3,
                'category_id': 3,
                'publisher': 'NXB Tổng Hợp',
                'year': 2020,
                'price': 86000,
                'stock': 60,
                'description': 'Nghệ thuật thu phục lòng người của Dale Carnegie.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/d0/c7/21/6b3e3c6c4e98f6d8d5b3e5c3e5f3e5f3.jpg'
            },
            {
                'title': 'Kafka Bên Bờ Biển',
                'author_id': 4,
                'category_id': 1,
                'publisher': 'NXB Hội Nhà Văn',
                'year': 2019,
                'price': 139000,
                'stock': 25,
                'description': 'Tiểu thuyết nổi tiếng của Haruki Murakami.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/ca/31/81/8a2d0b8c7b1b4c9b8c7b1b4c9b8c7b1b.jpg'
            },
            {
                'title': 'Dế Mèn Phiêu Lưu Ký',
                'author_id': 5,
                'category_id': 4,
                'publisher': 'NXB Kim Đồng',
                'year': 2020,
                'price': 68000,
                'stock': 40,
                'description': 'Tác phẩm kinh điển của văn học thiếu nhi Việt Nam.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/bb/3b/fc/aa81d0a534b45706ae1eee1e344e80d9.jpg'
            },
            {
                'title': '13 Nguyên Tắc Nghĩ Giàu Làm Giàu',
                'author_id': 6,
                'category_id': 2,
                'publisher': 'NXB Lao Động',
                'year': 2019,
                'price': 89000,
                'stock': 35,
                'description': 'Bí quyết thành công từ Napoleon Hill.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/5e/18/24/2a6154ba3e93db9a0c60766e8e5f4973.jpg'
            },
            {
                'title': 'Sapiens: Lược Sử Loài Người',
                'author_id': 7,
                'category_id': 6,
                'publisher': 'NXB Thế Giới',
                'year': 2018,
                'price': 189000,
                'stock': 20,
                'description': 'Cuốn sách về lịch sử loài người từ thời kỳ đồ đá.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/d0/c7/21/6b3e3c6c4e98f6d8d5b3e5c3e5f3e5f3.jpg'
            },
            {
                'title': 'Cha Giàu Cha Nghèo',
                'author_id': 8,
                'category_id': 2,
                'publisher': 'NXB Lao Động',
                'year': 2020,
                'price': 99000,
                'stock': 55,
                'description': 'Cuốn sách về tư duy tài chính của Robert Kiyosaki.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/ca/31/81/8a2d0b8c7b1b4c9b8c7b1b4c9b8c7b1b.jpg'
            },
            {
                'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
                'author_id': 1,
                'category_id': 1,
                'publisher': 'NXB Trẻ',
                'year': 2021,
                'price': 108000,
                'stock': 38,
                'description': 'Truyện về tuổi thơ dữ dội với biết bao trò tinh nghịch.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/31/1d/b6/6f3666c42c6bd6b991ce5c2dbdaa6b74.jpg'
            },
            {
                'title': 'Homo Deus: Lược Sử Tương Lai',
                'author_id': 7,
                'category_id': 5,
                'publisher': 'NXB Thế Giới',
                'year': 2019,
                'price': 199000,
                'stock': 15,
                'description': 'Tương lai của loài người trong thế kỷ 21.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/bb/3b/fc/aa81d0a534b45706ae1eee1e344e80d9.jpg'
            },
            {
                'title': 'Norwegian Wood',
                'author_id': 4,
                'category_id': 1,
                'publisher': 'NXB Hội Nhà Văn',
                'year': 2020,
                'price': 129000,
                'stock': 28,
                'description': 'Rừng Na Uy - câu chuyện tình buồn của Murakami.',
                'image_url': 'https://salt.tikicdn.com/cache/280x280/ts/product/5e/18/24/2a6154ba3e93db9a0c60766e8e5f4973.jpg'
            },
        ]
        
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
        
        db.session.commit()
        print(f"Created {len(books_data)} books!")
        
        print("\n" + "="*50)
        print("Database initialization completed!")
        print("="*50)
        print("\nLogin credentials:")
        print("Admin:")
        print("  Email: admin@bookstore.com")
        print("  Password: admin123")
        print("\nTest User:")
        print("  Email: user@example.com")
        print("  Password: user123")
        print("="*50)

if __name__ == '__main__':
    init_db()
