# fullstack-landing-admin

A full-stack web application built with Flask featuring a responsive landing page and an admin panel to manage projects, clients, contact form submissions, and newsletter subscriptions.

## Features

- **Landing Page**: Beautiful, responsive landing page showcasing projects and clients
- **Admin Panel**: Complete admin interface to manage:
  - Projects (with image uploads)
  - Clients (with image uploads)
  - Contact form submissions
  - Newsletter subscribers
- **Database**: SQLite database with SQLAlchemy ORM
- **File Uploads**: Image upload functionality for projects and clients

## Tech Stack

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database
- **Jinja2**: Template engine
- **Bootstrap 5**: Frontend framework

## Project Structure

```
fullstack-landing-admin/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── instance/              # Database files (created automatically)
│   └── database.db
├── static/                # Static files
│   └── uploads/           # Uploaded images
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Landing page
    └── admin/             # Admin panel templates
        ├── base.html
        ├── dashboard.html
        ├── projects.html
        ├── add_project.html
        ├── edit_project.html
        ├── clients.html
        ├── add_client.html
        ├── edit_client.html
        ├── contacts.html
        └── subscribers.html
```

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Arjunparashar1/fullstack-landing-admin.git
   cd fullstack-landing-admin
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Landing page: http://localhost:5000
   - Admin panel: http://localhost:5000/admin

## Database Models

### Project
- `id`: Primary key
- `image`: Image file path
- `name`: Project name
- `description`: Project description
- `created_at`: Timestamp

### Client
- `id`: Primary key
- `image`: Image file path
- `name`: Client name
- `description`: Client testimonial/description
- `designation`: Client designation/role
- `created_at`: Timestamp

### Contact
- `id`: Primary key
- `full_name`: Full name
- `email`: Email address
- `mobile`: Mobile number
- `city`: City
- `created_at`: Timestamp

### Subscriber
- `id`: Primary key
- `email`: Email address (unique)
- `created_at`: Timestamp

## Usage

### Landing Page
- View projects and clients
- Submit contact form
- Subscribe to newsletter

### Admin Panel
- **Dashboard**: View statistics
- **Projects**: Add, edit, delete projects with image uploads
- **Clients**: Add, edit, delete clients with image uploads
- **Contacts**: View and delete contact submissions
- **Subscribers**: View and delete newsletter subscribers

## Configuration

The application uses a configuration file (`config.py`) with the following settings:
- Database URI (defaults to SQLite)
- Upload folder path
- Allowed file extensions
- Maximum file size

## Development

The application uses Flask's application factory pattern for better organization and testability.

## License

This project is open source and available for educational purposes.
