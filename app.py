# This is the page which you run to actually run the website, it is outside the website in the file structure, don't move it, it's meant to be outside it
# Additionally, don't add or remove anything from here

# Import create app fuction from  __init__.py
from website import create_app

# run create app function as main
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
