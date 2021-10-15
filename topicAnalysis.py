from matplotlib import pyplot as plt

def plotHist(x:list, xAxis:str='Count', yAxis:str='Date', topic:str='Histogram'):

    plt.hist(x)
    plt.set(xlabel=xAxis, ylabel=yAxis, title=topic)
    plt.show()

def plotScatter(x:list, y:list, xAxis:str='X', yAxis:str='Y', topic:str=''):

    if topic ==  '':
        topic = yAxis + ' vs. ' + xAxis
    plt.scatter(x,y)
    plt.set(xlabel=xAxis, ylabel=yAxis, title=topic)
    plt.show()