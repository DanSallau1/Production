from flask import Flask,render_template,request
import AccountController
from forms import AccountForm

class CheckoutController(object):

	def __init__(self,request):
	    self.request = request

	def checkout(self):
	    """ To address user pop up login , we have to pass formLogin to each page """
	    formLogin = AccountForm.LoginForm(request.form)
	    if request.method == 'GET' :
	        return render_template('checkout.html',formLogin=formLogin)
	    if request.method == 'POST' :
	        if request.form.get('login', None)  == 'Login' :
	            return AccountController.authenticatePopUpLogin(formLogin,'checkout')
