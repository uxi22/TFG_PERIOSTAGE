import pandas as pd

lista = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
lista2 = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
lista3 = [12, 23, 34, 2, 1, 34 ,2, 4, 5, 23]
data = {}
dfs = []

#data["primera"] = lista
dfs.append(pd.DataFrame(data=lista, columns=["primera"]))
#data.clear()
dfs.append(pd.DataFrame(data=lista2, columns=[""]))

dfs.append(pd.DataFrame(data=lista3, columns=[""]))

df = pd.concat(dfs, axis=1)
print(df)
df.index = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

df.to_excel("output.xlsx")

