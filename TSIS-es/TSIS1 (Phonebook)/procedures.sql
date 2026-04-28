-- ФУНКЦИЯ ПОИСКА (Расширенная: ищет по имени, почте и всем телефонам)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone_numbers TEXT -- Собираем все телефоны в одну строку для вывода
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.contact_id, c.first_name, c.last_name, c.email,
        string_agg(p.phone || ' (' || p.type || ')', ', ') as phones
    FROM contacts c
    LEFT JOIN phones p ON c.contact_id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.contact_id;
END;
$$ LANGUAGE plpgsql;



-- ПРОЦЕДУРА ДОБАВЛЕНИЯ ТЕЛЕФОНА
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT contact_id INTO v_id FROM contacts WHERE first_name = p_contact_name OR last_name = p_contact_name LIMIT 1;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    END IF;
END;
$$ LANGUAGE plpgsql;



-- ПРОЦЕДУРА СМЕНЫ ГРУППЫ (создает группу, если её нет)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_f_name VARCHAR,
    p_l_name VARCHAR, -- Требуем и имя, и фамилию для точности
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- Создаем группу, если её нет
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    -- Обновляем контакт только при совпадении пары Имя + Фамилия
    UPDATE contacts SET group_id = v_group_id 
    WHERE first_name = p_f_name AND last_name = p_l_name;
    
    -- Если контакт не найден, процедура просто ничего не изменит (безопасно)
END;
$$ LANGUAGE plpgsql;



-- ПАГИНАЦИЯ И ФИЛЬТРАЦИЯ (Универсальная функция для вывода)
CREATE OR REPLACE FUNCTION get_contacts_advanced(
    p_limit INT, 
    p_offset INT, 
    p_group_name TEXT DEFAULT NULL,
    p_sort_by TEXT DEFAULT 'name'
)
RETURNS TABLE (
    id INT,
    f_name VARCHAR,
    l_name VARCHAR,
    c_email VARCHAR,
    c_birthday DATE,
    g_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.contact_id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE (p_group_name IS NULL OR g.name ILIKE p_group_name)
    ORDER BY 
        CASE WHEN p_sort_by = 'name' THEN c.first_name END ASC,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday::text END ASC,
        CASE WHEN p_sort_by = 'date' THEN c.created_at::text END ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;



-- УДАЛЕНИЕ КОНТАКТА
CREATE OR REPLACE PROCEDURE delete_contact_safe(
    p_f_name VARCHAR,
    p_l_name VARCHAR
)
AS $$
BEGIN
    -- Удаляем только конкретного человека по паре Имя+Фамилия
    DELETE FROM contacts WHERE first_name = p_f_name AND last_name = p_l_name;
END;
$$ LANGUAGE plpgsql;



-- ДОБАВЛЕНИЕ/ОБНОВЛЕНИЕ КОНТАКТА
CREATE OR REPLACE PROCEDURE upsert_full_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR,
    p_email VARCHAR,
    p_birthday DATE
)
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    -- 1. Вставляем или обновляем основные данные
    INSERT INTO contacts (first_name, last_name, email, birthday)
    VALUES (p_first_name, p_last_name, p_email, p_birthday)
    ON CONFLICT (first_name, last_name) 
    DO UPDATE SET 
        email = EXCLUDED.email, 
        birthday = EXCLUDED.birthday
    RETURNING contact_id INTO v_contact_id;

    -- 2. Добавляем телефон
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, 'mobile')
    ON CONFLICT DO NOTHING;
END;
$$ LANGUAGE plpgsql;