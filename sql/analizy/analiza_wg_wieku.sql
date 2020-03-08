--Do wykluczenia z badań 3 stany: Colodrado, North Dakota, Maine
select r.fips,r.county,f.inc910213,
sum(case when r.party like 'Repub%'then r.votes end) Republikanie,
sum(case when r.party like 'Democ%' then r.votes end) Demokraci
from primary_results r
join county_facts f on r.fips=f.fips 
where state not in ('Colodrado', 'North Dakota', 'Maine')
group by r.fips,r.county,f.inc910213

--AGE135214	Persons under 5 years, percent, 2014
--AGE295214	Persons under 18 years, percent, 2014
--AGE775214	Persons 65 years and over, percent, 2014

---Wstpna kategoryzacja ze wzgldu na wiek
select 
case 
when age775214<=15 then '1) niski udzial starszych osob'
when age775214<=20 then '2) sredni udzial'
else '3) bardzo wysoki'
end as kategoria, count(*) hrabstwa
from county_facts
group by kategoria
order by kategoria

-- Analiza ze wzgldu na wiek wyborcow.
-- Z analizy wynika, że im niższy udział osob starszych tym wicej glosow uzykiwala partia demokratow
with k1 as
(select
case 
when f.age775214<=15 then '1) niski udzial starszych osob'
when f.age775214<=20 then '2) sredni udzial'
else '5) bardzo wysoki'
end as kategoria,
sum(votes) as liczba_glosow,
sum(case when r.party like 'Repub%'then r.votes end) republikanie,
sum(case when r.party like 'Democ%' then r.votes end) demokraci
from primary_results r
join county_facts f on r.fips=f.fips 
where state not in ('Colodrado', 'North Dakota', 'Maine')
group by kategoria
order by kategoria),
k2 as 
(select *,
republikanie/sum(republikanie) over()::numeric d_republikanie,
demokraci/sum(demokraci) over()::numeric d_demokraci
from k1
),
k3 as
(select *,
ln(d_republikanie/d_demokraci) woe,
d_republikanie-d_demokraci dr_minus_dd
from k2),
k4 as
(select *, woe*dr_minus_dd  iv from k3)
select *, sum(iv) over() suma_iv from k4