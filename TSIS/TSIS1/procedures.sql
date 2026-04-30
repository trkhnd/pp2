CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    cid INTEGER;
BEGIN
    SELECT id INTO cid
    FROM contacts
    WHERE name = p_contact_name
    LIMIT 1;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    gid INTEGER;
    cid INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT(name) DO NOTHING;

    SELECT id INTO gid
    FROM groups
    WHERE name = p_group_name;

    SELECT id INTO cid
    FROM contacts
    WHERE name = p_contact_name
    LIMIT 1;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    UPDATE contacts
    SET group_id = gid
    WHERE id = cid;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    surname VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id,
           c.name,
           c.surname,
           c.email,
           c.birthday,
           g.name,
           COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.surname ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$;