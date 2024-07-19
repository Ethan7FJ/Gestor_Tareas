from flask import Flask
from APP import dab
import datetime

class Tareas(dab.Model):
    id = dab.Column(dab.Integer,Primary_Key = True)
    nombre_t = dab.Column(dab.String(200),nullable = False)
    fecha_inicio_t =  dab.Column(dab.DateTime,default=datetime.utcnow)
    fecha_final_t =  dab.Column(dab.DateTime)
    estado =  dab.Column(dab.String(50),default = 'Por asignar')

    


