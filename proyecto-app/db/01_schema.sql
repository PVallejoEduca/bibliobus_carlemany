DROP SCHEMA IF EXISTS lib CASCADE;
CREATE SCHEMA lib;

CREATE TABLE IF NOT EXISTS lib.books (
    book_id INTEGER PRIMARY KEY,
    isbn VARCHAR(40),
    authors TEXT,
    original_publication_year INTEGER,
    original_title TEXT,
    title TEXT NOT NULL,
    language_code VARCHAR(16),
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS lib.copies (
    copy_id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES lib.books (book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lib.users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    member_since DATE
);

CREATE TABLE IF NOT EXISTS lib.ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES lib.users (user_id) ON DELETE CASCADE,
    copy_id INTEGER NOT NULL REFERENCES lib.copies (copy_id) ON DELETE CASCADE,
    rating INTEGER NOT NULL,
    comment TEXT,
    CONSTRAINT rating_range CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT uq_user_copy UNIQUE (user_id, copy_id)
);

CREATE INDEX IF NOT EXISTS idx_copies_book_id ON lib.copies (book_id);
CREATE INDEX IF NOT EXISTS idx_ratings_copy_id ON lib.ratings (copy_id);
CREATE INDEX IF NOT EXISTS idx_ratings_user_id ON lib.ratings (user_id);
