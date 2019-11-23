from flask import Flask, request,jsonify
import json
import pymongo
from bson import ObjectId
import requests
import os
import sys


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



app = Flask(__name__)
myclient    = ''
mydb        = ''
mycol       = ''


def get_ip():
    # file = open(os.path.dirname(os.path.realpath(__file__))+'/ip', 'r')
    # ip = file.read() 
    # file.close()
    micro_service_ip = sys.argv[1]+':5000'
    return micro_service_ip

def get_all_tarefas_json():
    r = requests.get('http://'+get_ip()+'/Tarefa')
    return r.text


def post_tarefa(nome):
    data = {
        'nome' : nome
    }

    r = requests.post('http://'+get_ip()+'/Tarefa',params = data)

    return r.text

def delete_tarefa(id):

    r = requests.delete('http://'+get_ip()+'/Tarefa/{0}'.format(id))

    return r.text

def get_tarefa(id):
    r = requests.get('http://'+get_ip()+'/Tarefa/{0}'.format(id))
    return r.text

def home_r():
    r = requests.get('http://'+get_ip()+'/')
    return r.text


def atualiza_tarefa(id, nome, done):

    data = {
            'id' : id,
            'nome': nome,
            'done': done
    }

    r = requests.put('http://'+get_ip()+'/Tarefa/{0}'.format(id),params = data)
    return r.text


@app.route("/")
def home():
    return home_r()


@app.route('/Tarefa',methods=["GET","POST"])
def tarefa():
    if request.method == 'POST': 
        nome = request.args.get('nome')

        
        return post_tarefa(nome)
    elif request.method == 'GET':
        return get_all_tarefas_json() 

@app.route('/Tarefa/<id>',methods=["GET","PUT","DELETE"])
def tarefa_id(id):
    id = int(id)

    if request.method == 'PUT': 
        nome = request.args.get('nome')
        done = request.args.get('done')

        
        return atualiza_tarefa(id,nome,done)

    elif request.method == 'GET':
        return get_tarefa(id) 

    elif request.method == 'DELETE':
         
        return delete_tarefa(id)

@app.route('/healthcheck/')
def healthcheck():
    return ('', 200)

if __name__ == '__main__':

    app.run(host= '0.0.0.0')
    