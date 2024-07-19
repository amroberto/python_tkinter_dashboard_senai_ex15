import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

url = "https://bea3853.github.io/site_teste/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table')

df = pd.read_html(str(table))[0]
df_agrupado = df.groupby('Região')['Compra'].sum().reset_index()
df_agrupado2 = df.groupby('Nome')['Compra'].sum().reset_index()

# Gráfico 1: Gráfico de barra
fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=80)
ax1.bar(df_agrupado['Região'], df_agrupado['Compra'])
ax1.set_title("FATURAMENTO POR REGIÃO")
ax1.set_xlabel("Região")
ax1.set_ylabel("Valor")
ax1.bar_label(ax1.bar(df_agrupado['Região'], df_agrupado["Compra"]), fmt='{:,.0f}')

# Gráfico 2: Barra Horizontal de Faturamento por Cliente
fig2, ax2 = plt.subplots(figsize=(6, 4), dpi=80)
ax2.barh(df_agrupado2['Nome'], df_agrupado2['Compra'])
ax2.set_title("FATURAMENTO POR CLIENTE")
ax2.set_xlabel("Valor")
ax2.set_ylabel("Cliente")

root = tk.Tk()

# Configuração da janela
w = 1000
h = 600
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw - w) / 2
y = (sh - h) / 2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.title("Dashboard")

# Medidas estatísticas
total_compras = df['Compra'].sum()
ticket_medio = df['Compra'].mean()
mediana = df['Compra'].median()
desvio = df['Compra'].std()

# Formatação das medidas
total_formatado = f"{total_compras:.2f}"
ticket_medio_formatado = f"{ticket_medio:.2f}"
mediana_formatada = f"{mediana:.2f}"
desvio_formatado = f"{desvio:.2f}"

# Frame principal
mainframe = tk.Frame(root)
mainframe.pack(fill="both", expand=True)

# Frame para conteúdo
frame = tk.Frame(mainframe, bg='#ffffff')
frame.pack(fill="both", expand=True)

# Top Bar Frame
topbarframe = tk.Frame(frame, bg='#ebedf7')
topbarframe.pack()

# Total Frame
total_frame = tk.Frame(topbarframe, bg='#ffb229', width=250, height=150)
total_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
total_frame.grid_columnconfigure(0, weight=1)
total_title = tk.Label(total_frame, text='Faturamento', font=('Verdana', 12), bg='#e89f20', width=19, pady=12)
total_title.grid(row=0, column=0, sticky='nsew')
total_count = tk.Label(total_frame, text=total_formatado, font=('Verdana', 12), bg='#ffb229', padx=11, pady=10)
total_count.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

# Média Frame
media_frame = tk.Frame(topbarframe, bg='#4bc012', width=250, height=150)
media_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
media_frame.grid_columnconfigure(0, weight=1)
media_title = tk.Label(media_frame, text='Ticket Médio', font=('Verdana', 12), bg='#379409', width=19, pady=12)
media_title.grid(row=0, column=0, sticky='nsew')
media_count = tk.Label(media_frame, text=ticket_medio_formatado, font=('Verdana', 12), bg='#4bc012', padx=11, pady=10)
media_count.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

# Mediana Frame
mediana_frame = tk.Frame(topbarframe, bg='#9b59b6', width=250, height=150)
mediana_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
mediana_frame.grid_columnconfigure(0, weight=1)
mediana_title = tk.Label(mediana_frame, text='Mediana', font=('Verdana', 12), bg='#7d3c9b', width=19, pady=12)
mediana_title.grid(row=0, column=0, sticky='nsew')
mediana_count = tk.Label(mediana_frame, text=mediana_formatada, font=('Verdana', 12), bg='#9b59b6', padx=11, pady=10)
mediana_count.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

# Desvio Padrão Frame
desvio_frame = tk.Frame(topbarframe, bg='#7f95f5', width=250, height=150)
desvio_frame.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')
desvio_frame.grid_columnconfigure(0, weight=1)
desvio_title = tk.Label(desvio_frame, text='Desvio Padrão', font=('Verdana', 12), bg='#596dc2', width=19, pady=12)
desvio_title.grid(row=0, column=0, sticky='nsew')
desvio_count = tk.Label(desvio_frame, text=desvio_formatado, font=('Verdana', 12), bg='#7f95f5', padx=11, pady=10)
desvio_count.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

# Content Frame
contentframe = tk.Frame(frame)
contentframe.pack(fill="both", expand=True)

# Canvas para Gráficos
canvas1 = FigureCanvasTkAgg(fig1, contentframe)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas2 = FigureCanvasTkAgg(fig2, contentframe)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()