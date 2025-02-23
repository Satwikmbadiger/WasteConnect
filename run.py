from wastePickup import create_app

app = create_app()
@app.route("/")
def index(): 
    return "<h1>Homepage for Website<h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    
