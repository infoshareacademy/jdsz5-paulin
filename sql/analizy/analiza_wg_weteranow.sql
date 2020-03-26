---------------------------------------------------------------
--Analiza wg odsetka weteranow
---------------------------------------------------------------
with k1 as
(
select r.fips,
case 
when (VET605213*100)/POP010210::numeric<6 then '1) udzial weteranow do 6%'
when (VET605213*100)/POP010210::numeric<8 then '2) udzial weteranow do 8%'
when (VET605213*100)/POP010210::numeric<10 then '3) udzial weteranow do 10%'
else '4) udzial weteranow pow 10%'
end as kategoria,
case when sum(case when r.party like 'Repub%'then r.votes end)>sum(case when r.party like 'Democ%' then r.votes end) then 1 else 0 end republikanie,
case when sum(case when r.party like 'Repub%'then r.votes end)<sum(case when r.party like 'Democ%' then r.votes end) then 1 else 0 end demokraci
from primary_results r
join county_facts f on r.fips=f.fips
where r.state not in ('Colodrado', 'North Dakota', 'Maine')
group by r.fips,kategoria
),
k2 as
(
select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci  
from k1
where republikanie is not null or demokraci is not null
group by kategoria
order by kategoria
),
k3 as
(
select *,
republikanie/sum(republikanie) over()::numeric d_republikanie,
demokraci/sum(demokraci) over()::numeric d_demokraci
from k2
),
k4 as
(select *,
ln(d_republikanie/d_demokraci) woe,
d_republikanie-d_demokraci dr_minus_dd
from k3),
k5 as
(select *, woe*dr_minus_dd  iv from k4)
select *, sum(iv) over() suma_iv from k5