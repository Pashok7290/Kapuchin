import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.search()

    def search(self):
        res = self.cur.execute('SELECT id, sort, burn, type, taste, price, size FROM Coffies').fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена РБ', 'Объем упаковки ML'])
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
