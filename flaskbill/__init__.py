# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy 
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager



# app = Flask(__name__)
# app.config['SECRET_KEY'] = '89962f947fc3314a8778ea268d8d8dc1'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

# app.app_context().push()


# from flaskbill import routes




from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.url_map.strict_slashes = False



app.config['SECRET_KEY'] = '89962f947fc3314a8778ea268d8d8dc1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Test_123@flaskdatabase.cqvo8lagofmc.ap-south-1.rds.amazonaws.com/db'




db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.app_context().push()


from flaskbill import routes