from flask import render_template
from application import create_app
from config import Config

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html', error=e)


if __name__ == '__main__':
    app.run(host=Config.HOST)
