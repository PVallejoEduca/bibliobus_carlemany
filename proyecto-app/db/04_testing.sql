-- Libros
SELECT COUNT(*) AS libros_err
FROM lib.books
WHERE book_id IS NULL
   OR title IS NULL OR TRIM(title) = ''
   OR authors IS NULL OR TRIM(authors) = ''
   OR original_publication_year IS NULL OR original_publication_year < 0 OR original_publication_year > 2025;

SELECT original_publication_year, title
FROM lib.books
WHERE book_id IS NULL
   OR title IS NULL OR TRIM(title) = ''
   OR authors IS NULL OR TRIM(authors) = ''
   OR original_publication_year IS NULL OR original_publication_year < 0 OR original_publication_year > 2025;

-- Copias
SELECT COUNT(*) AS copias_err
FROM lib.copies
WHERE copy_id IS NULL OR book_id IS NULL;

-- Ratings
SELECT COUNT(*) AS ratings_err
FROM lib.ratings
WHERE user_id IS NULL OR copy_id IS NULL OR rating IS NULL OR rating < 1 OR rating > 5;