import os
from functools import wraps
from functools import wraps
import datetime
import g4f
import json5
from celery import Celery
from dotenv import load_dotenv
from flask import (Flask, Response, redirect, render_template, request,
                   session, url_for)
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from GeneratePPT import GeneratePPT
from ImageGetter import ImageGetter

load_dotenv()

MONGODB_URI           = os.environ.get('MONGODB_URI') 
UNSPLASH_ACCESS_TOKEN = os.environ.get('UNSPLASH_ACCESS_TOKEN') 

app = Flask(__name__)
app.secret_key = 'VeryVeryComify#@666'  

# Configure MongoDB
app.config['MONGO_URI'] = MONGODB_URI
mongo = PyMongo(app)
db = mongo.db 

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Redis broker URL
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Redis result backend

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



# API Code
api = Api(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip login for Localhost
        if "127.0.0.1" in request.url_root or "localhost" in request.url_root:
            return f(*args, **kwargs)
        
        if 'google_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def deduct_credit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user has limited credits and deduct 50 credits
        user_id = session.get('id')
        users_collection = db.users
        user_data = users_collection.find_one({"user_id": user_id})
            
        if user_data and user_data.get('credit') != "Unlimited":
            current_credit = int(user_data.get('credit'))
            if current_credit >= 50:
                new_credit = current_credit - 50
                users_collection.update_one({"user_id": user_id}, {"$set": {"credit": new_credit}})
            else:
                # Handle insufficient credit (optional)
                return {"error": "Insufficient credit"}
    
        return f(*args, **kwargs)
    return decorated_function

    

class Images(Resource):
    @login_required
    @deduct_credit
    def post(self):

        try:
            topic = request.form['topic']
            json_data = json5.loads(request.form['json_data'])
               
            img = ImageGetter(UNSPLASH_ACCESS_TOKEN) 
            image_list = img.get_image_paths(topic, json_data)
            return {'images': image_list}
        except Exception as e:
            return {"error": str(e)}
    
class Generate(Resource):
    @login_required
    @deduct_credit
    def post(self):
        try:
            data = request.get_json()
            topic = data.get('topic')
            json_data = json5.loads(data.get('json_data'))
            image_list_dict = data.get('image_paths')
            image_list = [img_dict['image_path'] for img_dict in image_list_dict] 

            output_path = f"static/{topic.lower().replace(' ', '_').replace('-', '_')}_presentation.pptx"
            design_template = "static/template.pptx"
            
            ppt = GeneratePPT(output_path, design_template)
            ppt_file_path = ppt.start(image_list, json_data)

            if os.path.exists(ppt_file_path):
                return {"download_link": output_path}
            else:
                return {"error": "PPT Generation Failed"}
        except Exception as e:
            return {"error": str(e)}

api.add_resource(Images, '/images')
api.add_resource(Generate, '/generate')

@app.route('/content')
@login_required
def content():
    topic = request.args.get('topic')
    slidecount = request.args.get('slidecount')
    
    current_prompt = f"I Want You to Write Content for a {slidecount} slides PPT on Topic: '{topic}', in this format with no placeholder: <div><li>Slide 1</li><li>[HEADING OF SLIDE 1]</li><li>[CONTENT OF SLIDE 1]</li></div><div><li>Slide 2</li><li>[HEADING OF SLIDE 2]</li><li>[CONTENT OF SLIDE 2]</li></div>"
    # response = g4f.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": current_prompt}], stream=True)
    response = g4f.ChatCompletion.create(model="airoboros-70b", messages=[{"role": "user", "content": current_prompt}], stream=True)
    
    def generate():
        for message in response:
            yield f"data: {message}\n\n"
            print(message, end="")
        yield f"data: Session Terminated\n\n"
    
    return Response(generate(), content_type='text/event-stream')

@app.route('/')
def login_page():
    if 'google_token' in session:
        # User is logged in, redirect to the dashboard
        return redirect('/dashboard')
    else:
        # User is not logged in, render the login page
        current_year = datetime.datetime.now().year
        return render_template('index.html', current_year=current_year)

@app.route('/dashboard')
@login_required
def index():
    user_full_name = session.get('user_full_name')
    user_id = session.get('id')  
    users_collection = db.users
    user_data = users_collection.find_one({"user_id": user_id})

    # If user_data exists, get credit and plan_type
    if user_data:
        credit = user_data.get('credit')
        plan_type = user_data.get('plan_type')
    elif "127.0.0.1" in request.url_root or "localhost" in request.url_root:
        user_full_name = "LocalUser"
        credit = "Unlimited"
        plan_type = "Freemium"
    else:
        return redirect("/logout")

    return render_template('dashboard.html', full_name=user_full_name, credit=credit, plan_type=plan_type)

@app.route('/slide')
@login_required
def slide():
    return render_template('slide.html')

@app.route('/login')
def login():
    if "127.0.0.1" in request.url_root or "localhost" in request.url_root:
        return redirect('/dashboard')
    return redirect('https://www.witeso.com/login?redirect=https://makeit.witeso.com')

@app.route('/logout')
def logout():
    if "127.0.0.1" in request.url_root or "localhost" in request.url_root:
        return redirect(request.url_root)
    return redirect("https://www.witeso.com/logout?redirect=https://makeit.witeso.com")

if __name__ == '__main__':
    app.run(debug=True)
