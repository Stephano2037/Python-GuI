# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 00:17:53 2017

@author: All
"""
import sqlite3 #가벼운 DB sqlite3
import sys
import disasterintroui
import showpopulationeffectbydisaster #uifile
#import showpopdisaster
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * #table 쓰기위한 import 형식 
from xml.dom.minidom import parse,parseString
from xml.etree import ElementTree
from http.client import HTTPConnection
import ShowGraph 
DBcon=None
cursor=None
conn =None;
year=None
g_sortArrayDate=[]
g_sortArrayDeadcnt=[]
g_missingpeoplecnt= []
g_victimcnt=[] #이재민수

server = "openapi.mpss.go.kr"
regKey='DDXL%2BLNCCmRozJ46Dxv%2FMprdc%2FeMiRN5XZpSCGAjBdGn5KC%2FnSSc3%2FhC8sFOWNQkC1ADJgG%2FRgdUEsF%2FdF6gg%3D%3D'

'''
def Uishow(Ui_table,getInstanceself):
     Ui_table.setupUi(getInstanceself)
'''
class DisasterIntro(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.completed=0
        self.sortArrayDate=[]
        self.ui = disasterintroui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(self.completed)
        self.ui.pushButton.clicked.connect(self.button_clicked)#버튼눌를때 넘어가게
    
    def button_clicked(self):
        global year
        if self.ui.lineEdit.text() == '2015':
            year='2015'     
            self.dictofDatePeople={}
            self.dictOfDatePeople=self.SearchDeathPopulation(); 
            self.tupleofDateandDeathnum=self.distinguishKeyValueFromDictwithSort(self.dictOfDatePeople)
            self.show = showpopulationeffectbydisaster.Ui_MainWindow()#ui를 py로 바꾼파일의 전체 메인클래스가져온다.
            self.Uishow(self.show,self)
            
    def exit_clicked(self):
        print(1)
        sys.exit()
    
    def draw_graphClicked(self):
    
        self.mywindow = ShowGraph.MyWindow()
        self.mywindow.show()

    def saveDB_clicked(self):
        global cursor,g_sortArrayDate,g_sortArrayDeadcnt,g_missingpeoplecnt,g_victimcnt,DBcon
        cursor.execute("DROP TABLE IF EXISTS Disaster")
        cursor.execute("CREATE TABLE Disaster(Period text,DeathCnt int,MissingCnt int,VictimCnt int)")
        for i in range(len(g_sortArrayDate)):
            cursor.execute("INSERT INTO Disaster VALUES(?,?,?,?)",
                           (g_sortArrayDate[i],g_sortArrayDeadcnt[i],g_missingpeoplecnt[i],g_victimcnt[i]))
        DBcon.commit();
        DBcon.close();
    def InitiateDb(self):
        global DBcon,cursor
        if DBcon==None:
            DBcon = sqlite3.connect("./DisasterGUi.db")
            sqlite3.Connection
            print("Complete Connect to Database")
        if cursor==None:
            cursor=DBcon.cursor()
            print("Get cursor of DataBase")
        
    def Uishow(self,Ui_table,getInstanceself):
        global g_sortArrayDate,g_sortArrayDeadcnt,g_missingpeoplecnt
        self.InitiateDb() # db연
        column_headers=['재해발발기간','사망자수','이재민수','실종자']
        Ui_table.setupUi(getInstanceself)   
        Ui_table.pushButton.clicked.connect(self.saveDB_clicked)
        Ui_table.pushButton_3.clicked.connect(self.draw_graphClicked)#나가기가아닌 그래프그리는버
        Ui_table.pushButton_4.clicked.connect(self.exit_clicked)
        #db헤
        Ui_table.tableWidget.setHorizontalHeaderLabels(column_headers)
        for col in range(4):
                if col==0:
                    for raw, val in enumerate(g_sortArrayDate):
                        item= QTableWidgetItem(str(val))
                        Ui_table.tableWidget.setItem(raw,col,item)
                elif col==1:
                    for raw, val in enumerate(g_sortArrayDeadcnt):
                        item= QTableWidgetItem(str(val))
                        Ui_table.tableWidget.setItem(raw,col,item)
                elif col==2:
                    for raw, val in enumerate(g_victimcnt):
                        item= QTableWidgetItem(str(val))
                        Ui_table.tableWidget.setItem(raw,col,item)
                elif col==3:
                    for raw, val in enumerate(g_missingpeoplecnt):
                        item= QTableWidgetItem(str(val))
                        Ui_table.tableWidget.setItem(raw,col,item)
   
        
    def uriBuilder(self,server,service,year):
    #service = service_type_information
        global regKey
        self.uri =  "https://"+server+"/openapi/service/"+service+"?serviceKey="+regKey+"&year="+year;
        return self.uri;
    
    def connectOpenAPIServer(self):
        global conn,server
        conn = HTTPConnection(server);
        print("conn",conn)
                         
    def SearchDeathPopulation(self):
        global year
        global conn;
        if conn==None:
            self.connectOpenAPIServer()
            
        self.uri = self.uriBuilder(server,"disasterInfoService/getPeriodicDisaster",year);  
        conn.request("GET",self.uri) #이 사이트에대한  메인화면을 요청하는 방법   
        self.req = conn.getresponse()
        
        if int(self.req.status)==200:
            while self.completed<100:
                self.completed+=0.1
                self.ui.progressBar.setValue(self.completed)
            print("GetDiasterDataDownloading complete")
        #extractDeadpeople(req.read());
            return self.extractDeadpeople(self.req.read())
        else:
            print ("OpenAPI request has been failed!! please retry")
            return None
    def extractDeadpeople(self,strXML):
    
        self.tree=ElementTree.fromstring(strXML);
        self.itemElements = list(self.tree.iter("item"))
        self.nodedic={}
        self.disasterdate=None;
        self.deadpeopleCnt=None;
   
        for self.item in self.itemElements:
     
            self.disasterdate = self.item.find("title").text
            self.deadpeopleCnt = self.item.find("deadcnt").text
            g_missingpeoplecnt.append(self.item.find("misscnt").text)
            g_victimcnt.append(self.item.find("victimcnt").text)
            self.nodedic[self.disasterdate] = self.deadpeopleCnt;
        print(self.nodedic)
        return self.nodedic

    def distinguishKeyValueFromDictwithSort(self,dictionary):
        global cursor,g_sortArrayDate,g_sortArrayDeadcnt,g_missingpeoplecnt  
    #간단한 정렬기능 , 기간과 사람사망자에만 한정되있는 키,value 분리 메소드 
        self.num=[]
        for self.title in dictionary:
            g_sortArrayDate.append(self.title)
            g_sortArrayDeadcnt.append(dictionary[self.title])
      
        for self.i in range(len(g_sortArrayDate)):
            self.Number = str(g_sortArrayDate[self.i][5])+str(g_sortArrayDate[self.i][6])+str(g_sortArrayDate[self.i][8])+str(g_sortArrayDate[self.i][9])
            self.num.append(int(self.Number))
    #인덱스로 값들 정렬하기
        for self.i in range(len(g_sortArrayDate)):
            for self.j in range(self.i+1,len(g_sortArrayDate)):
                if(self.num[self.i]>self.num[self.j]):
          
                
                    self.temp = self.num[self.i]
                    self.num[self.i] = self.num[self.j];
                    self.num[self.j]=self.temp
              
                
                    self.temp = g_sortArrayDate[self.i];
                    g_sortArrayDate[self.i]=g_sortArrayDate[self.j]
                    g_sortArrayDate[self.j] = self.temp;
               
                    self.temp = g_sortArrayDeadcnt[self.i];
                    g_sortArrayDeadcnt[self.i]=g_sortArrayDeadcnt[self.j]
                    g_sortArrayDeadcnt[self.j] = self.temp;
                
                    self.temp = g_missingpeoplecnt[self.i]
                    g_missingpeoplecnt[self.i] =g_missingpeoplecnt[self.j]
                    g_missingpeoplecnt[self.j] =self.temp
                                      
             

        return g_sortArrayDate,g_sortArrayDeadcnt  

    


        
