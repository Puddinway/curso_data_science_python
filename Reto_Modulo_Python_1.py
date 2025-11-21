import csv

archivo = "200412COVID19MEXICO.csv"

# Variables para acumular datos
suma_edades = 0
conteo_registros = 0
conteo_hombres = 0
conteo_mujeres = 0

with open(archivo, newline='', encoding='utf-8') as f:
    lector = csv.DictReader(f)
    for fila in lector: #for para checar cada fila por fila
        try:
            edad = int(fila["EDAD"])
            sexo = int(fila["SEXO"])
        except ValueError:
            # En caso de no encotrar valor valido, salta el valor y continua
            continue

        # Acumular edad
        suma_edades += edad
        conteo_registros += 1

        # Contar hombres y mujeres
        if sexo == 1:
            conteo_hombres += 1
        elif sexo == 2:
            conteo_mujeres += 1

# Calcular edad promedio
if conteo_registros > 0:
    edad_promedio = suma_edades / conteo_registros
else:
    edad_promedio = 0

# Determinar mayoría
if conteo_hombres > conteo_mujeres:
    mayoritario = "Hombres (1)"
elif conteo_mujeres > conteo_hombres:
    mayoritario = "Mujeres (2)"
else:
    mayoritario = "Igual número de hombres y mujeres"

# Mostrar resultados
print(f"Edad promedio: {edad_promedio:.2f}")
print(f"Hombres: {conteo_hombres}, Mujeres: {conteo_mujeres}")
print(f"Mayoría: {mayoritario}")