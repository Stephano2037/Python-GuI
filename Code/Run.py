# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:44:55 2017

@author: All
"""
#Qlabel 은 text
#Qpushbutton 은 버튼 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from IntroUI import *
'''
print(sys.argv)#['D:/Python/GuiPython/HelloPyqt.py'] #현재파일의절대경
app = QApplication(sys.argv)#App인스턴스생성, app변수로 바인딩
#label = QLabel("Hello Pyqt")#ui 구성 담당 ,인스턴스 생
label = QPushButton("Quit")
label.show()
app.exec_()#exec_()메서드를 호출하면 프로그램은 이벤트 루프에 진
'''
#이벤트루프란 무한반복하면서 이벤트를 처리하는 상태 
#항상 윈도우기반 프로그램은 사용자가 윈도우 창을 닫기전까지 계속 실행된 채로 
#남아있는다.
#윈도우창을 클릭하면 클릭이벤트가 발생하는데, 이때 이벤트 루프에서 클릭이벤트
#에대해 처리를 해주는것 

if __name__=="__main__":
    app=QApplication(sys.argv)
    disasterintro=DisasterIntro()
    disasterintro.show()
    app.exec_()