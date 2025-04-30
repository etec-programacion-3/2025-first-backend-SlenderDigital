from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import DoesNotExist
from tortoise.exceptions import IntegrityError
from typing import List, Optional
from app.database.db_models import Book
from app.schemas import BookIn, BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookOut])
async def list_books():
    """Retrieve all books from the database."""
    try:
        return await Book.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve books: {str(e)}")

@router.get("/find", response_model=List[BookOut])
async def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None
):
    """Search for books using optional filters."""
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
        raise HTTPException(status_code=500, detail=f"Search operation failed: {str(e)}")

@router.post("/", response_model=BookOut)
async def create_book(book_in: BookIn):
    """Create a new book entry."""
    try:
        book = await Book.create(**book_in.dict())
        return book
    except IntegrityError:
        raise HTTPException(status_code=400, detail="A book with this ISBN already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")

@router.get("/{id}", response_model=BookOut)
async def get_book(id: int):
    """Retrieve a specific book by its ID."""
    try:
        book = await Book.get(id=id)
        return book
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve book: {str(e)}")

@router.put("/{id}", response_model=BookOut)
async def update_book(id: int, book_in: BookIn):
    """Update an existing book's information."""
    try:
        book = await Book.get(id=id)
        await book.update_from_dict(book_in.dict())
        await book.save()
        return book
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Update failed: ISBN conflict with existing book")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update book: {str(e)}")

@router.delete("/{id}")
async def delete_book(id: int):
    """Delete a book from the database."""
    try:
        deleted_count = await Book.filter(id=id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete book: {str(e)}")
