CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name TEXT,
    p_surname TEXT,
    p_phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names TEXT[],
    p_surnames TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    n INT;
BEGIN
    n := array_length(p_names, 1);

    IF n IS NULL OR n <> array_length(p_surnames, 1) OR n <> array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Input arrays must have the same length';
    END IF;

    FOR i IN 1..n LOOP
        IF p_phones[i] ~ '^[0-9]{11}$' THEN
            IF EXISTS (
                SELECT 1
                FROM contacts
                WHERE name = p_names[i] AND surname = p_surnames[i]
            ) THEN
                UPDATE contacts
                SET phone = p_phones[i]
                WHERE name = p_names[i] AND surname = p_surnames[i];
            ELSE
                INSERT INTO contacts(name, surname, phone)
                VALUES (p_names[i], p_surnames[i], p_phones[i]);
            END IF;
        ELSE
            INSERT INTO invalid_contacts(name, surname, phone, reason)
            VALUES (p_names[i], p_surnames[i], p_phones[i], 'Invalid phone format');
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(
    p_name TEXT DEFAULT NULL,
    p_surname TEXT DEFAULT NULL,
    p_phone TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM contacts
        WHERE phone = p_phone;
    ELSIF p_name IS NOT NULL AND p_surname IS NOT NULL THEN
        DELETE FROM contacts
        WHERE name = p_name AND surname = p_surname;
    ELSE
        RAISE EXCEPTION 'Provide either phone or both name and surname';
    END IF;
END;
$$;