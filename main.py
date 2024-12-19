# main.py
import functions as fn
import yfinance as yf
from datetime import datetime, timedelta

def main():
    print("******Welcome to the Stock Analysis App******\n")

    while True:
        choice = input("Select an option:\n1. Register\n2. Login\n3. Exit\nEnter your choice: ")

        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            if fn.register_user(email, password):
                print("Registration successful! You can now log in.")
            else:
                print("Registration failed. Email already exists.")

        elif choice == '2':
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            if fn.authenticate_user(email, password):
                print("Login successful!")

                while True:
                    user_action = input("\nSelect an action:\n1. Retrieve Stock Data\n2. View Saved Data\n3. Logout\nEnter your choice: ")

                    if user_action == '1':
                        ticker = input("Enter the stock ticker (e.g., 1155.KL): ")
                        period = input("Enter the period (e.g., 1mo, 1y): ")
                        end_date = datetime.today()
                        start_date = end_date - timedelta(days=30 if period == '1mo' else 365)

                        data = fn.get_closing_prices(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                        if data is not None:
                            analysis = fn.analyze_closing_prices(data)
                            print("\nAnalysis Results:")
                            for key, value in analysis.items():
                                print(f"{key}: {value}")

                            save = input("Do you want to save this analysis? (y/n): ")
                            if save.lower() == 'y':
                                interaction = {
                                    'email': email,
                                    'ticker': ticker,
                                    **analysis
                                }
                                fn.save_to_csv(interaction, 'user_interactions.csv')
                                print("Analysis saved successfully.")

                    elif user_action == '2':
                        fn.read_from_csv('user_interactions.csv')

                    elif user_action == '3':
                        print("Logged out successfully.")
                        break

                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Login failed. Incorrect email or password.")

        elif choice == '3':
            print("Thank you for using the Stock Analysis App. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
