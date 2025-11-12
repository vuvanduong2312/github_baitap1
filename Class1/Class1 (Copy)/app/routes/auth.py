from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Address

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('Vui lòng điền đầy đủ thông tin!', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email đã được đăng ký!', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(name=name, email=email, phone=phone)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Tài khoản đã bị khóa!', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=remember)
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Email hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất!', 'info')
    return redirect(url_for('main.index'))


@bp.route('/profile')
@login_required
def profile():
    addresses = Address.query.filter_by(user_id=current_user.id).order_by(Address.is_default.desc(), Address.created_at.desc()).all()
    return render_template('profile.html', user=current_user, addresses=addresses)


@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if not current_user.check_password(current_password):
                flash('Mật khẩu hiện tại không đúng!', 'danger')
                return redirect(url_for('auth.edit_profile'))
            
            confirm_password = request.form.get('confirm_password')
            if new_password != confirm_password:
                flash('Mật khẩu mới không khớp!', 'danger')
                return redirect(url_for('auth.edit_profile'))
            
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Cập nhật thông tin thành công!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('edit_profile.html', user=current_user)


@bp.route('/address/add', methods=['GET', 'POST'])
@login_required
def add_address():
    if request.method == 'POST':
        label = request.form.get('label')
        recipient_name = request.form.get('recipient_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        is_default = request.form.get('is_default') == 'on'
        
        if not all([recipient_name, phone, address]):
            flash('Vui lòng điền đầy đủ thông tin!', 'danger')
            return redirect(url_for('auth.add_address'))
        
        # If set as default, remove default from other addresses
        if is_default:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        # If this is the first address, make it default
        if Address.query.filter_by(user_id=current_user.id).count() == 0:
            is_default = True
        
        new_address = Address(
            user_id=current_user.id,
            label=label,
            recipient_name=recipient_name,
            phone=phone,
            address=address,
            is_default=is_default
        )
        
        db.session.add(new_address)
        db.session.commit()
        
        flash('Đã thêm địa chỉ mới!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('add_address.html')


@bp.route('/address/<int:address_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    # Check ownership
    if address.user_id != current_user.id:
        flash('Bạn không có quyền chỉnh sửa địa chỉ này!', 'danger')
        return redirect(url_for('auth.profile'))
    
    if request.method == 'POST':
        address.label = request.form.get('label')
        address.recipient_name = request.form.get('recipient_name')
        address.phone = request.form.get('phone')
        address.address = request.form.get('address')
        is_default = request.form.get('is_default') == 'on'
        
        if is_default and not address.is_default:
            # Remove default from other addresses
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
            address.is_default = True
        elif not is_default and address.is_default:
            # Don't allow removing default if it's the only address
            if Address.query.filter_by(user_id=current_user.id).count() > 1:
                address.is_default = False
            else:
                flash('Phải có ít nhất một địa chỉ mặc định!', 'warning')
        
        db.session.commit()
        flash('Đã cập nhật địa chỉ!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('edit_address.html', address=address)


@bp.route('/address/<int:address_id>/delete', methods=['POST'])
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    # Check ownership
    if address.user_id != current_user.id:
        flash('Bạn không có quyền xóa địa chỉ này!', 'danger')
        return redirect(url_for('auth.profile'))
    
    # If this is default, set another address as default
    if address.is_default:
        other_address = Address.query.filter(
            Address.user_id == current_user.id,
            Address.id != address_id
        ).first()
        
        if other_address:
            other_address.is_default = True
    
    db.session.delete(address)
    db.session.commit()
    
    flash('Đã xóa địa chỉ!', 'info')
    return redirect(url_for('auth.profile'))


@bp.route('/address/<int:address_id>/set_default', methods=['POST'])
@login_required
def set_default_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    # Check ownership
    if address.user_id != current_user.id:
        flash('Bạn không có quyền!', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Remove default from all addresses
    Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
    
    # Set this as default
    address.is_default = True
    db.session.commit()
    
    flash('Đã đặt làm địa chỉ mặc định!', 'success')
    return redirect(url_for('auth.profile'))

