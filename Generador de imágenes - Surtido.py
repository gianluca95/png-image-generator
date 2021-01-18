# ---------- GENERADOR DE IMÁGENES DE SURTIDO ----------

import pandas as pd
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.filterwarnings("ignore")
import textwrap

# Defino la ruta de los archivos:
ruta = "C:\\Users\\gperetti\\OneDrive - Embotelladora Andina\\Data Mining\\7. Imágenes - MiCC\\1. Generador de imágenes\\2. Combo Store\\Combo Store 2020\\"

# Cargo los combos con su descripción:
df_combos = pd.read_excel("C:\\Users\\gperetti\\OneDrive - Embotelladora Andina\\Data Mining\\7. Imágenes - MiCC\\1. Generador de imágenes\\2. Combo Store\\Imágenes a generar.xlsx", sheet_name = "Surtido")

# Limpieza de datos:
df_combos["9mil"] = df_combos["9mil"].astype(int).astype(str)

for i in ["SKU1", "SKU2", "Fondo", "Frame"]:
    df_combos[i] = df_combos[i].str.replace("/", "-")
    
for i in ["Q2", "SKU2", "Q3", "SKU3"]:
    df_combos[i] = df_combos[i].fillna(0)

# Fuentes (tipos de letra) que voy a utilizar:
gotham_bold = "Gotham-Bold.otf"
gotham_black = "GothamBlack.otf"
gotham_cond_bold = "GothamCond-Bold.otf"

# Creo un diccionario vacío donde voy a almacenar las imágenes:
imagenes = {}

# En cada iteración voy insertando los distintos elementos que componen la imagen:
for i in df_combos["9mil"]:
    
    # Creo todas las imágenes en blanco
    imagenes[i] = Image.new('RGBA', (637, 481), "white")
    
    # Fondos y frames según la capa
    fondo = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Fondo"])
    fondo2 = Image.open(ruta + "Fondos\\" + fondo.iloc[0, :]["Fondo"] + ".png").convert("RGBA")
    imagenes[i].paste(fondo2, mask = fondo2)
    frame = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Frame"])
    frame2 = Image.open(ruta + "Frames\\" + frame.iloc[0, :]["Frame"] + ".png").convert("RGBA")
    imagenes[i].paste(frame2, mask = frame2)
    
    # 9miles
    draw = ImageDraw.Draw(imagenes[i])
    font1 = ImageFont.truetype(ruta + "Fuentes\\" + gotham_bold, 45)
    nueve_mil = str(i)
    draw.text((90, 12), nueve_mil, (255, 255, 255), font=font1)
    
    # "Dispara" o "No Dispara"
    df_dispara = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Dispara?"])
    if df_dispara.iloc[0, :]["Dispara?"] == "DP":
        dispara = Image.open(ruta + "Fondos\\Elementos\\DP.png").convert("RGBA")
    else:
        dispara = Image.open(ruta + "Fondos\\Elementos\\ND.png").convert("RGBA")
    imagenes[i].paste(dispara, (5, 2), mask = dispara)
    
    # Bocha blanca del descuento
    bocha_descuento = Image.open(ruta + "Fondos\\Elementos\\bochon.png").convert("RGBA")
    bocha_descuento = bocha_descuento.resize((200, 200))
    imagenes[i].paste(bocha_descuento, (430, 20), mask = bocha_descuento)
    
    # Porcentaje descuento y abajo palabra "de descuento"
    font2 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_black, 70)
    descuento = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Dto"]).iloc[0, :]["Dto"]
    porcentaje = str(int(descuento * 100)) + "%"
    if len(porcentaje) == 2:
        draw.text((478, 65), porcentaje, (255, 0, 0), font=font2)
    else:
        draw.text((460, 65), porcentaje, (255, 0, 0), font=font2)
    
    # Descripción de los SKUs del combo
    font4 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_bold, 23)
    
    SKU1 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["SKU1"])
    SKU1 = SKU1.iloc[0, :]["SKU1"]
    
    SKU2 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["SKU2"])
    SKU2 = SKU2.iloc[0, :]["SKU2"]
    
    SKU3 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["SKU3"])
    SKU3 = SKU3.iloc[0, :]["SKU3"]
    
    if SKU3 != 0:
        SKUs = SKU1 + " + " + SKU2 + " + " + SKU3
        lines = textwrap.wrap(SKUs, width=46)
        y_text = 400
        for line in lines:
            width, height = font4.getsize(line)
            draw.text(((imagenes[i].size[0] - width) / 2, y_text), line, (255, 255, 255), font=font4)
            y_text += height
    else:
        SKUs = SKU1 + " + " + SKU2
        lines = textwrap.wrap(SKUs, width=44)
        y_text = 400
        for line in lines:
            width, height = font4.getsize(line)
            draw.text(((imagenes[i].size[0] - width) / 2, y_text), line, (255, 255, 255), font=font4)
            y_text += height

    # Descripción de los SKUs abajo para el OCR
    font5 = ImageFont.truetype("tahoma.ttf", 14)
    texto_desc = str(i) + " > " + str(fondo.iloc[0, :]["Fondo"]).upper() + " > " + str(SKUs) + " > " + str(descuento)
    w, h = draw.textsize(texto_desc, font5)
    draw.text(((imagenes[i].size[0]-w)/2, 453), texto_desc, (0, 0, 0), font=font5)
    
    # Aplica hasta X combos
    font6 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 30)
    texto_max = "Aplica hasta 3"
    draw.text((270, 10), texto_max, (255, 255, 255), font=font6)
    font7 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 20)
    texto_acto = "Combos"
    draw.text((270, 40), texto_acto, (255, 255, 255), font=font6)
    
    # Bocha blanca cantidad de SKU
    bocha_cajas = Image.open(ruta + "\\Fondos\\Elementos\\bochon-BL.png").convert("RGBA")
    bocha_cajas = bocha_cajas.resize((80, 80))
    imagenes[i].paste(bocha_cajas, (20, 250), mask = bocha_cajas)
    imagenes[i].paste(bocha_cajas, (170, 250), mask = bocha_cajas)
    
    # Envases
    tiene_envase = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Envase"])
    tiene_envase = tiene_envase.iloc[0, :]["Envase"]
    
    if tiene_envase != "No":
        envases = Image.open(ruta + "\\Fondos\\Elementos\\envases_corregido.png").convert("RGBA")
        imagenes[i].paste(envases, (330, 250), mask = envases)
        envase_ret = Image.open(ruta + "Fondos\\Elementos\\" + tiene_envase + ".png").convert("RGBA")
        envase_ret.thumbnail((130, 130), Image.ANTIALIAS)
        imagenes[i].paste(envase_ret, (335, 265), mask = envase_ret)
        font_envase = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_bold, 16)
        if tiene_envase == "FN 2L":
            draw.text((535, 361), "9006", (0, 0, 0), font = font_envase)
        if tiene_envase == "SP 2L":
            draw.text((535, 361), "9008", (0, 0, 0), font = font_envase)
        if tiene_envase == "SWP 2L":
            draw.text((535, 361), "9010", (0, 0, 0), font = font_envase)
        if tiene_envase == "CC 1,25L":
            draw.text((535, 361), "9026", (0, 0, 0), font = font_envase)
        if tiene_envase == "CCSA 1,25L":
            draw.text((535, 361), "9032", (0, 0, 0), font = font_envase)
        if tiene_envase == "SP 1,25L":
            draw.text((535, 361), "9030", (0, 0, 0), font = font_envase)
        if tiene_envase == "FN 1,25L":
            draw.text((535, 361), "9028", (0, 0, 0), font = font_envase)
            
        font15 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 20)
        texto_comodato = "SOLO PARA CLIENTES"
        texto_comodato_1 = "CON MARCA DE COMODATO"
        draw.text((470, 250), texto_comodato, (255, 255, 255), font=font15)
        draw.text((455, 270), texto_comodato_1, (255, 255, 255), font=font15)
    
    # Texto cantidad de SKU
    font8 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 55)
    
    q1 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Q1"])
    q1 = q1.iloc[0, :]["Q1"]
    texto_q1 = "X" + str(q1)
    draw.text((42, 267), texto_q1, (0, 0, 0), font=font8)
    
    q2 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Q2"])
    q2 = q2.iloc[0, :]["Q2"]
    texto_q2 = "X" + str(q2)
    draw.text((192, 267), texto_q2, (0, 0, 0), font=font8)
    
    if SKU3 != 0:
        imagenes[i].paste(bocha_cajas, (320, 250), mask = bocha_cajas)
        q3 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Q3"])
        q3 = q3.iloc[0, :]["Q3"]
        texto_q3 = "X" + str(q3)[0]
        draw.text((340, 267), texto_q3, (0, 0, 0), font=font8)
    
    # Agrego el "+" entre los SKU
    signo_mas = Image.open(ruta + "Fondos\\Elementos\\Mas.png").convert("RGBA")
    signo_mas.thumbnail((50, 50), Image.ANTIALIAS)
    imagenes[i].paste(signo_mas, (165, 200), mask = signo_mas)
    
    if SKU3 != 0:
        signo_mas = Image.open(ruta + "Fondos\\Elementos\\Mas.png").convert("RGBA")
        signo_mas.thumbnail((50, 50), Image.ANTIALIAS)
        imagenes[i].paste(signo_mas, (315, 200), mask = signo_mas)
    
    # Inserto los SKUs
    SKU1 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["SKU1"])
    SKU1 = str(SKU1.iloc[0, :]["SKU1"])
    SKU1 = Image.open(ruta + "SKUs\\" + SKU1 + ".png").convert("RGBA")
    SKU1.thumbnail((100, 280), Image.ANTIALIAS)
    imagenes[i].paste(SKU1, (75, 120), mask = SKU1)
        
    if SKU2 != 0:
        SKU2 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["SKU2"])
        SKU2 = str(SKU2.iloc[0, :]["SKU2"])
        SKU2 = Image.open(ruta + "SKUs\\" + SKU2 + ".png").convert("RGBA")
        SKU2.thumbnail((100, 280), Image.ANTIALIAS)
        imagenes[i].paste(SKU2, (225, 120), mask = SKU2)
            
    if SKU3 != 0:
        SKU3 = pd.DataFrame(df_combos[df_combos["9mil"] == i]["SKU3"])
        SKU3 = str(SKU3.iloc[0, :]["SKU3"])
        SKU3 = Image.open(ruta + "SKUs\\" + SKU3 + ".png").convert("RGBA")
        SKU3.thumbnail((100, 280), Image.ANTIALIAS)
        imagenes[i].paste(SKU3, (375, 120), mask = SKU3)
         
    # Agrego sticker de "nueva"
    #nueva = Image.open(ruta + "Fondos\\Elementos\\nueva.png").convert("RGBA")
    #imagenes[i].paste(nueva, (90, 90), mask = nueva)
    
    # Guardo las imágenes
    imagenes[i].save(ruta + "Imágenes surtido\\" + str(i) + ".png")

print("Listo!")

