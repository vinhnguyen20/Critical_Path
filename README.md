# Dự án thực hiện phân tích dữ liệu và giải quyết Critical Path và Problem Solving.

## Tổng quan 

Có một file dữ liệu đầu vào bao gồm các nhiệm vụ có liên quan đến nhau trên một cung đường critical path. Các nhiệm vụ bao gồm:
- Đầu vào là một tệp gồm các file dữ liệu nhiệm vụ.
- Bước 1: Tiến hành đọc xử lý dữ liệu phân tích và cho ra đường Critical Path chính.
- Bước 2: Từ bước Critical Path từ đó tiến hành các bước chuyển đổi dữ liệu tính toán thời gian delay chậm nhất và start chậm nhất các nhiệm vụ không nằm trên trục Critical Path chính.
- Bước 3: Từ các hàm ràng buộc của Problem Solving thì áp dụng Gamspy là một model để tính toán tuyến tính để tính toán hàm và các rang buộc đi kèm để cho ra Min_z là một biến chưa giá trị tối ưu cho phép trễ nhất của từng nhiệm vụ và chi phí thấp nhất đi kèm.
- Bước 4: Từ hàm Min_z dùng công thức tính toán lại Critical Path cho cả chi phí lẫn thời gian sao cho tối ưu.

## Công cụ
- Ngôn ngữ : Python
- Thư viện : Pandas(Dùng để phân tích dữ liệu), Numpy(Dùng để tính toán thực hiện trên Python).
- Model : <a href="https://gamspy.readthedocs.io/en/latest/user/index.html" target="_blank">Gamspy</a> 

## Triển khai dự án

1. Clone project về máy
2. Tiến hành install các thư viện trong file Requirement.txt
3. Chạy run trong file main.py

<!-- <a href="https://gamspy.readthedocs.io/en/latest/user/index.html" target="_blank">Gamspy</a> -->






