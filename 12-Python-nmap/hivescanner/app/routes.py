from flask import render_template
from flask import request
from app import app
import json
import nmap


def nmapdef(data):
   print('Executing')
   nm = nmap.PortScanner()
   rData = nm.scan(data)
   if rData['scan']:
      return rData['scan'][str(data)]
   else:
      return rData['nmap']['scanstats']['uphosts']


@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', title='hive')

@app.route('/scaner', methods=['POST'])
def scanner():
   if (request.form['domainname'] != '127.0.0.1'):
      user =  nmapdef(request.form['domainname'])
      print(user)
      return json.dumps({'status':'OK','user':user})
   else:
      return json.dumps({'status':'OK','user':'local Ip cannot be used'})