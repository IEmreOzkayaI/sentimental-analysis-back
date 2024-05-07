from .controllers import home, predict, login, register, post, comment, like
from .auth import token_required

def register_routes(app):
    app.add_url_rule('/health', view_func=home, methods=['GET'])
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.add_url_rule('/register', view_func=register, methods=['POST'])
    
    app.add_url_rule('/predict', view_func=token_required(predict), methods=['POST'])
    app.add_url_rule('/post', view_func=token_required(post), methods=['POST'])
    app.add_url_rule('/comment', view_func=token_required(comment), methods=['POST'])
    app.add_url_rule('/like', view_func=token_required(like), methods=['POST'])
