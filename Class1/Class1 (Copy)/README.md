## Tính năng

### Dành cho Người dùng
-  Đăng ký / Đăng nhập
- Xem và tìm kiếm sách
- Lọc theo thể loại, tác giả, giá
- Thêm vào giỏ hàng
- Đặt hàng và thanh toán
- Theo dõi đơn hàng
- Quản lý hồ sơ cá nhân

### Dành cho Quản trị viên
- Dashboard tổng quan
- Quản lý sách (thêm, sửa, xóa)
- Quản lý thể loại
- Quản lý tác giả
- Quản lý đơn hàng
- Quản lý khách hàng
- Báo cáo doanh thu
- Cảnh báo tồn kho

## Công nghệ sử dụng

- **Backend**: Python Flask 3.0
- **Database**: SQLite với SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Authentication**: Flask-Login

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên


## Thông tin đăng nhập

### Tài khoản Admin
- **Email**: admin@bookstore.com
- **Mật khẩu**: admin123
- **Quyền**: Truy cập tất cả chức năng quản trị

### Tài khoản User (test)
- **Email**: user@example.com
- **Mật khẩu**: user123
- **Quyền**: Mua hàng, xem đơn hàng





### Public Routes
- `GET /` - Trang chủ
- `GET /books` - Danh sách sách
- `GET /book/<id>` - Chi tiết sách
- `GET /search` - Tìm kiếm
- `GET /auth/register` - Đăng ký
- `GET /auth/login` - Đăng nhập

### Protected Routes (Login required)
- `GET /cart` - Giỏ hàng
- `POST /cart/add/<id>` - Thêm vào giỏ
- `GET /checkout` - Thanh toán
- `GET /orders` - Đơn hàng của tôi
- `GET /auth/profile` - Hồ sơ

### Admin Routes (Admin only)
- `GET /admin/dashboard` - Bảng điều khiển
- `GET /admin/books` - Quản lý sách
- `GET /admin/orders` - Quản lý đơn hàng
- `GET /admin/customers` - Quản lý khách hàng
- `GET /admin/reports` - Báo cáo



### Thay đổi Database
Trong `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/dbname'
```

### Thêm dữ liệu mẫu
Chỉnh sửa file `init_db.py` để thêm sách, thể loại, tác giả.


