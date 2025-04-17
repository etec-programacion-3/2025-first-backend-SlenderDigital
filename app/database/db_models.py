"""
Database models for the library management system.
This module defines the Book model, which represents a book in the library.
The Book model includes fields for the book's ID, title, author, ISBN, category,
status, and creation date.
"""

from tortoise import fields, Model

class Book(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)  
    isbn = fields.CharField(max_length=13, unique=True)
    category = fields.CharField(max_length=100)
    status = fields.CharField(max_length=50) 
    creation_date = fields.DatetimeField(auto_now_add=True)
