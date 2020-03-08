--Do wykluczenia z badn 3 stany: Colodrado, North Dakota, Maine
select state,
       sum(votes)                                        Liczba_glosow,
       sum(case when party like 'Repub%' then votes end) Republikanie,
       sum(case when party like 'Democ%' then votes end) Demokraci
from primary_results
group by state
having sum(case when party like 'Repub%' then votes end) is null
    or sum(case when party like 'Democ%' then votes end) is null;

-----------------------------------------------------------
-- Propozycja kategorii wg dochodu
-----------------------------------------------------------
select case
           when inc910213 < 18000 then 'bardzo niskie dochody'
           when inc910213 < 22000 then 'niskie dochody'
           when inc910213 < 26000 then 'srednie dochody'
           when inc910213 < 30000 then 'wysokie dochody'
           else 'bardzo wysokie dochody'
           end as kategoria,
       count(*)
from county_facts
group by kategoria;

---------------------------------------------------------------
--Analiza wg kategorii
---------------------------------------------------------------
with k1 as
         (select case
                     when f.inc910213 < 22000 then '1) niskie dochody'
                     when f.inc910213 < 26000 then '2) srednie dochody'
                     when f.inc910213 < 30000 then '3) wysokie dochody'
                     else '4) bardzo wysokie dochody'
                     end    as                                         kategoria,
                 sum(votes) as                                         liczba_glosow,
                 sum(case when r.party like 'Repub%' then r.votes end) republikanie,
                 sum(case when r.party like 'Democ%' then r.votes end) demokraci
          from primary_results r
                   join county_facts f on r.fips = f.fips
          where state not in ('Colodrado', 'North Dakota', 'Maine')
          group by kategoria
          order by kategoria),
     k2 as
         (select *,
                 republikanie / sum(republikanie) over ()::numeric d_republikanie,
                 demokraci / sum(demokraci) over ()::numeric       d_demokraci
          from k1
         ),
     k3 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from k2),
     k4 as
             (select *, woe * dr_minus_dd iv from k3)
select *, sum(iv) over () suma_iv
from k4;


