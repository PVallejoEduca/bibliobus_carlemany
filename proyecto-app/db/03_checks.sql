SELECT 'books' AS tabla, COUNT(*) AS filas FROM lib.books
UNION ALL
SELECT 'copies', COUNT(*) FROM lib.copies
UNION ALL
SELECT 'users', COUNT(*) FROM lib.users
UNION ALL
SELECT 'ratings', COUNT(*) FROM lib.ratings;

SELECT c.*
FROM lib.copies c
LEFT JOIN lib.books b ON b.book_id = c.book_id
WHERE b.book_id IS NULL;

SELECT r.*
FROM lib.ratings r
LEFT JOIN lib.copies c ON c.copy_id = r.copy_id
WHERE c.copy_id IS NULL;

SELECT r.*
FROM lib.ratings r
LEFT JOIN lib.users u ON u.user_id = r.user_id
WHERE u.user_id IS NULL;
