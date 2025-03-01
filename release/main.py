import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Form


class Form(QMainWindow, Ui_Form):
    def __init__(self, parent, id=-1):
        super().__init__(parent)
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.con.cursor()
        self.id = id
        self.p = parent
        if id != -1:
            self.dat = self.cur.execute(
                f'SELECT id, sort, burn, type, taste, price, size FROM Coffies WHERE id = {id}').fetchone()
            for i in range(1, 7):
                eval(f'self.edit{i}.setText(str(self.dat[{i}]))')
        self.btn.clicked.connect(self.do)

    def do(self):
        if self.id != -1:
            self.cur.execute(
                f'UPDATE Coffies SET sort = ?, burn = ?, type = ?, taste = ?, price = ?, size = ? WHERE id = {self.id}',
                [eval(f'self.edit{i}.text()') for i in range(1, 7)])
        else:
            self.cur.execute(f'INSERT INTO Coffies (sort, burn, type, taste, price, size) VALUES (?, ?, ?, ?, ?, ?)',
                             [eval(f'self.edit{i}.text()') for i in range(1, 7)])
        self.con.commit()
        self.p.search()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.con.cursor()
        self.search()
        self.add.clicked.connect(self.addform)
        self.edit.clicked.connect(self.editform)

    def search(self):
        res = self.cur.execute('SELECT id, sort, burn, type, taste, price, size FROM Coffies').fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена РБ',
             'Объем упаковки ML'])
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def addform(self):
        prog = Form(self)
        prog.show()

    def editform(self):
        prog = Form(self, int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()))
        prog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
