from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017")
banco = cliente["biblioteca"]

livros = banco["livros"]
usuarios = banco["usuarios"]