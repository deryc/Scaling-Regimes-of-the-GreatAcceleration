import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from scipy import stats as sts

df = pd.read_csv('UN_Pop_Data_Normalized_Total_v2.csv',delimiter=',',parse_dates=['Year'])

decades = df.groupby(pd.Grouper(key='Year', freq='10y', closed='left'))

#print(df)

columns = list(df)

##TOTAL
##columnlist = ['Global Real GDP','Global Foreign Direct Investment (Trillion US Dollar)','Global Primary Energy Use (Exajoule)',
##    'Global Fertilizer Consumption (Million Ton)','Global Accumulative Large Dams (Thousand)','Global Water Use (Thousand km3)','Global Paper Production (Million Ton)',
##    'Global Transportation (Million Vehicles)','Global Telecommunications (Billion Landlines & Subscriptions)','International Tourism (Million Arrivals)','Global Carbon Dioxide Concentration (ppm)',
##    'Nitrous Oxide (ppb)','Methane (ppb)','Ozone % Loss','Temperature Anomaly (Degree Celcius)','Mean H+ Concentration (nmol kg-1)','Marine Fish Capture (Million Ton)','Shrimp Aquaculture (Million Ton)',
##    'Tropical Forest % Loss','% Domesticated Land','Global CO2 emissions (kt)','Global Methane emissions (kt of CO2 equivalent)','Global Nitrous oxide emissions (thousand metric tons of CO2 equivalent)',
##    'USPTO Patent Grants','Web of Science Publications']

##SOCIOECONOMIC FACTORS
columnlist = ['Global Real GDP','Global Foreign Direct Investment (Trillion US Dollar)','Global Primary Energy Use (Exajoule)',
    'Global Fertilizer Consumption (Million Ton)','Global Accumulative Large Dams (Thousand)','Global Paper Production (Million Ton)',
    'Global Transportation (Million Vehicles)','Global Telecommunications (Billion Landlines & Subscriptions)','International Tourism (Million Arrivals)',
    'USPTO Patent Grants','Web of Science Publications']

##GEOLOGICAL FACTORS
##columnlist = ['Global Carbon Dioxide Concentration (ppm)','Global CO2 emissions (kt)', 'Nitrous Oxide (ppb)','Global Nitrous oxide emissions (thousand metric tons of CO2 equivalent)',
##    'Methane (ppb)','Global Methane emissions (kt of CO2 equivalent)', 'Ozone % Loss','Temperature Anomaly (Degree Celcius)','Mean H+ Concentration (nmol kg-1)','Marine Fish Capture (Million Ton)',
##    'Tropical Forest % Loss','% Domesticated Land',
##              'Global Water Use (Thousand km3)','Shrimp Aquaculture (Million Ton)']

betalist=[]

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
            
###SORT BETAS INTO THE FOUR REGIMES
###COMMENT OUT TO USE RAW BETAS
            if beta < 0.85:
                beta = 0
                betalist.append(beta)
            if 1.16 > beta > 0.84:
                beta = 1
                betalist.append(beta)
            if 3.5 > beta > 1.15:
                beta = 2.5
                betalist.append(beta)
            if beta > 3.49:
                beta = 4
                betalist.append(beta)



betaframe = pd.DataFrame(betalist).dropna()


print(betaframe)



fig, ax = plt.subplots()
N, bins, patches = ax.hist(betaframe[0], edgecolor='white', linewidth=1,bins=16)


for i in range(0,1):
    patches[i].set_facecolor('b')
for i in range(1,6):
    patches[i].set_facecolor('r')
for i in range(6,13):    
    patches[i].set_facecolor('violet')
for i in range(13,16):
    patches[i].set_facecolor('g')

plt.xlabel(r'$\beta$',size=24)
plt.ylabel('Frequency',size=24)

###TITLES FOR FIGURE
##plt.title(r'$\beta$-Distribution of the Great Acceleration',size=24)
plt.title(r'$\beta$-Distribution of the Socioeconomic Great Acceleration',size=24)
##plt.title(r'$\beta$-Distribution of the Geophysical Great Acceleration',size=24)


plt.xticks(np.arange(0,5,step=0.5),fontsize=16)
plt.yticks(np.arange(0,60,step=10),fontsize=16)

legend = [Patch(facecolor='b', edgecolor='b', label=r'$\beta<0.85$'),
          Patch(facecolor='r', edgecolor='r', label=r'$0.85\leq\beta<1.15$'),
          Patch(facecolor='violet', edgecolor='violet', label=r'$1.15\leq\beta<3.50$'),
          Patch(facecolor='g', edgecolor='g', label=r'$\beta\geq3.50$')]

ax.legend(handles=legend,loc='upper right',title='Regimes',fontsize=16,title_fontsize = 16,shadow=True)
ax.grid(b=None, which='both', axis='both')

plt.show()

