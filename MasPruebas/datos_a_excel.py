import pandas as pd

dientes = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
sangrados = [False] * 3 * 16
placas = [False] * 3 * 16
supuraciones = [False] * 3 * 16
margenes = [0] * 3 * 16
profundidades = [0] * 3 * 16
defectosfurca = [0] * 16
implantes = [False] * 16
desactivados = []
inicializados = []


defectosfurca[4] = 2
implantes[12] = True
sangrados[3] = True
sangrados[16] = True
placas[1] = True
margenes[16] = -4
desactivados.append(5)

data = {}

for i in range(len(dientes)):
    diente = dientes[i]
    if diente not in desactivados:
        data[int(diente)] = [defectosfurca[i], implantes[i], [1, 2, 3]]

df = pd.DataFrame(data)
df.to_excel("./excel/prueba.xlsx")


