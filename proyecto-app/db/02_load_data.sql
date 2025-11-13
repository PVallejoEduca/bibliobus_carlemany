TRUNCATE lib.ratings, lib.copies, lib.user_info, lib.books RESTART IDENTITY CASCADE;
SET datestyle TO 'DMY';

-- COPY lib.books (isbn, authors, original_publication_year, original_title, title, language_code, book_id, image_url)
-- FROM '/data/raw/book_mkp.csv'
-- WITH (FORMAT csv, HEADER true);

-- COPY lib.users (user_id, full_name, email, member_since)
-- FROM '/data/raw/user_info_mkp.csv'
-- WITH (FORMAT csv, HEADER true);

-- COPY lib.copies (copy_id, book_id)
-- FROM '/data/raw/copies_mkp.csv'
-- WITH (FORMAT csv, HEADER true);

-- COPY lib.ratings (user_id, copy_id, rating)
-- FROM '/data/raw/ratings_mkp.csv'
-- WITH (FORMAT csv, HEADER true);

-- Para cargar la versión limpia (_clean_1), comenta el bloque anterior y descomenta el siguiente.
COPY lib.books (isbn, authors, original_publication_year, original_title, title, language_code, image_url, book_id)
FROM '/data/raw/books_clean_1.csv'
WITH (FORMAT csv, HEADER true);

COPY lib.users (user_id, full_name, email, member_since)
FROM '/data/raw/user_info_clean_1.csv'
WITH (FORMAT csv, HEADER true);

COPY lib.copies (copy_id, book_id)
FROM '/data/raw/copies_clean_1.csv'
WITH (FORMAT csv, HEADER true);

COPY lib.ratings (user_id, copy_id, rating)
FROM '/data/raw/ratings_clean_1.csv'
WITH (FORMAT csv, HEADER true);
