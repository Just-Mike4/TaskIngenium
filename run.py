from TaskApp import create_app


app=create_app()

if __name__ == '__main__':
    app.run(debug=True, port=2023)
