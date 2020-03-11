SELECT COUNT(*)
FROM (select distinct state, county
      from primary_results
      where state not in ('Colodrado', 'North Dakota', 'Maine')) as sc;

SELECT COUNT(*)
FROM (select distinct state, county
      from primary_results) as sc;

SELECT COUNT(*)
FROM (select distinct state, county
      from primary_results
      where state not in ('Colodrado', 'North Dakota', 'Maine')) as sc
UNION
SELECT COUNT(*)
FROM (select distinct state, county
      from primary_results) as sc;

select (select count(*)
        from (select distinct state, county
              from primary_results
              where state not in ('Colodrado', 'North Dakota', 'Maine')) as sc) as liczba_hrabstw_wykluczenia,
       (select count(*)
        from (select distinct state, county
              from primary_results) as s)                                       as liczba_hrabstw;


---------------------------------------------------------------
-- Counts of all important values / check db data
---------------------------------------------------------------

with counts as (select distinct state,
                                county,
                                case
                                    when sum(case when party ilike '%repub%' then votes end) >
                                         sum(case when party ilike '%democ%' then votes end) then 1
                                    else 0 end republicans,
                                case
                                    when sum(case when party ilike '%repub%' then votes end) <
                                         sum(case when party ilike '%democ%' then votes end) then 1
                                    else 0 end democrats
                from primary_results
                group by state, county
                order by state, county),
     res as (
         select (select count(*) from (select distinct state, county from primary_results) as s)   county_all,
                (select count(*)
                 from (select distinct state, county
                       from primary_results
                                left join county_facts cf on primary_results.fips = cf.fips) as s) county_with_facts_left_join,
                (select count(*)
                 from (select distinct state, county
                       from primary_results
                                join county_facts cf on primary_results.fips = cf.fips) as s)      county_with_facts_join,
                count(case when republicans = 1 then republicans end)                              republican_wins,
                count(case when democrats = 1 then democrats end)                                  democrats_wins
         from counts)
select *
from res;


select distinct state,
                county,
                case
                    when sum(case when r.party like 'Repub%' then r.votes end) >
                         sum(case when r.party like 'Democ%' then r.votes end) then 1
                    else 0 end republikanie,
                case
                    when sum(case when r.party like 'Repub%' then r.votes end) <
                         sum(case when r.party like 'Democ%' then r.votes end) then 1
                    else 0 end demokraci
from primary_results r
         left join county_facts f on r.fips = f.fips
where r.state not in ('Colodrado', 'North Dakota', 'Maine')
group by state, county;


with k1 as
         (
             select r.fips,
                    case
                        when f.inc910213 < 20000 then '1) niskie dochody'
                        when f.inc910213 < 30000 then '2) srednie dochody'
                        else '3) wysokie dochody'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      left join county_facts f on r.fips = f.fips
             where r.state not in ('Colodrado', 'North Dakota', 'Maine')
             group by r.fips, kategoria
         ),
     k2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from k1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
             order by kategoria
         ),
     k3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from k2
         ),
     k4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from k3),
     k5 as
             (select *, woe * dr_minus_dd iv from k4)
select *, sum(iv) over () suma_iv
from k5;


