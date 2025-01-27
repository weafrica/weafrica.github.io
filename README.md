# WeAfrica Web Application

Welcome to the WeAfrica web application! This project is designed to provide users with a comprehensive platform offering news, games, recreational activities, and online shopping. The application is built using Flask, a lightweight web framework for Python.

## Features

- **User Authentication**: Users can register, log in, and manage their accounts.
- **News Management**: Users can view and add news articles.
- **Online Shop**: Browse and shop for various items.
- **Data Analyzer**: Access and analyze data.
- **Games and Recreational Activities**: Enjoy various games and activities.
- **Blogs**: Read and write blogs.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/saulesto/project.git
    cd weafrica
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database**:
    ```bash
    flask init-db
    ```

5. **Run the application**:
    ```bash
    flask run
    ```

## Usage

- **Home Page**: Navigate to the home page to see an overview of the platform.
- **User Authentication**: Register or log in to access personalized features.
- **News Management**: View the latest news articles or add your own.
- **Online Shop**: Browse and purchase items from the online shop.
- **Data Analyzer**: Access and analyze various datasets.
- **Games and Recreational Activities**: Enjoy a variety of games and activities.
- **Blogs**: Read and write blogs on various topics.

## Project Structure

## Routes

- **Home**: `/`
- **News**: `/news/news_list`, `/news/news_detail/<int:news_id>`
- **Shop**: `/shop/shop_list`
- **Data Analyzer**: `/data_analyzer/data_analyzer_list`
- **Games**: `/game/game_list`
- **Recreational Activities**: `/recreational_activities/recreational_activities_list`
- **Blogs**: `/blogs/blogs_list`
- **Search**: `/search`

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m "Add some feature"
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
6. **Create a new Pull Request**.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Flask: [Flask Documentation](https://flask.palletsprojects.com/)
- Bootstrap: [Bootstrap Documentation](https://getbootstrap.com/)
- Font Awesome: [Font Awesome Icons](https://fontawesome.com/)

---

Thank you for using WeAfrica! If you have any questions or feedback, please feel free to reach out.