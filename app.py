from flask import Flask, render_template, request, url_for, flash, redirect


from distutils.log import debug 
from fileinput import filename 
from flask import *  

import time
import os
today = time.strftime("%Y-%m-%d")
from bancointer.bancointer import BancoInter
from decouple import config
API_VERSION = 2
dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V"+ str(API_VERSION)), dir_base_ssl + config("PRIVATE_KEY_V"+ str(API_VERSION)))
bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

bi.set_client_id(value=config("CLIENT_ID"))

bi.set_client_secret(value=config("CLIENT_SECRET"))
bi.set_base_url(value=config("API_URL_COBRA_V2"))
bi.set_base_url_token(value=config("API_URL_TOKEN_V2"))
# ...

app = Flask(__name__)
app.config['SECRET_KEY'] = '60d7f9e8d9f1fdd2db7bafec2190859e63ad61842e288f05'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
pagador = {
    "cpfCnpj": "19103298000",
    "nome": "Nome do Pagador",
    "cep": "99999999",
    "numero": "00",
    "bairro": "Bairro do Pagador",
    "cidade": "Cidade do Pagador",
    "uf": "PR",
    "endereco": "Logradouro do Pagador",
    "tipoPessoa": "FISICA",
    }

mensagem = {
    "linha5": "mensagem da linha5",
    }

@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.form['pdf-file']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            pagador["cpfCnpj"] = title
            #gera boleto
            #reponse1 = bi.boleto(pagador=pagador,mensagem=mensagem,dataEmissao=today,dataVencimento=today,seuNumero="00001",valorNominal=5)
            #download do boleto no DOWNLOAD PATH
            #reponse2 = bi.download(nosso_numero="01264163577", download_path=config("DOWNLOAD_PATH"))
            #scp 01264025784.pdf root@143.110.246.33:/tmp/root/M@xprint4
            #aws s3 copy 01264025784.pdf BucketName:/*
            #print(reponse)
            #reponse1["nossoNumero"]
            #filename = secure_filename(img_file.filename)
#            filename = "kdldlkkl.pdf"
            #file = request.files['pdf-file']
#            f = request.files['pdf-file'] 
#            f.save(f.filename) 
            #file.save(os.path.join("./", filename + '.' + 'pdf'))
                                   
            messages.append({'title': title, 'content': content})


            return redirect(url_for('index'))

    return render_template('create.html')