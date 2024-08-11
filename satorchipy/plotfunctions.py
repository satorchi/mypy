'''
$Id: plotfunctions.py
$auth: Steve Torchinsky <satorchi@apc.in2p3.fr>
$created: Wed 25 Apr 2018 07:33:21 CEST
$license: GPLv3 or later, see https://www.gnu.org/licenses/gpl-3.0.txt

          This is free software: you are free to change and
          redistribute it.  There is NO WARRANTY, to the extent
          permitted by law.

some plotting utilities
'''
import matplotlib.pyplot as plt

def quickplot(x=None,y=None,title='working',fig=None):
    '''
    make a plot with some basic labeling
    '''
    
    plt.ion()
    if fig is None:
        fig=plt.figure(figsize=(12.8,4.8))
        fig.canvas.set_window_title('plt: '+title)
        plt.title(title)
    ax=fig.axes[0]
    if y is None: ax.plot(x,label=title)
    else: ax.plot(x,y,label=title)
    ax.legend()
    return fig

def newplot():
    # start a new plot
    fig = plt.figure()
    fig.canvas.manager.set_window_title('plt: working')
    ax = fig.add_axes([0.02,0.05,0.97,0.85])
    return fig,ax

        
def figtitle():
    # name the window of the current figure
    fig=plt.gcf()
    fig.canvas.manager.set_window_title('plt: working')
    return

def closeall():
    # close all plot windows
    plt.close('all')
    return

def savefig(pngname,fig=None):
    # save a figure
    if fig is None: fig = plt.gcf()
    fig.savefig(pngname,format='png',dpi=100,bbox_inches='tight')
    return

global mousepts
mousepts = []
def mouse_click(event):
    global mousepts
    x, y = event.xdata, event.ydata
    if x is None or y is None: return

    msg = '%.8e %.8e\n' % (x,y)
    
    h = open('mousepts.txt','a')
    h.write(msg)
    h.close()
    print(msg)
    return

def mouse_click_int(event):
    global mousepts
    x, y = event.xdata, event.ydata
    mousepts.append((x,y))
    print(int(x), y)
    return

def mouse_click_date(event):
    x, y = event.xdata, event.ydata
    # convert matplotlib to datetime
    # https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html
    # matplotlib: days since 0001-01-01 00:00:00 UTC plus one day
    # tstamp0 = float(str2dt('0001-01-01 00:00:00').strftime('%s'))
    # #tstamp0 -= (24*3600 - 600 + 40 - 1) # weird extra correction?
    # tstamp0_days = tstamp0/3600/24
    # x_stamp = (x + tstamp0_days)*3600*24
    if x is None: return
    x_stamp = x*3600*24
    x_date = dt.datetime.utcfromtimestamp(x_stamp)
    print(x,x_date.strftime('%Y-%m-%d %H:%M:%S.%f'), y)
    return
          
def winminmax(ax=None,data=None,plot=True):
    '''
    find the max/min values in the window and mark them if requested
    '''
    if ax is None: ax = plt.gca()
    while data is None:
        for child in ax.get_children():
            if isinstance(child,matplotlib.lines.Line2D):
                data = child.get_data()
    if data is None:
        print('Could not get the data')
        return None
    winxmin,winxmax = ax.axis()[0:2]
    mask = (data[0]>=winxmin) & (data[0]<=winxmax)
    print('npts: %i' % mask.sum())
    if mask.sum()==0:
        print('no data in the plot window')
        return None
    ymin = data[1][mask].min()
    ymax = data[1][mask].max()
    imin = np.argmin(data[1][mask])
    imax = np.argmax(data[1][mask])
    xmin = data[0][mask][imin]
    xmax = data[0][mask][imax]
    if plot:
        bot,top = ax.axis()[2:]
        ax.plot(xmin,ymin,ls='none',marker='v',markersize=15,color='red')
        ax.plot(xmax,ymax,ls='none',marker='^',markersize=15,color='red')
        

    return xmin,xmax,ymin,ymax
