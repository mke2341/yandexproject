import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QInputDialog
from project1 import Ui_MainWindow


class MyWidget(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.btn.clicked.connect(self.Vo)
        self.btn.clicked.connect(self.DNAPOL)
        self.btn.clicked.connect(self.FWPR)
        self.btn.clicked.connect(self.REVPR)
        self.btn.clicked.connect(self.KCL)
        self.btn.clicked.connect(self.DNA)
        self.btn.clicked.connect(self.BUF)        
        self.btn.clicked.connect(self.DNTP)
        self.btn.clicked.connect(self.WATER)
        
    def Vo(self):
        self.v = float(self.Volume.text())
        
    def DNAPOL(self):
        try:
            a = float(self.CDNAPOL.text())
            self.VDNAPOL.setText(str(round((0.03 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())        
    
    def FWPR(self):
        try:
            a = float(self.CFWPR.text())
            self.VFWPR.setText(str(round((30000 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())          
    
    def REVPR(self):
        try:
            a = float(self.CREVPR.text())
            self.VREVPR.setText(str(round((30000 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())  
            
    def KCL(self):
        try:
            a = float(self.CKCL.text())
            self.VKCL.setText(str(round((40 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())          
    
    def DNA(self):
        try:
            a = float(self.CDNA.text())
            self.VDNA.setText(str(round((4.5 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())              
    
    def BUF(self):
        try:
            a = float(self.CBUF.text())
            self.VBUF.setText(str(round((0.15 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())          
    
    def DNTP(self):
        try:
            a = float(self.CDNTP.text())
            self.VDNTP.setText(str(round((1.6 * self.v/a), 2)))
        except:
            sys.exit(app.exec_())          
    
    def WATER(self):
        try:
            c = self.v - float(self.VDNTP.text()) - float(self.VBUF.text()) - float(self.VDNA.text())
            - float(self.VKCL.text()) - float(self.VFWPR.text()) - float(self.VREVPR.text())
            - float(self.VDNAPOL.text())
            if c < 0:
                c = 0
            self.VWater.setText(str(c))
        except:
            sys.exit(app.exec_())         

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())