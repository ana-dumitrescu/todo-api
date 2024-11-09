from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register main blueprints
    from app.routes.auth import auth_bp
    from app.routes.todos import todos_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(todos_bp, url_prefix='/api')

    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Todo API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Create database tables
    with app.app_context():
        db.create_all()

    @app.route("/api/swagger.json")
    def specs():
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Todo API",
                "version": "1.0.0",
                "description": "A simple Todo API"
            },
            "paths": {
                "/api/register": {
                    "post": {
                        "tags": ["Authentication"],
                        "summary": "Register a new user",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "email": {"type": "string", "format": "email"},
                                            "password": {"type": "string", "minLength": 6}
                                        },
                                        "required": ["email", "password"]
                                    }
                                }
                            }
                        },
                        "responses": {
                            "201": {"description": "User registered successfully"},
                            "400": {"description": "Invalid input"},
                            "409": {"description": "Email already registered"}
                        }
                    }
                },
                "/api/login": {
                    "post": {
                        "tags": ["Authentication"],
                        "summary": "Login to get access token",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "email": {"type": "string", "format": "email"},
                                            "password": {"type": "string"}
                                        },
                                        "required": ["email", "password"]
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Login successful",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "access_token": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            },
                            "401": {"description": "Invalid credentials"}
                        }
                    }
                },
                "/api/todos": {
                    "get": {
                        "tags": ["Todos"],
                        "summary": "Get all todos for authenticated user",
                        "security": [{"Bearer": []}],
                        "responses": {
                            "200": {"description": "List of todos"},
                            "401": {"description": "Unauthorized"}
                        }
                    },
                    "post": {
                        "tags": ["Todos"],
                        "summary": "Create a new todo",
                        "security": [{"Bearer": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "title": {"type": "string"},
                                            "description": {"type": "string"},
                                            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                                            "completed": {"type": "boolean"}
                                        },
                                        "required": ["title"]
                                    }
                                }
                            }
                        },
                        "responses": {
                            "201": {"description": "Todo created"},
                            "401": {"description": "Unauthorized"}
                        }
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "Bearer": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }

    return app