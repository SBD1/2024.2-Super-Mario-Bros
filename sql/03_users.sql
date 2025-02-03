\c supermario;

DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dba') THEN
        CREATE USER dba WITH PASSWORD 'senha_dba';
        ALTER USER dba WITH SUPERUSER;
    END IF;
END
$$;

DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'gamer') THEN
        CREATE USER gamer WITH PASSWORD 'senha_gamer';
    END IF;
END
$$;