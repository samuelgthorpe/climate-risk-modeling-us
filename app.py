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
#import numpy as np
import pandas as pd
import sqlite3 as lite
#import bokeh
#from bokeh.plotting import figure
#from bokeh.io import show
#from bokeh.embed import components
#bv = bokeh.__version__
#from sampy.common import keyboard


# # app Flask & database connect
# -----------------------------------------------------|
app = Flask(__name__)
app.vars={}
feat = ['Warming','Drought']
conn = lite.connect('clim_zip_trunc')
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
	#keyboard(locals(),globals())
	
	# construct representatives html
	# --------------------------------------------|
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
	
	
	# Get zipcode descriptor stings
	# --------------------------------------------|
	medinc_str = 'Median Income: %i (%i percentile)' % (df.med_income[0],df.med_income_pct[0])
	popden_str = 'Population Density: %i (%i percentile)' % (df.density[0],df.density_pct[0])
	#keyboard(locals(),globals())
	
	# Get zipcode opinion stings
	# --------------------------------------------|
	happ_str = '%s%% Agree (%i percentile)' % (df.happening[0],df.happening_pct[0])
	happop_str = '%s%% Oppose (%i percentile)' % (df.happeningOppose[0],df.happeningOppose_pct[0])
	hum_str = '%s%% Agree (%i percentile)' % (df.human[0],df.human_pct[0])
	humop_str = '%s%% Oppose (%i percentile)' % (df.humanOppose[0],df.humanOppose_pct[0])
	cons_str = '%s%% Agree (%i percentile)' % (df.consensus[0],df.consensus_pct[0])
	consop_str = '%s%% Oppose (%i percentile)' % (df.consensusOppose[0],df.consensusOppose_pct[0])
	#keyboard(locals(),globals())
	
	
	if app.vars['select'][0]=='Warming':
		embed = '<iframe width="100%" height="520" frameborder="0" src="https://samuelgthorpe.cartodb.com/viz/8264153a-ba2d-11e5-b57e-0e31c9be1b51/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>'
		tmpr = df.rW_pct[0]
		crisk_str = 'Warming Risk Index: %s (%i percentile)' % (df.rW[0],tmpr)
	elif app.vars['select'][0]=='Drought':
		embed = '<iframe width="100%" height="520" frameborder="0" src="https://samuelgthorpe.cartodb.com/viz/30864d8c-ba2d-11e5-9db3-0ecfd53eb7d3/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>'
		tmpr = df.rD_pct[0]
		crisk_str = 'Drought Risk Index: %s (%i percentile)' % (df.rD[0],tmpr)
	
	rlab = ['Very Low','Low','Moderate','High','Very High']
	rlab_bnd = [0,5,35,65,95]
	rlab_clr = ["green","green","yellow","red","red"]
	rlab_str = []
	for k, q in enumerate(rlab_bnd):
		if tmpr >= q:
			#rlab_str = rlab[q]
			rlab_str = '<font color="%s" size="8"><b>%s</b></font>' % (rlab_clr[k],rlab[k])
	#keyboard(locals(),globals())


	return render_template('graph.html',zipcode=app.vars['zipcode'],
	                        ftag=app.vars['select'][0],div=embed,conhtml=conhtml,
	                        medinc_str=medinc_str,popden_str=popden_str,crisk_str=crisk_str,
	                        happ_str=happ_str,happop_str=happop_str,
	                        hum_str=hum_str,humop_str=humop_str,
	                        cons_str=cons_str,consop_str=consop_str,
	                        rlab=rlab_str)

	
#@app.errorhandler(500)
#def error_handler(e):
#	return render_template('error.html',ticker=app.vars['ticker'],year=app.vars['start_year'])
    
    
# # If main
# -----------------------------------------------------|
if __name__ == '__main__':
  app.run(port=33507,debug=False)
  
  
  
#                                    END ALL
# # ---------------------------------------------------------------------------|
    
