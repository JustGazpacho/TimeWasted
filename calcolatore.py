'''import pandas as pd
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
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, df["delta_rolling"], marker="o", linestyle="-", color="#ff7f0e")
ax.set_title("Delta giornaliero del rolling 14 giorni")
ax.set_ylabel("Variazione rispetto al giorno precedente")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))
ax.grid(alpha=0.3)
plt.tight_layout()
fig.savefig("grafici/grafico_delta_rolling.png", dpi=300, format='png')
'''
# seconda iterazione
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

# 2) Calcolo rolling 14 giorni e delta giornaliero del rolling
df["rolling_14d"] = df["hours"].rolling(window=14).sum()
df["delta_rolling"] = df["rolling_14d"].diff()

# 3) Grafico #1: trend delle ore
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, df["rolling_14d"], marker="o", linestyle="-", color="#1f77b4")
ax.set_title("Andamento delle ore (rolling 14 giorni)")
ax.set_ylabel("Ore nelle ultime 2 settimane")
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))
ax.grid(alpha=0.3)
plt.tight_layout()
fig.savefig("grafici/grafico_andamento_ore.png", dpi=300, format='png')

# 4) Grafico #2: variazione giornaliera del rolling
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, df["delta_rolling"], marker="o", linestyle="-", color="#ff7f0e")
ax.set_title("Delta giornaliero del rolling 14 giorni")
ax.set_ylabel("Variazione rispetto al giorno precedente")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))
ax.grid(alpha=0.3)
plt.tight_layout()
fig.savefig("grafici/grafico_delta_rolling.png", dpi=300, format='png')

'''
plt.tight_layout()
plt.show()
'''
