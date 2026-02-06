from enum import Enum

class VisitStatus(str, Enum):
    AGENDADA = "AGENDADA"
    REALIZADA = "REALIZADA"
    CANCELADA = "CANCELADA"
    REMARCADA = "REMARCADA"

RESULTADOS = ["Excelente", "Bom", "Neutro", "Ruim"]

UF_LIST = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",
    "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"
]
