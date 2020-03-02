select * from primary_results pr ;
select * from county_facts cf ;
select * from county_facts_dictionary cfd 

select max(votes) from primary_results pr ;
select min(votes) from primary_results pr

select * from primary_results pr 
join county_facts cf on cf.fips =  pr.fips 

select county, party, abs(SBO001207 - SBO015207)
from primary_results pr 
join county_facts cf on cf.fips =  pr.fips
where party ilike 'democrat'
or party ilike 'Republican'

select   state, party, abs(SBO001207 - SBO015207),
count (case when party ilike '%demo%' then 1 end) democrat, 
count (case when party ilike '%repo%' then 1 end) repo

from primary_results pr
join county_facts cf on cf.fips = pr.fips
group by state, party, abs(SBO001207 - SBO015207)

select area_name, max(votes) as il_gl_na_domokratow from primary_results pr 
join county_facts cf on cf.fips =  pr.fips
where party ilike '%demo%'
group by 1

-- srednia ilosc glosow, wariancja i odchylenie pod kontem narodowosci 
select party,
avg(votes) as srednia_ilosc_glosow,
stddev(votes) as odchylenie,
variance(votes) as wariancja,
count(1) as ilosc_glosow
from primary_results pr 
left join county_facts cf on pr.fips = cf.fips
where RHI125214 is not null and RHI225214 is not null  and RHI325214 is not null  and RHI425214 is not null  
and RHI525214  is not null and RHI625214 is not null  and RHI725214 is not null  and RHI825214 is not null 
group by 1
order by ilosc_glosow

-- mediana i kwartyle

 select
percentile_disc(0.5) within group (order by votes) as mediana,
percentile_disc(0.25) within group (order by votes) as q1,
percentile_disc(0.75) within group (order by votes) as q3
from primary_results pr 


-- nieudane

with primary_results as

(select candidate, state, party,
(
case 
when votes < 68 then 'niski'
when votes between 68 and 358 then 'œrednio-niski'
when votes between 359 and 1375 then 'srednio-wysoki'
when votes > 1375 then 'wysoki'
else 'inny'
end
)as glosy_repub
from primary_results pr 

where party ilike '%rep%'
order by state asc
) as republikanie
join 
(select  candidate, state, party,
(
case 
when votes < 377 then 'niski'
when votes between 377 and 921 then 'œrednio-niski'
when votes between 922 and 2387 then 'srednio-wysoki'
when votes > 2387 then 'wysoki'
else 'inny'
end
) as glosy_demo
from primary_results pr 

where party ilike '%demo%'
order by state asc
) as demokraci
on glosy_demo.fips = glosy_repub.fips

select *
from
-- % udzia³ w wyborach wg narodowosci

select distinct state, area_name, 

RHI125214,
RHI225214,
RHI325214,
RHI425214,
RHI525214,
RHI625214,
RHI725214,
RHI825214

from primary_results pr 
left join county_facts cf on pr.fips = cf.fips
order by state asc;

-- wybor partii wg narodowosci

select state, county , party, podzapytanie
from primary_results pr 
join
(select 
RHI125214,
RHI225214,
RHI325214,
RHI425214,
RHI525214,
RHI625214,
RHI725214,
RHI825214
from county_facts cf 
) as podzapytanie
on podzapytanie.fips = pr.fips




-- maksymalne % udzia³y w wyborach w poszczegolnych stanach z podzialem na narodowosc
select distinct state,

max(cf.RHI125214) as bialy,
max(cf.RHI225214) as czarny,
max(cf.RHI325214) as indianin_i_alaska,
max(cf.RHI425214) as azjata,
max(cf.RHI525214) as hawajczyk,
max(cf.RHI625214) as dwie_lub_wiecej_ras,
max(cf.RHI725214) as latynos,
max(cf.RHI825214) as bialy_nie_latynos

from county_facts cf
left join primary_results pr on cf.fips = pr.fips

group by 1
order by state


-- œredni udzia³ % w wyborach w poszczegolnych stanach z podzialem na narodowosc
select distinct state, party,
avg(cf.RHI125214) as bialy,
avg(cf.RHI225214) as czarny,
avg(cf.RHI325214) as indianin_i_alaska,
avg(cf.RHI425214) as azjata,
avg(cf.RHI525214) as hawajczyk,
avg(cf.RHI625214) as dwie_lub_wiecej_ras,
avg(cf.RHI725214) as latynos,
avg(cf.RHI825214) as bialy_nie_latynos

from county_facts cf
left join primary_results pr on cf.fips = pr.fips
where state is not null 
group by 1,2
order by state asc



-- najczesciej wystepujacy kandydaci w obu partiach -- DOKOÑCZYÆ Z INNYMI STANAMI!!!!!!!!!!
select party, mode() within group (order by distinct candidate)
from primary_results pr
full join county_facts cf on cf.fips = pr.fips
where party is not null 
and 
group by party

and state ilike '%alabama%'

select
count(RHI125214) as ilo_gl_demo
from county_facts cf 
join primary_results pr on pr.fips = cf.fips
where party like 'Democrat'

select count(RHI125214) 
from county_facts cf 
join primary_results pr on pr.fips = cf.fips
where party like 'Republican' 

-- korelacje liczby g³osów i narodowoœci
select 
corr (votes, RHI125214) as gl_vs_bialy,
corr (votes, RHI225214) as glo_vs_czarny,
corr (votes, RHI325214) as glo_vs_indianin,
corr (votes, RHI425214) as glo_vs_azjata,
corr (votes, RHI525214) as glo_vs_hawajczyk,
corr (votes, RHI625214) as glo_vs_dwie_rasy,
corr (votes, RHI725214) as glo_vs_latynos,
corr (votes, RHI825214) as glo_vs_bialy_nie_latynos

from primary_results pr 
left join county_facts cf on cf.fips = pr.fips

-- brak silnej korelacji glosy Vs narodowosc

-- korelacja liczby g³osów na trumpa i narodowosci
select 
corr (votes, RHI125214) as gl_vs_bialy,
corr (votes, RHI225214) as glo_vs_czarny,
corr (votes, RHI325214) as glo_vs_indianin,
corr (votes, RHI425214) as glo_vs_azjata,
corr (votes, RHI525214) as glo_vs_hawajczyk,
corr (votes, RHI625214) as glo_vs_dwie_rasy,
corr (votes, RHI725214) as glo_vs_latynos,
corr (votes, RHI825214) as glo_vs_bialy_nie_latynos

from primary_results pr 
left join county_facts cf on cf.fips = pr.fips
where candidate ilike '%trump%'

-- wybor kandydata z podzia³em na stany

select distinct candidate, state, county

from primary_results pr 
order by candidate 






