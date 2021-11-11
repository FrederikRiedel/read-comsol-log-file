#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 09:50:38 2021

@author: Frederik Riedel
"""

import numpy as np

import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure



root = tk.Tk()
root.wm_title("Embedding in Tk")

root.title("Check on Comsol simulation")
root.geometry('500x500')


# TextBox Creation
inputtxt = tk.Text(root,
                   height = 1,
                   width = 200)
inputtxt.insert(tk.END, "M:\\20211109-round_electrodes-CSimport-boundary2e-3mm.mph.log")

inputtxt.pack()

# Text output Creation
output = tk.Text(root,
                height = 10,
                width =200)

output.pack()

def update_plot(data):

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)

    # adding the subplot
    plot1 = fig.add_subplot(111)
    
    plot1.set_yscale('log')
    
    convergence = []
    for i in range(len(data)):
        if data[i][3].isdigit():
            if data[i][18:19].isdigit():
                #print(data[i][18:28])
                convergence.append(float(data[i][18:28]))

    convergence = np.asarray(convergence)
    
    # plotting the graph
    plot1.plot(np.reciprocal(convergence))

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = root)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

def check_txtfield():
    logfile = inputtxt.get("1.0",'end-1c')
    if logfile == '':
        output.insert(tk.END, 'empty\n')
        #print('empty')
    else:
        #print(logfile)
        try:
            f = open(logfile, 'rb')
        except FileNotFoundError:
            output.insert(tk.END, f"File {logfile} not found.  Aborting\n")
            #print(f"File {logfile} not found.  Aborting")
        else: 
            with open(inputtxt.get("1.0",'end-1c'),'r') as f:
                data = f.readlines()
            f.close()
            data_tmp = []
            for i in range(len(data)):
                if data[i][3].isdigit():
                    data_tmp.append(data[i][0:15] + '\n')
            output.delete('1.0', tk.END) 
            for i in range(len(data_tmp)-10,len(data_tmp)):
                output.insert(tk.END, data_tmp[i])
            
            update_plot(data)
    
    root.after(10*1000, check_txtfield)



check_txtfield()
    

tk.mainloop()