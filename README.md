# Phân tích và dự đoán giá laptop trên các website bán hàng ở Việt Nam

Đây là repository được sử dụng để thực hiện đồ án môn học Phân tích và trực quan dữ liệu (DS105).

Các công việc chính được thực hiện:
1. Thu thập dữ liệu giá laptop cũ trên trang thegioididong.com
1. Tiền xử lí (Làm sạch, biến đổi dữ liệu)
1. Phân tích thăm dò
1. Xây dựng mô hình dự đoán giá
1. Đánh giá mô hình

Bộ dữ liệu trong đồ án này được nh lấy trên trang bán hàng online của Thế Giới Di Động (https://thegioididong.com) với công cụ hỗ trợ thu thập là Selenium. Thời gian thu thập bắt đầu vào lúc 11:35, 28/10/2021 và quá trình thu thập kéo dài xấp xỉ 45 phút. Kết quả thu được là bộ dữ liệu về các laptop đã qua sử dụng, với 1234 dòng và 35 cột. 

Trong đồ án này, chúng tôi đã tự tiến hành thu thập bộ dữ liệu trên trang thegioididong.com. Ở bước tiếp theo, cũng là bước tiêu tốn nhiều thời gian nhất, chúng tôi lặp lại quá trình tiền xử lí nhiều lần để xử lí những trường hợp ngoại lệ tồn tại sẵn trong bộ dữ liệu lẫn trong các code của chính nhóm. Sau đó, áp dụng các kĩ thuật phân tích thăm dò, phân tích thống kê, các thuộc tính quan trọng được phát hiện bao gồm : brand, material, cpu_type, gpu_type, ram, has_touchscreen, weight, ppi. Cuối cùng, nhóm em thử nghiệm nhiều loại mô hình hồi quy khác nhau, và thu được mô hình tốt nhất là mô hình hồi quy đa thức bậc 5 Ridge Regression với r2 trên test là 0.775. Sản phẩm được triển khai trên nền tảng đám mây Heroku.


Bên cạnh việc thu thập laptop cũ tại thegioididong.com, nhóm còn xây dựng script để lấy dữ liệu từ các trang web:
- dienmayxanh.com (máy mới): 144 dòng, 31 cột
- tiki.vn (máy mới): 104 dòng, 41 cột
- fptshop.com.vn (máy mới): 144 dòng, 67 cột
- gearvn.com (máy mới): 96 dòng, 41 cột
- fptshop.com.vn (máy cũ): 28 dòng, 69 cột
