# Tích hợp và xử lý dữ liệu lớn 
- Đề bài: Thu thập, tích hợp, và xử lý dữ liệu về việc làm từ các trang web tuyển dụng. Hệ thống
có thể cập nhật dữ liệu định kỳ một cách tự động, dựa trên cấu hình được thiết lập
- Yêu cầu: Tối thiểu 5 nguồn khác nhau

# Hướng làm 
1. Tìm các trang web sẽ sử dụng 
2. Thu thập dữ liệu 
3. Tiền xử lý dữ liệu (tích hợp) sau đó lưu vào database 
4. Lập trang web hiển thị thông tin dữ liệu trong database 
5. Viết cấu hình code cập nhật thu thập dữ liệu theo ngày. 

## Các trang web sử dụng 
- Theo đánh giá ở trang này: https://resources.base.vn/hr/danh-sach-cac-trang-web-tuyen-dung-hang-dau-viet-nam-194
- Chọn ra được 7 trang web với số lượng truy cập > 1 triệu / 1 tháng để làm 
```code 
https://careerbuilder.vn/

https://www.jobstreet.vn/

https://www.timviecnhanh.com/

https://mywork.com.vn/

https://www.careerlink.vn/

https://topdev.vn/it-jobs

https://itviec.com/

https://vieclam24h.vn/
```
- Các trang còn lại số lượng truy cập ít và cũng ít job đăng tuyển hoặc có thể là không 
crawl dữ liệu về được vì nó sử dụng các framework như React, Angular ,... hoặc đơn giản 
là dùng javascript để chặn việc lấy link.

## Thu thập dữ liệu 
- Mỗi trang web đều có riêng 1 spider để crawl 
- Khi crawl 1 website thì chỉ crawl thông tin về job, các thông tin khác không quan tâm 
- Không lưu thông tin chi tiết về công ty tuyển dụng 

### Thứ tự thực hiện các trang 
1. Careerbuilder
- Được xây dựng spider model đầu tiên 
- Có 2 trường có thể xuất hiện hoặc không: experience và tags 
- Link ở các thẻ <a> đều có dạng đầy đủ nên dùng: scrapy.Request()

2. Mywork 
- Xây dựng thứ 2 
- Trang này thì lại không có trường: tags, thay vào đó có thêm trường: entitlements (lợi ích) 
- Link ở các thẻ <a> đều có dạng không đầy đủ nên dùng: response.follow()

3. Careerlink 
- Xây dựng thứ 3 
- Ngược với cái thứ 2, trang này lại có trường: tags, và không có trường: entitlements (lợi ích) 
- Link ở các thẻ <a> đều có dạng không đầy đủ nên dùng: response.follow()


4. Jobsgo
- Xay dung thu 4
- Trang này không có other_information và tags nhưng lại có entitlements 


5. https://timviec365.vn
- Xay dung thu 5


6. Timviecnhanh
- Xay dung thu 6
- Trang nay van con nhieu loi va kha la it bai







## Chua lam 
https://tuyencongnhan.vn
https://1001vieclam.com/


5. Vieclam Tuoitre
- Xay dung thu 4
- Giong y nguyen trang 1 (careerbuilder)


6. Itviec
- Xây dựng thứ 4
- Điều đặc biệt ở trang này là nó là trang về IT nên rất ít job
- Link ở các thẻ <a> đều có dạng không đầy đủ nên dùng: response.follow(), nhưng link ở trang pagination thì nó lại ở dạng 
không đầy đủ nên dùng: scrapy.Request()
- Do không hiển thị thông tin : lương (đăng nhập thì hiển thị) nên không dùng trang này nữa. 

7. https://www.jobstreet.vn/
- Trang này khá là shit vì nó không có cấu trúc cố định, có lẫn tiếng anh và việt crawl hơi khó 
- Bài viết thì không chi tiết, không phân mục rõ ràng như mấy trang bên trên.
- Do vậy bỏ, không làm trang này 

## Hướng dẫn chạy 
```code
1. Liệt kê toàn bộ các spider (các trang web sẽ crawl) có sẵn 
    scrapy list
    
2. Crawl 1 trang website ví dụ:
    scrapy crawl name_website -o name_file.json 
(name_website nam tren cai : scrapy list, name_file: ten file dau` ra)
    scrapy crawl careerbuilder -o careerbuilder.json
```