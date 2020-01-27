import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
from scipy import stats as sts
from collections import OrderedDict
from matplotlib import cm

columnlist = ['Global Foreign Direct Investment (Trillion US Dollar)','Web of Science Publications',
                      'Global Telecommunications (Billion Landlines & Subscriptions)',
                      'USPTO Patent Grants']

start = 1950
end = 1959

n = 7

plt.rcParams['axes.labelsize'] = 16

number = 0
fig = plt.figure()
for column in columnlist:
    df = pd.read_csv('UN_Pop_Data_Normalized_GreatAcceleration.csv',delimiter=',',parse_dates=['Year'])
    
    number += 1

    
    
    
    measure = column
    df = df.dropna(subset = [column])
    df = df.dropna(subset=['Normalized UN Population Estimate'])
    x = df['Normalized UN Population Estimate'] 

    y =  df[column]

    #fig, ax = plt.subplots()
    if number == 1:
        ax1 = axis = fig.add_subplot(2,2,number,xlabel=None,ylabel=measure)
    if number == 2:
        ax2 = axis = fig.add_subplot(2,2,number,xlabel=None,ylabel=measure)
    if number == 3:
        ax3 = axis = fig.add_subplot(2,2,number,sharex=ax1,xlabel='Normalized UN Population Estimate',ylabel=measure)
    if number == 4:
        ax4 = axis = fig.add_subplot(2,2,number,sharex=ax2,xlabel='Normalized UN Population Estimate',ylabel=measure)



    

    

    plt.scatter(x,y,label=None,color='black',s=10)

    


    axis.set_xscale('log')
    axis.set_yscale('log')
    

    

    
    
    
    if number == 4:
        next(ax4._get_lines.prop_cycler)['color']
    
    decades = df.groupby(pd.DatetimeIndex(df['Year']).year // 10 * 10)
    for name, d in decades:


        x2 = round(np.log(d['Normalized UN Population Estimate']),4)
        y2 = round(np.log(d[column]),4)
        x3 = d['Normalized UN Population Estimate']
        
        slope, intercept, r_value, p_value, std_err = sts.linregress(x2,y2)
        alpha = np.exp(intercept)
        beta = slope
        

        

        Y = eval('alpha*x3**beta')


        
        if d.shape[0] > 1:
            

            plt.plot(x3,Y,label=r"{}s".format(name))

        axis.text(x3.median(),Y.median(),r'$\beta=${}'.format(round(beta,4)),bbox=dict(facecolor='white', boxstyle='round'),horizontalalignment='left',verticalalignment='top',visible=True,fontsize=14)
        axis.set_zorder(1)
        axis.set_facecolor('none')
        
    
    
    axis.grid(which='both')




h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
h3, l3 = ax3.get_legend_handles_labels()
h4, l4 = ax4.get_legend_handles_labels()

fig.legend(h2,l2,loc='center',fontsize=14)
fig.suptitle('Scaling Relationships of the Great Accleration',fontsize=48)

plt.tight_layout
plt.show()







        



    
