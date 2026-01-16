import pandas as pd			#Pandas
from pathlib import Path 	#pathing de libreria paths

def prints (df): ##Debuging para poder ver que funcionen los dfs
    print("\nEstructura general del DataFrame:") #muestra estructura y tipos de datos
    print(df.info())
    print("\nPrimeras filas (referencia):")	#Se agrega como referencia para probar que muestre la info correcta
    print(df.head())


def sums_OS(df): #Convierte los valores de conteo a porcentajes
    total=sum(df)
    for col in range (len(df)):
        df[col]=(df[col]/total)*100
        
    return df
#llamada de archivos para dfs
csv_path_test = "Test.csv"
csv_path_test2 = "Test2.csv"
csv_path_train = "Train.csv"
csv_path_train2 = "Train2.csv"

dftest = pd.read_csv(
    csv_path_test,
)
dftest2 = pd.read_csv(
    csv_path_test2,
)
dftrain = pd.read_csv(
    csv_path_train,
)

dftrain2 = pd.read_csv(
    csv_path_train2,
)

##da valor 'no registrado' a valores faltantes de OS ##
dftest2[[" Computer_OS"," Mobile_OS"]] = dftest2[[" Computer_OS"," Mobile_OS"]].fillna('no registrado')
dftrain2[[" Computer_OS"," Mobile_OS"]] = dftrain2[[" Computer_OS"," Mobile_OS"]].fillna('no registrado')


##imprime muestras del codigo##
prints(dftest)
prints(dftest2)
prints(dftrain)
prints(dftrain2)

##Join de test2/train2 con test/train para juntar toda la informacion
dftestjoin = dftest2.join(dftest.set_index('Employee_ID'),on='Employee_ID')
dftrainjoin = dftrain2.join(dftrain.set_index('Employee_ID'),on='Employee_ID')

##concat de toda la informacion para tener un solo data frame total para realizar conteos
dffinal=pd.concat([dftestjoin,dftrainjoin])

#dffinal es el df con toda la informacion junta

##Group by para realizar conteo de cada OS como requerid0
PCOScount = dffinal.groupby(' Computer_OS').size()
MBOScount = dffinal.groupby(" Mobile_OS").size()

#debugging
print(PCOScount.head())
print(MBOScount.head())

PCOSperc= sums_OS(PCOScount)
MBOSperc= sums_OS(MBOScount)

#Cambia la serie del join de vuelta a un df
PCOSprint = PCOSperc.reset_index()
MBOSprint = MBOSperc.reset_index()


#debugging
print(PCOSprint.head())
print(MBOSprint.head())

#divide el df por OS
windowsdf = dffinal.loc[dffinal[' Computer_OS']=='Windows']
macosdf = dffinal.loc[dffinal[' Computer_OS']=='MacOS']
linuxdf = dffinal.loc[dffinal[' Computer_OS']=='Linux']
noregistradodf = dffinal.loc[dffinal[' Computer_OS']=='no registrado']
androiddf = dffinal.loc[dffinal[' Mobile_OS']=='Android']
iosdf = dffinal.loc[dffinal[' Mobile_OS']=='iOS']
noregistradombdf = dffinal.loc[dffinal[' Mobile_OS']=='no registrado']


#mean de cada edad
WOSaverageage = windowsdf.loc[:,'Age'].mean()
MOSaverageage = macosdf.loc[:,'Age'].mean()
LOSaverageage = linuxdf.loc[:,'Age'].mean()
NRaverageage = noregistradodf.loc[:,'Age'].mean()
ANDaverageage = androiddf.loc[:,'Age'].mean() #se agregaron opciones de mobil pero no se ocupan
iOSaverageage = iosdf.loc[:,'Age'].mean()
NRMaverageage = noregistradombdf.loc[:,'Age'].mean()

#genera df para imprimir la edad promedio 
OSagedf=pd.DataFrame({'PC OS':['Windows', 'MacOS', 'Linux', 'no registrado PC'], 'Edad promedio de uso':[WOSaverageage, MOSaverageage, LOSaverageage, NRaverageage]})
print(OSagedf.head()) #debugging


#mean de cada nivel de educacion
WOSaverageedu = windowsdf.loc[:,'Education_Level'].mean()
MOSaverageedu = macosdf.loc[:,'Education_Level'].mean()
LOSaverageedu = linuxdf.loc[:,'Education_Level'].mean()
NRaverageedu = noregistradodf.loc[:,'Education_Level'].mean()
ANDaverageedu = androiddf.loc[:,'Education_Level'].mean() #se agregaron opciones de mobil pero no se ocupan
iOSaverageedu = iosdf.loc[:,'Education_Level'].mean()
NRMaverageedu = noregistradombdf.loc[:,'Education_Level'].mean()

#genera df para imprimir el nivel de educacion promedio
OSedudf=pd.DataFrame({'PC OS':['Windows', 'MacOS', 'Linux', 'no registrado PC'], 'Nivel de educacion promedio':[WOSaverageedu, MOSaverageedu, LOSaverageedu, NRaverageedu]})
print(OSedudf.head())#debugging


#suma de cantidad de tickets por OS de escritorio
WOStickets = windowsdf.loc[:,' Computer_tickets'].sum()
MOStickets = macosdf.loc[:,' Computer_tickets'].sum()
LOStickets = linuxdf.loc[:,' Computer_tickets'].sum()
NRtickets = noregistradodf.loc[:,' Computer_tickets'].sum()

OSticketdf=pd.DataFrame({'PC OS':['Windows', 'MacOS', 'Linux', 'no registrado PC'], 'Numero de Tickets': [WOStickets, MOStickets, LOStickets, NRtickets]})
print(OSticketdf.head())#debugging

'''
#debugging
salida_excel = Path("resultadosReto.xlsx") ##Salida para debuging

with pd.ExcelWriter(salida_excel, engine="openpyxl") as writer:
    dftest.to_excel(writer, sheet_name="test", index=False)
    dftest2.to_excel(writer, sheet_name="test2", index=False)
    dftrain.to_excel(writer, sheet_name="train", index=False)
    dftrain2.to_excel(writer, sheet_name="train2", index=False)
    dftestjoin.to_excel(writer, sheet_name="jointest", index=False)
    dftrainjoin.to_excel(writer, sheet_name="jointrain", index=False)
    dffinal.to_excel(writer, sheet_name="finaljoin", index=False)
'''
 
 
#salida finala excel
salida_excel2=Path("Resulatados_finales_reto.xlsx")
with pd.ExcelWriter(salida_excel2, engine="openpyxl") as writer:
    PCOSprint.to_excel(writer, sheet_name="PC_OS_porcentajes", index=False)
    MBOSprint.to_excel(writer, sheet_name="MOBILE_OS_porcentajes", index=False)
    OSagedf.to_excel(writer, sheet_name="Promedio_de_edad_por_OS", index=False)
    OSedudf.to_excel(writer, sheet_name="Promedio_de_educacion_por_OS", index=False)
    OSticketdf.to_excel(writer, sheet_name="Cantidad_de_tickets_por_OS", index=False)


