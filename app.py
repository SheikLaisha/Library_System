from flask import Flask ,render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu"

userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1"
dbname = "/lms"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, name, author, genre, year):
        self.name = name
        self.author = author
        self.genre = genre
        self.year = year
      

@app.route('/')
def index():
    data_books = db.session.query(Books)
    return render_template('index.html', data=data_books)

@app.route('/input', methods=['GET' , 'POST'])
def input_data():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']

        add_data = Books(name, author, genre, year)

        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('index'))

    return render_template('input.html')

# EDIT
@app.route('/edit/<int:id>')
def edit_data(id):
    data_books = Books.query.get(id)
    return render_template('edit.html', data=data_books)

@app.route('/proses_edit', methods=['POST', 'GET'])
def proses_edit():
    data_books = Books.query.get(request.form.get('id'))

    data_books.name = request.form['name']
    data_books.author = request.form['author']
    data_books.genre = request.form['genre']
    data_books.year = request.form['year']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    data_books = Books.query.get(id)
    db.session.delete(data_books)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('index'))


@app.route('/view/<int:id>')
def view_data(id):
    data_books = Books.query.get(id)
    return render_template('view.html', data=data_books)

# @app.route('/search')
# def search():
#     q=request.args.get("q")
#     print(q)

#     if q:
#         results=Books.query.filter(Books.name.icontains(q) | Books.author.icontains(q) | Books.genre.icontains(q)).order_by(Books.year.asc()).all()
#     else:
#         results = []
    
#     return render_template('search_res.html', results=results )


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         search_query = request.form.get('search_query')
#         # Perform search based on the query
#         results = Books.query.filter(Books.name.icontains(f'%{search_query}%')).all()
#         return render_template('search_res.html', results=results, search_query=search_query)
#     return render_template('search.html')



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        # Perform search query based on the search_query string
        # Assuming you have a function to perform search and return results
        search_results = Books.query.filter(Books.name.icontains(f'%{search_query}%') | Books.author.icontains(f'%{search_query}%') | Books.genre.icontains(f'%{search_query}%') | Books.year.icontains(f'%{search_query}%')).all()
        return render_template('search_res.html', search_results=search_results)
    # else:
    #     return render_template('search.html')

