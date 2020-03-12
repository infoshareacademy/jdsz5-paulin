--ogolne dane
select sum(votes) as ilo_glosow_suma, count(distinct candidate) as candidate 
from primary_results pr 
--- ilosc hrabstw
SELECT COUNT(*)
FROM (select distinct state, county as stany
	from primary_results) as sc

--kto wygral Demokracji vs Republikanie
with df1 as(
select county, party, sum(votes) as ilo_glos
from primary_results pr
group by county, party
),
df2 as ( select
sum(case when df1.party like 'Repub%' then df1.ilo_glos end) as sum_repub,
sum(case when df1.party like 'Democ%' then df1.ilo_glos  end) as sum_demo
from df1
)
select * from df2

--statystyki najlepszego republikana i demokraty
with df1 as(
select party, candidate,sum(votes) as ilo_glos
from primary_results pr
group by party,pr.candidate
),
df2 as ( select *,
row_number() over (partition by party order by sum(ilo_glos) desc) as numer
from df1
group by df1.party,df1.candidate,df1.ilo_glos
),
df3 as (select *
from df2
where numer =1)

select * from df3

-----ile stanów republikańskich a ile demokratycznych
with ogol as (select distinct pr.state, pr.county,
case when sum(case when pr.party like 'Repub%'then pr.votes end)>sum(case when pr.party like 'Democ%' then pr.votes end) then 1 else 0 end republikanie,
case when sum(case when pr.party like 'Repub%'then pr.votes end)<sum(case when pr.party like 'Democ%' then pr.votes end) then 1 else 0 end demokraci
from primary_results pr
where pr.state not in ('Colodrado', 'North Dakota', 'Maine')
group by pr.state,pr.county),

suma as (
select count(o.county) ilo_hrabstw, sum(republikanie) as republikanie, sum(demokraci) as demokraci  
from ogol as o
where republikanie<>0 or demokraci<>0
--group by 
)
select * from suma

