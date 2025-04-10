#This is the page which you run to actually run the website, it is outside the website in the file structure, don't move it, it's meant to be outside it
#Additionally, don't add or remove anything from here
#create_app is from __init__
from website import create_app
#running the app
if __name__=="__main__":
    app=create_app()
    app.run(debug=True)