# ocr_diploma
Chạy trên python 3.7 và cài môi trường bằng cách pip install -r requirements.txt \br
usage: ocr.py [-h] -d DIR_IMAGES [-w WEIGHTS] [-o OUTPUT]\br
optional arguments:\br
-h, --help\br
show this help message and exit\br
-d DIR_IMAGES, --dir_images DIR_IMAGES\br
Đường dẫn tới thư mục cha chứa các thư mục có ảnh cần OCR\br
-w WEIGHTS, --weights WEIGHTS\br
Loaị weight muốn sử dụng: transformer hoặc seq2seq\br
-o OUTPUT, --output OUTPUT\br
Dường dẫn tới thư mục cha chứa thư mục đầu ra của các file text ocr\br
Các trường dữ liệu sẽ được lưu theo tên ảnh nên có thể tùy chọn cách đặt tên\br
Như trong dữ liệu test là:\br
fullname(họ và tên)|dateofbirth(ngày,tháng,năm sinh)|placeofbirth(nơi sinh)|gender(giới tính)|ethnicgroup(dân tộc)|school(học sinh trường)|examterm(khóa thi)|examboard(hội đồng thi)|typeofgraduation(tốt nghiệp loại)|typeoftraining(hình thức đào tạo)|date(ngày và nơi cấp bằng)|serialno(số hiệu)|regno(số vào sổ cấp bằng)\br
