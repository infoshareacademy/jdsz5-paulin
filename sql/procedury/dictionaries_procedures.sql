-- ##################################################
-- --------------------------------------------------
-- get_categories_list(delimiter VARCHAR) - wyświetla kategorie (pierwsze 3 znaki z kolumny kategorii) oraz wszystkie opisy odpowiadające danej kategorii
-- parametr "delimiter" typu VARCHAR tworzy przerwy między kolejnymi opisami.
-- --------------------------------------------------

CREATE OR REPLACE FUNCTION get_categories_list(delimiter VARCHAR)
    RETURNS SETOF county_facts_dictionary
as
$$
SELECT LEFT(column_name, 3)                               categories,
       string_agg(concat_ws(',', description), delimiter) descriptions
FROM county_facts_dictionary
GROUP BY categories;
$$
    LANGUAGE SQL;

-- USAGE:
select *
from get_categories_list(' --||-- ');

-- ##################################################
-- --------------------------------------------------
-- get_categories_by_name(name VARCHAR) - wyświetla opisy z podanej kategorii
-- parametr "name" typu VARCHAR wyszukuje daną kategorię.
-- --------------------------------------------------

CREATE OR REPLACE FUNCTION get_categories_by_name(name VARCHAR)
    RETURNS SETOF county_facts_dictionary
as
$$
SELECT LEFT(column_name, 3) categories,
       description          descriptions
FROM county_facts_dictionary
where column_name ilike concat('%', name, '%')
GROUP BY categories, descriptions;
$$
    LANGUAGE SQL;

-- USAGE:
select *
from get_categories_by_name('rhi');

-- ##################################################
-- --------------------------------------------------
-- select_by_column_names(_tbl regclass, _pattern text) - wyświetla select ze wszystkimi kolumnami zawartymi w zmiennej _pattern.
-- parametr "_tbl" typu REGCLASS znajduje tabele, parametr "_pattern" typu TEXT wyszukuje kolumny zawierające część nazwy kolumny np. RHI
-- --------------------------------------------------
CREATE OR REPLACE FUNCTION select_by_column_names(_tbl REGCLASS, _pattern TEXT)
    RETURNS TEXT AS
$func$
SELECT format('SELECT %s FROM %s'
           , string_agg(quote_ident(attname), ', ')
           , $1)
FROM pg_attribute
WHERE attrelid = $1
  AND attname ilike ('%' || $2 || '%')
  AND NOT attisdropped
  AND attnum > 0;
$func$ LANGUAGE sql;

-- USAGE:
SELECT * from select_by_column_names('county_facts', 'RHI');
-- ##################################################
