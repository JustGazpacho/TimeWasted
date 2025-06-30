import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
import json
  
# 1) Carico i dati e creo cartella per output
'''
data = [
    ("2025-05-30 20:39", 62),
    ("2025-06-01 20:48", 66.7),
    ("2025-06-02 15:28", 71.9),
    ("2025-06-03 13:40", 76.4),
    ("2025-06-04 11:07", 77.6),
    ("2025-06-06 10:48", 78.4),
    ("2025-06-07 16:43", 70.3),
    ("2025-06-08 22:55", 65),
    ("2025-06-09 12:01", 65.9),
    ("2025-06-10 15:30", 63),
    ("2025-06-12 08:50", 60),
    ("2025-06-13 19:55", 62.2),
    ("2025-06-15 21:05", 57),
    ("2025-06-16 23:44", 50.7),
    ("2025-06-17 23:12", 48.2),
    ("2025-06-18 22:56", 45.6),
    ("2025-06-19 22:59", 40.4),
    ("2025-06-22 23:39", 32.8),
    ("2025-06-25 13:27", 27.8),
    ("2025-06-26 16:16", 30.2),
    ("2025-06-29 17:13", 21.4),
    ("2025-06-30 09:00", 23)
]
'''
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
