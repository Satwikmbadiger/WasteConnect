# WasteConnect

WasteConnect is a web-based waste management and sustainable shopping platform designed to promote environmentally conscious habits. The application allows users to schedule waste pickups, track their recycling efforts, and purchase eco-friendly products from a marketplace. Users can earn rewards, known as EcoPoints, for engaging in sustainable actions such as recycling and making purchases.

## Features

- **Waste Pickup Scheduling**: Users can easily schedule waste pickups at their convenience.
- **Recycling Tracking**: Track recycling efforts and view statistics on environmental impact.
- **Eco-Friendly Marketplace**: Browse and purchase a variety of eco-friendly products.
- **EcoPoints Rewards**: Earn EcoPoints for sustainable actions, which can be redeemed for rewards.
- **User Dashboard**: A user-friendly dashboard to manage pickups, view EcoPoints, and access the marketplace.

## Tech Stack

- **Backend**: Flask
- **Frontend**: React.js
- **Authentication**: Firebase
- **Payments**: Stripe

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the backend directory and install dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Set up Firebase and Stripe configurations in `config.py`.
4. Run the backend server:
   ```
   python wsgi.py
   ```
5. Navigate to the frontend directory and install dependencies:
   ```
   cd frontend
   npm install
   ```
6. Start the frontend application:
   ```
   npm start
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.