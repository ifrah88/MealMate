import sqlite3
import hashlib
import PySimpleGUI as sg

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_to_db(self):
        conn = sqlite3.connect('mealmate.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
        conn.commit()
        conn.close()

def create_db():
    conn = sqlite3.connect('mealmate.db')
    c = conn.cursor()

    # Drop existing tables if they exist
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS restaurants')
    c.execute('DROP TABLE IF EXISTS meals')
    c.execute('DROP TABLE IF EXISTS deals')
    c.execute('DROP TABLE IF EXISTS reviews')

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY ,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        dietary_restrictions TEXT,
        budget INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY ,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        cuisine TEXT NOT NULL,
        price_range INTEGER NOT NULL,
        seats_available INTEGER NOT NULL DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY ,
        restaurant_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY ,
        restaurant_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        discount INTEGER NOT NULL,
        is_group INTEGER NOT NULL,
        meal_id INTEGER,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
        FOREIGN KEY (meal_id) REFERENCES meals (id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY ,
        restaurant_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect('mealmate.db')
    c = conn.cursor()

    # Insert sample restaurants
    c.execute('INSERT INTO restaurants (name, location, cuisine, price_range, seats_available) VALUES (?, ?, ?, ?, ?)',
              ("Pizza Palace", "123 Main St", "Italian", 20, 30))
    c.execute('INSERT INTO restaurants (name, location, cuisine, price_range, seats_available) VALUES (?, ?, ?, ?, ?)',
              ("Burger Barn", "456 Elm St", "American", 15, 25))
    c.execute('INSERT INTO restaurants (name, location, cuisine, price_range, seats_available) VALUES (?, ?, ?, ?, ?)',
              ("Sushi Central", "789 Oak St", "Japanese", 25, 20))
    c.execute('INSERT INTO restaurants (name, location, cuisine, price_range, seats_available) VALUES (?, ?, ?, ?, ?)',
              ("Taco Town", "321 Pine St", "Mexican", 10, 15))
    c.execute('INSERT INTO restaurants (name, location, cuisine, price_range, seats_available) VALUES (?, ?, ?, ?, ?)',
              ("Curry House", "654 Maple St", "Indian", 30, 10))
    c.execute('INSERT INTO restaurants (name, location, cuisine, price_range, seats_available) VALUES (?, ?, ?, ?, ?)',
              ("Vegan Delight", "987 Cedar St", "Vegan", 20, 5))
    
    # Insert sample meals for the restaurants
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (1, "Pepperoni Pizza", 12))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (1, "Cheese Pizza", 10))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (2, "Cheeseburger", 8))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (2, "Veggie Burger", 9))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (3, "California Roll", 12))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (3, "Spicy Tuna Roll", 14))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (4, "Chicken Taco", 5))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (4, "Beef Taco", 6))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (5, "Butter Chicken", 18))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (5, "Paneer Tikka", 16))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (6, "Vegan Burger", 15))
    c.execute('INSERT INTO meals (restaurant_id, name, price) VALUES (?, ?, ?)',
              (6, "Quinoa Salad", 12))
    
    # Insert sample deals
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (1, "20% off on all pizzas", 20, 1, 1))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (2, "10% off on all burgers", 10, 0, 3))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (1, "15% off on cheese pizza", 15, 0, 2))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (2, "25% off on veggie burgers", 25, 1, 4))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (3, "20% off on California Roll", 20, 0, 5))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (4, "15% off on all tacos", 15, 1, None))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (5, "10% off on Butter Chicken", 10, 0, 9))
    c.execute('INSERT INTO deals (restaurant_id, description, discount, is_group, meal_id) VALUES (?, ?, ?, ?, ?)',
              (6, "20% off on Quinoa Salad", 20, 1, 12))

    conn.commit()
    conn.close()

def register():
    layout = [
        [sg.Text('Username:'), sg.Input(key='username')],
        [sg.Text('Password (min 5 characters):'), sg.Input(key='password', password_char='*')],
        [sg.Text('', size=(30,1), key='password_warning', text_color='red')],
        [sg.Button('Register'), sg.Button('Back')]
    ]
    window = sg.Window('Register', layout)
    user_registered = False
    while True:
        event, values = window.read()
        if event == 'Register':
            username = values['username']
            password = values['password']
            
            if len(password) < 5:
                window['password_warning'].update('Password must be at least 5 characters')
                continue
            
            user = User(username, password)
            try:
                user.save_to_db()
                sg.popup('Registration Successful!')
                user_registered = True
            except sqlite3.IntegrityError:
                sg.popup('Username already exists!')
            break
        elif event == 'Back' or event == sg.WIN_CLOSED:
            break
    window.close()
    return user_registered

def login():
    layout = [
        [sg.Text('Username:'), sg.Input(key='username')],
        [sg.Text('Password:'), sg.Input(key='password', password_char='*')],
        [sg.Button('Login'), sg.Button('Back')]
    ]
    window = sg.Window('Login', layout)
    user_id = None
    while True:
        event, values = window.read()
        if event == 'Login':
            username = values['username']
            password = hashlib.sha256(values['password'].encode()).hexdigest()
            conn = sqlite3.connect('mealmate.db')
            c  = conn.cursor()
            c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            result = c.fetchone()
            conn.close()
            if result:
                sg.popup('Login Successful!')
                user_id = result[0]  # Return the user_id
                break
            else:
                sg.popup('Invalid Username or Password!')
        elif event == 'Back' or event == sg.WIN_CLOSED:
            break
    window.close()
    return user_id

def ask_single_or_group(user_id, user_details):
    layout = [
        [sg.Text('Are you single or in a group?')],
        [sg.Radio('Single', 'GROUP', key='single'), sg.Radio('Group', 'GROUP', key='group')],
        [sg.Text('Budget:'), sg.Input(key='budget')],
        [sg.Button('Submit')]
    ]
    window = sg.Window('Single or Group', layout)
    is_group = False
    while True:
        event, values = window.read()
        if event == 'Submit':
            is_single = values['single']
            is_group = values['group']
            budget = int(values['budget'])
            conn = sqlite3.connect('mealmate.db')
            c = conn.cursor()
            c.execute('UPDATE users SET budget=? WHERE id=?', (budget, user_id))
            conn.commit()
            conn.close()
            user_details['is_group'] = is_group
            user_details['budget'] = budget
            sg.popup('Budget Updated!', 'You are logged in as', 'Single' if is_single else 'Group')
            break
    window.close()
    return is_group

def location_and_display_restaurants(user_id, is_group, user_details):
    conn = sqlite3.connect('mealmate.db')
    c = conn.cursor()
    
    # Get user's budget
    c.execute('SELECT budget FROM users WHERE id=?', (user_id,))
    budget = c.fetchone()[0]
    
    # Ask for location
    c.execute('SELECT DISTINCT location FROM restaurants')
    locations = [row[0] for row in c.fetchall()]
    
    layout = [
        [sg.Text('Select your location:')],
        [sg.Listbox(locations, size=(30, 6), key='location')],
        [sg.Button('Submit')]
    ]
    window = sg.Window('Select Location', layout)
    location = None
    while True:
        event, values = window.read()
        if event == 'Submit':
            location = values['location'][0]
            break
    window.close()
    
    user_details['location'] = location
    
    # Retrieve restaurants with meals, deals, and seat availability based on location and budget
    c.execute('''
        SELECT r.id, r.name, r.seats_available, m.name AS meal_name, m.price AS meal_price, d.description AS deal_description, d.discount AS deal_discount
        FROM restaurants r
        LEFT JOIN meals m ON r.id = m.restaurant_id
        LEFT JOIN deals d ON r.id = d.restaurant_id
        WHERE r.location=? AND r.price_range<=? AND (d.is_group=? OR d.is_group IS NULL)
    ''', (location, budget, int(is_group)))
    restaurant_info = c.fetchall()
    
    if not restaurant_info:
        sg.popup('No restaurants found for your budget and location.')
        conn.close()
        return
    
    # Display restaurants, meals, deals, and seat availability
    layout = [
        [sg.Text('Available Restaurants, Meals, Deals, and Seat Availability:')]
    ]
    current_restaurant_id = None
    for restaurant_row in restaurant_info:
        restaurant_id, restaurant_name, seats_available, meal_name, meal_price, deal_description, deal_discount = restaurant_row
        if restaurant_id != current_restaurant_id:
            current_restaurant_id = restaurant_id
            layout.append([sg.Text(f"Restaurant ID: {restaurant_id}, Name: {restaurant_name}, Seats Available: {seats_available}")])
        if meal_name:
            layout.append([sg.Text(f"    Meal: {meal_name}, Price: ${meal_price}")])
        if deal_description and (is_group or not deal_description):
            layout.append([sg.Text(f"    Deal: {deal_description}, Discount: {deal_discount}%")])
        layout.append([sg.Button(f'Review {meal_name}', key=f'review_{meal_name}_{restaurant_id}')])
        layout.append([sg.Button(f'Book Seat at {restaurant_name}', key=f'book_{restaurant_id}')])
    
    layout.append([sg.Button('Back')])
    
    window = sg.Window('Available Restaurants, Meals, Deals, and Seat Availability', layout)
    while True:
        event, values = window.read()
        if event == 'Back' or event == sg.WIN_CLOSED:
            break
        elif event.startswith('review'):
            meal_name = event.split('_')[1]
            restaurant_id = int(event.split('_')[2])
            user_details['reviews'] = user_details.get('reviews', [])
            user_details['reviews'].append(write_review(user_id, restaurant_id, meal_name))
        elif event.startswith('book'):
            restaurant_id = int(event.split('_')[1])
            book_seat(user_id, restaurant_id)
            sg.popup(f'Seat booked at Restaurant ID: {restaurant_id}')
            # Update seats_available in UI (not implemented here)
    window.close()
    
    conn.close()

def write_review(user_id, restaurant_id, meal_name):
    layout = [
        [sg.Text(f'Review for {meal_name} at Restaurant ID: {restaurant_id}')],
        [sg.Text('Rating (1-5):'), sg.Input(key='rating', size=(10, 1))],
        [sg.Text('Comment:'), sg.Input(key='comment')],
        [sg.Button('Submit')]
    ]
    window = sg.Window('Write Review', layout)
    review_details = {}
    while True:
        event, values = window.read()
        if event == 'Submit':
            try:
                rating = int(values['rating'])
                comment = values['comment']
                conn = sqlite3.connect('mealmate.db')
                c = conn.cursor()
                c.execute('INSERT INTO reviews (restaurant_id, user_id, rating, comment) VALUES (?, ?, ?, ?)',
                          (restaurant_id, user_id, rating, comment))
                conn.commit()
                conn.close()
                sg.popup('Review submitted successfully!')
                review_details = {
                    'restaurant_id': restaurant_id,
                    'meal_name': meal_name,
                    'rating': rating,
                    'comment': comment
                }
                break
            except ValueError:
                sg.popup('Please enter a valid rating (1-5).')
    window.close()
    return review_details

def book_seat(user_id, restaurant_id):
    conn = sqlite3.connect('mealmate.db')
    c = conn.cursor()
    c.execute('UPDATE restaurants SET seats_available = seats_available - 1 WHERE id = ?', (restaurant_id,))
    conn.commit()
    conn.close()

def display_user_details(user_details):
    layout = [[sg.Text('Collected User Details:')]]
    
    for key, value in user_details.items():
        if key == 'reviews':
            layout.append([sg.Text(f'{key}:')])
            for review in value:
                layout.append([sg.Text(f'  Restaurant ID: {review["restaurant_id"]}, Meal: {review["meal_name"]}, Rating: {review["rating"]}, Comment: {review["comment"]}')])
        else:
            layout.append([sg.Text(f'{key}: {value}')])
    
    layout.append([sg.Button('Close')])
    window = sg.Window('User Details', layout)
    
    while True:
        event, values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSED:
            break
    
    window.close()

def main_menu(user_id, is_group, user_details):
    while True:
        layout = [
            [sg.Button('View Restaurants'), sg.Button('User Details'), sg.Button('Logout')]
        ]
        window = sg.Window('MealMate - Main Menu', layout)
        event, values = window.read()
        if event == 'View Restaurants':
            location_and_display_restaurants(user_id, is_group, user_details)
        elif event == 'User Details':
            display_user_details(user_details)
        elif event == 'Logout' or event == sg.WIN_CLOSED:
            break
    window.close()

def main():
    create_db()
    insert_sample_data()  # Insert sample data into the database
    user_details = {}
    while True:
        layout = [
            [sg.Button('Register'), sg.Button('Login'), sg.Button('Exit')]
        ]
        window = sg.Window('MealMate', layout)
        event, values = window.read()
        if event == 'Register':
            if register():
                sg.popup('Please log in with your new credentials.')
        elif event == 'Login':
            user_id = login()
            if user_id:
                sg.popup('Welcome to MealMate!')
                user_details['user_id'] = user_id
                is_group = ask_single_or_group(user_id, user_details)
                user_details['is_group'] = is_group
                main_menu(user_id, is_group, user_details)  # Go to main menu after successful login
        elif event == 'Exit' or event == sg.WIN_CLOSED:
            break
        window.close()

if __name__ == '__main__':
    main()

