from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from models import Veiculo
from mongoengine import *

import time
from mongoengine.connection import get_db
from gridfs import GridFS, NoFile
from bson.objectid import ObjectId
from django.http import Http404, HttpResponse
from django.utils.http import http_date


connect('revenda')



def serve_file(request, file_id):
    db = get_db()
    fs = GridFS(db)
    try:
        f = fs.get(ObjectId(file_id))
    except NoFile:
        fs = GridFS(db, collection='images') # mongoengine stores images in a separate collection by default
        try:
            f = fs.get(ObjectId(file_id))
        except NoFile:
            raise Http404

    response = HttpResponse(f.read(), content_type=f.content_type)
    #timestamp = time.mktime(gridout.upload_date.timetuple())
    #response["Last-Modified"] = http_date(timestamp)
    # add other header data like etags etc. here
    return response



def index(request):
    if not request.user.is_authenticated():
        return render_to_response('vlogin.html', {}, context_instance=RequestContext(request))

    if request.method == 'POST':
        veiculo = Veiculo()
        veiculo.ano = request.POST['ano']
        veiculo.fabricante = request.POST['fabricante']
        veiculo.modelo = request.POST['modelo']
        foto = request.FILES.get('foto')
        if foto:
            veiculo.foto.put(foto)
        veiculo.save()

    veiculos = Veiculo.objects
    return render_to_response('index.html', {'Veiculos': veiculos}, context_instance=RequestContext(request))

def update(request):
    if not request.user.is_authenticated():
        return render_to_response('vlogin.html', {}, context_instance=RequestContext(request))

    id = eval("request." + request.method + "['id']")
    veiculo = Veiculo.objects(id=id)[0]

    if request.method == 'POST':
        veiculo.ano = request.POST['ano']
        veiculo.fabricante = request.POST['fabricante']
        veiculo.modelo = request.POST['modelo']
        foto = request.FILES.get('foto')
        if foto:
            veiculo.foto.replace(foto)

        veiculo.save()
        template = 'index.html'
        params = {'Veiculos': Veiculo.objects}
    elif request.method == 'GET':
        template = 'update.html'
        params = {'veiculo':veiculo}

    return render_to_response(template, params, context_instance=RequestContext(request))


def delete(request):
    if not request.user.is_authenticated():
        return render_to_response('vlogin.html', {}, context_instance=RequestContext(request))

    id = eval("request." + request.method + "['id']")

    if request.method == 'POST':
        veiculo = Veiculo.objects(id=id)[0]
        veiculo.delete()
        template = 'index.html'
        params = {'Veiculos': Veiculo.objects}
    elif request.method == 'GET':
        template = 'delete.html'
        params = {'id':id}

    return render_to_response(template, params, context_instance=RequestContext(request))


def vlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            #mensagem de falha
            return render_to_response('vlogin.html', {}, context_instance=RequestContext(request))
    else:
        #usuario invalido
        return render_to_response('vlogin.html', {}, context_instance=RequestContext(request))
    request.method = 'GET'
    return index(request) 

def vlogout(request):
    logout(request)
    request.method = 'GET'
    return index(request)
