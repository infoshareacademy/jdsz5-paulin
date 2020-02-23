--udział przedziału wielowieko <5=5lat,<=18lat i =>65lat z uwgzlędnieniem, udziału kobiet w roku 2014, pozostała cz.to grupa głosujacych
select area_name,AGE135214 as populacja5lat,SEX255214 as kobiety, percent_rank()over () as udzial_dzieci_2014
from county_facts cf 
--group by area_name,AGE135214,SEX255214,PST045214

--AGE295214 as populacja18lat,AGE775214 as  populacja65 pozostałe też bym chciała mmieć w uziale

--ile osób uprawnionych do głosowania
select sum(PST045214)-(sum(AGE295214)+sum(AGE775214)) as os_uprawnione
from county_facts cf 
--jaki udział w populacji to kobiety i mężczyzni
select state_abbreviation,sum(ilosc_kobiet) as ilo_kobiet, sum(ilosc_mezczyzn) as ilo_mezczyzn from
	(select area_name,state_abbreviation,SEX255214/100 as udzial_kobiet,PST045214*(SEX255214/100) as ilosc_kobiet,
	(100-SEX255214)/100 as udzial_mezczyzn,PST045214*((100-SEX255214)/100) as ilosc_mezczyzn
	from county_facts cf) as dane_wsad
group  by state_abbreviation

--jaki udział 
--ogolne statystyki
--ile osób głosowało na republokan i demokratow w stanach
select party, sum(votes)
from primary_results pr 
group by state,party 

--w jakich stanach głosowano podwójcie (są stany gdzie można głosować i ne R i na D, ale na konkretnych kandydatów)
select county,sum(fraction_votes)
from primary_results pr 
group by county
having sum(fraction_votes) >1
--dla hrabstw które oddały głosów więcej niż 100% jaki jest udział głosów na R i D
select county,party,sum(fraction_votes)
from primary_results pr2 
--where county ='Clay'
group by county, party
order by county
--having sum(fraction_votes) >1

--udział danej frakcji w dystrykcie
select state,party,county, percent_rank() over(partition by party order by votes )
from primary_results pr 
group by party,state,county,votes

--jaki % dystryktów w stanie głosował za republikanami a jaki za demokratami
select count(case when party='Democrat' and fraction_votes >0.5
then 1 END)/count(county) ::numeric as udzial_D,
count(case when party='Republican' and fraction_votes >0.5
then 1 END )/count(county) ::numeric as udzial_R
from primary_results

--jaki kandydat w ilu stanach brał uddział
select candidate,party,count(state)
from primary_results pr 
group by candidate,party 

--kto w jakim stanie miał największe poparcie
select county,candidate,percent_rank()over (partition by county order by votes)
from primary_results pr 
--kto wygrał w którym hrabstwie
select county ,candidate,max(fraction_votes)
from primary_results pr2 

--statustyki na kogo oddano nawiecej głosoów w kolejności kolejność max-min
select candidate, sum(votes)
from primary_results pr 
group by candidate 
order by sum(votes) desc 

