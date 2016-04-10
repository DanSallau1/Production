from flask import Flask,render_template,request,redirect,url_for,flash,g
from models.models import Base,User,Product,ProductItem,InsertRow,DBSession
from sqlalchemy import exists, func
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager,login_user, logout_user,login_required,current_user
from forms import AccountForm
import json 
from flask.ext.bcrypt import generate_password_hash


#authenticate user
def authenticate(form):
    if form.validate_on_submit():
        try:
            session = DBSession()
            user = session.query(User).filter(User.email == formLogin.email.data).first()
        except :# models.DoesNotExist:
            flash("Your email or password does not match !", "error")
        else :
            if user is not None:
                if check_password_hash(user.password,form.password.data):
                    login_user(user, remember = form.remember.data)
                    flash("You've been logged in", "success")
                    return render_template('index')
            else :
                flash("Your email or password does not match !", "error")
                return render_template('login.html',formLogin = form)
    return render_template('login.html',formLogin = form)

#authenticate pop up login
def authenticatePopUpLogin(formLogin,route):
    if formLogin.validate_on_submit():
        try:
            session = DBSession()
            user = session.query(User).filter(User.email == formLogin.email.data).first()
        except :# models.DoesNotExist:
            flash("Your email or password does not match !", "error")
            return render_template('login.html',form=formLogin,formLogin = formLogin)
        else :
            if user is not None:
                if check_password_hash(user.password,formLogin.password.data):
                    login_user(user, remember = formLogin.remember.data)
                    flash("You've been logged in", "success")
                    return redirect(url_for(route))
            else :
                flash("Your email or password does not match !", "error")
                return render_template('login.html',form=formLogin,formLogin = formLogin)

    return render_template('login.html',form=formLogin,formLogin = formLogin)

#Create Account
def createUser(form, formLogin):
    if form.validate_on_submit():
        flash("yay, you registered!", "success")
        User.create_user(
            title = None,
            fname = None,
            lname = None,
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            address = None,
            state = None,
            is_Admin = False
            )
        return render_template('accountsuccess.html', email=request.form['email'],formLogin=formLogin)
    return render_template('createaccount.html', form=form,formLogin=formLogin)

def editUser(form):
    if  form.validate_on_submit():
        session = DBSession()
        user = session.query(User).filter(User.id == current_user.id).update({
            'title' : form.title.data,
            'fname' : form.fname.data,
            'lname' : form.lname.data,
            'username' : form.username.data,
            'email' : form.email.data,
            'password' : generate_password_hash(form.newpassword.data),
            'address' : form.address.data,
            'state' : form.state.data,
            'is_Admin' : False

            })
        if user is not None :
            session.commit()
            return redirect(url_for('editaccount'))
    return render_template('editaccount.html',form= form)

class AccountController(object):

    def __init__(self,request):
        self.request = request

    def createaccount(self):
        form = AccountForm.RegisterForm()
        formLogin = AccountForm.LoginForm(request.form)

        if request.method =='GET':
            if g.user.is_authenticated == False:
                return render_template('createaccount.html',form=form,formLogin=formLogin)
            else:
                return redirect(url_for('index'))
        elif request.method =='POST':
            if request.form.get('login', None)  == 'Login' :
                return authenticatePopUpLogin(formLogin,'index')
            return createUser(form, formLogin)

    def editaccount(self):
        user = current_user
        form = AccountForm.EditAccountForm(request.form,user)
        if(request.method == 'GET'):
            return render_template('editaccount.html',form=form)
        elif (request.method == 'POST'):
            return editUser(form)
        return render_template('editaccount.html',form = form)

    def add_collection(self):
        form = AccountForm.LoginForm(request.form)
        if self.request.method == 'GET' :
            return render_template('add_collection.html',user=current_user,formLogin = form)
        elif self.request.method == 'POST' :
            parsed_json = json.loads(self.request.data)

            print current_user

            product_id = None
            for data in parsed_json :
                print "the data is %s" % data
                if ('collection_title' in data):
                    produc = Product(
                        title =  data['collection_title'],
                        description =  data['collection_description'],
                        user_id = g.user.id
                    )

                    product_id =InsertRow(produc)

                elif(product_id is not None):
                    prodItem = ProductItem(
                        image_url = data['image_url'],
                        image_description = data['image_description'],
                        product_id = product_id
                        )
                    Item_id =InsertRow(prodItem)

            return self.request.data


    def collections(self):
        print 'The userid is %d' % g.user.id
        session = DBSession()
        #products = session.query(Product).filter(Product.user_id == g.user.id).all()
        products = session.query(User) \
                           .join(User.products) \
                           .join(Product.productitems) \
                           .group_by(Product.id,Product.created_date,Product.title) \
                           .order_by(Product.created_date)                           \
                           .values( Product.id.label('product_id'),                           
                                    Product.title.label('title'),   
                                    Product.created_date.label('created_date'), 
                                    (func.row_number().over(order_by='products.created_date').label('number')),
                                    (func.count(ProductItem.id)).label('total'))  

        if products is not None:
            if(self.request.method =='GET'):
                return render_template('user_collections.html',products=products)
        return render_template('user_collections.html',products=products)

    def editCollection(self):
        
        product_id = self.request.args.get('product_id')

        session = DBSession()

        product = session.query(Product).filter(Product.id == product_id).first()
        print 'the new w wwwwww   is %s' %product_id
        session = DBSession()

        productItem = session.query(ProductItem).filter(ProductItem.product_id == product_id).all()


        if(product is not None):
            if(self.request.method == 'GET'):
                print 'it comes here'
                return render_template('editCollection.html',product=product, productItem = productItem)
            elif (self.request.method == 'POST') :
                print 'Its post'
                jsonData = json.loads(self.request.data)
                newProduct = None
                for data in jsonData :

                    if ('collection_title' in data):
                        session = DBSession()
                        newProduct = session.query(Product).filter(Product.id == product_id).update({
                                    'title' :  data['collection_title'],
                                    'description' : data['collection_description']
                                }
                            )
                        session.commit()
                        if (newProduct is not None):
                            print 'Its deleting '
                            print productItem
                            session = DBSession()
                            session.query(ProductItem).filter(ProductItem.product_id == product_id).delete()
                            session.commit()

                    elif(newProduct is not None):
                        prodItem = ProductItem(
                            image_url = data['image_url'],
                            image_description = data['image_description'],
                            product_id = product_id
                            )
                        Item_id =InsertRow(prodItem)

                return json.dumps({'success': True})        

        return render_template('editCollection.html',product=product)        



    def accountsuccess(self):
        """ To address user pop up login , we have to pass formLogin to each page """
        formLogin = AccountForm.LoginForm
        if self.request.method == 'GET' :
            return render_template('accountsuccess.html',formLogin=formLogin)
        if self.request.method == 'POST' :
            if request.form.get('login', None)  == 'Login' :
                return authenticatePopUpLogin(formLogin,'index')

    def login(self):
        form = AccountForm.LoginForm(request.form)
        print request.form
        if request.method == 'GET' :
            # Check if user is already logged in, return login page if not, otherwise index
            if g.user.is_authenticated == False:
                return render_template('login.html', form=form,formLogin=form)
            elif g.user.is_authenticated:
                return redirect(url_for('index'))
        elif (request.method == 'POST') :
            if request.form.get('login', None)  == 'Login' :
                return authenticatePopUpLogin(form,'login')
            else :
                return authenticate(form)
