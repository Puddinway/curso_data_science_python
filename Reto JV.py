import pandas as pd			#Pandas
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

###





###


#lectura de archivos y creacion de dfs
csv_path_happy = "Happiness_report.csv"
csv_path_meta = "Metadata.csv"
dfhappy = pd.read_csv(csv_path_happy)
dfmeta = pd.read_csv(csv_path_meta)
print(dfhappy.head())

#aisla a mexico en su df y pone country or region como index
mexicodatadf = dfhappy.loc[dfhappy['Country or region']=='Mexico']
mexicodatadf = mexicodatadf.set_index('Country or region')
print(mexicodatadf)


#histograma
sb.histplot(data = dfhappy, x='Score',bins=10).set_title('Frequencia de indice de felizidad')
plt.text(x=6.595, y=12.5, s='Mexico', color='red', ha='center')

#boxplot
sb.catplot(kind='box', x ='Healthy life expectancy', data=dfhappy)
plt.text(x=0.861, y=-0.1,s='Mexico', color='red', ha='center')

#grafica circular
dfmexico=mexicodatadf.drop(['Overall rank', 'Score'], axis=1)
dfmexico = dfmexico.transpose()
print(dfmexico.head())
dfmexico.plot.pie(y='Mexico',figsize=(5,5),legend=False).set_title('Factores de felizidad de Mexico')

#Grafica circular de 5 paises
dfpaises = dfhappy.loc[(dfhappy['Country or region']=='Finland') | (dfhappy['Country or region']=='Mexico') | (dfhappy['Country or region']== 'South Sudan') | (dfhappy['Country or region']== 'United States') | (dfhappy['Country or region']=='Japan') ]
dfpaises = dfpaises.set_index('Country or region')
dfpaises = dfpaises.drop(['Overall rank', 'Score'], axis=1)
dfpaises = dfpaises.transpose()
print(dfpaises)

#Subplots
fig=plt.figure(figsize=(20,20))
fig.suptitle('Evaluacion de felicidad de varios paises', fontsize=18)
#Finland
ax1=fig.add_subplot(231)
dfpaises.plot.pie(y='Finland',figsize=(5,5),ax=ax1,legend=False)
ax1.set_title('Finland')

#Mexico
ax2=fig.add_subplot(232)
dfpaises.plot.pie(y='Mexico',figsize=(5,5),ax=ax2,legend=False)
ax2.set_title('Mexico')

#South Sudan
ax3=fig.add_subplot(233)
dfpaises.plot.pie(y='South Sudan',figsize=(5,5),ax=ax3,legend=False)
ax3.set_title('South Sudan')

#United States
ax4=fig.add_subplot(234)
dfpaises.plot.pie(y='United States',figsize=(5,5),ax=ax4,legend=False)
ax4.set_title('United States')

#Japan
ax5=fig.add_subplot(236)
dfpaises.plot.pie(y='Japan',figsize=(5,5),ax=ax5,legend=False)
ax5.set_title('Japan')

plt.show()


#Scatter Plot
fig=plt.figure(figsize=(20,20))
fig.suptitle('Evaluacion de valores para felicidad', fontsize=18)

ax1=fig.add_subplot(231)
ax1.scatter(x=dfhappy['GDP per capita'],y=dfhappy['Score'])
ax1.set_title('GDP per capita')

ax2=fig.add_subplot(232)
ax2.scatter(x=dfhappy['Social support'],y=dfhappy['Score'])
ax2.set_title('Social support')

ax3=fig.add_subplot(233)
ax3.scatter(x=dfhappy['Healthy life expectancy'],y=dfhappy['Score'])
ax3.set_title('Healthy life expectancy')

ax4=fig.add_subplot(234)
ax4.scatter(x=dfhappy['Freedom to make life choices'],y=dfhappy['Score'])
ax4.set_title('Freedom to make life choices')

ax5=fig.add_subplot(235)
ax5.scatter(x=dfhappy['Generosity'],y=dfhappy['Score'])
ax5.set_title('Generosity')

ax6=fig.add_subplot(236)
ax6.scatter(x=dfhappy['Perceptions of corruption'],y=dfhappy['Score'])
ax6.set_title('Perceptions of corruption')

plt.show()

#Heat Map
heatmapdf = dfhappy.drop('Overall rank',axis=1)
heatmapdf = heatmapdf.set_index('Country or region')
sb.heatmap(round(heatmapdf.corr(),2),annot=True).set_title('Heatmap de relacion de parametros')
plt.show()


#Join de las 2 tablas para filtrar por region
dfregions = dfhappy.set_index('Country or region').join(dfmeta.set_index('TableName'), how='left', on='Country or region')
LATAM = dfregions.loc[dfregions['Region']=='Latin America & Caribbean']
LATAMav = LATAM.loc[:,'Score'].mean()

#Obtencion de average de cada region
Europe = dfregions.loc[dfregions['Region']=='Europe & Central Asia']
Europeav= Europe.loc[:,'Score'].mean()

EAsia = dfregions.loc[dfregions['Region']=='East Asia & Pacific']
EAsiaav = EAsia.loc[:,'Score'].mean()

MidE = dfregions.loc[dfregions['Region']=='Middle East & North Africa']
MidEav = MidE.loc[:,'Score'].mean()

NA = dfregions.loc[dfregions['Region']=='North America']
NAav = NA.loc[:,'Score'].mean()

SAsia = dfregions.loc[dfregions['Region']=='South Asia']
SAsiaav = SAsia.loc[:,'Score'].mean()

Sahara = dfregions.loc[dfregions['Region']=='Sub-Saharan Africa']
Saharaav = Sahara.loc[:,'Score'].mean()

RegionHappy = pd.DataFrame({'Region':['Latin America & Caribbean','Europe & Central Asia','East Asia & Pacific','Middle East & North Africa','North America','South Asia','Sub-Saharan Africa'],'Average Happyness':[LATAMav,Europeav,EAsiaav,MidEav,NAav,SAsiaav,Saharaav]})
print(RegionHappy)

RegionHappy.plot(x='Region',y='Average Happyness', kind='bar', title='Felicidad Promedio por Region', rot=45)
plt.show()


