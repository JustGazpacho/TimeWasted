import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
import json
  
# 1) Carico i dati e creo cartella per output
with open("dati.json", "r") as file:
    data = json.load(file)

os.makedirs("grafici", exist_ok=True)

df = pd.DataFrame(data, columns=["timestamp", "hours"])
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp").sort_index()

# 2) Calcolo delta giornaliero (variazione netta del rolling window)
df["delta"] = df["hours"].diff()


# 3) Grafico #1: trend delle ore
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(df.index, df["hours"], marker="o", linestyle="-", color="#1f77b4")
ax.set_title("Andamento delle ore (rolling 14 giorni)")
ax.set_ylabel("Ore nelle ultime 2 settimane")
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))
ax.grid(alpha=0.3)
# 3.5) salvo
plt.tight_layout()
fig.savefig("grafici/grafico_andamento_ore.png", dpi=300, format='png')


# 4) Grafico #2: ore aggiunte (o rimosse) ogni registrazione
fig, bx = plt.subplots(figsize=(10,4))
colors = df["delta"].apply(lambda x: "g" if x>=0 else "r")
bx.bar(df.index, df["delta"], color=colors, width=0.8)
bx.set_title("Variazione netta di ore rispetto al rilevamento precedente")
bx.set_ylabel("Ore aggiunte (positivo) o tolte (negativo)")
bx.xaxis.set_major_formatter(DateFormatter("%d/%m"))
bx.axhline(0, color="k", linewidth=0.8)
bx.grid(alpha=0.3)
# 4.5) salvo
plt.tight_layout()
fig.savefig("grafici/grafico_variazione_ore.png", dpi=300, format='png')

'''
plt.tight_layout()
plt.show()
'''
