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

        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse_file)
        self.save_location.setText(r'C:\data\Leveranciers.C-schijf\Codipack\ArtikelLijsten\ImagesTest')

    def browse_file(self):
        ##save_file = QFileDialog.getSaveFileName(self,caption="Save File As", directory=("."),
        ##                                        filter="All Files (*.*)")
        save_file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.save_location.setText(QDir.toNativeSeparators(save_file))

    def download(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=CODICPLPT039;'
                              'Database=TEST;'
                              'Trusted_Connection=yes;'
                              'MARS_Connection=Yes;')
        conn2 = pyodbc.connect('Driver={SQL Server};'
                              'Server=CODICPLPT039;'
                              'Database=TEST;'
                              'Trusted_Connection=yes;'
                              'MARS_Connection=Yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT [dbo].[Tbl_Scansource].ManufacturerItemNumber, [dbo].[Tbl_Scansource].[ItemImageURL] FROM dbo.Tbl_Zebra LEFT OUTER JOIN dbo.Tbl_Scansource ON dbo.Tbl_Zebra.[product id] = [dbo].[Tbl_Scansource].[ManufacturerItemNumber] WHERE Tbl_Zebra.Picture = ''")
        updater = conn2.cursor()
        FailedImages = []
        for row in cursor:

            url = row[1]
            item = row[0]
            print(item)
            #_thread.start_new_thread(self.download_thread, (row[1], row[0]))
            if url != "":
                self.url.setText(url)
                save_location_path = self.save_location.text() + "\\" + str(item) + ".jpg"
                #print(save_location_path)
                try:
                    urllib.request.urlretrieve(url, save_location_path, self.report)
                    self.progress.setValue(0)
                    self.url.setText("")
                    updater.execute("UPDATE [dbo].[Tbl_Zebra] SET [Picture] = ? WHERE [product id] = ?",
                                    (item + ".jpg"), item)
                    updater.commit()

                except Exception:
                    FailedImages.append(item)
                    #print(item)
                    #self.updater.execute(
                    #    "UPDATE Tbl_scansource SET FileDownloaded=0, FileDownloadError=?  WHERE ManufacturerItemNumber = ?",
                    #    "The download failed for item " + item, item)
                    #QMessageBox.warning(self, "Warning", "The download failed")

        cursor.execute("SELECT [dbo].[Tbl_Jarltech].ORIGINAL_ART_NO, [dbo].[Tbl_Jarltech].[PICTURE] FROM dbo.Tbl_Zebra LEFT OUTER JOIN dbo.Tbl_Jarltech ON dbo.Tbl_Zebra.[product id] = [dbo].[Tbl_Jarltech].[ORIGINAL_ART_NO] WHERE Tbl_Zebra.Picture = ''")
        for row in cursor:

            url = row[1]
            item = row[0]
            print(item)
            #_thread.start_new_thread(self.download_thread, (row[1], row[0]))
            if url != "":
                self.url.setText(url)
                save_location_path = self.save_location.text() + "\\" + str(item) + ".jpg"
                #print(save_location_path)
                try:
                    urllib.request.urlretrieve(url, save_location_path, self.report)
                    self.progress.setValue(0)
                    self.url.setText("")
                    updater.execute("UPDATE [dbo].[Tbl_Zebra] SET [Picture] = ? WHERE [product id] = ?",
                                    (item + ".jpg"), item)
                    updater.commit()

                except Exception:
                    FailedImages.append(item)
                    #print(item)
                    #self.updater.execute(
                    #    "UPDATE Tbl_scansource SET FileDownloaded=0, FileDownloadError=?  WHERE ManufacturerItemNumber = ?",
                    #    "The download failed for item " + item, item)
                    #QMessageBox.warning(self, "Warning", "The download failed")

        ##self.save_location.setText("")
        QMessageBox.information(self, "Information", "All downloads are completed")
        print("Failed downloads: " )
        print(FailedImages)

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