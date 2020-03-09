CREATE OR REPLACE FUNCTION category(delimiter VARCHAR)
    RETURNS SETOF county_facts_dictionary
as
$$
DO
$do$
    BEGIN
        FOR i IN 1..25
            LOOP
                SELECT i,
                FROM primary_results;
            END LOOP;
    END
$do$;
$$
    LANGUAGE SQL;