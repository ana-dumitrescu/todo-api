$readmeContent = @"
# Advanced Todo API

A production-ready RESTful API built with Flask, featuring authentication, testing, and Docker support.

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
[![Tests](https://github.com/ana-dumitrescu/todo-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ana-dumitrescu/todo-api/actions)
[![Coverage](https://img.shields.io/codecov/c/github/ana-dumitrescu/todo-api)](https://codecov.io/gh/ana-dumitrescu/todo-api)

## Features

- 🔐 JWT Authentication
- 📝 Todo CRUD Operations
- ✅ Input Validation
- 📊 Test Coverage >90%
- 🐳 Docker Support
- 🚀 CI/CD Pipeline
- 📚 Swagger Documentation

## Tech Stack

- **Backend**: Flask
- **Database**: SQLAlchemy with SQLite
- **Authentication**: JWT
- **Testing**: pytest
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Getting Started

### Local Development

1. Clone the repository:
\`\`\`bash
git clone https://github.com/ana-dumitrescu/todo-api.git
cd todo-api
\`\`\`

2. Create and activate virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\\venv\\Scripts\\activate   # Windows
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Set up environment variables:
\`\`\`bash
cp .env.example .env
# Edit .env with your settings
\`\`\`

5. Run the application:
\`\`\`bash
python run.py
\`\`\`

### Using Docker

1. Build and run with Docker Compose:
\`\`\`bash
docker-compose up --build
\`\`\`

## API Documentation

Access the Swagger documentation at: \`http://localhost:5000/api/docs\`

### Key Endpoints

#### Authentication
- \`POST /api/register\` - Register a new user
- \`POST /api/login\` - Login and receive JWT token

#### Todos
- \`GET /api/todos\` - Get all todos
- \`POST /api/todos\` - Create a new todo
- \`GET /api/todos/{id}\` - Get a specific todo
- \`PUT /api/todos/{id}\` - Update a todo
- \`DELETE /api/todos/{id}\` - Delete a todo

## Testing

Run tests with coverage:
\`\`\`bash
pytest --cov=app
\`\`\`

## Project Structure
\`\`\`
todo-api/
├── app/
│   ├── models/
│   │   ├── todo.py
│   │   └── user.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── todos.py
│   └── schemas/
│       ├── todo.py
│       └── user.py
├── tests/
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
\`\`\`

## Contributing

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Ana Dumitrescu - [GitHub](https://github.com/ana-dumitrescu)

Project Link: [https://github.com/ana-dumitrescu/todo-api](https://github.com/ana-dumitrescu/todo-api)
"@

$readmeContent | Out-File -FilePath "README.md" -Encoding utf8