''' ps_test_QWebView1.py
exploring PySide.QtWebKit.QWebView()
display a web page with a given url
(PySide is the official LGPL-licensed version of PyQT)
for Python33 you can use the Windows self-extracting installer
PySide-1.2.1.win32-py3.3.exe
from:
http://qt-project.org/wiki/PySide
or:
http://www.lfd.uci.edu/~gohlke/pythonlibs/
PySide 1.2.1 (August 16, 2013) has access to the complete Qt 4.8 framework
modified example from:
http://www.pyside.org/docs/pyside/PySide/QtWebKit/
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
# create a PySide/PyQt application
app = QApplication([])
# create a PySide.QtWebKit.QWebView() to display a web page
# (your computer needs to be connected to the internet)
view = QWebView()
# setGeometry(x_pos, y_pos, width, height)
view.setGeometry(100, 150, 1200, 600)
# pick a known url
#url = "http://www.google.com/"
url = "http://www.DaniWeb.com/"
view.setWindowTitle(url)
view.load(QUrl(url))
view.show()
# run the application event loop
app.exec_()