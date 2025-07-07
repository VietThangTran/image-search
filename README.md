# Image Search API

A powerful and scalable image search service built with FastAPI and PostgreSQL, designed to help you manage and search through your image collection efficiently.

## 🚀 Features

- **Image Upload**: Easily upload and store images with metadata
- **Keyword Tagging**: Tag images with multiple keywords for better organization
- **Fast Search**: Quickly find images using keyword searches
- **RESTful API**: Clean and intuitive API endpoints for integration
- **Docker Support**: Easy deployment using Docker and Docker Compose
- **Scalable Architecture**: Built with scalability in mind

## 🛠️ Tech Stack

- **Backend**: Python 3.13 with FastAPI
- **Database**: PostgreSQL
- **Package Management**: UV (Python package installer and resolver)
- **Containerization**: Docker & Docker Compose
- **API Documentation**: Automatic OpenAPI (Swagger) documentation

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd image-search
   ```

2. Copy the example environment file and update it with your configuration:
   ```bash
   cp .env.example .env
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

The application will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🗄️ Database Schema

The application uses the following database schema:

### Images Table
- `image_id`: Unique identifier for each image (auto-incrementing)
- `image_path`: Path to the stored image
- `image_type`: MIME type of the image
- `status`: Current status of the image

### Keywords Table
- `keyword_id`: Unique identifier for each keyword (auto-incrementing)
- `keyword`: The keyword text (unique)

### Keywords of Images (Junction Table)
- `image_id`: Reference to the images table
- `keyword_id`: Reference to the keywords table

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using FastAPI and PostgreSQL
- Containerized with Docker for easy deployment
- Uses UV for fast and reliable Python package management