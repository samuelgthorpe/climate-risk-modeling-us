#!/usr/bin/env python
"""
app.py 

This repository contains a simple Quandl Stock Ticker Flask app that runs on Heroku.
The app takes as input a stock ticker code (and optional start year) and displays a Bokeh plot of the stock time series. Stock price data comes from the Quandl WIKI database (https://www.quandl.com/data/WIKI), queried via the requests module.
Link to the finished app: https://hello-flask-samuelgthorpe.herokuapp.com

The project was completed for the purpose of learning how to tie together some important concepts and
technologies, including Git, Flask, JSON, Pandas, Requests, Heroku, and Bokeh for visualization.
  
# INPUTS 
# -----------------------------------------------------------------------------|
 
  
# OUTPUTS 
# -----------------------------------------------------------------------------| 

  
# NOTES 
# -----------------------------------------------------------------------------|
http://nbviewer.ipython.org/github/samuelgthorpe/climate-risk-modeling-us/blob/master/capstone_content.ipynb

to debug locally:
http://127.0.0.1:33507

 
Written 12/08/2015
By Sam Thorpe 
"""


# # Module Imports
# -----------------------------------------------------|
from flask import Flask, render_template, request, redirect
import requests
import numpy as np
import pandas as pd
import sqlite3 as lite
#import bokeh
#from bokeh.plotting import figure
#from bokeh.io import show
#from bokeh.embed import components
#bv = bokeh.__version__
from sampy.common import keyboard


# # app Flask & database connect
# -----------------------------------------------------|
app = Flask(__name__)
app.vars={}
feat = ['Warming','Drought']
conn = lite.connect('clim_zip')
cursor = conn.cursor()    


@app.route('/')
def main():
	return redirect('/index')
	

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		#request was a POST
		app.vars['zipcode'] = request.form['zipcode'].upper()
		app.vars['select'] = [feat[q] for q in range(2) if feat[q] in request.form.values()]
		return redirect('/graph')


@app.route('/graph',methods=['GET','POST'])
def graph():
	
	
	# Request data from database and get into pandas
	# --------------------------------------------|
	qry = "SELECT * FROM zip_dat WHERE zip=%s;" % app.vars['zipcode']
	df = pd.read_sql_query(qry,conn)
	Nrep = len(str(df.names[0]).split(','))
	name = []
	contact = []
	conhtml = '<p>'
	for q in range(Nrep):
		contact.append(str(df.contacts[0]).split(',')[q])
		name.append(str(df.names[0]).split(',')[q])
		tmphtml = '<i><a href=%s>Rep. %s</a></i><br>' % (contact[q],name[q])
		conhtml = conhtml + tmphtml
	conhtml = conhtml + '</p>'
	#keyboard(locals(),globals())
	
	
	if app.vars['select'][0]=='Warming':
		#embed = 'dA'
		embed = '<iframe width="100%" height="520" frameborder="0" src="https://samuelgthorpe.cartodb.com/viz/8264153a-ba2d-11e5-b57e-0e31c9be1b51/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>'
	elif app.vars['select'][0]=='Drought':
		#embed = 'dP'
		embed = '<iframe width="100%" height="520" frameborder="0" src="https://samuelgthorpe.cartodb.com/viz/30864d8c-ba2d-11e5-9db3-0ecfd53eb7d3/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>'
	
	

	return render_template('graph.html',zipcode=app.vars['zipcode'],
	                        ftag=app.vars['select'][0],div=embed,conhtml=conhtml)

	
	#keyboard(locals(),globals())
#	if Nrep==1:
#		return render_template('graph1.html',zipcode=app.vars['zipcode'],
#	                        ftag=app.vars['select'][0],div=embed,contact1=contact[0],name1=name[0])
#	elif Nrep==2:
#		return render_template('graph2.html',zipcode=app.vars['zipcode'],
#	                        ftag=app.vars['select'][0],div=embed,
#	                        contact1=contact[0],name1=name[0],contact2=contact[1],name2=name[1])
	
#@app.errorhandler(500)
#def error_handler(e):
#	return render_template('error.html',ticker=app.vars['ticker'],year=app.vars['start_year'])

    
    
#    				<p><i><a href={{contact1}}>Rep. {{name1}}</a></i><br>
#				   <i><a href={{contact2}}>Rep. {{name2}}</a></i></p>
    
    
# # If main
# -----------------------------------------------------|
if __name__ == '__main__':
  app.run(port=33507,debug=False)
  
  
  
#                                    END ALL
# # ---------------------------------------------------------------------------|
    
