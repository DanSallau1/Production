from flask import Flask,render_template,request
from forms import AccountForm

class AboutController(object):

	def __init__(self,request):
	    self.request = request
		
	def about(self):	
	    """ To address user pop up login , we have to pass formLogin to each page """
	    formLogin = AccountForm.LoginForm(request.form)
	    if request.method == 'GET' :
	        return render_template('about.html',formLogin=formLogin)
	    if request.method == 'POST' :
	        if request.form.get('login', None)  == 'Login' :
	            return AccountController.authenticatePopUpLogin(formLogin,'about')
