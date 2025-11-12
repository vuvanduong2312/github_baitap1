from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Book, Category, Author, Order, OrderDetail, User, Address
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bạn không có quyền truy cập trang này!', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Statistics
    total_books = Book.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='Chờ xử lý').count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
    
    # Low stock books
    low_stock_books = Book.query.filter(Book.stock <= 5).order_by(Book.stock.asc()).limit(10).all()
    
    # Revenue statistics (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    revenue_query = db.session.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.status == 'Đã giao',
        Order.order_date >= thirty_days_ago
    ).scalar()
    
    total_revenue = revenue_query if revenue_query else 0
    
    return render_template('admin/dashboard.html', 
                         total_books=total_books,
                         total_users=total_users,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders,
                         low_stock_books=low_stock_books,
                         total_revenue=total_revenue)


# ===== BOOK MANAGEMENT =====
@bp.route('/books')
@login_required
@admin_required
def books():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    books = Book.query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/books.html', books=books)


@bp.route('/books/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author_id = request.form.get('author_id', type=int)
        category_id = request.form.get('category_id', type=int)
        publisher = request.form.get('publisher')
        year = request.form.get('year', type=int)
        price = request.form.get('price', type=float)
        stock = request.form.get('stock', type=int)
        description = request.form.get('description')
        image_url = request.form.get('image_url', 'default-book.jpg')
        
        book = Book(
            title=title,
            author_id=author_id,
            category_id=category_id,
            publisher=publisher,
            year=year,
            price=price,
            stock=stock,
            description=description,
            image_url=image_url
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash(f'Đã thêm sách "{title}"!', 'success')
        return redirect(url_for('admin.books'))
    
    categories = Category.query.order_by(Category.name).all()
    authors = Author.query.order_by(Author.name).all()
    
    return render_template('admin/add_book.html', categories=categories, authors=authors)


@bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author_id = request.form.get('author_id', type=int)
        book.category_id = request.form.get('category_id', type=int)
        book.publisher = request.form.get('publisher')
        book.year = request.form.get('year', type=int)
        book.price = request.form.get('price', type=float)
        book.stock = request.form.get('stock', type=int)
        book.description = request.form.get('description')
        book.image_url = request.form.get('image_url')
        
        db.session.commit()
        
        flash(f'Đã cập nhật sách "{book.title}"!', 'success')
        return redirect(url_for('admin.books'))
    
    categories = Category.query.order_by(Category.name).all()
    authors = Author.query.order_by(Author.name).all()
    
    return render_template('admin/edit_book.html', book=book, categories=categories, authors=authors)


@bp.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if book has orders
    if book.order_details.count() > 0:
        flash('Không thể xóa sách đã có đơn hàng!', 'danger')
        return redirect(url_for('admin.books'))
    
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Đã xóa sách "{book.title}"!', 'info')
    return redirect(url_for('admin.books'))


# ===== CATEGORY MANAGEMENT =====
@bp.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories)


@bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if Category.query.filter_by(name=name).first():
            flash('Thể loại đã tồn tại!', 'danger')
            return redirect(url_for('admin.add_category'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash(f'Đã thêm thể loại "{name}"!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/add_category.html')


@bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        
        if name != category.name and Category.query.filter_by(name=name).first():
            flash('Tên thể loại đã tồn tại!', 'danger')
            return redirect(url_for('admin.edit_category', category_id=category_id))
        
        category.name = name
        category.description = request.form.get('description')
        
        db.session.commit()
        flash(f'Đã cập nhật thể loại "{name}"!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/edit_category.html', category=category)


@bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if category.books.count() > 0:
        flash('Không thể xóa thể loại có sách!', 'danger')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash(f'Đã xóa thể loại "{category.name}"!', 'info')
    return redirect(url_for('admin.categories'))


# ===== AUTHOR MANAGEMENT =====
@bp.route('/authors')
@login_required
@admin_required
def authors():
    authors = Author.query.order_by(Author.name).all()
    return render_template('admin/authors.html', authors=authors)


@bp.route('/authors/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        bio = request.form.get('bio')
        
        if Author.query.filter_by(name=name).first():
            flash('Tác giả đã tồn tại!', 'danger')
            return redirect(url_for('admin.add_author'))
        
        author = Author(name=name, bio=bio)
        db.session.add(author)
        db.session.commit()
        
        flash(f'Đã thêm tác giả "{name}"!', 'success')
        return redirect(url_for('admin.authors'))
    
    return render_template('admin/add_author.html')


@bp.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        
        if name != author.name and Author.query.filter_by(name=name).first():
            flash('Tên tác giả đã tồn tại!', 'danger')
            return redirect(url_for('admin.edit_author', author_id=author_id))
        
        author.name = name
        author.bio = request.form.get('bio')
        
        db.session.commit()
        flash(f'Đã cập nhật tác giả "{name}"!', 'success')
        return redirect(url_for('admin.authors'))
    
    return render_template('admin/edit_author.html', author=author)


@bp.route('/authors/delete/<int:author_id>', methods=['POST'])
@login_required
@admin_required
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    
    if author.books.count() > 0:
        flash('Không thể xóa tác giả có sách!', 'danger')
        return redirect(url_for('admin.authors'))
    
    db.session.delete(author)
    db.session.commit()
    
    flash(f'Đã xóa tác giả "{author.name}"!', 'info')
    return redirect(url_for('admin.authors'))


# ===== ORDER MANAGEMENT =====
@bp.route('/orders')
@login_required
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status')
    per_page = 20
    
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(Order.order_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, current_status=status_filter)


@bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    order_details = OrderDetail.query.filter_by(order_id=order_id).all()
    
    return render_template('admin/order_detail.html', order=order, order_details=order_details)


@bp.route('/orders/<int:order_id>/confirm', methods=['POST'])
@login_required
@admin_required
def confirm_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.status != 'Chờ xử lý':
        flash('Chỉ có thể xác nhận đơn hàng đang chờ xử lý!', 'danger')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    
    order.status = 'Đang giao'
    db.session.commit()
    
    flash(f'Đã chuyển đơn hàng #{order.id} sang trạng thái Đang giao!', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))


@bp.route('/orders/<int:order_id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = ['Chờ xử lý', 'Đang giao', 'Đã giao', 'Giao thất bại']
    if new_status not in valid_statuses:
        flash('Trạng thái không hợp lệ!', 'danger')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    
    old_status = order.status
    
    # Nếu chuyển sang "Giao thất bại", hoàn hàng về kho
    if new_status == 'Giao thất bại' and old_status != 'Giao thất bại':
        for detail in order.order_details:
            detail.book.stock += detail.quantity
        flash(f'Đã hoàn {sum(d.quantity for d in order.order_details)} sản phẩm về kho!', 'info')
    
    # Nếu từ "Giao thất bại" chuyển sang trạng thái khác, trừ lại kho
    if old_status == 'Giao thất bại' and new_status != 'Giao thất bại':
        for detail in order.order_details:
            if detail.book.stock < detail.quantity:
                flash(f'Không đủ hàng trong kho để cập nhật trạng thái!', 'danger')
                return redirect(url_for('admin.order_detail', order_id=order_id))
            detail.book.stock -= detail.quantity
    
    order.status = new_status
    db.session.commit()
    
    flash(f'Đã cập nhật trạng thái đơn hàng #{order.id} thành "{new_status}"!', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))


@bp.route('/orders/<int:order_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.status != 'Đã giao':
        flash('Chỉ có thể xóa đơn hàng đã giao!', 'danger')
        return redirect(url_for('admin.orders'))
    
    db.session.delete(order)
    db.session.commit()
    
    flash(f'Đã xóa đơn hàng #{order.id}!', 'info')
    return redirect(url_for('admin.orders'))


# ===== CUSTOMER MANAGEMENT =====
@bp.route('/customers')
@login_required
@admin_required
def customers():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    customers = User.query.filter_by(is_admin=False).order_by(
        User.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/customers.html', customers=customers)


@bp.route('/customers/<int:user_id>')
@login_required
@admin_required
def customer_detail(user_id):
    customer = User.query.get_or_404(user_id)
    
    if customer.is_admin:
        flash('Không thể xem chi tiết quản trị viên!', 'danger')
        return redirect(url_for('admin.customers'))
    
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()
    addresses = Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc(), Address.created_at.desc()).all()
    
    return render_template('admin/customer_detail.html', customer=customer, orders=orders, addresses=addresses)


@bp.route('/customers/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_customer(user_id):
    customer = User.query.get_or_404(user_id)
    
    if customer.is_admin:
        flash('Không thể khóa tài khoản quản trị viên!', 'danger')
        return redirect(url_for('admin.customers'))
    
    customer.is_active = not customer.is_active
    db.session.commit()
    
    status = 'mở khóa' if customer.is_active else 'khóa'
    flash(f'Đã {status} tài khoản {customer.email}!', 'success')
    
    return redirect(url_for('admin.customer_detail', user_id=user_id))


# ===== REPORTS =====
@bp.route('/reports')
@login_required
@admin_required
def reports():
    # Date range
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total revenue
    revenue_query = db.session.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.status == 'Đã giao',
        Order.order_date >= start_date
    ).scalar()
    
    total_revenue = revenue_query if revenue_query else 0
    
    # Orders count
    total_orders = Order.query.filter(Order.order_date >= start_date).count()
    completed_orders = Order.query.filter(
        Order.status == 'Đã giao',
        Order.order_date >= start_date
    ).count()
    
    # Best selling books
    best_sellers = db.session.query(
        Book.id,
        Book.title,
        Author.name.label('author_name'),
        func.sum(OrderDetail.quantity).label('total_sold')
    ).join(
        OrderDetail, Book.id == OrderDetail.book_id
    ).join(
        Order, OrderDetail.order_id == Order.id
    ).join(
        Author, Book.author_id == Author.id
    ).filter(
        Order.status == 'Đã giao',
        Order.order_date >= start_date
    ).group_by(
        Book.id, Book.title, Author.name
    ).order_by(
        func.sum(OrderDetail.quantity).desc()
    ).limit(10).all()
    
    # Low stock alert
    low_stock = Book.query.filter(Book.stock <= 5).order_by(Book.stock.asc()).all()
    
    return render_template('admin/reports.html',
                         total_revenue=total_revenue,
                         total_orders=total_orders,
                         completed_orders=completed_orders,
                         best_sellers=best_sellers,
                         low_stock=low_stock,
                         days=days)
