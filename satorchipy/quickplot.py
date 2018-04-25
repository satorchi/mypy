'''
$Id: quickplot.py
$auth: Steve Torchinsky <satorchi@apc.in2p3.fr>
$created: Wed 25 Apr 2018 07:33:21 CEST
$license: GPLv3 or later, see https://www.gnu.org/licenses/gpl-3.0.txt

          This is free software: you are free to change and
          redistribute it.  There is NO WARRANTY, to the extent
          permitted by law.

make a plot with some basic labeling
'''
import matplotlib.pyplot as plt
def quickplot(x=None,y=None,title='working',fig=None):
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
