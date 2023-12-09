from app import app

scheduler = BackgroundScheduler(daemon=True)

if __name__ == "__main__":
    app.run()
