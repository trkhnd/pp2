CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_surname VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
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