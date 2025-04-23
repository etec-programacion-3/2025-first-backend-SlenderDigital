"""
Book Management API

This module implements a REST API for managing books using FastAPI and Tortoise ORM.
It provides CRUD operations and search functionality for books.
"""

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, DoesNotExist
from tortoise.exceptions import IntegrityError
from app.database.db_models import Book
from app.models import BookIn, BookOut
from typing import List, Optional

app = FastAPI(
    title="Book Management API",
    description="API for managing books with CRUD operations and search functionality",
    version="1.0.0"
)

# Database configuration
register_tortoise(
    app,
    db_url="sqlite://app/database/sqlite/db.sqlite3",
    modules={"models": ["app.database.db_models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/books", response_model=List[BookOut])
async def list_books():
    """
    Retrieve all books from the database.

    Returns:
        List[BookOut]: A list of all books in the database.

    Raises:
        HTTPException: If there's a database error.
    """
    try:
        return await Book.all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve books: {str(e)}"
        )

@app.get("/books/find", response_model=List[BookOut])
async def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Search for books using optional filters.

    Args:
        title: Optional title to search for (case-insensitive)
        author: Optional author to search for (case-insensitive)
        category: Optional category to search for (case-insensitive)

    Returns:
        List[BookOut]: A list of books matching the search criteria.

    Raises:
        HTTPException: If there's a database error.
    """
    try:
        query = Book.all()
        if title:
            query = query.filter(title__icontains=title)
        if author:
            query = query.filter(author__icontains=author)
        if category:
            query = query.filter(category__icontains=category)
        return await query
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search operation failed: {str(e)}"
        )

@app.post("/books", response_model=BookOut)
async def create_book(book_in: BookIn):
    """
    Create a new book entry.

    Args:
        book_in: Book data including title, author, ISBN, category, and status.

    Returns:
        BookOut: The created book's data.

    Raises:
        HTTPException: If ISBN already exists or if creation fails.
    """
    try:
        book = await Book.create(**book_in.dict())
        return book
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="A book with this ISBN already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create book: {str(e)}"
        )

@app.get("/books/{id}", response_model=BookOut)
async def get_book(id: int):
    """
    Retrieve a specific book by its ID.

    Args:
        id: The unique identifier of the book.

    Returns:
        BookOut: The requested book's data.

    Raises:
        HTTPException: If the book is not found or if retrieval fails.
    """
    try:
        book = await Book.get(id=id)
        return book
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve book: {str(e)}"
        )

@app.put("/books/{id}", response_model=BookOut)
async def update_book(id: int, book_in: BookIn):
    """
    Update an existing book's information.

    Args:
        id: The unique identifier of the book to update.
        book_in: Updated book data.

    Returns:
        BookOut: The updated book's data.

    Raises:
        HTTPException: If the book is not found or if update fails.
    """
    try:
        book = await Book.get(id=id)
        await book.update_from_dict(book_in.dict())
        await book.save()
        return book
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Update failed: ISBN conflict with existing book"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update book: {str(e)}"
        )

@app.delete("/books/{id}")
async def delete_book(id: int):
    """
    Delete a book from the database.

    Args:
        id: The unique identifier of the book to delete.

    Returns:
        dict: A message confirming successful deletion.

    Raises:
        HTTPException: If the book is not found or if deletion fails.
    """
    try:
        deleted_count = await Book.filter(id=id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete book: {str(e)}"
        )