from applications import create_app

app = create_app('testing')

if __name__ == '__main__':
    app.run(debug=True)
