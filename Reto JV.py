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
plot_bbox={'boxstyle':'circle', 'facecolor':'green','alpha':0.3}
plt.text(6.595,12.5,'Mexico\n6.595', bbox=plot_bbox)

#boxplot
sb.catplot(kind='box', x ='Healthy life expectancy', data=dfhappy, color='green')

plt.annotate('Mexico',xy=(0.861,0),xytext=(1,0.1),arrowprops=dict(arrowstyle='->'))

#grafica circular
dfmexico=mexicodatadf.drop(['Overall rank', 'Score'], axis=1)
dfmexico = dfmexico.transpose()
print(dfmexico.head())
dfmexico.plot.pie(y='Mexico',figsize=(5,5), autopct='%1.1f%%',legend=False,color=['red','blue','yellow','green','orange','purple'])
plt.title('Factores de felizidad de Mexico')
plt.show()

#Grafica de barras de 5 paises
dfpaises = dfhappy.loc[(dfhappy['Country or region']=='Finland') | (dfhappy['Country or region']=='Mexico') | (dfhappy['Country or region']== 'South Sudan') | (dfhappy['Country or region']== 'United States') | (dfhappy['Country or region']=='Japan') ]
dfpaises = dfpaises.drop(['Overall rank', 'Score'], axis=1)
dfpaises = dfpaises.set_index('Country or region')
dfpaises =dfpaises.transpose().reset_index()
print(dfpaises)
dfpaises.plot('index', label='Indice de Felicidad', kind='bar')



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
heatmapdf = dfhappy.set_index('Country or region')
corrdf=heatmapdf.corr()
print(corrdf)
sb.heatmap(round(heatmapdf.corr(),2),annot=True).set_title('Heatmap de relacion de parametros')
plt.show()


#Join de las 2 tablas para filtrar por region
dfregions = dfhappy.set_index('Country or region').join(dfmeta.set_index('TableName'), how='left', on='Country or region')
print(dfregions)

#Obtencion de valores promedio
dfregions = dfregions.drop(['Country Code','IncomeGroup', 'SpecialNotes','Overall rank'],axis=1).reset_index(drop=True) #drop de valores de texto
print(dfregions)
RegionHappy = dfregions.groupby(['Region']).mean()
RegionHappy = RegionHappy.reset_index()
print(RegionHappy)

''' Depcrecated average method
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
'''
RegionHappy.plot(x='Region', y='Score', kind='bar', title='Felicidad Promedio por Region', rot=45,color=['red','blue','yellow','green','orange','purple','Black'])
plt.show()


