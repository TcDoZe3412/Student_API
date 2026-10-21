
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class BookRequest(BaseModel):
    bookName: str
    NoOfCopies: int = Field(gt=0)


inventory = {
    "wings of fire": 2
}

@app.get("/library")
def get_library_books():
    return inventory


@app.get("/library/{bookName}")
def get_library(bookName: str):

    if bookName not in inventory:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "bookName": bookName,
        "available_copies": inventory[bookName]
    }

@app.post("/library")
def add_book(book: BookRequest):

    if book.bookName in inventory:
        inventory[book.bookName] += book.NoOfCopies
    else:
        inventory[book.bookName] = book.NoOfCopies


    return {
        "message": "Book added successfully",
        "bookName": book.bookName,
        "total_copies": inventory[book.bookName]
    }

@app.post("/library_borrow")
def borrow_book(book_name):

    if book_name not in inventory:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )


   
    if inventory[book_name] <= 0:
        raise HTTPException(
            status_code=400,
            detail="No copies available"
        )

    inventory[book_name] -= 1

    return {
        "message": "Book borrowed successfully",
        "bookName": book_name,
        "remaining_copies": inventory[book_name]
    }
