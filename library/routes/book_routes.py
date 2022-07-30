# internal imports
from library.forms import book_form
from library.scan_book import gen_frames, capture_frame, img_to_pdf, startscan
from library import app, db
from library.models import Book, Member
from library.ocr_convertor import ocr

# external imports 
import os
import mmap
import requests
import json
from flask import render_template, redirect, url_for, flash, request, jsonify, Response
from sqlalchemy import or_


# Renders book page
@app.route('/books', methods=['GET','POST'])
def books_page():
    # reads all books from db
    books = Book.query.order_by('id').all()
    # print(books[0].id)
    form_book = book_form() 
    # checks book stock to borrow
    books_to_borrow = Book.query.filter(Book.borrow_stock > 0).all()
    #checks member rent due is not greater than 500
    members_can_borrows = Member.query.filter(Member.to_pay < 500).all()
    books_to_return =  Book.query.filter(Book.borrower).all()
    # if no validation error while creating book
    if form_book.validate_on_submit():  
        book_to_create = Book(title = book_form().title. data,
                              isbn = book_form().isbn.data,
                              author = book_form().author.data,
                              stock = book_form().stock.data,
                              borrow_stock = book_form().stock.data)
        db.session.add(book_to_create)
        db.session.commit()
        flash('Successfully create a book', category="success")
        return redirect(request.referrer)

    # if error occurs
    if form_book.errors != {}:
        for err_msg in form_book.errors.values():
            flash(f'There was an error with creating a book: {err_msg}', category='danger')
    
    return render_template('books/book.html', book_form=book_form(), 
                            books=books, length = len(books),
                            books_to_borrow = books_to_borrow, 
                            members_can_borrow = members_can_borrows, 
                            books_to_return = books_to_return)

@app.route('/bookos', methods=['GET']) #XX
def book_os():
    books=[]
    output = os.listdir("library/static/pdf")

    for i in range(0,len(output)):
        if (output[i].split("."))[-1]=="pdf":
            books.append({"id":i+1,"title":output[i],"isbn":i+1,"author":"OCR Convertor","borrow_stock":1})
    # output = subprocess.check_output("dir library\\books", shell=True)
    print(books)
    return render_template('books/bookos.html',book_form=book_form(),books=books,length = len(books))

@app.route('/pdfview') ## XX
def pdf_view():
    content=[]
    path = "library/static/pdf"
    a = os.listdir(path)
    print(a)
    content=[]
    for i in range(0,len(a)):
        if a[i].split(".")[-1]=="pdf":
            content.append(a[i])
    print(content)
    text = json.dumps(sorted(content))
    return render_template("pdf_viewer.html", contents = text)

@app.route('/singlepdfview', methods=['GET','POST']) ## XX
def single_pdf_view():
    content=[]    
    print(request.form.get('query'))
    content.append(request.form.get('query')) 
    print(content)
    text = json.dumps(sorted(content))
    return render_template("pdf_viewer.html", contents = text)

# deletes a book
@app.route('/delete-book/<book_id>', methods=['GET','POST'])
def delete_book(book_id):
    try:
        # reads the requested book
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash("Deleted Successfully", category="success")

    except:
        flash("Error in deletion", category="danger")

    return redirect(url_for('books_page'))


# updates a book
@app.route('/update-book/<book_id>', methods=['GET','POST'])
def update_book(book_id):
    # reads requested book from db
    book = Book.query.filter_by(id=book_id).first()
    newTitle = request.form.get("title")
    newAuthor = request.form.get("author")
    newIsbn = request.form.get("isbn")
    newStock = request.form.get('stock')

    try:
        if(book.title is not newTitle):
            book.title = newTitle
        if(book.author is not newAuthor):
            book.author = newAuthor
        if(book.isbn is not newIsbn):
            book.isbn = newIsbn
        if(book.stock is not newStock):
            book.stock =  book.stock + int(newStock)
            book.borrow_stock = int(newStock)
        db.session.commit()
        flash("updated sucessfully", category="success")

    except:
        flash("Nothing to update!", category="warning")

    return redirect(url_for('books_page'))


# search for book and/or author
@app.route('/search', methods=['GET','POST'])
def search_book():
    query = request.form.get("query")
    # searches in both title and author column to check the like string
    books = Book.query.filter(or_(Book.title.ilike('%{}%'.format(query)), Book.author.ilike('%{}%'.format(query)))).all()
    print(books)

    return render_template('books/search_page.html', 
                            books = books, length = len(books))


@app.route('/searchos', methods=['GET','POST']) #XX
def search_bookos():
    query = request.form.get("query")
    path = "library/static/pdf"
    a = os.listdir(path)
    books=[]

    for i in range(0,len(a)):
        if a[i].split(".")[-1]=="txt":
            with open(r'library\\static\\pdf\\'+a[i], 'rb', 0) as file:
                s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                if s.find(bytes(query, 'utf-8')) != -1:
                    books.append({"id":i+1,"title":a[i].split(".")[:-1][0]+".pdf","isbn":i+1,"author":"OCR Convertor","borrow_stock":1})
    print(books)                

    return render_template('books/search_page.html', 
                            books = books, length = len(books))

@app.route('/scanbook', methods=['GET'])
def scan_book():
    return render_template('books/scan_book.html')
    
@app.route('/startscan', methods=['POST'])
def start_scan():
    startscan()
    return {}

@app.route('/capture', methods=['POST'])
def capture():
    capture_frame()
    return {}

@app.route('/stopscan', methods=['POST'])
def stop_scan():
    ocr()
    img_to_pdf()
    return {}

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# imports books from Frappe API with given title
@app.route('/import-from-frappe', methods=['GET','POST'])
def import_books_from_frappe():
    title = request.form.get('title')
    books = []
    url = f"https://frappe.io/api/method/frappe-library?page=1&title={title}"
    books = requests.get(url).json()['message']
    book_list = db.session.query(Book.title).all()
    book_list = list(map(' '.join, book_list))
    author_list = db.session.query(Book.author).all()
    author_list = list(map(' '.join, author_list))
    # if books are succesfully imported
    if len(books) > 0:
        for book in books:
            # if no duplicate book is found
            if(book['title'] not in book_list and book['authors'] not in author_list):
                book_to_create = Book(title = book['title'], 
                                      isbn = (book['isbn']),
                                      author = book['authors'],
                                      stock = 20,
                                      borrow_stock = 20)
                db.session.add(book_to_create)
                db.session.commit()
            #skips when a duplicate is found
            else:
                continue
        flash("succesfully Imported", category="success")
    #if error in importing the books
    else:
        flash("No response from the API", category="danger")

    return redirect(url_for('books_page'))


# gives the member list to dropdown options
@app.route('/book/<id>')
def mem(id):
    books = Book.query.get(id)
    members = []
    for member in books.borrower:
        member_obj = {}
        member_obj['id'] = member.id
        member_obj['member_name'] = member.member_name
        members.append(member_obj)
   
    return jsonify({'members': members})
