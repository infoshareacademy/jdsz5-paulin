with a as
(
select r.fips,
case 
when f.POP645213<5 then '1) niski udzia³ imigrantow'
when f.POP645213<10 then '2) sredni udzia³ imigrantow'
when f.POP645213<20 then '3) wysoki udzia³ imigrantow'
else '4) bardzo wysoki udzia³ imigrantow'
end as kategoria,
case when sum(case when r.party like 'Repub%'then r.votes end)>sum(case when r.party like 'Democ%' then r.votes end) then 1 else 0 end republikanie,
0 demokraci
from primary_results r
join county_facts f on r.fips=f.fips
group by r.fips, kategoria
having (case when sum(case when r.party like 'Repub%'then r.votes end)>sum(case when r.party like 'Democ%' then r.votes end) then 1 else 0 end)=1
),
b as
(
select r.fips,
case
when f.POP645213<5 then '1) niski udzia³ imigrantow'
when f.POP645213<10 then '2) sredni udzia³ imigrantow'
when f.POP645213<20 then '3) wysoki udzia³ imigrantow'
else '4) bardzo wysoki udzia³ imigrantow'
end as kategoria,
0 republikanie,
case when sum(case when r.party like 'Repub%'then r.votes end)<sum(case when r.party like 'Democ%' then r.votes end) then 1 else 0 end demokraci
from primary_results r
join county_facts f on r.fips=f.fips
group by r.fips, kategoria
having (case when sum(case when r.party like 'Repub%'then r.votes end)<sum(case when r.party like 'Democ%' then r.votes end) then 1 else 0 end)=1
),
k1 as
(
select * from a
union
select * from b
),
k2 as
(
select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci  
from k1
where republikanie<>0 or demokraci<>0
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
