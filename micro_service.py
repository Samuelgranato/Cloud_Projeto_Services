from flask import Flask, request,jsonify
import json
import pymongo
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



app = Flask(__name__)
myclient    = ''
mydb        = ''
mycol       = ''


class Tarefas:
  def __init__(self, name,id):

    self.name = name
    self.done = False
    self.id = id
    self.active = True

  def toJSON(self):
        return json.dumps(self.__dict__)


def get_all_tarefas_json():
    t = []
    for x in mycol.find():
        t.append(x)
    print(t)
    new_dict = {item['id']:item for item in t}
    print(new_dict)
    return JSONEncoder().encode(t)

def get_all_tarefas_list():
    t = []
    for x in mycol.find():
        t.append(x)
    return t

def post_tarefa(nome):
    id = len(get_all_tarefas_list())


    tarefa = {
        'id'    : id,
        'nome'  : nome,
        'done'  : 'False',
        'active': 'True'
    }

    mycol.insert_one(tarefa)

    return

def delete_tarefa(id):

    myquery = { "id": id }
    mycol.delete_many(myquery)

    return

def get_tarefa(id):
    for x in mycol.find():
        if(x['id'] == id):
            return x
    return

def atualiza_tarefa(id, nome, done):

    myquery = { "id": id }
    newvalues = { "$set": { "nome": nome, 'done' : done } }

    mycol.update_one(myquery, newvalues)
    return


@app.route("/")
def home():
    return "OK"


@app.route('/Tarefa',methods=["GET","POST"])
def tarefa():
    if request.method == 'POST': 
        nome = request.args.get('nome')

        post_tarefa(nome)
        return 'ok'
    elif request.method == 'GET':
        return get_all_tarefas_json() 

@app.route('/Tarefa/<id>',methods=["GET","PUT","DELETE"])
def tarefa_id(id):
    id = int(id)

    if request.method == 'PUT': 
        nome = request.args.get('nome')
        done = request.args.get('done')

        atualiza_tarefa(id,nome,done)
        return 'ok'

    elif request.method == 'GET':
        return get_tarefa(id) 

    elif request.method == 'DELETE':
        delete_tarefa(id) 
        return ('',200)

@app.route('/healthcheck/')
def healthcheck():
    return ('', 200)

if __name__ == '__main__':
    # client = pymongo.MongoClient("mongodb://18.220.67.82/tarefa") # defaults to port 27017
    # db = client.tarefa

    myclient = pymongo.MongoClient("mongodb://18.220.67.82:27017/projeto")
    mydb = myclient["projeto"]
    mycol = mydb["tarefa"]

    app.run(host= '0.0.0.0')
    