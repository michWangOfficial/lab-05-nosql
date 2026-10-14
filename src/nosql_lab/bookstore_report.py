#!/usr/bin/env python3
"""Print each selected author's books from the MongoDB bookstore database."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


# Keep credentials in the environment, outside the source code.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

def main():
    """
    connect to Atlas, print the joined inventory report, close the client.
    """
    logging.basicConfig(level=logging.INFO)

    client = None
    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )

        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Include starter authors and the new author from Case Study 1.
        author_ids = ["author_002", "author_003", "author_004"]
        author_filter = {"_id": {"$in": author_ids}}
        author_count = authors.count_documents(author_filter)
        logging.info("Connected to MongoDB Atlas.")
        print(f"Authors: {author_count}")

        for author in authors.find(author_filter):
            print(f"\n{author['name']}")
            # Match the author's ID inside each book's author_ids array.
            # A co-authored book is printed under each matching author.
            author_books = books.find({"author_ids": author["_id"]})
            for book in author_books:
                print(f"  {book['title']} ({book['published_year']})")

    except PyMongoError as error:
        logging.error("MongoDB report failed: %s", error)
    finally:
        # Release the connection even if a database operation fails.
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()