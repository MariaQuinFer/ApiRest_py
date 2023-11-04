from flask import Flask
from flask_cors import CORS, cross_origin
from config import Config


# Routes
from .routes import AuthenticateRoute, BookCarrouselRoutes, BooksByAuthorRoutes, BooksByGenreRoutes, BooksByEditorialRoutes, BooksByTitleRoutes, BooksRoutes, AuthorRoutes, EditorialsRoutes, GenresRoutes, UserRoutes, LendRoute

# Appication initializations
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

CORS(app, resources={r"/*": {"origins": "*"}})


def page_not_found(error):
    return ("<h1>The page you are trying to access does not exist...</h1>", 404)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Error
    app.register_error_handler(404, page_not_found)

    # Blueprints
    app.register_blueprint(AuthenticateRoute.main)
    app.register_blueprint(BooksRoutes.books)
    app.register_blueprint(BookCarrouselRoutes.carousel)
    app.register_blueprint(BooksByAuthorRoutes.books_by_author)
    app.register_blueprint(BooksByTitleRoutes.books_by_title)
    app.register_blueprint(BooksByGenreRoutes.books_by_genre)
    app.register_blueprint(BooksByEditorialRoutes.books_by_editorial)
    app.register_blueprint(AuthorRoutes.authors)
    app.register_blueprint(EditorialsRoutes.editorials)
    app.register_blueprint(GenresRoutes.genres)
    app.register_blueprint(UserRoutes.users)
    app.register_blueprint(LendRoute.lend)

    return app
