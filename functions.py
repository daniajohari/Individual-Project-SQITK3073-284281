import csv
import hashlib
import os
import yfinance as yf

def register_user(email, password):
    users_file = 'users.csv'
    users = {}

    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                users[row[0]] = row[1]

    if email in users:
        return False

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open(users_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password])

    return True

def authenticate_user(email, password):
    users_file = 'users.csv'

    if not os.path.exists(users_file):
        return False

    with open(users_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                return hashed_password == row[1]

    return False

def get_closing_prices(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data['Close']
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def analyze_closing_prices(data):
    # Ensure `data` is sorted by index
    data = data.sort_index()
    
    first_price = data.iloc[0]  # Get the first closing price
    last_price = data.iloc[-1]  # Get the last closing price
    avg_price = data.mean()  # Calculate the average closing price
    percentage_change = ((last_price - first_price) / first_price) * 100
    highest_price = data.max()
    lowest_price = data.min()

    return {
        'Average Price': round(avg_price, 2),
        'Percentage Change': round(percentage_change, 2),
        'Highest Price': round(highest_price, 2),
        'Lowest Price': round(lowest_price, 2)
    }


def save_to_csv(data, filename):
    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

def read_from_csv(filename):
    if not os.path.exists(filename):
        print("No saved data found.")
        return

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
