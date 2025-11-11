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
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
nice_plot_colours = ['green',
                     '#1f77b4ff',
                     '#a20cffff',
                     'olive',
                     'red',
                     'blue',
                     'purple',
                     '#00cc00',
                     '#7210a7',
                     'darkblue',
                     '#cc0000',
                     'black',
                     'magenta',
                     'cyan']
nice_plot_markers = ['.','x','d','v','^','o']

labelprops = {}
labelprops['alpha'] = 0.50
labelprops['facecolor'] = 'red'
labelprops['boxstyle'] = 'round'
labelprops['edgecolor'] = 'red'

def get_colour(idx):
    '''
    get a nice plot colour
    '''
    ncolours = len(nice_plot_colours)
    while idx>ncolours:
        idx -= ncolours
    return nice_plot_colours[idx]

def get_marker(idx):
    '''
    get a nice plot marker
    '''
    nmarkers = len(nice_plot_markers)
    while idx>nmarkers:
        idx -= nmarkers
    return nice_plot_markers[idx]


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

    msg = '%.16e %.16e\n' % (x,y)
    
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
    if x is None: return
    x_stamp = x*3600*24
    x_date = dt.datetime.fromtimestamp(x_stamp)
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

def plot_flags(ax,flag,flagpos=None):
    '''
    plot labels at data time positions

    arguments:

    ax:  matplotlib axis
    flag: dictionary with keys that are datetime
    '''
    if flagpos is None:
        minmax = ax.axis()[2:]
        flagpos = minmax[0] + 0.3*(minmax[1] - minmax[0])
    for flag_time in flag.keys():
        tstamp = flag_time.timestamp()
        axmin_stamp = ax.axis()[0]*3600*24
        axmin_date = dt.datetime.fromtimestamp(axmin_stamp)
        axmax_stamp = ax.axis()[1]*3600*24
        axmax_date = dt.datetime.fromtimestamp(axmax_stamp)

        if flag_time > axmin_date and flag_time < axmax_date:
            ax.plot([flag_time,flag_time],ax.axis()[2:],ls='dashed',color='red')
            ax.text(flag_time,flagpos,flag[flag_time],
                    ha='center',va='bottom',rotation=90,
                    fontsize=18,
                    color='black',
                    bbox=labelprops)
    return    

def make_legend_label(val_name,val_str,legend_width=40):
    nspaces = legend_width  - len(val_str)
    if val_str.find('times')>0:
        latex_stripped = val_str.replace('$','').replace('{','').replace('}','').replace('\\times','X')
        nspaces = legend_width - len(latex_stripped)
    lbl = '%s%s' % (val_name.ljust(nspaces),val_str)
    print(lbl)
    return lbl

def plot_dayboundaries(ax,H=18,M=0,S=0):
    '''
    plot vertical lines showing the days

    ax is a matplotlib axis with x-axis in datetime

    arguments:
    H,M,S : hour, minutes seconds for the start of each day
            18:00 UT corresponds to Alto Chorrillos peak temperature
    '''

    minmax = np.array(ax.axis())
    xminmax = minmax[:2]
    yminmax = minmax[2:]
    x_stamp = xminmax*3600*24
    d_start = dt.datetime.fromtimestamp(x_stamp[0])
    d_end = dt.datetime.fromtimestamp(x_stamp[1])

    first_day = dt.datetime(year=d_start.year,month=d_start.month,day=d_start.day,hour=H,minute=M,second=S)
    last_day = dt.datetime(year=d_end.year,month=d_end.month,day=d_end.day,hour=H,minute=M,second=S)

    day = first_day
    while day<=last_day:
        ax.plot([day,day],yminmax,ls='dotted',color='grey')
        day += dt.timedelta(hours=24)

    return

        
    
    
