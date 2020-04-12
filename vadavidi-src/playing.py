print("hello");

if True:
    # https://datatofish.com/scatter-line-bar-charts-using-matplotlib/
    import matplotlib.pyplot as plt
    xAxis = [6.1,5.8,5.7,5.7,5.8,5.6,5.5,5.3,5.2,5.2]
    yAxis = [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
    plt.plot(xAxis,yAxis)
    plt.show()

if False:
    #http://www.pygal.org/en/latest/documentation/first_steps.html
    import pygal                                                       # First import pygal
    bar_chart = pygal.Bar()                                            # Then create a bar graph object
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    #bar_chart.render_to_file('/tmp/bar_chart.svg')  
    bar_chart.render()
    #bar_chart.render_in_browser()

# # http://mpld3.github.io/examples/interactive_legend.html
# import matplotlib.pyplot as plt
# from mpld3 import plugins
# import mpld3
# import numpy as np
# import pandas as pd
# 
# 
# np.random.seed(9615)
# 
# # generate df
# N = 100
# df = pd.DataFrame((.1 * (np.random.random((N, 5)) - .5)).cumsum(0),
#                   columns=['a', 'b', 'c', 'd', 'e'],)
# 
# # plot line + confidence interval
# fig, ax = plt.subplots()
# ax.grid(True, alpha=0.3)
# 
# for key, val in df.iteritems():
#     l, = ax.plot(val.index, val.values, label=key)
#     ax.fill_between(val.index,
#                     val.values * .5, val.values * 1.5,
#                     color=l.get_color(), alpha=.4)
# 
# # define interactive legend
# 
# handles, labels = ax.get_legend_handles_labels() # return lines and labels
# interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
#                                                          ax.collections),
#                                                      labels,
#                                                      alpha_unsel=0.5,
#                                                      alpha_over=1.5, 
#                                                      start_visible=True)
# plugins.connect(fig, interactive_legend)
# 
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_title('Interactive legend', size=20)
# 
# mpld3.display()

if False:
    # https://plotly.com/python/line-charts/
    import plotly.express as px
    
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    fig.show()

if False:
    #https://python-graph-gallery.com/10-barplot-with-number-of-observation/
    # library
    import matplotlib.pyplot as plt
     
    # Create bars
    barWidth = 0.9
    bars1 = [3, 3, 1]
    bars2 = [4, 2, 3]
    bars3 = [4, 6, 7, 10, 4, 4]
    bars4 = bars1 + bars2 + bars3
     
    # The X position of bars
    r1 = [1,5,9]
    r2 = [2,6,10]
    r3 = [3,4,7,8,11,12]
    r4 = r1 + r2 + r3
     
    # Create barplot
    plt.bar(r1, bars1, width = barWidth, color = (0.3,0.1,0.4,0.6), label='Alone')
    plt.bar(r2, bars2, width = barWidth, color = (0.3,0.5,0.4,0.6), label='With Himself')
    plt.bar(r3, bars3, width = barWidth, color = (0.3,0.9,0.4,0.6), label='With other genotype')
    # Note: the barplot could be created easily. See the barplot section for other examples.
     
    # Create legend
    plt.legend()
     
    # Text below each barplot with a rotation at 90°
    plt.xticks([r + barWidth for r in range(len(r4))], ['DD', 'with himself', 'with DC', 'with Silur', 'DC', 'with himself', 'with DD', 'with Silur', 'Silur', 'with himself', 'with DD', 'with DC'], rotation=90)
     
    # Create labels
    label = ['n = 6', 'n = 25', 'n = 13', 'n = 36', 'n = 30', 'n = 11', 'n = 16', 'n = 37', 'n = 14', 'n = 4', 'n = 31', 'n = 34']
     
    # Text on the top of each barplot
    for i in range(len(r4)):
        plt.text(x = r4[i]-0.5 , y = bars4[i]+0.1, s = label[i], size = 6)
     
    # Adjust the margins
    plt.subplots_adjust(bottom= 0.2, top = 0.98)
     
    # Show graphic
    plt.show()

if False:
    # https://riptutorial.com/matplotlib/example/23577/interactive-controls-with-matplotlib-widgets
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.widgets import Slider
    
    TWOPI = 2*np.pi
    
    fig, ax = plt.subplots()
    
    t = np.arange(0.0, TWOPI, 0.001)
    initial_amp = .5
    s = initial_amp*np.sin(t)
    l, = plt.plot(t, s, lw=2)
    
    ax = plt.axis([0,TWOPI,-1,1])
    
    axamp = plt.axes([0.25, .03, 0.50, 0.02])
    # Slider
    samp = Slider(axamp, 'Amp', 0, 1, valinit=initial_amp)
    
    def update(val):
        # amp is the current value of the slider
        amp = samp.val
        # update curve
        l.set_ydata(amp*np.sin(t))
        # redraw canvas while idle
        fig.canvas.draw_idle()
    
    # call update function on slider value change
    samp.on_changed(update)
    
    plt.show()
    
if False:
    from tkinter import *
    
    window = Tk()
    
    window.title("Welcome to LikeGeeks app")
    
    lbl = Label(window, text="Hello")
    
    lbl.grid(column=0, row=0)
    
    window.mainloop()

print("done")