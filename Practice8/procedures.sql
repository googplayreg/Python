-- Процедура для добавления/обновления контакта
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    INSERT INTO contacts (first_name, last_name, phone_number)
    VALUES (p_first_name, p_last_name, p_phone)
    ON CONFLICT (first_name, last_name) 
    DO UPDATE SET phone_number = EXCLUDED.phone_number;
END;
$$ LANGUAGE plpgsql;

-------------------------------------------------------------------------------

-- Процедура для множественного добаления контактов
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_first_names VARCHAR[],
    p_last_names VARCHAR[],
    p_phones VARCHAR[],
    INOUT p_errors TEXT DEFAULT ''
)
AS $$
DECLARE
    i INTEGER;
BEGIN
    -- Проходим циклом по массиву (от 1 до длины массива)
    FOR i IN 1 .. array_upper(p_first_names, 1)
    LOOP
        -- Простая валидация: номер должен быть длиной от 10 до 15 символов
        -- (Можно усложнить проверку под твои нужды)
        IF length(p_phones[i]) >= 10 AND length(p_phones[i]) <= 15 THEN
            INSERT INTO contacts (first_name, last_name, phone_number)
            VALUES (p_first_names[i], p_last_names[i], p_phones[i])
            ON CONFLICT (first_name, last_name) 
            DO UPDATE SET phone_number = EXCLUDED.phone_number;
            -- Вариант с нормальной проверкой (RegEx)
            -- IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            -- INSERT INTO phonebook(name, phone) VALUES(p_names[i], p_phones[i])
            -- ON CONFLICT (phone) DO NOTHING;
            -- Вставляем, если это цифры, возможно с + в начале, длиной от 10 до 15
        ELSE
            -- Если номер не прошел проверку, добавляем инфо в строку ошибок
            p_errors := p_errors || 'Ошибка в данных: ' || p_first_names[i] || ' ' || p_last_names[i] || ' (тел: ' || p_phones[i] || '); ';
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-------------------------------------------------------------------------------

-- Процедура для удаления контакта
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
AS $$
BEGIN
    -- Удаляем, если совпадает имя ИЛИ фамилия (p_name)
    -- ИЛИ если совпадает номер телефона (p_phone)
    DELETE FROM contacts
    WHERE (p_name IS NOT NULL AND (first_name = p_name OR last_name = p_name))
       OR (p_phone IS NOT NULL AND phone_number = p_phone);
END;
$$ LANGUAGE plpgsql;