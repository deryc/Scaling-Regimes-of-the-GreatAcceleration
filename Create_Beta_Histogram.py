###CREATED BY DERYC T. PAINTER
###02.27.2020
###USED IN THE FOUR REGIMES OF THE GREAT ACCELERATION TO CREATE FIGURE 1

import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from scipy import stats as sts
import matplotlib.gridspec as gridspec


df = pd.read_csv('UN_Pop_Data_Normalized_GreatAcceleration.csv',delimiter=',',parse_dates=['Year'])

decades = df.groupby(pd.Grouper(key='Year', freq='10y', closed='left'))



columns = list(df)

###TOTAL
##columnlist = ['Global Real GDP','Global Foreign Direct Investment (Trillion US Dollar)','Global Primary Energy Use (Exajoule)',
##    'Global Fertilizer Consumption (Million Ton)','Global Accumulative Large Dams (Thousand)','Global Water Use (Thousand km3)','Global Paper Production (Million Ton)',
##    'Global Transportation (Million Vehicles)','Global Telecommunications (Billion Landlines & Subscriptions)','International Tourism (Million Arrivals)','Global Carbon Dioxide Concentration (ppm)',
##    'Nitrous Oxide (ppb)','Methane (ppb)','Ozone % Loss','Temperature Anomaly (Degree Celcius)','Mean H+ Concentration (nmol kg-1)','Marine Fish Capture (Million Ton)','Shrimp Aquaculture (Million Ton)',
##    'Tropical Forest % Loss','% Domesticated Land','Global CO2 emissions (kt)','Global Methane emissions (kt of CO2 equivalent)','Global Nitrous oxide emissions (thousand metric tons of CO2 equivalent)',
##    'USPTO Patent Grants','Web of Science Publications']

###SOCIOECONOMIC INDICATORS
columnlist = ['Global Real GDP','Global Foreign Direct Investment (Trillion US Dollar)',
    'Global Primary Energy Use (Exajoule)',
    'Global Fertilizer Consumption (Million Ton)','Global Accumulative Large Dams (Thousand)',
    'Global Paper Production (Million Ton)',
    'Global Transportation (Million Vehicles)','Global Telecommunications (Billion Landlines & Subscriptions)',
    'International Tourism (Million Arrivals)',
    'USPTO Patent Grants','Web of Science Publications']

###GEOPHYSICAL INDICATORS
##columnlist = ['Global Carbon Dioxide Concentration (ppm)','Global CO2 emissions (kt)', 'Nitrous Oxide (ppb)',
##    'Global Nitrous oxide emissions (thousand metric tons of CO2 equivalent)',
##    'Methane (ppb)','Global Methane emissions (kt of CO2 equivalent)',
##    'Ozone % Loss','Temperature Anomaly (Degree Celcius)','Mean H+ Concentration (nmol kg-1)',
##    'Marine Fish Capture (Million Ton)',
##    'Tropical Forest % Loss','% Domesticated Land',
##    'Global Water Use (Thousand km3)','Shrimp Aquaculture (Million Ton)']

betalist=[]
betalist1=[]
betalist2=[]
betalist3=[]
betalist4=[]

regimecount1=0
regimecount2=0
regimecount3=0
regimecount4=0

with open('Total_Scaling_Relationships_per_Decade.csv','w') as f:
    print('Measurement\tDecade\t{}\t{}\tP value\tStandard Error'.format(r'$\beta$',r'$R^2$'),file=f)

    for column in columnlist:
        df = pd.read_csv('UN_Pop_Data_Normalized_Total_v2.csv',delimiter=',',parse_dates=['Year'])
        df = df.dropna(subset = [column])
        df = df.dropna(subset=['Normalized UN Population Estimate'])
        for name, d in df.groupby(pd.DatetimeIndex(df['Year']).year // 10 * 10):
            
            x = round(np.log(d['Normalized UN Population Estimate']),4)
            y = round(np.log(d[column]),4)
            

            slope, intercept, r_value, p_value, std_err = sts.linregress(x,y)
            alpha = np.exp(intercept)
            
            beta=slope
            print('{}\t{}\t{}\t{}\t{}\t{}'.format(column,name,beta,r_value, p_value, std_err),file=f)
            if beta < 0.85:
                
                regimecount1+=1
                betalist1.append(beta)
                #beta = 0.235 #Geo
                beta = 0.396 #Soc
                
                betalist.append(beta)
            if 1.16 > beta > 0.84:
                
                regimecount2+=1
                betalist2.append(beta)
                
                #beta = 0.998 #Geo
                beta = 0.979 #Soc
                betalist.append(beta)
            if 3.5 > beta > 1.15:
                
                regimecount3+=1
                betalist3.append(beta)
                #beta = 1.827 #Geo
                beta = 2.286 #Soc
                
                betalist.append(beta)
            if beta > 3.49:
                
                regimecount4+=1
                betalist4.append(beta)
                #beta = 9.894 #Geo
                beta = 5.643 #Soc
                
                betalist.append(beta)



betaframe = pd.DataFrame(betalist).dropna()
rawbetas = dict(A=np.array(betalist1),B=np.array(betalist2),C=np.array(betalist3),D=np.array(betalist4))
rawbeta = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in rawbetas.items() ]))
print(rawbeta)
means=[]
for column in rawbeta:
    means.append(round(rawbeta[column].median(),3))

print(means)

bins = []

for mean in means:
    bins.append(mean-0.15)
    bins.append(mean+0.15)

print(bins)

print(betaframe)



colors = ['b', 'r', 'violet', 'g']


fig = plt.figure()
gs1 = gridspec.GridSpec(10, 1)
ax_box = fig.add_subplot(gs1[0])
ax_hist = fig.add_subplot(gs1[1:10],sharex=ax_box)

ax_box.xaxis.set_visible(False)
ax_box.yaxis.set_visible(False)
c=0
for column in rawbeta:
    sns.boxplot(rawbeta[column],ax=ax_box,showfliers=False, color=colors[c])
    c+=1
    


 

    

N, bins, patches = ax_hist.hist(betaframe[0], edgecolor='white', linewidth=1,bins=bins)


patches[0].set_facecolor('b')
patches[2].set_facecolor('r')
patches[4].set_facecolor('violet')
patches[6].set_facecolor('g')



plt.xlabel(r'$\beta$',size=24)
plt.ylabel('Count',size=24)
##plt.title(r'$\beta$-Range of the Great Acceleration',size=24) #TOTAL
fig.suptitle(r'$\beta$-Range of the Socioeconomic Great Acceleration',fontsize=24) #Soc
##fig.suptitle(r'$\beta$-Range of the Geophysical Great Acceleration',fontsize=24) #Geo

plt.yticks(np.arange(0,60,step=10),fontsize=16)


ax_hist.set_xticks(np.arange(-1,16,step=1))
ax_box.set_xticks(np.arange(-1,16,step=1))

ax_box.set(xlabel=None)

ax_box.spines['top'].set_visible(False)
ax_box.spines['right'].set_visible(False)
ax_box.spines['left'].set_visible(False)
ax_box.spines['bottom'].set_visible(False)

legend = [Patch(facecolor='b', edgecolor='b', label=r'$\beta<0.85$'),
          Patch(facecolor='r', edgecolor='r', label=r'$0.85\leq\beta<1.15$'),
          Patch(facecolor='violet', edgecolor='violet', label=r'$1.15\leq\beta<3.50$'),
          Patch(facecolor='g', edgecolor='g', label=r'$\beta\geq3.50$')]
ax_hist.legend(handles=legend,loc='upper right',title='Regimes',fontsize=16,title_fontsize = 16,shadow=True)

ax_hist.grid(b=None, which='both', axis='both')




plt.show()

