from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox


class Product:
    def __init__(self, str_product):
        name, price = str_product.split()
        self.name = name
        self.price = price

    def __str__(self):
        return self.name + ': ' + self.price + 'руб.\n'


class User:
    def __init__(self, str_user):
        login, password, role, phone, surname, name = str_user.split()
        self.login = login
        self.password = password
        self.role = role
        self.phone = phone
        self.surname = surname
        self.name = name

    def userToStr(self):
        return "   ".join([self.login, self.phone, self.surname, self.name]) + "\n"

    def __str__(self):
        return " ".join([self.login, self.password, self.role, self.phone, self.surname, self.name]) + "\n"


class Order:
    def __init__(self, str_order):
        login, product, price, count = str_order.split()
        self.login = login
        self.product = product
        self.price = price
        self.count = count

    def __str__(self):
        return " ".join([self.login, self.product, self.price, "("+self.count+" шт.)"]) + "\n"


def getAllUsers():
    f = open('users.txt', 'r', encoding='utf-8')
    list_users = [User(s) for s in f.read().splitlines()]
    f.close()
    return list_users


def getAllProducts():
    f = open('products.txt', 'r', encoding='utf-8')
    list_products = [Product(s) for s in f.read().splitlines()]
    f.close()
    return list_products


def getAllOrders():
    f = open('orders.txt', 'r', encoding='utf-8')
    list_orders = [Order(s) for s in f.read().splitlines()]
    f.close()
    return list_orders


class App:
    current_user = None

    def __init__(self, window):
        window.geometry('450x300')
        window.title('Авторизация')
        # можно ли изменять размер окна - нет
        window.resizable(False, False)
        title = Label(window, text="\nАвторизуйтесь, чтобы продолжить!\n", font=('Arial', 15), justify=CENTER, padx=20)
        title.pack()
        button = Button(root, text="Авторизоваться", background="#555", foreground="#ccc", padx="12", pady="12",
                        font="13")
        button["command"] = lambda w=window: self.pageAutorization(w)
        button.place(x=125, y=100)
        button2 = Button(root, text="Регистрация", background="#555", foreground="#ccc", padx="12", pady="12",
                         font="13")
        button2["command"] = lambda w=window: self.pageRegistration(w)
        button2.place(x=140, y=180)

    def showRoot(self, tmp, rw):
        tmp.destroy()
        rw.deiconify()

    def showUsers(self, field):
        field.configure(state='normal')
        field.delete('1.0', END)
        field.insert(END, 'ЛОГИН ТЕЛЕФОН ФАМИЛИЯ ИМЯ\n')
        field.insert(END, '-------------------------------------------------\n')
        for user in getAllUsers():
            field.insert(END, user.userToStr())
        field.configure(state='disabled')

    def showProducts(self, field):
        field.configure(state='normal')
        field.delete('1.0', END)
        field.insert(END, 'НАЗВАНИЕ: ЦЕНА\n')
        field.insert(END, '--------------------------\n')
        products = getAllProducts()
        for prod in products:
            field.insert(END, prod.__str__())
        field.configure(state='disabled')

    def addProduct(self, n, p, field):
        if not n.get() or not p.get():
            msg = "Заполните все поля"
            messagebox.showerror("Ошибка", msg)
            return

        try:
            float(p.get())
        except:
            msg = "В поле Цена введено не число"
            messagebox.showerror("Изменение цены", msg)
            return

        products = getAllProducts()
        change_price = False
        for product in products:
            if product.name == n.get():
                change_price = True
                product.price = p.get()
                break

        if change_price:
            f = open('products.txt', 'w', encoding='utf-8')
            for product in products:
                f.write(product.name + ' ' + product.price + '\n')
            msg = "Цена на данный продукт изменена"
        else:
            f = open('products.txt', 'a', encoding='utf-8')
            f.write('\n' + n.get() + ' ' + p.get())
            msg = "Новый продукт создан"
        n.delete(0, 'end')
        p.delete(0, 'end')
        messagebox.showinfo("Успешно", msg)
        f.close()
        self.showProducts(field)

    def showOrdersWithoutUser(self, field):
        field.configure(state='normal')
        field.delete('1.0', END)
        field.insert(END, 'ПОЛЬЗОВАТЕЛЬ  ПРОДУКТ  ЦЕНА  КОЛИЧЕСТВО\n')
        field.insert(END, '-------------------------------------------------------------------------\n')
        orders = getAllOrders()
        summa = 0
        for order in orders:
            field.insert(END, order.__str__())
            summa += float(order.price) * float(order.count)
        field.insert(END, "Итого заказано на сумму: {0} руб.".format(summa))
        field.configure(state='disabled')

    def goAdmin(self, rw):
        win_admin = Toplevel()
        win_admin.title("Панель Администратора")
        win_admin.geometry('550x450')
        win_admin.resizable(False, False)

        Label(win_admin, text=self.current_user.surname + ' ' + self.current_user.name, font=('Arial', 13)).pack()

        field_users = Text(win_admin, width=50, height=5, font=('Arial', 11), wrap=WORD)
        field_users.configure(state='disabled')
        field_users.place(x=140, y=30)

        show_users = Button(win_admin, text="Список\nпользователей", background="#555", foreground="#ccc",
                            padx="7", pady="7", font=('Arial', 10))
        show_users["command"] = lambda f=field_users: self.showUsers(f)
        show_users.place(x=10, y=47)

        field_product = Text(win_admin, width=17, height=5, font=('Arial', 11), wrap=WORD)
        field_product.configure(state='disabled')
        field_product.place(x=140, y=135)

        show_product = Button(win_admin, text="Список\nпродуктов", background="#555", foreground="#ccc",
                              padx="7", pady="7", font=('Arial', 10))
        show_product["command"] = lambda f=field_product: self.showProducts(f)
        show_product.place(x=10, y=152)

        Label(win_admin, text='Название', font=('Arial', 11)).place(x=410, y=130)
        name_entry = Entry(win_admin, bg='#fff', fg='#444', font=('Arial', 12), width=15)
        name_entry.place(x=405, y=150)
        Label(win_admin, text='Цена', font=('Arial', 11)).place(x=410, y=170)
        price_entry = Entry(win_admin, bg='#fff', fg='#444', font=('Arial', 12), width=15)
        price_entry.place(x=405, y=190)

        add_product = Button(win_admin, text="Добавить\nили изменить\nпродукт", background="#555", foreground="#ccc",
                             padx="7", pady="7", font=('Arial', 10))
        add_product["command"] = lambda n=name_entry, p=price_entry, f=field_product: self.addProduct(n, p, f)
        add_product.place(x=290, y=140)

        field_orders = Text(win_admin, width=50, height=5, font=('Arial', 11), wrap=WORD)
        field_orders.configure(state='disabled')
        field_orders.place(x=140, y=240)

        show_orders = Button(win_admin, text="Список\nЗаказов", background="#555", foreground="#ccc",
                            padx="7", pady="7", font=('Arial', 10))
        show_orders["command"] = lambda f=field_orders: self.showOrdersWithoutUser(f)
        show_orders.place(x=10, y=257)

        exit_btn = Button(win_admin, text='Выйти', background="#555", foreground="#ccc", padx="14", pady="14",
                          font="13")
        exit_btn["command"] = lambda r=rw, tmp=win_admin: self.showRoot(tmp, r)
        exit_btn.place(x=430, y=350)

        # приветственное корневое окно временно закрыть
        rw.withdraw()

    def showOrdersByUser(self, field):
        field.configure(state='normal')
        field.delete('1.0', END)
        field.insert(END, 'ПРОДУКТ  ЦЕНА  КОЛИЧЕСТВО\n')
        field.insert(END, '---------------------------------------------------\n')
        orders = getAllOrders()
        summa = 0
        for order in orders:
            if self.current_user.login == order.login:
                field.insert(END, " ".join([order.product, order.price, "("+order.count+" шт.)"]) + "\n")
                summa += float(order.price) * float(order.count)
        field.insert(END, "Итого заказано на сумму: {0} руб.".format(summa))
        field.configure(state='disabled')

    def makeOrder(self, product, count, field):
        try:
            float(count.get())
        except:
            msg = "В поле Количество введено не число"
            messagebox.showerror("Ошибка", msg)
            return
        ind = product.current()
        f = open('orders.txt', 'a', encoding='utf-8')
        f.write('\n' + self.current_user.login + ' ' + getAllProducts()[ind].name + ' ' + getAllProducts()[ind].price
                + ' ' + count.get())
        msg = "Заказано"
        messagebox.showinfo("Успешно", msg)
        f.close()
        self.showOrdersByUser(field)


    def goUser(self, rw):
        win_user = Toplevel()
        win_user.title("Панель Пользователя")
        win_user.geometry('550x400')
        win_user.resizable(False, False)

        Label(win_user, text=self.current_user.surname + ' ' + self.current_user.name, font=('Arial', 13)).pack()

        Label(win_user, text='Продукт', font=('Arial', 11)).place(x=10, y=40)
        c = Combobox(win_user, values=(getAllProducts()), state='readonly')
        c.current(0)
        c.place(x=10, y=60)

        Label(win_user, text='Количество', font=('Arial', 11)).place(x=170, y=40)
        count_entry = Entry(win_user, bg='#fff', fg='#444', font=('Arial', 12), width=15)
        count_entry.place(x=170, y=60)

        Label(win_user, text='Мои Заказы:', font=('Arial', 14)).place(x=40, y=110)
        field_order = Text(win_user, width=45, height=8, font=('Arial', 11), wrap=WORD)
        field_order.configure(state='disabled')
        field_order.place(x=10, y=145)

        order_btn = Button(win_user, text='Сделать\nзаказ', background="#555", foreground="#ccc", padx="14", pady="14",
                           font=('Arial', 11))
        order_btn["command"] = lambda comb=c, count=count_entry, f=field_order: self.makeOrder(comb, count, f)
        order_btn.place(x=350, y=40)

        exit_btn = Button(win_user, text='Выйти', background="#555", foreground="#ccc", padx="14", pady="14",
                          font="13")
        exit_btn["command"] = lambda r=rw, tmp=win_user: self.showRoot(tmp, r)
        exit_btn.place(x=400, y=300)

        self.showOrdersByUser(field_order)
        # приветственное корневое окно временно закрыть
        rw.withdraw()

    def clicked(self, u, p, w, rw):
        users = getAllUsers()
        for user in users:
            if user.login == u.get() and user.password == p.get():
                self.current_user = user
                w.destroy()
                if user.role == '1':
                    self.goAdmin(rw)
                else:
                    self.goUser(rw)
                return
        msg = "Неверный логин или пароль"
        messagebox.showerror("Ошибка", msg)
        w.lift()
        u.delete(0, 'end')
        p.delete(0, 'end')

    def addUser(self, u, p, ph, sur, na, w, rw):
        users = getAllUsers()
        exist = False

        if not u.get() or not p.get() or not ph.get() or not sur.get() or not na.get():
            msg = "Заполните все поля"
            messagebox.showerror("Ошибка", msg)
            w.lift()
            return

        if ph.get()[0] != '8' and ph.get()[0:2] != '+7' or \
                ph.get()[0] == '8' and len(ph.get()) != 11 or \
                ph.get()[0:2] == '+7' and len(ph.get()) != 12:
            msg = "Некорректный телефон"
            messagebox.showerror("Ошибка", msg)
            w.lift()
            return

        for user in users:
            if user.login == u.get() or user.phone == ph.get():
                exist = True
                msg = "Пользователь с таким логином или номером телефона существует"
                messagebox.showerror("Ошибка", msg)
                w.lift()
                break

        if not exist:
            f = open('users.txt', 'a', encoding='utf-8')
            f.write(' '.join(['\n' + u.get(), p.get(), '0', ph.get(), sur.get(), na.get()]))
            f.close()
            msg = "Новый пользователь создан"
            messagebox.showinfo("Успешно", msg)
            w.destroy()
            return

    def pageRegistration(self, root_w):
        win_auto = Toplevel()
        win_auto.title("Регистрация")
        # размер окна
        win_auto.geometry('450x400')
        # можно ли изменять размер окна - нет
        win_auto.resizable(False, False)
        main_label = Label(win_auto, text='Регистрация', font=('Arial', 15), justify=CENTER)
        main_label.pack()

        Label(win_auto, text='Логин', font=('Arial', 11)).pack()
        username_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        username_entry.pack()

        Label(win_auto, text='Пароль', font=('Arial', 11)).pack()
        password_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        password_entry.pack()

        Label(win_auto, text='Номер телефона', font=('Arial', 11)).pack()
        phone_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        phone_entry.pack()

        Label(win_auto, text='Фамилия', font=('Arial', 11)).pack()
        surname_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        surname_entry.pack()

        Label(win_auto, text='Имя', font=('Arial', 11)).pack()
        name_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        name_entry.pack()

        send_btn = Button(win_auto, text='Зарегистрироваться', background="#555", foreground="#ccc",
                          padx="10", pady="8", font="13")
        send_btn["command"] = lambda u=username_entry, p=password_entry, ph=phone_entry, sur=surname_entry, \
                                     na=name_entry, w=win_auto, rw=root_w: self.addUser(u, p, ph, sur, na, w, rw)
        send_btn.place(x=180, y=280)

    def pageAutorization(self, root_w):
        win_auto = Toplevel()
        win_auto.title("Авторизация")
        # размер окна
        win_auto.geometry('450x300')
        # можно ли изменять размер окна - нет
        win_auto.resizable(False, False)
        main_label = Label(win_auto, text='Авторизация', font=('Arial', 15), justify=CENTER)
        main_label.pack()

        # метка для поля ввода имени
        username_label = Label(win_auto, text='Логин', font=('Arial', 11))
        username_label.pack()
        # поле ввода имени
        username_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        username_entry.pack()
        # метка для поля ввода пароля
        password_label = Label(win_auto, text='Пароль', font=('Arial', 11))
        password_label.pack()
        # поле ввода пароля
        password_entry = Entry(win_auto, bg='#fff', fg='#444', font=('Arial', 12))
        password_entry.pack()
        # кнопка отправки формы
        send_btn = Button(win_auto, text='Войти', background="#555", foreground="#ccc", padx="10", pady="8", font="13")
        send_btn["command"] = lambda u=username_entry, p=password_entry, w=win_auto, rw=root_w: self.clicked(u, p, w,
                                                                                                             rw)
        send_btn.place(x=175, y=150)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
