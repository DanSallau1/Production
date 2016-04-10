from flask import Flask,render_template,request
import AccountController
from forms import AccountForm

class HomeController(object):

	def __init__(self,request):
		self.request = request

	def index(self):
	    formLogin = AccountForm.LoginForm(request.form)
	    if request.method == 'GET' :
	    	return render_template('index.html',formLogin=formLogin)
	    if request.method == 'POST' :
	        if request.form.get('login', None)  == 'Login' :
	            return AccountController.authenticatePopUpLogin(formLogin,'index')	
