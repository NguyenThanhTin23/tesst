from flask import Flask, render_template, request, flash, send_file, redirect  
import pandas as pd  
import os  
from CRUD.Creat import creat  
from clean import cleanData  

app = Flask(__name__, static_folder='static')  
app.secret_key = 'your_secret_key_here'  # Thêm khóa bí mật  

# Đọc dữ liệu từ tệp CSV  
file_path = 'data_dirty.csv'  
data = pd.read_csv(file_path)  
cleaned_file_path = 'cleaned_data.csv'  
ROWS_PER_PAGE = 12  

def paginate_data(data, page, rows_per_page):  
    start_idx = (page - 1) * rows_per_page  
    end_idx = start_idx + rows_per_page  
    paginated_data = data.iloc[start_idx:end_idx]  
    table_data = paginated_data.to_dict(orient='records')  
    total_pages = (len(data) + rows_per_page - 1) // rows_per_page  
    start_page = max(1, page - 2)  
    end_page = min(total_pages, page + 2)  
    nearby_pages = range(start_page, end_page + 1)  

    return {  
        "table_data": table_data,  
        "total_pages": total_pages,  
        "has_next": page < total_pages,  
        "has_prev": page > 1,  
        "nearby_pages": nearby_pages,  
    }  

@app.route('/')  
def index():  
    # Đọc lại dữ liệu từ tệp CSV để đảm bảo có dữ liệu mới  
    data = pd.read_csv(file_path)  
    page = int(request.args.get('page', 1))  
    pagination = paginate_data(data, page, ROWS_PER_PAGE)  
    
    return render_template(  
        'index.html',  
        table_data=pagination["table_data"],  
        headers=data.columns,  
        page=page,  
        total_pages=pagination["total_pages"],  
        has_next=pagination["has_next"],  
        has_prev=pagination["has_prev"],  
        nearby_pages=pagination["nearby_pages"]  
    )  

@app.route('/add', methods=['GET', 'POST'])  
def add_data():  
    if request.method == 'POST':  
        Date = request.form['Date']  
        Country_Region = request.form['Country_Region']  
        Confirmed = int(request.form['Confirmed'])  
        Deaths = int(request.form['Deaths'])  
        Recovered = int(request.form['Recovered'])  
        Active = int(request.form['Active'])  
        New_cases = int(request.form['New_cases'])  
        New_deaths = int(request.form['New_deaths'])  
        New_recovered = int(request.form['New_recovered'])  
        WHO_Region = request.form['WHO_Region']  

        new_row = [Date, Country_Region, Confirmed, Deaths, Recovered, Active, New_cases, New_deaths, New_recovered, WHO_Region]  

        try:  
            creat(file_path, new_row)  
            flash("Dòng mới đã được thêm vào thành công!", 'success')  
            return redirect('/add')  
        except Exception as e:  
            flash(f"Lỗi: {str(e)}", 'danger')  
            return redirect('/add')  

    return render_template('add.html')  

# Thêm route xử lý tải lên file CSV  
@app.route('/upload_csv', methods=['POST'])  
def upload_csv():  
    if 'file' not in request.files:  
        flash('Không có tệp nào được chọn', 'danger')  
        return redirect('/add')  

    file = request.files['file']  
    if file.filename == '':  
        flash('Tệp không hợp lệ', 'danger')  
        return redirect('/add')  

    if file and file.filename.endswith('.csv'):  
        try:  
            file_upload = os.path.join('uploads', file.filename)  
            file.save(file_upload)  

            # Đọc tệp CSV và kiểm tra các trường dữ liệu  
            new_data = pd.read_csv(file_upload)  
            if set(new_data.columns) != set(data.columns):  
                flash('Tệp CSV không có cùng các trường dữ liệu với dữ liệu hiện có', 'danger')  
                return redirect('/add')  

            # Thêm dữ liệu mới vào dữ liệu hiện có  
            new_data.to_csv(file_path, mode='a', header=False, index=False)  
            flash(f'Dữ liệu từ {file.filename} đã được thêm thành công!', 'success')  
            return redirect('/add')  
        except Exception as e:  
            flash(f"Lỗi khi thêm dữ liệu từ tệp CSV: {str(e)}", 'danger')  
            return redirect('/add')  

    flash('Vui lòng chọn tệp CSV hợp lệ', 'danger')  
    return redirect('/add') 
# Các route khác cho chức năng sửa, xóa, làm sạch, thống kê và biểu đồ  
@app.route('/edit')  
def edit_data():  
    return "Trang Sửa Dữ Liệu"  

@app.route('/delete', methods=['GET', 'POST'])  
def delete_data():  
    return "Trang delete"  

@app.route('/clean')  
def clean_data():  
    # Làm sạch dữ liệu  
    cleaned_data = cleanData('data_dirty.csv')  
    
    # Lưu dữ liệu đã làm sạch vào tệp mới  
    cleaned_data.to_csv(cleaned_file_path, index=False)
    cleaned_data.to_csv(file_path, index=False)
    # Phân trang dữ liệu đã làm sạch  
    page = int(request.args.get('page', 1))  
    pagination = paginate_data(cleaned_data, page, ROWS_PER_PAGE)  
    
    # Truyền dữ liệu đã làm sạch vào template  
    return render_template(  
        'clean.html',  
        table_data=pagination["table_data"],  
        headers=cleaned_data.columns,  
        page=page,  
        total_pages=pagination["total_pages"],  
        has_next=pagination["has_next"],  
        has_prev=pagination["has_prev"],  
        nearby_pages=pagination["nearby_pages"]  
    )  

@app.route('/download_clean_data')  
def download_clean_data():  
    return send_file(cleaned_file_path, as_attachment=True)  

@app.route('/statistics')
def statistics():
    return "Trang Thống Kê"

@app.route('/chart')
def chart():
    return "Trang Vẽ Biểu Đồ"

if __name__ == '__main__':
    app.run(debug=True)