import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy import stats,polyval
import pylab as pl
import IntroUI #이게제일 나한테는 맞는 방법인
#from pylab import plot,title,show,legend


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.slope = 0
        self.intercept = 0
        self.r_value = 0
        self.p_value = 0
        self.stderr = 0
        self.ry =0 #예측식 y값 
        #리스트안에있는 객체들의 타입 대개 str타입이다. 그렇기때문에  stats.linregress안에 들어가는 리스트들이 갖고있는 값들을 int로 바꿔야
        #lx=IntroUI.g_victimcnt[0:len(IntroUI.g_missingpeoplecnt)]
        #ly=IntroUI.g_sortArrayDeadcnt[0:len(IntroUI.g_missingpeoplecnt)]
        for i in range(len(IntroUI.g_missingpeoplecnt)):
            IntroUI.g_sortArrayDeadcnt[i]=int(IntroUI.g_sortArrayDeadcnt[i])
            IntroUI.g_victimcnt[i]=int(IntroUI.g_victimcnt[i])
        self.slope,self.intercept,self.r_value,self.p_value,self.stderr = stats.linregress(IntroUI.g_victimcnt,IntroUI.g_sortArrayDeadcnt)
        self.ry = polyval([self.slope,self.intercept],IntroUI.g_victimcnt)
    
        self.setupUI()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 1000)
        self.setWindowTitle("PyChart Viewer v0.1")
        self.setWindowIcon(QIcon('icon.png'))

        self.lineEdit = QLineEdit()
        self.pushButton = QPushButton("DrawChart")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        
        self.fig = plt.Figure() 
        self.canvas = FigureCanvas(self.fig)
        self.Rogistec=plt.Figure()
        self.RogistecCanvas=FigureCanvas(self.Rogistec)
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.lineEdit)
        rightLayout.addWidget(self.pushButton)
        rightLayout.addWidget(self.RogistecCanvas)
        rightLayout.addStretch(1)
        
        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)
        
        self.setLayout(layout)

    def pushButtonClicked(self):
        self.fig.clear()
        self.Rogistec.clear()
        code = self.lineEdit.text() 
        ax = self.fig.add_subplot(111)
        rogi=self.Rogistec.add_subplot(111)


        if code=="":
            ax.plot(range(17), IntroUI.g_sortArrayDeadcnt, label='DeadPopulation') 
            ax.plot(range(17), IntroUI.g_victimcnt, label='VictimPeopleCnt')#이재민
            ax.plot(range(17), IntroUI.g_missingpeoplecnt, label='MissingPeopleCnt')   
           
           
            #ax.grid() 
        elif code=="사망자":
            ax.plot(range(17), IntroUI.g_sortArrayDeadcnt, label='DeadPopulation')
            
        elif code=="실종자":
            ax.plot(range(17), IntroUI.g_missingpeoplecnt, label='MissingPeopleCnt')
           
        elif code=="이재민":
            ax.plot(range(17), IntroUI.g_victimcnt, label='VictimPeopleCnt')#이재민
          
        ax.set_xticks(range(17))
        ax.set_xticklabels(IntroUI.g_sortArrayDate,rotation=45,fontsize=7)#fontsize는 default 10 
        ax.legend(loc='upper right') #
        ax.grid() 
        rogi.plot(IntroUI.g_victimcnt,IntroUI.g_sortArrayDeadcnt,'k.')
        rogi.plot(IntroUI.g_victimcnt,self.ry,'r.-')
        #rogi.title('Regrssion result')
        #rogi.legend(['Victimcnt','DeadPeoplecnt'])
        self.canvas.draw()
        self.RogistecCanvas.draw()
        
        
       
          #df = web.DataReader(code, "yahoo")
        #df['MA20'] = df['Adj Close'].rolling(window=20).mean()
        #df['MA60'] = df['Adj Close'].rolling(window=60).mean()
        #ax.plot(range(17), IntroUI.g_sortArrayDeadcnt, label='DeadPopulation')
        #ax.xticks(range(17),IntroUI.g_sortArrayDate)
        #ax.plot(x, y, label='MA20') #1차실
         #ax.plot(df.index, df['MA60']) #그래프의 선들이 무엇인지 표시하는것들,라벨 지정 안해도 불러오면 알아서 default로 이름 
         #ax.legend(loc='upper right') #그래프의 선들이 무엇인지 표시하는것들의 위치 지정 함수 
        #ax.grid() #뒤에 격자모양을그려 좀더 안정감있게 그려줌.