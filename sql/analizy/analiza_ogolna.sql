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
select party, candidate, 
row_number() over (partition by candidate order by sum(votes) desc) as numer
from primary_results pr
where numer =1
group by pr.party,pr.candidate
