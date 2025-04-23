from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, DoesNotExist
from tortoise.exceptions import IntegrityError
from app.database.db_models import Book
from app.models import BookIn, BookOut

app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://app/database/sqlite/db.sqlite3",
    modules={"models": ["app.database.db_models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# List all books
@app.get("/books", response_model=list[BookOut])
async def list_books():
    return await Book.all()

# Search books by title, author, or category
@app.get("/book/find", response_model=list[BookOut])
async def search_books(title: str = None, author: str = None, category: str = None):
    query = Book.all()
    if title:
        query = query.filter(title__icontains=title)
    if author:
        query = query.filter(author__icontains=author)
    if category:
        query = query.filter(category__icontains=category)
    return await query

# Create a new book
@app.post("/books", response_model=BookOut)
async def create_book(book_in: BookIn):
    try:
        book = await Book.create(**book_in.dict())
        return book
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="A book with this ISBN already exists"
        )

# Update a book by ID
@app.put("/books/{id}", response_model=BookOut)
async def update_book(id: int, book_in: BookIn):
    try:
        book = await Book.get(id=id)
        await book.update_from_dict(book_in.dict())
        await book.save()
        return book
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")

# Get a specific book by ID
@app.get("/books/{id}", response_model=BookOut)
async def get_book(id: int):
    try:
        book = await Book.get(id=id)
        return book
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")

# Delete a book by ID
@app.delete("/books/{id}")
async def delete_book(id: int):
    deleted_count = await Book.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}