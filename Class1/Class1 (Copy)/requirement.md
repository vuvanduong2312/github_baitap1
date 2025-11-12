PHÂN TÍCH YÊU CẦU HỆ THỐNG BÁN HÀNG ĐƠN GIẢN 

 

1. Giới thiệu 

Lý do chọn đề tài: Xu hướng thương mại điện tử, nhu cầu mua bán trực tuyến ngày càng tăng. 

Mục tiêu: Xây dựng một website bán hàng trực tuyến hỗ trợ quản lý sản phẩm, đơn hàng và khách hàng. 

Đối tượng sử dụng: Người mua (khách hàng) và Người quản trị (Admin). 

2. Phạm vi đề tài 

Xây dựng hệ thống bán hàng cơ bản, gồm: 

o   Quản lý sản phẩm. 

o   Giỏ hàng & thanh toán. 

o   Quản lý đơn hàng. 

o   Trang quản trị (Admin). 

Ngoại phạm vi: Chưa tích hợp cổng thanh toán trực tuyến (VNPay, PayPal); chỉ mô phỏng trạng thái thanh toán. 

3. Mô tả nghiệp vụ 

Ngữ cảnh hoạt động: Khách chọn sách → thêm giỏ → điền thông tin giao hàng → xác nhận đặt → hệ thống tạo đơn ở trạng thái “Chờ xử lý” → nhân viên xử lý/giao → Admin cập nhật “Đã giao” và lưu lịch sử. 

Tác nhân liên quan: 

Khách hàng: Người mua sản phẩm. 

Quản Trị viên: Quản lý sách/thể loại/tác giả/tồn kho, khách hàng, đơn hàng, báo cáo doanh thu. 

 

 

 

ĐẶC TẢ YÊU CẦU – WEBSITE BÁN SÁCH ONLINE 

1.Chức Năng Dành Cho Người Dùng 

 Đăng kí/ Đăng Nhập 

 

Nhập vào 

Người dùng nhập thông tin vào form đăng ký: họ tên, email, mật khẩu, số điện thoại. 

Đăng nhập bằng email và mật khẩu. 

 

Xử lý 

Kiểm tra tính hợp lệ của thông tin. 

Nếu hợp lệ, lưu vào cơ sở dữ liệu. 

Đăng nhập xác thực thông tin và tạo phiên làm việc. 

 

Hiển thị 

Thông báo đăng ký thành công hoặc yêu cầu nhập lại nếu lỗi. 

Nếu đăng nhập thành công, chuyển hướng đến trang chủ hoặc tài khoản cá nhân. 

 

 

Xem sản phẩm, tìm kiếm, thêm vào giỏ hàng 

Xem sản phẩm  

Nhập vào 

Người dùng truy cập danh mục sách. 

Duyệt danh sách theo thể loại, tác giả, nhà xuất bản. 

 

Xử lý 

Truy vấn cơ sở dữ liệu để lấy danh sách sách. 

Phân trang và sắp xếp theo tiêu chí mặc định (mới nhất, phổ biến…). 

Hiển thị 

Hiển thị danh sách sách với thông tin cơ bản: tiêu đề, giá, ảnh bìa, mô tả ngắn. 

 

Tìm kiếm sách 

Nhập vào 

 Người dùng nhập từ khóa vào ô tìm kiếm. 

Có thể chọn thêm bộ lọc: thể loại, tác giả, khoảng giá, năm xuất bản. 

Xử lý 

Truy vấn cơ sở dữ liệu theo từ khóa và bộ lọc. 

Sắp xếp kết quả theo tiêu chí người dùng chọn (giá tăng/giảm, mới nhất…) 

Hiển thị 

Danh sách sách phù hợp với từ khóa và bộ lọc. 

Thông báo nếu không tìm thấy kết quả phù hợp. 

 

 

Thêm vào giỏ hàng 

Nhập vào 

Người dùng chọn sách cần mua. 

Nhập số lượng và nhấn nút “Thêm vào giỏ”. 

Xử lý 

Kiểm tra tồn kho hiện tại của sách. 

Nếu còn hàng, lưu thông tin vào giỏ hàng tạm thời (session hoặc database). 

Nếu sách đã có trong giỏ, cộng dồn số lượng. 

Hiển thị 

Thông báo “Thêm vào giỏ thành công”. 

Hiển thị tổng số sản phẩm trong giỏ. 

Nếu hết hàng, hiển thị thông báo lỗi. 

 

 

Đặt hàng  

Nhập vào 

Người dùng xác nhận giỏ hàng, nhập thông tin giao hàng. 

Chọn phương thức thanh toán (mô phỏng). 

Xử lý 

Kiểm tra tồn kho lần cuối.( Chặn Khi hết hàng) 

Tạo đơn hàng với trạng thái “Chờ xử lý”. 

Lưu thông tin đơn hàng và chi tiết sản phẩm vào cơ sở dữ liệu. 

 

Hiển thị 

Thông báo đặt hàng thành công. 

Hiển thị mã đơn hàng và hướng dẫn theo dõi. 

 

Theo dõi đơn hàng 

Nhập vào 

Người dùng truy cập mục “Đơn hàng của tôi”. 

Xử lý 

Truy vấn danh sách đơn hàng theo tài khoản người dùng. 

Lấy trạng thái đơn hàng từ cơ sở dữ liệu. 

 

Hiển thị 

Danh sách đơn hàng với trạng thái: “Chờ xử lý”, “Đang giao”, “Đã giao”, “Đã hủy”. 

Chi tiết từng đơn hàng. 

 

 

Chức Năng cho Quản trị viên (Admin) 

Phần này chỉ dành riêng cho quản trị viên đăng nhập  

2.1 Quản lý sản phẩm 

a. Thêm Sách  

 

Nhập vào 

Admin nhập thông tin sách: tiêu đề, tác giả, thể loại, giá, tồn kho, mô tả, ảnh bìa. 

Xử lý 

Lưu thông tin Sách vào trong cơ sở dữ liệu. 

Hiển thị 

Thông báo thêm thành công. 

Hiển thị danh sách sách đã cập nhật. 

 

b. Sửa thông tin sách 

Nhập vào 

Chọn sách muốn sửa 

Xử lý 

Lưu hoặc cập nhật thông tin sách vào cơ sở dữ liệu. 

Hiển thị 

Thông báo sửa thành công. 

Hiển thị danh sách sách đã cập nhật. 

 

c. Xoá sách 

Nhập vào 

Chọn sách muốn xoá 

Xử lý 

Cho phép xóa sách nếu không còn nhập thêm  bán. 

Hiển thị 

Thông báo Xoá thành công. 

Hiển thị danh sách sách đã cập nhật. 

 

2.2 Quản lý khách hàng 

Nhập vào 

Admin truy cập danh sách khách hàng. 

Xử lý 

Truy vấn thông tin người dùng từ cơ sở dữ liệu. 

Cho phép khóa/mở tài khoản, xem lịch sử mua hàng. 

Hiển thị 

Danh sách khách hàng. 

Thông tin chi tiết từng người dùng. 

 

 

2.3 Quản lý đơn hàng  

Phần danh sách đơn hàng 

Quản trị viên có quyền quản trị login vào hệ thống, chọn danh mục "Quản lý Đơn Đặt Hàng", một danh sách đơn đặt hàng sẽ được hiển thị như mô tả giao diện  

Các đơn hàng mới nhất sẽ được hiển thị lên đầu. Trạng thái giao hàng gồm "Chưa Giao" và "Đã Giao Hàng". Quản trị viên có thể chọn nút "Xem" để xem chi tiết đơn đặt hàng như mô tả bên dưới.  

Các đơn hàng đã giao được phép xóa bằng cách nhấn nút "Xóa": Khi người dùng nhấn nút Xóa, hệ thống sẽ hiển thị thông báo xác nhận xóa, người dùng đồng ý, hệ thống sẽ xóa đơn hàng đó. 

Các đơn hàng chưa giao: Khi người dùng nhấn nút Xóa, hệ thống sẽ hiển thị thông báo lỗi, người dùng không thể xóa đơn hàng này. 

Phần chi tiết đơn đặt hàng 

Phần màn hình chi tiết đơn đặt hàng sẽ hiển thị thông tin chi tiết khách hàng và đơn hàng. Đồng thời, trạng thái đơn hàng cũng được hiển thị trong màn hình này. Những đơn hàng chưa giao sẽ được hiển thị nút "Xác nhận đã giao đơn hàng này" để người quản trị có thể chọn. Sau khi người dùng chọn nút này, trạng thái đơn hàng sẽ chuyển từ chưa giao sang đã giao hàng. 

Những đơn hàng đã giao thì không hiển thị. Người dùng (quản trị viên) có thể nhấn nút Back của trình duyệt để quay lại màn hình danh sách đơn hàng.  

Giao diện hai màn hình này cũng cần hiển thị tốt trên các trình duyệt IE, Firefox và Chrome mới nhất của máy kiểm thử như: Không bị vỡ giao diện, có thể zoom-in, zoom out, thứ tự tab từ trái sang phải, từ trên xuống dưới. 

 

Xem thông tin đơn hàng. 

 

Nhập vào 

Chọn đơn hàng cần xem. 

Xử lý 

Lấy thông tin đơn hàng trong cơ sở dữ liệu. 

Hiển thị 

Hiển thị thông tin về đơn hàng. 

 

Xoá đơn hàng. 

 

Nhập vào 

Chọn đơn hàng muốn xoá qua nút xoá 

Xử lý 

Xoá thông tin đơn hàng khỏi cơ sở dữ liệu. 

Hiển thị 

Hiển thị thông báo đơn hàng đã được xoá. 

 
 

 Xử lý đơn hàng. 

 

Mô tả 

Đơn hàng  được lưu lại và ở chế độ chờ xử lý, nhân viên của website sẽ giao hàng đến tận tay khách hàng, lúc đó quản trị viên xác nhận kết thúc quá trình xử lý đơn hàng. 

Nhập vào 

Chọn đơn hàng cần xử lý. 

Xử lý 

Update thông tin về đơn hàng. 

Hiển thị 

Hiện thông tin đơn hàng đã được xử lý. 

 

 

Quản lý tồn kho 

 

2.4 Tổng doanh thu 

Nhập vào 

Admin chọn khoảng thời gian cần thống kê. 

Xử lý 

Truy vấn dữ liệu đơn hàng đã giao. 

Tính tổng doanh thu, số lượng sách bán ra, top sách bán chạy. 

 

Hiển thị 

Biểu đồ doanh thu theo ngày/tuần/tháng. 

Danh sách sách bán chạy. 

Cảnh báo tồn kho thấp. 

 

 

3. Yêu cầu phi chức năng 

3.1 Giao diện đơn giản, dễ sử dụng. 

Thiết kế giao diện thân thiện với người dùng, dễ thao tác cho cả khách hàng và quản trị viên. 

Bố cục rõ ràng, phân nhóm chức năng hợp lý: tìm kiếm, giỏ hàng, quản lý đơn hàng, thống kê. 

Tương thích với các trình duyệt phổ biến như Chrome, Firefox, Edge. 

Hỗ trợ responsive trên thiết bị di động, máy tính bảng và desktop. 

3.2 Hệ thống đảm bảo tính toàn vẹn dữ liệu. 

Dữ liệu người dùng, đơn hàng, sách phải được lưu trữ và xử lý chính xác, không bị mất mát hoặc sai lệch. 

Áp dụng các ràng buộc dữ liệu (ràng buộc khóa chính, khóa ngoại, kiểm tra tồn kho, trạng thái đơn hàng). 

Cơ chế kiểm tra và xác thực dữ liệu đầu vào để tránh lỗi logic và bảo vệ hệ thống khỏi các truy vấn sai hoặc độc hại. 

 
