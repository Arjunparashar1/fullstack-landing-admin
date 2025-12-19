from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from models import db, Project, Client, Contact, Subscriber
from config import Config
import os
from pathlib import Path

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Create uploads directory if it doesn't exist
    upload_folder = Path(app.config['UPLOAD_FOLDER'])
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    # Create instance directory for database
    instance_folder = Path(app.instance_path)
    instance_folder.mkdir(parents=True, exist_ok=True)
    
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    # Landing page routes
    @app.route('/')
    def index():
        """Landing page"""
        projects = Project.query.order_by(Project.created_at.desc()).all()
        clients = Client.query.order_by(Client.created_at.desc()).all()
        return render_template('index.html', projects=projects, clients=clients)
    
    @app.route('/contact', methods=['POST'])
    def contact():
        """Handle contact form submission"""
        try:
            contact = Contact(
                full_name=request.form.get('full_name'),
                email=request.form.get('email'),
                mobile=request.form.get('mobile'),
                city=request.form.get('city')
            )
            db.session.add(contact)
            db.session.commit()
            flash('Thank you for contacting us! We will get back to you soon.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))
    
    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        """Handle newsletter subscription"""
        email = request.form.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        
        # Check if email already exists
        existing = Subscriber.query.filter_by(email=email).first()
        if existing:
            return jsonify({'success': False, 'message': 'Email already subscribed'}), 400
        
        try:
            subscriber = Subscriber(email=email)
            db.session.add(subscriber)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Successfully subscribed!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'An error occurred'}), 500
    
    # Admin routes
    @app.route('/admin')
    def admin_dashboard():
        """Admin dashboard"""
        projects_count = Project.query.count()
        clients_count = Client.query.count()
        contacts_count = Contact.query.count()
        subscribers_count = Subscriber.query.count()
        
        return render_template('admin/dashboard.html',
                             projects_count=projects_count,
                             clients_count=clients_count,
                             contacts_count=contacts_count,
                             subscribers_count=subscribers_count)
    
    # Project management routes
    @app.route('/admin/projects')
    def admin_projects():
        """List all projects"""
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('admin/projects.html', projects=projects)
    
    @app.route('/admin/projects/add', methods=['GET', 'POST'])
    def admin_add_project():
        """Add new project"""
        if request.method == 'POST':
            try:
                # Handle file upload
                image = None
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        # Add timestamp to avoid conflicts
                        from datetime import datetime
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        filepath = upload_folder / filename
                        file.save(filepath)
                        image = f'uploads/{filename}'
                
                project = Project(
                    name=request.form.get('name'),
                    description=request.form.get('description'),
                    image=image
                )
                db.session.add(project)
                db.session.commit()
                flash('Project added successfully!', 'success')
                return redirect(url_for('admin_projects'))
            except Exception as e:
                db.session.rollback()
                flash('Error adding project. Please try again.', 'error')
        
        return render_template('admin/add_project.html')
    
    @app.route('/admin/projects/<int:id>/edit', methods=['GET', 'POST'])
    def admin_edit_project(id):
        """Edit project"""
        project = Project.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                # Handle file upload
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename and allowed_file(file.filename):
                        # Delete old image if exists
                        if project.image:
                            old_path = Path(app.config['UPLOAD_FOLDER']) / project.image.replace('uploads/', '')
                            if old_path.exists():
                                old_path.unlink()
                        
                        filename = secure_filename(file.filename)
                        from datetime import datetime
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        filepath = upload_folder / filename
                        file.save(filepath)
                        project.image = f'uploads/{filename}'
                
                project.name = request.form.get('name')
                project.description = request.form.get('description')
                db.session.commit()
                flash('Project updated successfully!', 'success')
                return redirect(url_for('admin_projects'))
            except Exception as e:
                db.session.rollback()
                flash('Error updating project. Please try again.', 'error')
        
        return render_template('admin/edit_project.html', project=project)
    
    @app.route('/admin/projects/<int:id>/delete', methods=['POST'])
    def admin_delete_project(id):
        """Delete project"""
        project = Project.query.get_or_404(id)
        try:
            # Delete image file if exists
            if project.image:
                image_path = Path(app.config['UPLOAD_FOLDER']) / project.image.replace('uploads/', '')
                if image_path.exists():
                    image_path.unlink()
            
            db.session.delete(project)
            db.session.commit()
            flash('Project deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error deleting project. Please try again.', 'error')
        return redirect(url_for('admin_projects'))
    
    # Client management routes
    @app.route('/admin/clients')
    def admin_clients():
        """List all clients"""
        clients = Client.query.order_by(Client.created_at.desc()).all()
        return render_template('admin/clients.html', clients=clients)
    
    @app.route('/admin/clients/add', methods=['GET', 'POST'])
    def admin_add_client():
        """Add new client"""
        if request.method == 'POST':
            try:
                # Handle file upload
                image = None
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        from datetime import datetime
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        filepath = upload_folder / filename
                        file.save(filepath)
                        image = f'uploads/{filename}'
                
                client = Client(
                    name=request.form.get('name'),
                    description=request.form.get('description'),
                    designation=request.form.get('designation'),
                    image=image
                )
                db.session.add(client)
                db.session.commit()
                flash('Client added successfully!', 'success')
                return redirect(url_for('admin_clients'))
            except Exception as e:
                db.session.rollback()
                flash('Error adding client. Please try again.', 'error')
        
        return render_template('admin/add_client.html')
    
    @app.route('/admin/clients/<int:id>/edit', methods=['GET', 'POST'])
    def admin_edit_client(id):
        """Edit client"""
        client = Client.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                # Handle file upload
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename and allowed_file(file.filename):
                        # Delete old image if exists
                        if client.image:
                            old_path = Path(app.config['UPLOAD_FOLDER']) / client.image.replace('uploads/', '')
                            if old_path.exists():
                                old_path.unlink()
                        
                        filename = secure_filename(file.filename)
                        from datetime import datetime
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        filepath = upload_folder / filename
                        file.save(filepath)
                        client.image = f'uploads/{filename}'
                
                client.name = request.form.get('name')
                client.description = request.form.get('description')
                client.designation = request.form.get('designation')
                db.session.commit()
                flash('Client updated successfully!', 'success')
                return redirect(url_for('admin_clients'))
            except Exception as e:
                db.session.rollback()
                flash('Error updating client. Please try again.', 'error')
        
        return render_template('admin/edit_client.html', client=client)
    
    @app.route('/admin/clients/<int:id>/delete', methods=['POST'])
    def admin_delete_client(id):
        """Delete client"""
        client = Client.query.get_or_404(id)
        try:
            # Delete image file if exists
            if client.image:
                image_path = Path(app.config['UPLOAD_FOLDER']) / client.image.replace('uploads/', '')
                if image_path.exists():
                    image_path.unlink()
            
            db.session.delete(client)
            db.session.commit()
            flash('Client deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error deleting client. Please try again.', 'error')
        return redirect(url_for('admin_clients'))
    
    # Contact management routes
    @app.route('/admin/contacts')
    def admin_contacts():
        """List all contacts"""
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return render_template('admin/contacts.html', contacts=contacts)
    
    @app.route('/admin/contacts/<int:id>/delete', methods=['POST'])
    def admin_delete_contact(id):
        """Delete contact"""
        contact = Contact.query.get_or_404(id)
        try:
            db.session.delete(contact)
            db.session.commit()
            flash('Contact deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error deleting contact. Please try again.', 'error')
        return redirect(url_for('admin_contacts'))
    
    # Subscriber management routes
    @app.route('/admin/subscribers')
    def admin_subscribers():
        """List all subscribers"""
        subscribers = Subscriber.query.order_by(Subscriber.created_at.desc()).all()
        return render_template('admin/subscribers.html', subscribers=subscribers)
    
    @app.route('/admin/subscribers/<int:id>/delete', methods=['POST'])
    def admin_delete_subscriber(id):
        """Delete subscriber"""
        subscriber = Subscriber.query.get_or_404(id)
        try:
            db.session.delete(subscriber)
            db.session.commit()
            flash('Subscriber deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error deleting subscriber. Please try again.', 'error')
        return redirect(url_for('admin_subscribers'))
    
    # Initialize database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

