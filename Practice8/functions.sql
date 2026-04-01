-- Функция для поиска контакта (по паттерну)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_pattern TEXT)
RETURNS TABLE (
    contact_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone_number VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    WHERE contacts.first_name ILIKE '%' || search_pattern || '%'
       OR contacts.last_name ILIKE '%' || search_pattern || '%'
       OR contacts.phone_number ILIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-------------------------------------------------------------------------------

-- Функция для вывоа контактов (постранично)
CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE (
    contact_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone_number VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    ORDER BY first_name ASC  -- Сортировка важна для стабильности страниц
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;