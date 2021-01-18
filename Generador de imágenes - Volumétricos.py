# ---------- GENERADOR DE IMÁGENES VOLUMÉTRICOS ----------

import pandas as pd
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

# Defino la ruta de los archivos:
ruta = "C:\\Users\\gperetti\\OneDrive - Embotelladora Andina\\Data Mining\\7. Imágenes - MiCC\\1. Generador de imágenes\\2. Combo Store\\Combo Store 2020\\"

df_combos = pd.read_excel("C:\\Users\\gperetti\\OneDrive - Embotelladora Andina\\Data Mining\\7. Imágenes - MiCC\\1. Generador de imágenes\\2. Combo Store\\Imágenes a generar.xlsx", sheet_name = "Volumen")
df_capas = pd.read_excel("C:\\Users\\gperetti\\OneDrive - Embotelladora Andina\\Data Mining\\7. Imágenes - MiCC\\1. Generador de imágenes\\2. Combo Store\\Imágenes a generar.xlsx", sheet_name = "Capas")
df_descripcion = pd.read_excel("C:\\Users\\gperetti\\OneDrive - Embotelladora Andina\\Data Mining\\7. Imágenes - MiCC\\1. Generador de imágenes\\2. Combo Store\\Imágenes a generar.xlsx", sheet_name = "Descripción")

df_capas["Descripción"] = df_capas["Descripción"].str.replace("/", "-")

df_capas = df_capas[df_capas["Activo"] == "Si"]

#df_combos = df_combos[df_combos["Imprimir"] == "Si"]
#df_capas = df_capas[df_capas["Imagen"] == "Si"]

df_combos["Capa"] = df_combos["Capa"].str.replace("/", "-")
df_combos["Fondo"] = df_combos["Fondo"].str.replace("/", "-")
df_combos["Frame"] = df_combos["Frame"].str.replace("/", "-")
df_capas["Sku's Claves"] = df_capas["Sku's Claves"].str.replace("/", "-")

gotham_bold = "Gotham-Bold.otf"
gotham_black = "GothamBlack.otf"
gotham_cond_bold = "GothamCond-Bold.otf"

imagenes = {}

for i in df_combos["9mil"]:
    # Creo todas las imágenes en blanco
    imagenes[i] = Image.new('RGBA', (637, 481), "white")
    
    # Fondos y frames según la capa
    capa = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Capa"])
    fondo = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Fondo"])
    fondo = Image.open(ruta + "Fondos\\" + fondo.iloc[0, :]["Fondo"] + ".png").convert("RGBA")
    frame = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Frame"])
    frame = Image.open(ruta + "Frames\\" + frame.iloc[0, :]["Frame"] + ".png").convert("RGBA")
    imagenes[i].paste(fondo, mask = fondo)
    imagenes[i].paste(frame, mask = frame)
    
    # 9miles
    draw = ImageDraw.Draw(imagenes[i])
    fuente = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_bold, 45)
    nueve_mil = str(i)
    draw.text((90, 12), nueve_mil, (255, 255, 255), font=fuente)
    
    # "No Dispara"
    dispara = Image.open(ruta + "Fondos\\Elementos\\ND.png").convert("RGBA")
    imagenes[i].paste(dispara, (5, 2), mask = dispara)
    
    # Bocha blanca del descuento
    bocha_descuento = Image.open(ruta + "Fondos\\Elementos\\bochon-dcto.png").convert("RGBA")
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
    font3 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_black, 15)
    # draw.text((470, 135), "DE DESCUENTO", (0, 0, 0), font=font3)
    
    # Descripción de la capa
    # Agrego leyenda solo para las CC Pet 3L
    if capa.iloc[0, :]["Capa"] == "CC REG Futuro":
        font10 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_bold, 8) 
        solo_disponible = "(*) Solo disponible en Neuquén, Santa Rosa, Tres Arroyos, C. Suarez, Bariloche, Azul, Viedma, Olvarría, T. Lauquen, Bahía Blanca," 
        solo_disponible_2 = "G. Roca, Chicilcoy, Pehuajo, C. Casares, Bolivar, SM de los Andes, C. Pringles, General Pico"
        w, h = draw.textsize(solo_disponible, font10)
        draw.text(((imagenes[i].size[0]-w)/2, 425), solo_disponible, (255, 255, 255), font=font10)
        w, h = draw.textsize(solo_disponible_2, font10)
        draw.text(((imagenes[i].size[0]-w)/2, 435), solo_disponible_2, (255, 255, 255), font=font10) 
        
        font4 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_bold, 25)
        descripción = pd.DataFrame(df_descripcion[df_descripcion["Capa"] == capa.iloc[0, :]["Capa"]]["Descripción"])
        descripción = descripción.iloc[0, :]["Descripción"]
        w, h = draw.textsize(descripción, font4)
        draw.text(((imagenes[i].size[0]-w)/2, 390), descripción, (255, 255, 255), font=font4)
    else:
        font4 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_bold, 25)
        descripción = pd.DataFrame(df_descripcion[df_descripcion["Capa"] == capa.iloc[0, :]["Capa"]]["Descripción"])
        descripción = descripción.iloc[0, :]["Descripción"]
        w, h = draw.textsize(descripción, font4)
        draw.text(((imagenes[i].size[0]-w)/2, 410), descripción, (0, 0, 0), font=font4)
        
    # Nombre de la capa
    font5 = ImageFont.truetype("arial.ttf", 12)
    texto_desc = str(i) + " > " + str(capa.iloc[0, :]["Capa"]).upper() + " > " + str(descuento)
    w, h = draw.textsize(texto_desc, font5)
    draw.text(((imagenes[i].size[0]-w)/2, 460), texto_desc, (0, 0, 0), font=font5)
    
    # Máximo 1 combo por acto de compra
    font6 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 30)
    texto_max = "MAX. 1 COMBO"
    draw.text((270, 10), texto_max, (255, 255, 255), font=font6)
    font7 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 20)
    texto_acto = "X ACTO DE COMPRA"
    draw.text((270, 40), texto_acto, (255, 255, 255), font=font7)
    
    # Bocha blanca y "Llevando X cajas físicas"
    bocha_cajas = Image.open(ruta + "Fondos\\Elementos\\bochon-BL.png").convert("RGBA")
    bocha_cajas = bocha_cajas.resize((60, 60))
    imagenes[i].paste(bocha_cajas, (108, 142), mask = bocha_cajas)
    font8 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 30)
    texto_llevando = "LLEVANDO           PACKS (SE PUEDEN COMBINAR)"
    draw.text((20, 150), texto_llevando, (0, 0, 0), font=font8)
    
    # Cantidad de cajas requeridas
    font9 = ImageFont.truetype(ruta + "\\Fuentes\\" + gotham_cond_bold, 45)
    texto_llevando = pd.DataFrame(df_combos[df_combos["9mil"] == i]["Cantidad"])
    cantidad = str(texto_llevando.iloc[0, :]["Cantidad"])
    if len(cantidad) == 1:
        draw.text((130, 152), cantidad, (255, 0, 0), font=font9)
    else:
        draw.text((124, 152), cantidad, (255, 0, 0), font=font9)
        
    # Palabra "nuevo" arriba a la derecha
    # nuevo = Image.open(ruta + "Fondos\\Elementos\\NUEVO.png").convert("RGBA")
    # imagenes[i].paste(nuevo, mask = nuevo)
    
    # Inserto los SKU (Empiezo desde el centro y voy abriendo tipo abanico)
    p = 0
    a = -1
    r = 0
    h = 0
    for j in df_capas[df_capas["Sku\'s Claves"] == capa.iloc[0, :]["Capa"]]["Descripción"]:
        b = (a ** p) * h
        SKU = Image.open(ruta + "SKUs\\" + str(j) + ".png").convert("RGBA")
        # Si hay más de 7 SKUs en la capa, achico las imágenes para que entren todas
        if len(df_capas[df_capas["Sku\'s Claves"] == capa.iloc[0, :]["Capa"]]["Descripción"]) > 7:
            SKU.thumbnail((100, 200), Image.ANTIALIAS)
        else:
            SKU.thumbnail((100, 220), Image.ANTIALIAS)
        s = SKU.size[0]
        if len(df_capas[df_capas["Sku\'s Claves"] == capa.iloc[0, :]["Capa"]]["Descripción"]) > 7:
            imagenes[i].paste(SKU, ((int((imagenes[i].size[0]-s)/2) + (b * 60)), 190), mask = SKU)
        else:
            imagenes[i].paste(SKU, ((int((imagenes[i].size[0]-s)/2) + (b * 70)), 190), mask = SKU)
        p += 1
        r += 0.5
        h = math.ceil(r)
    
    # Etiqueta mínimo lleva una KIN
    # etiqueta_kin = Image.open(ruta + "Fondos\\Elementos\\etiqueta_kin.png").convert("RGBA")
    # etiqueta_kin.thumbnail((200, 100), Image.ANTIALIAS)
    # imagenes[i].paste(etiqueta_kin, (40, 300), mask = etiqueta_kin)
        
    # Guardo las imágenes
    imagenes[i].save(ruta + "Imágenes volumétricos\\" + str(i) + ".png")

print("Listo!")