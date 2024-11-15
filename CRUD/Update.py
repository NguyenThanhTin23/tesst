import pandas as pd


def update(file_path, list_to_update):
    """
    Chức năng:
    Cập nhật dữ liệu trong file CSV dựa trên danh sách đầu vào.

    Hàm đọc dữ liệu từ một file CSV vào DataFrame, xác định dòng cần cập nhật dựa trên các giá trị
    của cột 'Date' và 'Country/Region', sau đó cập nhật các giá trị khác dựa trên danh sách đầu vào.
    Kết quả cuối cùng sẽ được lưu lại vào file CSV, ghi đè lên file gốc.

    Tham số:
    file_path (str): Đường dẫn đến file CSV cần xử lý.
    list_to_update (list): Danh sách chứa các giá trị cần cập nhật theo thứ tự:
        [Date, Country/Region, Confirmed, Deaths, Recovered, Active, New_cases, New_deaths, New_recovered, WHO_Region].

    """
    # Đọc file CSV vào DataFrame
    df = pd.read_csv(file_path)

    # Cập nhật dữ liệu
    date_to_update = list_to_update[0]
    country_region_to_update = list_to_update[1]

    # Chuyển các cột có idx từ 2 đến 8 thành kiểu số nguyên
    for i in range(2, 9):
        list_to_update[i] = int(list_to_update[i])

    # Chuyển cột 'Date' thành kiểu datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Chuyển đổi ngày được nhập thành kiểu datetime
    date_to_update = pd.to_datetime(date_to_update)

    # Các cột sẽ update
    columns_to_update = ["Date", "Country/Region", "Confirmed", "Deaths", "Recovered",
                         "Active", "New cases", "New deaths", "New recovered", "WHO Region"]

    # Lọc dòng cần cập nhật với cả 2 điều kiện
    filter = (df['Date'] == date_to_update) & (df['Country/Region'].str.lower() == country_region_to_update.lower())

    # Cập nhật các giá trị trong dòng đã tìm thấy
    df.loc[id, columns_to_update] = list_to_update

    # Lưu lại DataFrame vào file CSV
    df.to_csv(file_path, index=False)
