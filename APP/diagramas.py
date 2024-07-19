import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import math

dab = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gestor"
)

curso = dab.cursor()

buscar = "SELECT COUNT(*) FROM usuarios"
curso.execute(buscar)
datos = curso.fetchone()[0]

buscarT1 = "SELECT COUNT(*) FROM tareas WHERE estado = 'Por asignar'"
curso.execute(buscarT1)
datosT1 = curso.fetchone()[0]

buscarT2 = "SELECT COUNT(*) FROM tareas WHERE estado = 'Terminado'"
curso.execute(buscarT2)
datosT2 = curso.fetchone()[0]

buscarT3 = "SELECT COUNT(*) FROM tareas WHERE estado = 'En proceso'"
curso.execute(buscarT3)
datosT3 = curso.fetchone()[0]

x = [datos,datosT1,datosT2,datosT3]
y = ["Usuarios","T.por asignar","T.Terminado","T.En proceso"]


plt.bar(y,x)
plt.xlabel('Categora')
plt.ylabel('Cantidades')
plt.grid()
plt.show()

