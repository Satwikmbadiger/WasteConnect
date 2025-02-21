# WasteConnect Frontend

Welcome to the WasteConnect frontend project! This application is designed to facilitate waste management and promote sustainable shopping habits.

## Project Structure

The frontend is built using React.js and follows a component-based architecture. Below is an overview of the key directories and files:

- **public/**: Contains static files such as the main HTML file and manifest.
  - **index.html**: The entry point for the web application.
  - **manifest.json**: Metadata for the web application.

- **src/**: Contains the source code for the React application.
  - **components/**: Contains reusable components for the application.
    - **Dashboard.js**: Displays user statistics and EcoPoints.
    - **PickupScheduler.js**: Allows users to schedule waste pickups.
    - **EcoPoints.js**: Displays the user's EcoPoints balance.
    - **Marketplace.js**: Enables users to browse and purchase eco-friendly products.
    - **Statistics.js**: Visualizes the user's environmental impact.
  - **contexts/**: Contains context providers for managing global state.
    - **AuthContext.js**: Provides authentication state and functions.
  - **services/**: Contains service files for API interactions.
    - **api.js**: Functions for making API calls to the backend.
    - **firebase.js**: Functions for interacting with Firebase services.
    - **stripe.js**: Functions for handling payments through Stripe.
  - **App.js**: The main component that sets up application routes and layout.
  - **index.js**: The entry point for the React application.
  - **styles/**: Contains CSS files for styling the application.
    - **main.css**: The main stylesheet for the application.

## Getting Started

To get started with the WasteConnect frontend, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd WasteConnect/frontend
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the application**:
   ```
   npm start
   ```

The application will be available at `http://localhost:3000`.

## Features

- Schedule waste pickups.
- Track recycling efforts.
- Purchase eco-friendly products.
- Earn EcoPoints for sustainable actions.
- View environmental impact statistics.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.