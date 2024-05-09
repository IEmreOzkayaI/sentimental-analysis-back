import jwt
import datetime
from flask import request, jsonify
from .models import User, db , Post ,Comment
from flask import current_app as app  # Assuming the Flask app is imported as 'app' in your models
from .services import predict_sentiment

def home():
    return "Hello, World!"

def predict():
    text = request.json['text']
    prediction = predict_sentiment(text)
    return jsonify({'prediction': prediction})

def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
        
        # Assuming password is stored in hashed form and User model has a method to check password
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Assuming you have a method to check hashed password
            # Create a token
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
            }, app.config['SECRET_KEY'], algorithm="HS256")  # Ensure you have a SECRET_KEY configured in your app's config

            return jsonify({'token': token ,"user":{ "name": user.name, "surname":user.surname, "id":user.id}}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Method not allowed'}), 405
    
def register():
    if request.method == 'POST':
        data = request.get_json()  # JSON verisini al
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        
        if not email or not password or not name or not surname:
            return jsonify({'message': 'All fields are required'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 409

        new_user = User(email=email, password=password, name=name, surname=surname)
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except:
            db.session.rollback()
            return jsonify({'message': 'Registration failed'}), 500
    return jsonify({'message': 'Method not allowed'}), 405

def post():
    if request.method == 'POST':
        user = request.current_user  # token_required tarafından sağlanan kullanıcı bilgisini al
        data = request.get_json()  # JSON verisini al
        title= data.get('title')
        content = data.get('content')        
        date  =  datetime.datetime.now().strftime("%I:%M %p - %d/%m/%Y")
        sentiment = predict_sentiment(content)
                
        new_post = Post(title=title, content=content, user=user, date=date, sentiment=sentiment)
        db.session.add(new_post)
        try:
            db.session.commit()
            return jsonify({'message': 'Post created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            print(e)  # Log or print the exception
            return jsonify({'message': 'Post creation failed'}), 500
    if request.method == 'GET':
        post_id = request.args.get('id')  
        
    if post_id:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            return jsonify({
                'title': post.title,
                'content': post.content,
                'name': post.user.name,
                'surname': post.user.surname,
                'email': post.user.email,
                'date': post.date,
                'sentiment': post.sentiment,
                'user_id': post.user.id,
                'id': post.id,
                'comments': [{
                    'content': comment.content,
                    'name': comment.user.name,
                    'surname': comment.user.surname,
                    'email': comment.user.email,
                    'date': comment.date,
                    'sentiment': comment.sentiment,
                    'user_id': comment.user.id,
                    'id': comment.id
                } for comment in post.comments
                ]
            }), 200
        else:
            return jsonify({'message': 'Post not found'}), 404
    else:
        posts = Post.query.order_by(Post.date.desc()).all()
        return jsonify([{
            'title': post.title,
            'content': post.content,
            'name': post.user.name,
            'surname': post.user.surname,
            'email': post.user.email,
            'date': post.date,
            'sentiment': post.sentiment,
            'user_id': post.user.id,
            'id':post.id
        } for post in posts])
        
    return jsonify({'message': 'Method not allowed'}), 405

def comment():
    if request.method == 'POST':
        user = request.current_user
        data = request.get_json()
        content = data.get('comment')
        post_id = data.get('postId')
        date = datetime.datetime.now().strftime("%I:%M %p - %d/%m/%Y")
        sentiment = predict_sentiment(content)
        
        new_comment = Comment(content=content, user=user, post_id=post_id, date=date, sentiment=sentiment)
        
        db.session.add(new_comment)
        try:
            db.session.commit()
            return jsonify({'message': 'Comment created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({'message': 'Comment creation failed'}), 500
    return jsonify({'message': 'Method not allowed'}), 405

