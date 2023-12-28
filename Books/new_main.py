# from database import BookDAO
#
# # ایجاد شیء BookDAO و ارتباط با دیتابیس
# book_dao = BookDAO('bookstore.db')
#
# # ساخت جدول books
# book_dao.create_table()
#
# # اضافه کردن چند کتاب به دیتابیس
# book_dao.insert_book('To Kill a Mockingbird', 'Harper Lee')
# book_dao.insert_book('Pride and Prejudice', 'Jane Austen')
# book_dao.insert_book('The Great Gatsby', 'F. Scott Fitzgerald')
#
# # دریافت تمام کتاب‌ها
# all_books = book_dao.get_all_books()
#
# # نمایش تمام کتاب‌ها
# for book in all_books:
#     print(f'Title: {book[1]}, Author: {book[2]}')
#
# # بستن اتصال به دیتابیس
# book_dao.close_connection()


import tkinter as tk
from tkinter import messagebox,Tk, Entry, Button, Frame, Scrollbar, Listbox, Label
import sqlite3
from PIL import ImageTk, Image
import datetime
from tkinter import ttk

def conn_dataset():
    conn = sqlite3.connect('bookstore.db')
    cursor = conn.cursor()
    return conn, cursor
def insert_data():
    # تابع برای اجرای دستورات مربوط به افزودن داده ها به پایگاه داده
    def save_data():
        title = entry_title.get()
        author = entry_author.get()
        price = entry_price.get()
        stock = entry_stock.get()

        conn, cursor = conn_dataset()

        # اجرای دستور افزودن داده جدید به جدول
        cursor.execute("INSERT INTO books (title, author, price, stock) VALUES (?, ?, ?, ?)", (title, author, price, stock))
        # cursor.execute("INSERT INTO books (title, author, price) VALUES (?, ?, ?)")

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "اطلاعات با موفقیت ذخیره شد!")
        insert_window.destroy()

    # ایجاد یک پنجره جدید برای ورود اطلاعات
    insert_window = tk.Toplevel()
    insert_window.title("افزودن کتاب")

    insert_window.geometry("250x200")
    insert_window.resizable(False, False)

    # افزودن تکست باکس ها برای عنوان و نویسنده
    label_title = tk.Label(insert_window, text="عنوان:")
    label_title.pack()
    entry_title = tk.Entry(insert_window)
    entry_title.pack()

    label_author = tk.Label(insert_window, text="نویسنده:")
    label_author.pack()
    entry_author = tk.Entry(insert_window)
    entry_author.pack()


    label_price = tk.Label(insert_window, text="قیمت:")
    label_price.pack()
    entry_price = tk.Entry(insert_window)
    entry_price.pack()


    label_stock = tk.Label(insert_window, text="موجودی:")
    label_stock.pack()
    entry_stock = tk.Entry(insert_window)
    entry_stock.pack()

    # افزودن دکمه برای ذخیره داده ها
    btn_save = tk.Button(insert_window, text="ذخیره", command=save_data)
    btn_save.pack()


# صفحه اصلی
def main_page():
    main_window = tk.Tk()
    main_window.title("Book Stock Management")

    # دکمه برای نمایش داده‌ها در دیتابیس
    def show_data():
        # conn, cursor = conn_dataset()
        #
        # cursor.execute("SELECT * FROM books")
        # data = cursor.fetchall()
        # conn.close()
        # messagebox.showinfo("Data", str(data))
        conn, cursor = conn_dataset()

        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        conn.close()

        # ایجاد پنجره جدید
        window = Tk()
        window.title("نمایش داده")

        # ایجاد عنوان جدول
        title_label = Label(window, text="جدول کتاب‌ها", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        # ایجاد ویجت Frame برای جدول
        table_frame = tk.Frame(window)
        table_frame.pack()

        # عنوان‌ها
        headers = ["ردیف", "عنوان", "نویسنده", "قیمت", "موجودی"]

        # مقادیر سطرها
        # rows = [
        #     ["آرمین", "25", "مهندس"],
        #     ["محمد", "30", "برنامه‌نویس"]
        # ]

        # ایجاد عنوان‌ها
        for i, header in enumerate(headers):
            header_label = tk.Label(table_frame, text=header, relief=tk.RIDGE, padx=10, pady=5)
            header_label.grid(row=0, column=i)

        # ایجاد سطرها
        # for i, row in enumerate(rows, start=1):
        #     for j, value in enumerate(row):
        #         value_label = tk.Label(table_frame, text=value, relief=tk.RIDGE, padx=10, pady=5)
        #         value_label.grid(row=i, column=j)

        for i, row in enumerate(data, start=1):
            for j, value in enumerate(row):
                value_label = tk.Label(table_frame, text=value, relief=tk.RIDGE, padx=10, pady=5)
                value_label.grid(row=i, column=j)

        window.mainloop()

    def search_books():
        # اتصال به پایگاه داده و تنظیم جدول
        conn, cursor = conn_dataset()

        # ایجاد پنجره جدید
        window = tk.Tk()
        window.title("جستجو داده")

        # ایجاد ویجت Frame برای فرم جستجو
        form_frame = tk.Frame(window)
        form_frame.pack(pady=10)

        # ایجاد برچسب و ورودی برای عنوان
        label_title = tk.Label(form_frame, text="عنوان:")
        label_title.grid(row=0, column=0, padx=5, pady=5)
        entry_title = tk.Entry(form_frame)
        entry_title.grid(row=0, column=1, padx=5, pady=5)

        # ایجاد برچسب و ورودی برای نویسنده
        label_author = tk.Label(form_frame, text="نویسنده:")
        label_author.grid(row=1, column=0, padx=5, pady=5)
        entry_author = tk.Entry(form_frame)
        entry_author.grid(row=1, column=1, padx=5, pady=5)

        # تابع add_to_cart
        def add_to_cart(book_id, stock_label):

            conn, cursor = conn_dataset()

            query = "SELECT * FROM books WHERE id = ?"
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()

            if book:
                stock = int(book[4])
                if stock > 0:
                    new_stock = stock - 1

                    query = "UPDATE books SET stock = ? WHERE id = ?"
                    cursor.execute(query, (new_stock, book_id))
                    conn.commit()

                    # اضافه کردن در جدول ریپورت
                    current_date = datetime.date.today().strftime("%Y-%m-%d")
                    print(current_date)
                    conn_insert, cursor_insert = conn_dataset()

                    selected_book_title = book[1]  # تعریف عنوان کتاب
                    selected_book_author = book[2]  # تعریف نویسنده کتاب
                    selected_book_price = book[3]  # تعریف قیمت کتاب
                    insert_query = "INSERT INTO report (title, author, price, date_buy) VALUES (?, ?, ?, ?)"
                    cursor_insert.execute(insert_query, (selected_book_title, selected_book_author, selected_book_price, current_date))
                    conn_insert.commit()

                    messagebox.showinfo("Success", f"کتاب '{selected_book_title}' با موفقیت به سبد خرید اضافه شد!")

                    # update_display(stock_label)
                    # فراخوانی تابع جدید برای بارگزاری مجدد فرم و نمایش اطلاعات جدید
                    # cursor.close()
                    # conn.close()
                else:
                    messagebox.showinfo("Error", "متأسفانه کتاب مورد نظر در دسترس نیست!")

            # cursor.close()
            # conn.close()

        # تابع برای نمایش نتایج جستجو
        def show_search_result():
            # search_window.destroy()
            search_title = entry_title.get()
            search_author = entry_author.get()

            if search_title and search_author:
                # جستجو بر اساس عنوان و نویسنده
                query = "SELECT * FROM books WHERE title LIKE ? AND author LIKE ?"
                cursor.execute(query, (f"%{search_title}%", f"%{search_author}%"))
            elif search_title:
                # جستجو بر اساس عنوان
                query = "SELECT * FROM books WHERE title LIKE ?"
                cursor.execute(query, (f"%{search_title}%",))
            elif search_author:
                # جستجو بر اساس نویسنده
                query = "SELECT * FROM books WHERE author LIKE ?"
                cursor.execute(query, (f"%{search_author}%",))
            else:
                # در صورت عدم وجود عنوان و نویسنده، همه رکوردها را بازیابی کنید
                messagebox.showinfo("Success", "اطلاعاتی با مشخصات وارد شده یافت نشد!")
                return

            data = cursor.fetchall()
            # بستن اتصال
            conn.close()

            # ایجاد پنجره جدید برای نمایش نتایج جستجو
            result_window = tk.Tk()
            result_window.title("نتایج جستجو")

            # ایجاد عنوان جدول
            title_label = tk.Label(result_window, text="نتایج جستجو", font=("Helvetica", 16, "bold"))
            title_label.pack(pady=10)

            # ایجاد ویجت Frame برای جدول
            table_frame = tk.Frame(result_window)
            table_frame.pack()

            # عنوان‌ها
            headers = ["ردیف", "عنوان", "نویسنده", "قیمت", "موجودی", "عملیات افزودن به خرید"]

            # ایجاد عنوان‌ها
            for i, header in enumerate(headers):
                header_label = tk.Label(table_frame, text=header, relief=tk.RIDGE, padx=10, pady=5)
                header_label.grid(row=0, column=i)

            # ایجاد سطرها
            for i, row in enumerate(data, start=1):
                for j, value in enumerate(row):
                    if j == 3:  # ایندکس ستون قیمت
                        value_label = tk.Label(table_frame, text=value + " تومان", relief=tk.RIDGE, padx=10, pady=5)
                        value_label.grid(row=i, column=j)
                    elif j == 4:  # ایندکس ستون موجودی
                        stock = int(value)  # تبدیل رشته به عدد صحیح
                        stock_label = tk.Label(table_frame, text=stock, relief=tk.RIDGE, padx=10, pady=5)
                        stock_label.grid(row=i, column=j)
                        if stock > 0:
                            decrease_button = tk.Button(table_frame, text="خرید",
                                                        command=lambda row=row: add_to_cart(row[0], stock_label))
                            decrease_button.grid(row=i, column=j + 1)  # عدد 1 به j اضافه میشود
                        else:
                            out_of_stock_label = tk.Label(table_frame, text="ناموجود", relief=tk.RIDGE, padx=10, pady=5)
                            out_of_stock_label.grid(row=i, column=j)
                            out_of_stock_label.grid(row=i, column=j + 1)
                    else:
                        value_label = tk.Label(table_frame, text=value, relief=tk.RIDGE, padx=10, pady=5)
                        value_label.grid(row=i, column=j)

            # شروع حلقه نمایش نتایج جستجو
            result_window.mainloop()

        # ایجاد دکمه جستجو
        search_button = tk.Button(window, text="جستجو", command=show_search_result)
        search_button.pack(pady=10)

        window.mainloop()

    def show_report():
        start_date = start_entry.get()
        end_date = end_entry.get()
        conn, cursor = conn_dataset()

        if start_date == "" or end_date == "":
            messagebox.showerror("خطا", "لطفا تاریخ را وارد کنید!")
            return

        if end_date < start_date:
            messagebox.showerror("خطا", "تاریخ شروع نمیتواند از تاریخ پایان بزرگتر باشد")
            return

        query = "SELECT  title, author, price FROM report WHERE date_buy BETWEEN ? AND ?"
        cursor.execute(query, (start_date, end_date))
        records = cursor.fetchall()

        report_result_window = tk.Tk()
        report_result_window.title("نتایج گزارش")



        # ایجاد جدول با استفاده از ttk.Treeview
        table = ttk.Treeview(report_result_window)
        table.pack()

        # تنظیم ستون‌ها
        table["columns"] = ("عنوان", "نویسنده", "قیمت")

        # تنظیم عنوان‌ها
        table.heading("#0", text="ردیف")
        for i, header in enumerate(table["columns"]):
            table.heading(header, text=header)

        # افزودن سطرها
        for i, row in enumerate(records, start=1):
            table.insert(parent="", index="end", iid=i, text=i, values=row)

        conn.close() # بعد از استفاده از دیتابیس باید آن را ببندید
        report_result_window.mainloop()





    def reports():
        global start_entry
        global end_entry

        # ایجاد پنجره جدید
        report_window = tk.Tk()
        report_window.title("گزارش ها برای فروش")

        # ایجاد تکس باکس برای تاریخ شروع
        start_label = tk.Label(report_window, text="تاریخ شروع:")
        start_label.pack()

        start_entry = tk.Entry(report_window)
        start_entry.pack()

        # ایجاد تکس باکس برای تاریخ پایان
        end_label = tk.Label(report_window, text="تاریخ پایان:")
        end_label.pack()

        end_entry = tk.Entry(report_window)
        end_entry.pack()

        # ایجاد دکمه برای نمایش گزارش
        show_button = tk.Button(report_window, text="نمایش گزارش", command=show_report)
        show_button.pack()

        report_window.mainloop()


    # دکمه برای بستن صفحه
    def close_window():
        main_window.destroy()

    # main_window.minsize(500, 500)
    # main_window.maxsize(500, 500)
    main_window.geometry("300x300")
    main_window.resizable(False, False)

    # دکمه‌ه افزودن
    btn_show_data = tk.Button(main_window, text="افزودن کتاب", command=insert_data)
    btn_show_data.pack()

    # دکمه‌ه نمایش کل داده ها
    btn_show_data = tk.Button(main_window, text="نمایش کل داده ها", command=show_data)
    btn_show_data.pack()


    # دکمه نمایش کل داده ها
    btn_search_data = tk.Button(main_window, text="جستجوی داده ها", command=search_books)
    btn_search_data.pack()

    # دکمه گزارش فروش ها
    btn_search_data = tk.Button(main_window, text="گزارش فروش ها", command=reports)
    btn_search_data.pack()


    btn_close = tk.Button(main_window, text="Close", command=close_window)
    btn_close.pack()

    main_window.mainloop()


# اجرای برنامه
if __name__ == "__main__":
    main_page()