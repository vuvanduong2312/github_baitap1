from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app import db
from app.models import Book, Category, Author, Order, OrderDetail, CartItem
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    books = Book.query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('index.html', books=books, categories=categories)


@bp.route('/books')
def books():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    author_id = request.args.get('author', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'newest')
    per_page = 12
    
    query = Book.query
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    if author_id:
        query = query.filter_by(author_id=author_id)
    if min_price:
        query = query.filter(Book.price >= min_price)
    if max_price:
        query = query.filter(Book.price <= max_price)
    
    # Apply sorting
    if sort == 'newest':
        query = query.order_by(Book.created_at.desc())
    elif sort == 'price_asc':
        query = query.order_by(Book.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Book.price.desc())
    elif sort == 'title':
        query = query.order_by(Book.title.asc())
    
    books = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = Category.query.all()
    authors = Author.query.all()
    
    return render_template('books.html', books=books, categories=categories, 
                         authors=authors, current_category=category_id,
                         current_author=author_id, current_sort=sort)


@bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    related_books = Book.query.filter(
        Book.category_id == book.category_id,
        Book.id != book.id
    ).limit(4).all()
    
    return render_template('book_detail.html', book=book, related_books=related_books)


@bp.route('/search')
def search():
    query_str = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    if query_str:
        books = Book.query.join(Author).filter(
            or_(
                Book.title.contains(query_str),
                Author.name.contains(query_str),
                Book.description.contains(query_str)
            )
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('search.html', books=books, query=query_str)


@bp.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    books_in_cart = []
    total = 0
    
    for item in cart_items:
        if item.book:
            subtotal = item.book.price * item.quantity
            books_in_cart.append({
                'book': item.book,
                'quantity': item.quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('cart.html', cart_items=books_in_cart, total=total)


@bp.route('/cart/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)
    quantity = request.form.get('quantity', 1, type=int)
    
    if book.stock < quantity:
        flash('Không đủ hàng trong kho!', 'danger')
        return redirect(request.referrer or url_for('main.index'))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if cart_item:
        new_quantity = cart_item.quantity + quantity
        if book.stock < new_quantity:
            flash('Không đủ hàng trong kho!', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(user_id=current_user.id, book_id=book_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'Đã thêm "{book.title}" vào giỏ hàng!', 'success')
    return redirect(request.referrer or url_for('main.index'))


@bp.route('/cart/update/<int:book_id>', methods=['POST'])
@login_required
def update_cart(book_id):
    quantity = request.form.get('quantity', 0, type=int)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if not cart_item:
        flash('Sản phẩm không có trong giỏ hàng!', 'danger')
        return redirect(url_for('main.cart'))
    
    if quantity <= 0:
        db.session.delete(cart_item)
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'info')
    else:
        book = Book.query.get(book_id)
        if book and book.stock >= quantity:
            cart_item.quantity = quantity
            flash('Đã cập nhật giỏ hàng!', 'success')
        else:
            flash('Không đủ hàng trong kho!', 'danger')
            return redirect(url_for('main.cart'))
    
    db.session.commit()
    return redirect(url_for('main.cart'))


@bp.route('/cart/remove/<int:book_id>')
@login_required
def remove_from_cart(book_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'info')
    
    return redirect(url_for('main.cart'))


@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Giỏ hàng trống!', 'warning')
        return redirect(url_for('main.cart'))
    
    if request.method == 'POST':
        # Get shipping information
        shipping_name = request.form.get('shipping_name')
        shipping_phone = request.form.get('shipping_phone')
        shipping_address = request.form.get('shipping_address')
        payment_method = request.form.get('payment_method', 'COD')
        
        # Validate stock and calculate total
        total = 0
        order_items = []
        
        for cart_item in cart_items:
            book = cart_item.book
            if not book:
                flash(f'Sách không tồn tại!', 'danger')
                return redirect(url_for('main.cart'))
            
            if book.stock < cart_item.quantity:
                flash(f'Không đủ hàng cho "{book.title}"!', 'danger')
                return redirect(url_for('main.cart'))
            
            order_items.append({
                'book': book,
                'quantity': cart_item.quantity,
                'price': book.price
            })
            total += book.price * cart_item.quantity
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_name=shipping_name,
            shipping_phone=shipping_phone,
            shipping_address=shipping_address,
            payment_method=payment_method,
            status='Chờ xử lý'
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order details and update stock
        for item in order_items:
            order_detail = OrderDetail(
                order_id=order.id,
                book_id=item['book'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_detail)
            
            # Update stock
            item['book'].stock -= item['quantity']
        
        # Clear cart from database
        for cart_item in cart_items:
            db.session.delete(cart_item)
        
        db.session.commit()
        
        flash(f'Đặt hàng thành công! Mã đơn hàng: {order.id}', 'success')
        return redirect(url_for('main.order_detail', order_id=order.id))
    
    # GET request - show checkout form
    books_in_cart = []
    total = 0
    
    for cart_item in cart_items:
        if cart_item.book:
            subtotal = cart_item.book.price * cart_item.quantity
            books_in_cart.append({
                'book': cart_item.book,
                'quantity': cart_item.quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('checkout.html', cart_items=books_in_cart, total=total, user=current_user)


@bp.route('/orders')
@login_required
def my_orders():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    orders = Order.query.filter_by(user_id=current_user.id).order_by(
        Order.order_date.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('my_orders.html', orders=orders)


@bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order or is admin
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền xem đơn hàng này!', 'danger')
        return redirect(url_for('main.index'))
    
    order_details = OrderDetail.query.filter_by(order_id=order_id).all()
    
    return render_template('order_detail.html', order=order, order_details=order_details)


@bp.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check ownership
    if order.user_id != current_user.id:
        flash('Bạn không có quyền hủy đơn hàng này!', 'danger')
        return redirect(url_for('main.my_orders'))
    
    # Only allow canceling if status is "Chờ xử lý"
    if order.status != 'Chờ xử lý':
        flash('Không thể hủy đơn hàng ở trạng thái này!', 'danger')
        return redirect(url_for('main.order_detail', order_id=order_id))
    
    # Return stock
    for detail in order.order_details:
        detail.book.stock += detail.quantity
    
    # Update order status
    order.status = 'Đã hủy'
    db.session.commit()
    
    flash('Đã hủy đơn hàng thành công!', 'success')
    return redirect(url_for('main.order_detail', order_id=order_id))
