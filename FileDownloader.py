from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import sys, pyodbc, time
from threading import Thread

import urllib.request

class Downloader(QDialog):

    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        self.url = QLineEdit()
        #self.url.setReadOnly(True)
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("Download")
        browse = QPushButton("Browse")
        self.webview = QWebView()
        self.webpage = QWebPage()
        self.webview.setPage(self.webpage)

        self.url.setPlaceholderText("URL")
        self.save_location.setPlaceholderText("File save location")

        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.url)
        layout.addWidget(self.webview)
        layout.addWidget(self.save_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        self.setLayout(layout)

        self.setWindowTitle("PyDownloader")
        self.setFocus()

        download.clicked.connect(self.downloadthread.start)
        browse.clicked.connect(self.browse_file)

    def browse_file(self):
        ##save_file = QFileDialog.getSaveFileName(self,caption="Save File As", directory=("."),
        ##                                        filter="All Files (*.*)")
        save_file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.save_location.setText(QDir.toNativeSeparators(save_file))

    def download(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=CODICPLPT039;'
                              'Database=TEST;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute("SELECT TOP (10) ManufacturerItemNumber, ItemImageURL FROM Tbl_scansource WHERE Manufacturer='Datalogic' ")
        self.updater = conn.cursor()

        for row in cursor:
            url = row[1]
            item = row[0]

            #_thread.start_new_thread(self.download_thread, (row[1], row[0]))
            if url != "":
                self.url.setText(url)


            #save_location = self.save_location.text() + "\\" + item + ".jpg"
            #print(save_location)
            #try:
            #    urllib.request.urlretrieve(url, save_location, self.report)
            #    #self.updater.execute("UPDATE Tbl_scansource SET FileDownloaded=1 WHERE ManufacturerItemNumber = ?",
            #    #                     item)
            #except Exception:
            #    print("The download failed for item " + item)
            #    #self.updater.execute(
            #    #    "UPDATE Tbl_scansource SET FileDownloaded=0, FileDownloadError=?  WHERE ManufacturerItemNumber = ?",
            #    #    "The download failed for item " + item, item)
            #    # QMessageBox.warning(self, "Warning", "The download failed")
        self.progress.setValue(0)
        self.url.setText("")
        self.save_location.setText("")
        QMessageBox.information(self, "Information", "All downloads are completed")

    def download_thread(self, url, item):
        save_location = self.save_location.text() + "\\" + item + ".jpg"
        try:
            urllib.request.urlretrieve(url, save_location, self.report)
            #self.updater.execute("UPDATE Tbl_scansource SET FileDownloaded=1 WHERE ManufacturerItemNumber = ?",item)
        except Exception:
            print("The download failed for item " + item)
            #self.updater.execute("UPDATE Tbl_scansource SET FileDownloaded=0, FileDownloadError=?  WHERE ManufacturerItemNumber = ?","The download failed for item " + item , item)
            #QMessageBox.warning(self, "Warning", "The download failed")

    def report(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar *100 / totalsize
            self.progress.setValue(int(percent))

app = QApplication(sys.argv)
dl = Downloader()
dl.show()
app.exec_()