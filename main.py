# coding=utf-8


import sys

from PyQt5 import QtWidgets
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
import pandas as pd
import datetime

class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("/Users/kimji/study/log4jViewerUI/fileSelect.ui", self)
        #self.ui = uic.loadUi("/Users/kimji/MIH/SHINWON/logs/y#96/server.2020-11-20.8.log", self)
        self.localFile.clicked.connect(self.localFileFunc)
        self.sfptFile.clicked.connect(self.sfptFileFunc)
        self.btnFileSelect.clicked.connect(self.clickBtnFileSelect)

        self.filePath.setText("/Users/kimji/study/log4jViewer/sample/sample.log")
        self.btnReadFile.clicked.connect(self.file_read)
        self.logTable.setColumnCount(7)
        self.logTable.setHorizontalHeaderLabels(["Date", "Time", "Priority", "Transaction", "Thread", "Category", "Log"])

        self.transactionList.clicked.connect(self.searchByTransaction)

    def file_read(self):
        fileName = self.filePath.text()
        front_line = ''
        outLine = []
        nullIndex = 3
        slicePos = 0

        with open(fileName) as file:
            for line in file:
                if len(front_line) == 0:
                    front_line = line

                current_line = line
                front_line = current_line

                split_line = current_line.split(' ')

                if split_line[0] != '' and self.checkDateType(split_line[0]):

                    if outLine != [] :
                        self.setLogData(outLine)

                    outLine = []
                    outLine.insert(0, split_line[0])
                    slicePos += len(split_line[0])

                    outLine.insert(1, split_line[1])
                    slicePos += len(split_line[1])

                    if split_line[nullIndex - 1] == '':
                        outLine.insert(2, split_line[nullIndex])
                        slicePos += len(split_line[nullIndex])

                        outLine.insert(3, split_line[nullIndex + 1])
                        slicePos += len(split_line[nullIndex + 1])

                        outLine.insert(4, split_line[nullIndex + 2])
                        slicePos += len(split_line[nullIndex + 2])

                        outLine.insert(5, split_line[nullIndex + 3])
                        slicePos += len(split_line[nullIndex + 3])

                        slicePos += 7
                    else:
                        outLine.insert(2, split_line[nullIndex - 1])
                        slicePos += len(split_line[nullIndex - 1])

                        outLine.insert(3, split_line[nullIndex])
                        slicePos += len(split_line[nullIndex])

                        outLine.insert(4, split_line[nullIndex + 1])
                        slicePos += len(split_line[nullIndex + 1])

                        outLine.insert(5, split_line[nullIndex + 2])
                        slicePos += len(split_line[nullIndex + 2])

                        slicePos += 6
                    outLine.insert(6, current_line[slicePos: len(current_line)])
                    slicePos = 0
                else:
                    outLine[6] = outLine[6] + line
        self.setLogData(outLine)

    # 로컬에서 파일선택 클릭
    def localFileFunc(self) :
        print("로컬에서 파일선택")

    # 파일선택 버튼 클릭
    def clickBtnFileSelect(self):
        fname = QFileDialog.getOpenFileName(self)
        print(fname[0])
        self.filePath.setText(fname[0])

    # SFTP 연결 클릭
    def sfptFileFunc(self) :
        print("SFTP 연결")

    def checkDateType(self, str):
        date_format = '%Y-%m-%d'

        try:
            datetime.datetime.strptime(str, date_format).date()
            return True
        except ValueError:
            return False

    def setLogData(self, data):
        row = self.logTable.rowCount()

        self.logTable.setRowCount(row+1)
        for idx, item in enumerate(data):
            self.logTable.setItem(row, idx, QTableWidgetItem(item))


        findItem = self.transactionList.findItems(data[3], QtCore.Qt.MatchExactly)
        if len(findItem) == 0 :
            self.transactionList.addItem(data[3])

    def searchByTransaction(self):
        print("searchByTransaction")

        findText = self.transactionList.currentItem().text()

        items = self.logTable.findItems(
            findText, QtCore.Qt.MatchRecursive)


        if items :
            # for item in items :
            #     row = item.row()
            #     self.logTable.hideRow(row)


            results = '\n'.join(
                'row %d column %d' % (item.row() + 1, item.column() + 1)
                for item in items)
        else:
            results = 'Found Nothing'

        print(results)
        # QtGui.QMessageBox.information(self, 'Search Results', results)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = Form()

    w.show()

    sys.exit(app.exec())