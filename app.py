from config import config
from src import init_app

configuration = config["development"]
app = init_app(configuration)

# Starting the app(server)
if __name__ == "__main__":
    app.run(port=5000)  # debug = True --> modo desarrollo
