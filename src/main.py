import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.models.deliverable import Deliverable
from src.models.business_process import BusinessProcess
from src.models.ai_technology import AITechnology
from src.models.software_tool import SoftwareTool
from src.models.research_item import ResearchItem
from src.models.integration import Integration
from src.routes.user import user_bp
from src.routes.deliverables import deliverables_bp
from src.routes.business_processes import business_processes_bp
from src.routes.ai_technologies import ai_technologies_bp
from src.routes.software_tools import software_tools_bp
from src.routes.research_items import research_items_bp
from src.routes.advanced_features import advanced_features_bp
from src.routes.integrations import integrations_bp
from src.routes.auth import auth_bp
from flask_cors import CORS

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'HL_Stearns_Capstone_2025_Secure_Key_#$%'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(deliverables_bp)
app.register_blueprint(business_processes_bp)
app.register_blueprint(ai_technologies_bp)
app.register_blueprint(software_tools_bp)
app.register_blueprint(research_items_bp)
app.register_blueprint(integrations_bp)
app.register_blueprint(advanced_features_bp)
app.register_blueprint(auth_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
