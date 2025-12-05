import pandas as pd			#Pandas
from pathlib import Path	#importa libreria de paths para obtener archivo mas rapido


###############################	NOTA IMPORTANTE	###############################
###	POR LIMITACIONES DE EXCEL, SE DEBE DE ELIMINAR LA COLUMNA DE LINKS		###
###	MARCA ERROR EN EL PROGRAMA DADA LA GRAN CANTIDAD DE LINKS EN EL MISMO 	###
###	EN UN MUESTREO MAS CHICO NO CAUSA PROBLEMAS, UNICAMENTE EN GRANDES		###
###############################################################################


### a. Extraer la información del archivo ###
csv_path = Path("country_vaccinations_copy.csv")

df = pd.read_csv(
    csv_path,
    encoding="utf-8-sig",
    parse_dates=["date"],   # Aseguramos que 'date' sea datetime64
    dayfirst=False          # El archivo usa formato MM/DD/YYYY
)

# Convertir columnas numéricas a tipo adecuado
num_cols = [
    "total_vaccinations",
    "people_vaccinated",
    "people_fully_vaccinated",
    "daily_vaccinations_raw",
    "daily_vaccinations",
    "total_vaccinations_per_hundred",
    "people_vaccinated_per_hundred",
    "people_fully_vaccinated_per_hundred",
    "daily_vaccinations_per_million"
]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

### b. Mostrar estructura y tipos de datos ###
print("\nEstructura general del DataFrame:")
print(df.info())

print("\nPrimeras filas (referencia):")	#Se agrega como referencia para probar que muestre la info correcta
print(df.head())

print("\nTipo de 'date' (debe ser datetime64[ns]):", df["date"].dtype)
### Dada la alta cantidad de valores, muestra numeros con e+xx ###


### c. Cantidad de vacunas aplicadas por combinación de compañías ###
# 	(agrupamos por la cadena completa en 'vaccines')
por_vacunas = (
    df.groupby("vaccines", dropna=False)["total_vaccinations"]
      .sum(min_count=1)
      .reset_index()
      .rename(columns={"total_vaccinations": "total_aplicadas"})
)

print("\nSumatoria de vacunas aplicadas por 'vaccines':")
print(por_vacunas)

### d. Cantidad de vacunas aplicadas en todo el mundo ##
total_mundo = df["total_vaccinations"].sum(min_count=1)

print("\nTotal de vacunas aplicadas en el mundo:", total_mundo)


### e. Calcular el promedio de vacunas aplicadas por país ###
promedio_por_pais = (
    df.groupby("country", dropna=True)["total_vaccinations"]
      .mean()
      .reset_index()
      .rename(columns={"total_vaccinations": "promedio_total_vaccinations"})
)
print("\nPromedio de vacunas aplicadas por país:")
print(promedio_por_pais)

### f. Determinar la cantidad de vacunas aplicadas el día 29/01/21 en todo el mundo ###
### 	Usamos daily_vaccinations como preferencia; si está vacío, recurrimos a daily_vaccinations_raw ###
df["daily_best"] = df["daily_vaccinations"].fillna(df["daily_vaccinations_raw"])
fecha_objetivo = pd.to_datetime("29/01/21", dayfirst=True)

vacunas_290121 = df.loc[df["date"] == fecha_objetivo, "daily_best"].sum(min_count=1)
vacunas_290121 = 0 if pd.isna(vacunas_290121) else vacunas_290121

print("\nVacunas aplicadas el 29/01/21 en todo el mundo:", vacunas_290121)

### g. Crear un dataframe conDiferencias ###
### 	en el enunciado aparece 'daily_vaccionations' con error ortográfico, ###
### 	pero la columna correcta es 'daily_vaccinations'. ###
conDiferencias = df.copy()
conDiferencias["diferencias"] = conDiferencias["daily_vaccinations"] - conDiferencias["daily_vaccinations_raw"]

print("\nDataFrame 'conDiferencias' creado. Columnas:", list(conDiferencias.columns))
print(conDiferencias.head())  # Muestra las primeras filas para verificar

### h. Obtener el periodo de tiempo entre el registro con fecha más reciente y el registro con fecha más antigua ###
fecha_min = df["date"].min()
fecha_max = df["date"].max()
periodo = fecha_max - fecha_min

print(f"\nPeriodo entre la fecha más reciente y la más antigua: {periodo} (desde {fecha_min.date()} hasta {fecha_max.date()})")

### i. Crear un dataframe nuevo denominado conCantidad ###
### 	con columna derivada 'canVac' que asigna la cantidad de vacunas utilizadas cada día ###
### 	Separa la columna 'vaccines' por el carácter ',' ###
def split_companies(x):
    if pd.isna(x):
        return []
    return [c.strip() for c in str(x).split(",") if c.strip()]

# Copia del DataFrame original
conCantidad = df.copy()

# Columna con la lista de compañías
conCantidad["company"] = conCantidad["vaccines"].apply(split_companies)
conCantidad = conCantidad.explode("company", ignore_index=True)

# Asignamos la cantidad de vacunas de esa fila a cada compañía
conCantidad["canVac"] = conCantidad["total_vaccinations"]

print("\nDataFrame 'conCantidad' creado. Columnas:", list(conCantidad.columns))
print(conCantidad.head())#Muestra ejemplo 

# Ejemplo de sumatoria por compañía. Confirma que se haya creado correctamente el nuevo DataFrame.
# Se deja comentado ya que no es parte del ejercicio, pero sirve para comprobar funionamiento.
'''
sumatoria_por_compania = (
    conCantidad.groupby("company")["canVac"]
        .sum(min_count=1)
        .reset_index()
        .sort_values("canVac", ascending=False)
)
print("\nSumatoria de 'canVac' por compañía:")
print(sumatoria_por_compania)
'''

### j. Generar un dataframe denominado antes20 ###
### 	con todos los registros antes del 20 de diciembre de 2020 ###
corte = pd.to_datetime("2020-12-20")
antes20 = df[df["date"] < corte].copy()

print("\nDataFrame 'antes20' creado. Número de registros:", len(antes20))
print(antes20.head())#Muestra ejemplo 

### k. Obtener un dataframe denominado pfizer ###
### 	con todos los registros donde se haya utilizado la vacuna Pfizer ###

pfizer = df[df["vaccines"].str.contains("Pfizer", case=False, na=False)].copy()

print("\nDataFrame 'pfizer' creado. Número de registros:", len(pfizer))
print(pfizer.head()) #Muestra ejemplo 

### l. Almacenar los dataframes generados en un archivo Excel ###
### 	Cada dataframe ocupa una hoja diferente ###

import pandas as pd
from pathlib import Path

# Definimos la ruta de salida
salida_excel = Path("resultadosReto.xlsx")

# Guardamos los DataFrames en distintas hojas
with pd.ExcelWriter(salida_excel, engine="xlsxwriter") as writer:
    conDiferencias.to_excel(writer, sheet_name="conDiferencias", index=False)
    conCantidad.to_excel(writer, sheet_name="conCantidad", index=False)
    antes20.to_excel(writer, sheet_name="antes20", index=False)
    pfizer.to_excel(writer, sheet_name="pfizer", index=False)

print(f"\nArchivo Excel generado: {salida_excel.resolve()}")