-- ---------------------------- POP -----------------------------

-- Wykorzystanie funkcji na wyświetlenie kategorii
select *
from get_categories_list(' --||-- ');

-- Wykorzystanie funkcji na wyświetlenie opisów danej kategorii
select *
from get_categories_by_name('pop');

select *
from get_categories_by_name('pst');

-- Wykorzystanie funkcji na stworzenie SQLa z kolumnami na temat kategorii dotyczącej populacji
SELECT *
from select_by_column_names('county_facts', 'pop');
SELECT *
from select_by_column_names('county_facts', 'pst');

-- Wykorzystanie funkcji na stworzenie SQLa z kolumnami na temat kilku kategorii dotyczych populacji
SELECT *
from select_by_multiple_column_names('county_facts', ARRAY ['%pst%', '%pop%']);

-- wszystkie głosy
SELECT DISTINCT county,
                state,
                sum(votes)                                        as votes_count,
                sum(case when party like 'Repub%' then votes end) as republicans_votes
FROM primary_results pr
         JOIN county_facts cf
              ON pr.fips = cf.fips
GROUP BY state, county
ORDER BY state, county;

-- Wyliczenie głosów (według SQL Leszka)
select state,
       sum(votes)                                                       votes_count,
       sum(case when party like 'Repub%' then votes end)                republicans_votes,
       sum(case when party like 'Democ%' then votes end)                democrats_votes,
       sum(votes) - (sum(case when party like 'Repub%' then votes end) +
                     sum(case when party like 'Democ%' then votes end)) votes_difference
from primary_results
group by state
having sum(case when party like 'Repub%' then votes end) is not null
   and sum(case when party like 'Democ%' then votes end) is not null
order by state;

-- Podstawowe wyświetlenie danych na temat populacji w hrabstwie
SELECT DISTINCT county,
                state,
                sum(votes)                                        as votes_count,
                sum(case when party like 'Repub%' then votes end) as republicans_votes,
                sum(case when party like 'Democ%' then votes end) as democrats_votes,
                pop010210                                         as "Population, 2010",
                (pop010210 * (pop645213 / 100))::int              as "Foreign born persons, 2009-2013",
                (pop010210 * (pop815213 / 100))::int              as "Living in same house 1 year & over, 2009-2013",
                (pop010210 * (pop060210 / 100))::int              as "Language other than English spoken at home age 5+ 2009-2013"
FROM primary_results pr
         JOIN county_facts cf
              ON pr.fips = cf.fips
GROUP BY state, county, (pop010210 * (pop645213 / 100))::int, (pop010210 * (pop815213 / 100))::int,
         (pop010210 * (pop060210 / 100))::int, pop010210
ORDER BY state, county;

-- Podstawowe wyświetlenie danych na temat populacji w stanie
SELECT DISTINCT state,
                sum(votes)                                        as votes_count,
                sum(case when party like 'Repub%' then votes end) as republicans_votes,
                sum(case when party like 'Democ%' then votes end) as democrats_votes,
                sum(pst045214)                                    as "Population, 2014 estimate",
                sum((pop010210 * (pop815213 / 100))::int)         as "Living in same house 1 year & over, 2009-2013"
FROM primary_results pr
         JOIN county_facts cf
              ON pr.fips = cf.fips
GROUP BY state
ORDER BY state;


-- Kategoria ludzi żyjących w tym samym domu w okresie 2009-2013
SELECT DISTINCT state,
                sum(votes)                                        as votes_count,
                sum(case when party like 'Repub%' then votes end) as republicans_votes,
                sum(case when party like 'Democ%' then votes end) as democrats_votes,
                sum(pst045214)                                    as "Population, 2014 estimate",
                sum((pop010210 * (pop815213 / 100))::int)         as "Living in same house 1 year, from all",
                sum((pop010210 * (pop645213 / 100))::int)         as "Foreign born persons, 2009-2013"
FROM primary_results pr
         JOIN county_facts cf
              ON pr.fips = cf.fips
GROUP BY state
ORDER BY state;



with pop_categories as (SELECT DISTINCT state                                             as state_of_vote,
                                        sum(votes)                                        as votes_count,
                                        sum(case when party like 'Repub%' then votes end) as republicans_votes,
                                        sum(case when party like 'Democ%' then votes end) as democrats_votes,
                                        sum(pst045214)                                    as "Population, 2014 estimate",
                                        sum((pop010210 * (pop815213 / 100))::int)         as "Living in same house 1 year, from all",
                                        sum((pop010210 * (pop645213 / 100))::int)         as "Foreign born persons, 2009-2013"
                        FROM primary_results pr
                                 JOIN county_facts cf
                                      ON pr.fips = cf.fips
                        GROUP BY state
                        ORDER BY state),
     pop_percent as (SELECT state_of_vote,
                            votes_count,
                            republicans_votes,
                            democrats_votes,
                            pop_categories."Living in same house 1 year, from all"::numeric /
                            pop_categories."Population, 2014 estimate"::numeric as "Living in same house 1 year, % from all",
                            pop_categories."Foreign born persons, 2009-2013"::numeric /
                            pop_categories."Population, 2014 estimate"::numeric as "Foreign born persons, % 2009-2013"
                     FROM pop_categories),
     estimate_of_pop_votes as (SELECT state_of_vote,
                                      votes_count,
                                      (republicans_votes *
                                       pop_percent."Living in same house 1 year, % from all")::int as estimate_of_republican_votes_for_living_in_same_house,
                                      (democrats_votes *
                                       pop_percent."Living in same house 1 year, % from all")::int as estimate_of_republican_votes_for_living_in_same_house,
                                      (republicans_votes *
                                       pop_percent."Foreign born persons, % 2009-2013")::int       as estimate_of_republican_votes_for_foreign_born_persons,
                                      (democrats_votes *
                                       pop_percent."Foreign born persons, % 2009-2013")::int       as estimate_of_republican_votes_for_foreign_born_persons
                               from pop_percent)
select *
from estimate_of_pop_votes;
