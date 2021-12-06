import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtWidgets import QTableWidgetItem

import main_ui
import catalog_ui
import students_ui

from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import datetime
import pyperclip

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class FirstForm(QMainWindow):
    def add_book(self):
        try:
            cur = self.con.cursor()
            id = QInputDialog.getText(self, "id", "Какой код книги?")[0]
            if not id:
                return 0
            title = QInputDialog.getText(self, "Название", "Как называется?")[0]
            author = QInputDialog.getText(self, "Автор", "Кто автор?")[0].replace(' ', '')
            genre = QInputDialog.getText(self, "Жанр", "Какого жанра произведение?")[0].replace(' ', '')
            n = QInputDialog.getText(self, "Колличество", "Сколько книг поступило?")[0]
            if author.isalpha() and n.isdigit() and genre.isalpha():
                cur.execute("INSERT INTO autors(autor) VALUES (?)", (author,)).fetchall()
                cur = self.con.cursor()
                cur.execute("INSERT INTO genres(title) VALUES (?)", (genre,)).fetchall()
                cur = self.con.cursor()
                cur.execute("INSERT INTO books(id, title, autor, genre, number, number_in_school) VALUES (?, ?, ?, ?, ?, ?)",
                            (id, title, (cur.execute("SELECT id FROM autors WHERE autor = ?", (author,)).fetchall()),
                             (cur.execute("SELECT id FROM genres WHERE genre = ?", (genre,)).fetchall()), n,
                             n)).fetchall()
                self.con.commit()
                self.update_result('*')
            else:
                self.statusBar().showMessage(f"Ошибка ввода")
                self.add_book()
        except Exception:
            pass

    def put(self):
        try:
            cur = self.con.cursor()
            clas = QInputDialog.getText(self, "Класс", "В каком ученик клвссе?")[0]
            name = QInputDialog.getItem(self, "Имя", "Как зовут ученика?",
                                        tuple(map(lambda x: x[0], cur.execute("SELECT name FROM students "
                                                                              "WHERE class = ?", (clas,)).fetchall())), 1,
                                        True)[0]
            id = cur.execute("SELECT book1 FROM students WHERE name = ?", (name,)).fetchall()[0][0]
            if not id:
                return 0
            if not cur.execute("SELECT * FROM students WHERE name = ?", (name,)).fetchall():
                self.statusBar().showMessage(f'Ученик {name} не найден')
            cur.execute("UPDATE students SET book1 = ?, date = ?, date_of_delivery = ? WHERE name = ? AND class = ?", (
                None, None, None, name, clas)).fetchall()
            cur.execute("UPDATE books SET number_in_school = number_in_school +1 WHERE id = ?", (id,)).fetchall()
            self.update_result('*')
            self.con.commit()
        except Exception:
            pass

    def give(self):
        try:
            cur = self.con.cursor()
            clas = QInputDialog.getText(self, "Класс", "В каком ученик клвссе?")[0]
            name = QInputDialog.getItem(self, "Имя", "Как зовут ученика?",
                                        tuple(map(lambda x: x[0], cur.execute("SELECT name FROM students "
                                                                    "WHERE class = ?", (clas, )).fetchall())), 1, True)[0]
            id = (QInputDialog.getText(self, "id книги", "Какую книгу берет ученик?")[0])
            if not cur.execute("SELECT * FROM students WHERE name = ?", (name, )).fetchall():
                cur.execute("INSERT INTO students(name, class) VALUES (?, ?)", (name, clas)).fetchall()

            cur.execute("UPDATE students SET book1 = ?, date = ?, date_of_delivery = ? WHERE name = ? AND class = ?", (
                id, datetime.date.today(), datetime.date.today() + datetime.timedelta(days=14), name, clas)).fetchall()
            cur.execute("UPDATE books SET number_in_school = number_in_school -1 WHERE id = ?", (id, )).fetchall()

            self.update_result('*')
            self.con.commit()
        except Exception:
            pass

    def find(self):
        try:
            id = QInputDialog.getText(self, "Введите id", "Что ищем?")[0]
            if len(id.split()) == 1 and id == '*' or len(id.split()) == 1 and id.isdigit() or id.split()[
                0].isdigit() and \
                    id.split()[-1].isdigit() and id.split()[1] == '-':
                self.update_result(id)
            else:
                self.statusBar().showMessage(f"Ошибка ввода")
                self.find()
        except Exception:
            pass

    def home(self):
        self.hide()


class MainForm(FirstForm, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('books_1_db.sqlite')
        self.cur = self.con.cursor()
        self.give_button.clicked.connect(self.give)
        self.put_button.clicked.connect(self.put)
        self.add_button.clicked.connect(self.add_book)
        self.data_button.clicked.connect(self.data)
        self.student_button.clicked.connect(self.student)

    def data(self):
        try:
            self.catalog_form = CatalogForm()
            self.catalog_form.show()
        except Exception:
            pass

    def student(self):
        self.student_form = StudentsForm()
        self.student_form.show()


class CatalogForm(FirstForm, catalog_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.con = sqlite3.connect("books_1_db.sqlite")
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.find)
        self.button_add.clicked.connect(self.add_book)
        self.foto_button.clicked.connect(self.barcode)
        self.home_button.clicked.connect(self.home)
        self.foto_button.setIcon(QIcon('camar.jpg'))
        self.foto_button.setIconSize(QSize(75, 15))
        self.modified = {}
        self.titles = None

        self.update_result('*')

    def update_result(self, text):
        try:
            cur = self.con.cursor()
            self.tableWidget.itemChanged.connect(lambda x: x)
            if '-' in text:
                self.item_id = tuple((int(text.split(' - ')[0]), int(text.split(' - ')[1])))
                result = cur.execute("SELECT * FROM books WHERE ? <= id AND id <= ?", self.item_id).fetchall()
            elif text == '*':
                self.item_id = 1, len(cur.execute("SELECT * FROM books").fetchall())
                result = cur.execute("SELECT * FROM books").fetchall()
            else:
                self.item_id = (int(text), int(text))
                self.tableWidget.itemChanged.connect(self.item_changed)
                result = cur.execute("SELECT * FROM books WHERE ? <= id AND id <= ?", self.item_id).fetchall()

            # Заполнили размеры таблицы
            self.tableWidget.setRowCount(len(result))
            # Если запись не нашлась, то не будем ничего делать
            if not result:
                self.statusBar().showMessage('Ничего не нашлось')
                return
            else:
                self.statusBar().showMessage(f"Нашлась запись с id = {self.item_id}")
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [i for i in cur.description]
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if j == 2:
                        self.tableWidget.setItem(i, j,
                                                 QTableWidgetItem(cur.execute("SELECT autor FROM autors WHERE id = ?",
                                                                              (val,)).fetchall()[0][0]))
                    elif j == 3:
                        self.tableWidget.setItem(i, j,
                                                 QTableWidgetItem(cur.execute("SELECT title FROM genres WHERE id = ?",
                                                                              (val,)).fetchall()[0][0]))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.tableWidget.resizeColumnsToContents()  # делаем ресайз колонок по содержимому
            self.modified = {}
        except Exception:
            pass

    def item_changed(self, item):
        try:
            self.modified[self.titles[item.column()]] = item.text()
        except Exception:
            pass

    def save_results(self):
        try:
            if self.modified:
                cur = self.con.cursor()
                que = "UPDATE films SET\n"
                que += ", ".join([f"{key}='{self.modified.get(key)}'"
                                  for key in self.modified.keys()])
                que += " WHERE id = ?"
                cur.execute(que, self.item_id)
                self.con.commit()
                self.modified.clear()
        except Exception:
            pass

    def barcode(self):
        try:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                cv2.imshow('frame', rgb)
                if cv2.waitKey(10) == 27:
                    out = cv2.imwrite('capture.jpg', frame)
                    break
            image = decode(Image.open('capture.jpg'))
            if image:
                pyperclip.copy(image[0].data.decode("utf-8"))
                self.statusBar().showMessage(f"id скопирован в буфер обмена")
            else:
                self.statusBar().showMessage(f"Не удолось сканировать")
        except Exception:
            self.statusBar().showMessage(f"Не удолось сканировать")


class StudentsForm(FirstForm, students_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("students.ui", self)
        self.con = sqlite3.connect("books_1_db.sqlite")
        self.button_give.clicked.connect(self.give)
        self.button_put.clicked.connect(self.put)
        self.button_find.clicked.connect(self.find)
        self.button_add.clicked.connect(self.add_student)
        self.home_button.clicked.connect(self.home)

        self.update_result('*')

    def add_student(self):
        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO students(name, class) VALUES (?, ?)", (
                        (QInputDialog.getText(self, "Имя", "Как зовут ученика?")[0]),
                        (QInputDialog.getText(self, "Класс", "В каком он(а) клвссе?")[0]))).fetchall()
            self.con.commit()
            self.update_result('*')
        except Exception:
            pass

    def update_result(self, text):
        try:
            cur = self.con.cursor()
            self.tableWidget.itemChanged.connect(lambda x: x)
            if '-' in text:
                self.item_id = tuple((int(text.split(' - ')[0]), int(text.split(' - ')[1])))
                result = cur.execute("SELECT * FROM students WHERE ? <= id AND id <= ?", self.item_id).fetchall()
            elif text == '*':
                self.item_id = 1, len(cur.execute("SELECT * FROM students").fetchall())
                result = cur.execute("SELECT * FROM students").fetchall()
            else:
                self.item_id = (int(text), int(text))
                result = cur.execute("SELECT * FROM students WHERE ? <= id AND id <= ?", self.item_id).fetchall()

            # Заполнили размеры таблицы
            self.tableWidget.setRowCount(len(result))
            # Если запись не нашлась, то не будем ничего делать
            if not result:
                self.statusBar().showMessage('Ничего не нашлось')
                return
            else:
                self.statusBar().showMessage(f"Нашлась запись с id = {self.item_id}")
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [i for i in cur.description]
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                    if j == 3 and val:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(cur.execute("SELECT title FROM books WHERE id = ?",
                                                                                    (val,)).fetchall()[0][0]))
            # делаем ресайз колонок по содержимому
            self.tableWidget.resizeColumnsToContents()
            self.modified = {}
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = FirstForm()
    ex = MainForm()
    ex.show()
    sys.exit(app.exec_())
