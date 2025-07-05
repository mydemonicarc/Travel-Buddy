from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Package, Booking, User, Contact
from forms import SignupForm, LoginForm
from db_setup import db


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eljks83lwp3ksi3j3s9s30k3l2j5h7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:blue19@localhost/travel_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============= Routes =============

@app.route('/')
def home():
    packages = Package.query.limit(3).all()
    return render_template('index.html', packages=packages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Here you would typically send the message via email or store it in a database
        new_message = Contact(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Thank you for your message! We will get back to you soon.')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('signup.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            flash(f'Welcome back, {user.username}!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/packages')
def packages():
    all_packages = Package.query.all()
    return render_template('packages.html', packages=all_packages)

@app.route('/packages/<int:id>')
def package_detail(id):
    package = Package.query.get_or_404(id)
    return render_template('package_detail.html', package=package)

@app.route('/packages/<int:id>/book', methods=['POST'])
@login_required
def book_package(id):
    package = Package.query.get_or_404(id)
    
    # Check if user already booked this package
    existing_booking = Booking.query.filter_by(user_id=current_user.id, package_id=id).first()
    if existing_booking:
        flash('You have already booked this package!')
        return redirect(url_for('package_detail', id=id))
    
    booking = Booking(user_id=current_user.id, package_id=id)
    db.session.add(booking)
    db.session.commit()
    
    flash('Package booked successfully!')
    return redirect(url_for('mybookings'))

@app.route('/mybookings')
@login_required
def mybookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    
    users = User.query.all()
    bookings = Booking.query.all()
    packages = Package.query.all()
    
    return render_template('admin.html', users=users, bookings=bookings, packages=packages)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_package():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        duration = request.form['duration']
        image_url = request.form['image_url']
        
        package = Package(
            title=title,
            description=description,
            price=price,
            duration=duration,
            image_url=image_url
        )
        db.session.add(package)
        db.session.commit()
        
        flash('Package added successfully!')
        return redirect(url_for('admin'))
    
    return render_template('add_package.html')

# def create_sample_data():
#     """Create sample users and packages for testing"""
    
#     # Create admin user
#     if not User.query.filter_by(username='admin').first():
#         admin = User(username='admin', email='admin@travel.com', is_admin=True)
#         admin.set_password('admin123')
#         db.session.add(admin)
    
#     # Create regular user
#     if not User.query.filter_by(username='john').first():
#         user = User(username='john', email='john@example.com')
#         user.set_password('password')
#         db.session.add(user)
    
#     # Create sample packages
#     if Package.query.count() == 0:
#         packages = [
#             Package(
#                 title='Tropical Paradise Getaway',
#                 description='Escape to pristine beaches and crystal-clear waters. Enjoy luxury resorts, water sports, and breathtaking sunsets in this tropical paradise.',
#                 price=1299.99,
#                 duration='7 days',
#                 image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'
#             ),
#             Package(
#                 title='Mountain Adventure Trek',
#                 description='Experience the thrill of mountain climbing and hiking through scenic trails. Perfect for adventure enthusiasts seeking adrenaline-pumping activities.',
#                 price=899.99,
#                 duration='5 days',
#                 image_url='https://dev-snowit.ams3.digitaloceanspaces.com/uploads/2023/06/30130308/trekking-montagna.jpg'
#             ),
#             Package(
#                 title='European City Tour',
#                 description='Explore the rich history and culture of European capitals. Visit iconic landmarks, museums, and enjoy local cuisine in this comprehensive tour.',
#                 price=2199.99,
#                 duration='14 days',
#                 image_url='https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800'
#             ),
#             Package(
#                 title='Safari Wildlife Experience',
#                 description='Witness magnificent wildlife in their natural habitat. Professional guides will take you on an unforgettable journey through national parks.',
#                 price=1799.99,
#                 duration='10 days',
#                 image_url='https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800'
#             ),
#             Package(
#                 title='Cultural Heritage of India',
#                 description='Immerse yourself in ancient cultures and traditions. Visit historical sites, temples, and experience local customs and festivals.',
#                 price=1599.99,
#                 duration='12 days',
#                 image_url='https://mysimplesojourn.com/wp-content/uploads/2023/06/UNESCO-India-1536x864.jpg'
#             ),
#             Package(
#                 title='Arctic Adventure Expedition',
#                 description='Explore the breathtaking Arctic wilderness. See northern lights, glaciers, and unique wildlife in this once-in-a-lifetime experience.',
#                 price=2999.99,
#                 duration='8 days',
#                 image_url='https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800'
#             )
#         ]
        
#         for package in packages:
#             db.session.add(package)
    
#     db.session.commit()

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
        # create_sample_data()
    app.run(debug=True)
