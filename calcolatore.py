import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
from datetime import timedelta
import os
import json
import locale
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
locale.setlocale(locale.LC_TIME, "italian")

# Carica i dati dal file JSON
with open("dati.json", "r") as file:
    data = json.load(file)

# Crea il DataFrame con indice temporale ordinato
df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp").sort_index()

# Calcola la differenza tra snapshot successivi
df["delta_hours"] = df["hours"].diff()

# Calcola la somma cumulativa delle differenze
df["cumulative_delta"] = df["delta_hours"].cumsum()

# Crea la cartella 'grafici' se non esiste
os.makedirs("grafici", exist_ok=True)

# Formatter asse X: giorno e ora su due righe
x_fmt = DateFormatter("%d/%m\n%H:%M")

# Margine ridotto sull'asse X
x_buffer = timedelta(days=2)
x_min = df.index.min() - x_buffer
x_max = df.index.max() + x_buffer

# Calcolo dei limiti Y con margine personalizzabile
def get_y_limits(series, margin=0.05):
    y_min, y_max = series.min(), series.max()
    pad = (y_max - y_min) * margin
    return y_min - pad, y_max + pad

# Funzione standard per configurare asse X con griglia precisa
def configure_x_axis(ax):
    ax.set_xlim(x_min, x_max)
    ax.xaxis.set_major_locator(DayLocator(interval=1))             # griglia ogni giorno a mezzanotte
    ax.xaxis.set_minor_locator(HourLocator(interval=6))            # griglia leggera ogni 6 ore
    ax.xaxis.set_major_formatter(x_fmt)
    ax.tick_params(axis='x', rotation=0)  # verticale per evitare sovrapposizione
    ax.grid(which="major", axis='x', alpha=0.3)
    ax.grid(which="minor", axis='x', linestyle=":", alpha=0.15)

# Grafico 1 – Ore registrate da Steam
fig, ax = plt.subplots(figsize=(80,24))
#ax.plot(df.index, df["hours"], marker="o", linestyle="-", color="#1f77b4")
plot_df = df[(df.index >= df.index.min()) & (df.index <= df.index.max())]
ax.plot(plot_df.index, plot_df["hours"], marker="o", linestyle="-", color="#1f77b4", linewidth=3,markersize=3)
ax.set_title("Ore registrate (Steam: ultime 2 settimane)")
ax.set_ylabel("Ore totali")
ax.set_ylim(*get_y_limits(df["hours"]))
configure_x_axis(ax)
plt.tight_layout()
fig.savefig("grafici/01_snapshot_ore.png", dpi=300)

# Grafico 2 – Delta tra snapshot consecutivi
'''
fig, ax = plt.subplots(figsize=(80,24))
#ax.plot(df.index, df["delta_hours"], marker="o", linestyle="-", color="#ff7f0e")
plot_df = df[(df.index >= df.index.min()) & (df.index <= df.index.max())]
#ax.plot(plot_df.index, plot_df["hours"], marker="o", linestyle="-", color="#ff7f0e")
ax.plot(plot_df.index, plot_df["delta_hours"], marker="o", linestyle="-", color="#ff7f0e")
ax.set_title("Differenza di ore tra snapshot consecutivi")
ax.set_ylabel("Δ ore")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_ylim(*get_y_limits(df["delta_hours"]))
configure_x_axis(ax)
plt.tight_layout()
fig.savefig("grafici/02_delta_ore.png", dpi=300)
'''
fig, ax = plt.subplots(figsize=(80, 24))
colors = df["delta_hours"].apply(lambda x: "#2ca02c" if x > 0 else "#d62728")
ax.bar(df.index, df["delta_hours"], color=colors, width=0.03)
ax.set_title("Differenza di ore tra snapshot consecutivi")
ax.set_ylabel("Δ ore")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_ylim(*get_y_limits(df["delta_hours"]))
configure_x_axis(ax)
plt.tight_layout()
fig.savefig("grafici/02_delta_ore_migliorato.png", dpi=300)

# Grafico 3 – Ore cumulative stimate
'''fig, ax = plt.subplots(figsize=(80,24))
#ax.plot(df.index, df["cumulative_delta"], marker="o", linestyle="-", color="#2ca02c")
plot_df = df[(df.index >= df.index.min()) & (df.index <= df.index.max())]
#ax.plot(plot_df.index, plot_df["hours"], marker="o", linestyle="-", color="#2ca02c")
ax.plot(plot_df.index, plot_df["cumulative_delta"], marker="o", linestyle="-", color="#2ca02c")
ax.set_title("Tempo di gioco cumulativo stimato dalle variazioni")
ax.set_ylabel("Ore totali aggiunte")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_ylim(*get_y_limits(df["cumulative_delta"]))
configure_x_axis(ax)
plt.tight_layout()
fig.savefig("grafici/03_delta_cumulativo.png", dpi=300)
'''
fig, ax = plt.subplots(figsize=(80, 24))
ax.plot(df.index, df["cumulative_delta"], marker="o", linestyle="-", color="#2ca02c", linewidth=3,markersize=3)
ax.set_title("Tempo di gioco cumulativo stimato dalle variazioni")
ax.set_ylabel("Ore totali aggiunte")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_ylim(*get_y_limits(df["cumulative_delta"]))
configure_x_axis(ax)

# Annotazione finale
final_value = df["cumulative_delta"].iloc[-1]
final_time = df.index[-1]
ax.annotate(f"{final_value:.1f} ore", xy=(final_time, final_value),
            xytext=(final_time + timedelta(days=1), final_value),
            arrowprops=dict(arrowstyle="->", color="gray"))

plt.tight_layout()
fig.savefig("grafici/03_delta_cumulativo_migliorato.png", dpi=300)


####### 18/09/2025: ANALISI MENSILE #######
os.makedirs("grafici/AnalisiMensile", exist_ok=True)

# Estrai anno e mese dal timestamp
df["year"] = df.index.year
df["month"] = df.index.month

# Ciclo su ogni combinazione anno/mese
for (year, month), group in df.groupby(["year", "month"]):
    # Mantieni solo l'ultima istanza per giorno
    group["date_only"] = group.index.date
    group = group.groupby("date_only").last()
    group.index = pd.to_datetime(group.index)
    group = group.sort_index()

    # Salta se il gruppo è vuoto
    if group.empty:
        continue

    # Imposta limiti X per il mese corrente
    x_min = group.index.min() - timedelta(days=2)
    x_max = group.index.max() + timedelta(days=2)

    fig, ax = plt.subplots(figsize=(20, 6))  # dimensione più contenuta
    ax.plot(group.index, group["hours"], marker="o", linestyle="-", color="#1f77b4", linewidth=3,markersize=3)
    #ax.set_title(f"Ore registrate – {group.index[0].strftime('%B %Y')}")
    ax.set_title(f"Ore registrate – {group.index[0].strftime('%B %Y')}")
    ax.set_ylabel("Ore totali")
    ax.set_ylim(*get_y_limits(group["hours"]))
    
    # Configura asse X con limiti personalizzati
    ax.set_xlim(x_min, x_max)
    ax.xaxis.set_major_locator(DayLocator(interval=1))
    ax.xaxis.set_minor_locator(HourLocator(interval=6))
    ax.xaxis.set_major_formatter(DateFormatter("%d/%m\n%H:%M"))
    ax.tick_params(axis='x', rotation=0)
    ax.grid(which="major", axis='x', alpha=0.3)
    ax.grid(which="minor", axis='x', linestyle=":", alpha=0.15)

    plt.tight_layout()
    filename = f"grafici/AnalisiMensile/{year}_{month:02d}_ore_mensili.png"
    fig.savefig(filename, dpi=200)
    plt.close(fig)
