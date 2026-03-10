from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from random import choice
import requests
import segno

class Ui_Estudo(object):
    def setupUi(self, Estudo):
        Estudo.setObjectName("Estudo")
        Estudo.resize(283, 101)
        self.gridLayout = QtWidgets.QGridLayout(Estudo)
        self.gridLayout.setObjectName("gridLayout")
        self.label_nome = QtWidgets.QLabel(Estudo)
        self.label_nome.setObjectName("label_nome")
        self.gridLayout.addWidget(self.label_nome, 0, 0, 1, 1)
        self.lineEdit_Url = QtWidgets.QLineEdit(Estudo)
        self.lineEdit_Url.setObjectName("lineEdit_Url")
        self.gridLayout.addWidget(self.lineEdit_Url, 1, 0, 1, 2)
        self.Botao_criar = QtWidgets.QPushButton(Estudo)
        self.Botao_criar.setObjectName("Botao_criar")
        self.Botao_criar.clicked.connect(self.criar_qrcode)
        self.gridLayout.addWidget(self.Botao_criar, 2, 1, 1, 1)

        self.retranslateUi(Estudo)
        QtCore.QMetaObject.connectSlotsByName(Estudo)

    def retranslateUi(self, Estudo):
        _translate = QtCore.QCoreApplication.translate
        Estudo.setWindowTitle(_translate("Estudo", "Dialog"))
        self.label_nome.setText(_translate("Estudo", "Digite o nome do cantor:"))
        self.Botao_criar.setText(_translate("Estudo", "Criar Qrcode"))

    def criar_qrcode(self):
        parametros = {  
            "part": "snippet",
            "q": f"{self.lineEdit_Url.text()}",
            "type": "video",
            "maxResults": 11,
            "key": ':D'
            
        }

        resposta=requests.get(f"https://www.googleapis.com/youtube/v3/search",params=parametros).json()

        ids_videos = [item["id"]["videoId"] for item in resposta["items"] if item["id"]["kind"] == "youtube#video"]
        segno.make_qr(f"https://www.youtube.com/watch?v={choice(ids_videos)}").save("qrcode.png",scale=10)
        dialog= QDialog()
        dialog.setWindowTitle("qrcode")
        layout=QVBoxLayout()
        label=QLabel()
    
        pixmap= QPixmap("qrcode.png")
        label.setPixmap(pixmap)

        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Estudo = QtWidgets.QDialog()
    ui = Ui_Estudo()
    ui.setupUi(Estudo)
    Estudo.show()
    sys.exit(app.exec_())