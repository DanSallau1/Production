from flask import Flask,render_template,request,redirect,url_for,flash,g,jsonify
from models.models import DBSession,User,Product,ProductItem, initialize
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager,login_user, logout_user,login_required,current_user
import logging
from hashlib import sha1
import time, os, json, base64, hmac, urllib
from controllers import HomeController,AboutController,AccountController,CheckoutController
from controllers import LookBookController,ProductController,TermsController,CollectionsController
import time

DEBUG  = True
PORT = 8080
HOST = '0.0.0.0'


#Set re-createtable to True to create tables. This is set excuted onnce.
re_createTable = False

app = Flask(__name__)

#To instanciate a session, flask use secret key to encryt cookies and session.
#Key the key secret please.
app.secret_key = 'Wamayyataqillahayajallahumakhraja!'

#Login_manager is used for user recognition on the website.
#It retain user autheticity between page request . It tells each page whether user is aiutheticated, anonymous, or admin as we are going to add later
login_manager = LoginManager()
login_manager.init_app(app)

#The login_view below is set to login. This tells Login_manager to send user back to login Page when
#he try to access a page that requires authentication
login_manager.login_view = 'login'

#Login_manager loader is called when creating user_login. It returns the user identitity to the login_manager.
@login_manager.user_loader
def load_user(userid):
    session = DBSession()
    return session.query(User).get(int(userid))


@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    i =  HomeController(request)
    return i.index()

@app.route('/accountsuccess',methods=['GET', 'POST'])
def accountsuccess():
    acct_suc = AccountController(request)
    acct_suc.accountsuccess()


@app.route('/about',methods=['GET', 'POST'])
def about():
    about = AbountController(request)
    return about.about()


@app.route('/checkout',methods=['GET', 'POST'])
def checkout():
    checkout = CheckoutController(request)
    return checkout.checkout()


@app.route('/collections',methods = ['GET','POST'])
def collections():
    coll = CollectionsController(request)
    return coll.collections()



@app.route('/contact',methods = ['GET','POST'])
def contact():
    contact = ContactController(request)
    return contact.contactus()


#Create Account view. The first if, If the request type is GET , return our form Else Post a form.
@app.route('/createaccount', methods = ['GET','POST'])
def createaccount():
    acct = AccountController(request)
    return acct.createaccount()


@app.route('/lookbook',methods = ['GET','POST'])
def lookbook():
    look = LookBookController(request)
    return look.lookbook()


@app.route('/product',methods=['GET', 'POST'])
def product():
    product = ProductController(request)
    return product.product()

@app.route('/terms',methods=['GET', 'POST'])
def terms():
    terms = TermsController(request)
    return terms.terms()

@app.route('/login', methods = ['GET','POST'])
def login():
    log = AccountController(request)
    return log.login()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You 've been logged out!", "success")
    return redirect(url_for('index'))

@app.route('/user/collections',methods=['GET','POST'])
@login_required
def user_collections(title=None):
    userCol =  AccountController(request)
    return userCol.collections()

@app.route('/user/editcollection',methods=['GET','POST'])
@login_required
def edit_collection():
    userCol =  AccountController(request)
    return userCol.editCollection()

@app.route('/user/add_collection',methods=['GET','POST'])
@login_required
def add_collection(username=None):
    add_coll = AccountController(request)
    return add_coll.add_collection()

@app.route('/get_collection/')
@login_required
def get_collection():

    product_id = urllib.quote_plus(request.args.get('product_id'))
    print product_id 
    session = DBSession()

    product = session.query(Product).filter(Product.id == product_id).first()

    session = DBSession()

    productItems = session.query(ProductItem).filter(ProductItem.product_id == product_id).all()

    #collectionData = ([product.serialize for product in productItems])

    return jsonify(productItems = [product.serialize for product in productItems])

@app.route('/sign_s3/')
@login_required
def sign_s3():
    AWS_ACCESS_KEY = 'AKIAJZ4CRYDAIKPX763Q'
    AWS_SECRET_KEY = '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'
    S3_BUCKET = 'cultureandbrancbucket'

    object_name = urllib.quote_plus(request.args.get('file_name'))
    mime_type = request.args.get('file_type')

    expires = int(time.time()+60*60*24)
    amz_headers = "x-amz-acl:public-read"
    print 'The line is' + object_name
    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY.encode(), string_to_sign.encode('utf8'), sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url,
    })
    return content



@app.route('/user/editaccount', methods=['GET','POST'])
@login_required
def editaccount():
    acct = AccountController(request)
    return acct.editaccount()


#The method before is called before each request(i.e GET,POST).
#It you want something to be executed before each request then add it below
@app.before_request
def before_request():
    """Connect to the database connection before each request. """
    logging.warning(request.form)
    #print 'db opene'
    #engine.connect()
    g.user = current_user

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format) 

#The method after is called after each request
@app.after_request
def after_request(response):
    """Close database connection after each request. """
    #engine.connect().close()
    return response

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

if __name__ == '__main__':
    initialize(re_createTable)
    try:
        User.create_user(
            title='Mr',
            fname = 'Musa',
            lname = 'Salihu',
            username = 'musa',
            email = 'musa@hotmail.com',
            password = 'password',
            address = 'Block 46A-3-4 Siri Ixora Jalan Pjs Seksen 29/11 Shah Alam Malaysia',
            state = 'Selangor',
            is_Admin = True
            )
    except:
        pass

    app.run(debug = DEBUG, host=HOST, port= PORT)
