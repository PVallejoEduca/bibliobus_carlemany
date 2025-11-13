CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    publisher TEXT,
    published_date DATE,
    category TEXT,
    language TEXT
);

CREATE TABLE IF NOT EXISTS copies (
    copy_id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books (book_id) ON DELETE CASCADE,
    location TEXT,
    status TEXT,
    inventory_code TEXT
);

CREATE INDEX IF NOT EXISTS idx_copies_book_id ON copies (book_id);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    member_since DATE
);

CREATE TABLE IF NOT EXISTS ratings (
    rating_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    copy_id INTEGER NOT NULL REFERENCES copies (copy_id) ON DELETE CASCADE,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, copy_id)
);

CREATE INDEX IF NOT EXISTS idx_ratings_user_id ON ratings (user_id);
CREATE INDEX IF NOT EXISTS idx_ratings_copy_id ON ratings (copy_id);
