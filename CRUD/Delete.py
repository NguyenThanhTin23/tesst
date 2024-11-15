import pandas as pd


def delete(file_path, Date_to_remove, Country_Region_to_remove):
    """
    Chức năng:
    Hàm xóa các dòng có giá trị trùng với cột 'Date' và 'Country/Region'.

    Tham số:
    file_path (str): Đường dẫn đến file CSV cần xử lý.
    Date_to_remove (str): Giá trị cụ thể của cột 'Date' cần loại bỏ.
    Country_Region_to_remove (str): Giá trị cụ thể của cột 'Country/Region' cần loại bỏ.

    """
    # Đọc dữ liệu từ file CSV vào DataFrame
    df = pd.read_csv(file_path)

    # Chuyển cột 'Date' thành kiểu datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Chuyển đổi ngày được nhập thành kiểu datetime
    Date_to_remove = pd.to_datetime(Date_to_remove)
    Country_Region_to_remove = Country_Region_to_remove.strip().lower()

    # Lọc dữ liệu, loại bỏ dòng có Date và Country/Region cần xóa
    filter = (df['Date'] == Date_to_remove) & (df['Country/Region'].str.lower() == Country_Region_to_remove)
    df.drop(index=df[filter].index, inplace=True)

    # Lưu lại DataFrame vào file CSV sau khi đã xóa dòng
    df.to_csv(file_path, index=False)
