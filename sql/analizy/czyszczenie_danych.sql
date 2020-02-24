--SQLe, ktore uzupeniaja brak wartosci w polu fips w tabeli primary_results fipsem znajdujcym sie w tabeli county_facts
--braki dotycza tylko jdnego stanu oznaczonego skrotem NH

--1 SQL wybierajacy rekordy z brakujacym fipsem
select county, state_abbreviation, fips from primary_results where fips is null

--2 SQL z polem fips, ktre powinno byc wykorzystane do uzupelnenia braku w tabeli primary_results
select area_name,state_abbreviation,fips from county_facts where area_name like 'Carroll%' and state_abbreviation='NH'

--3 - lista SQL, ktore wyczyszcza brak w polu fips w tabeli primary_results. Trzeba je uruchomic na swojej bazie.
update primary_results set fips=(select fips from county_facts 
where area_name like 'Belknap%') where county='Belknap';
update primary_results set fips=(select fips from county_facts where area_name like 'Carroll%' and state_abbreviation='NH') 
where county='Carroll' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Cheshire%' and state_abbreviation='NH') 
where county='Cheshire' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Coos%' and state_abbreviation='NH') 
where county='Coos' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Grafton%' and state_abbreviation='NH') 
where county='Grafton' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Hillsborough%' and state_abbreviation='NH') 
where county='Hillsborough' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Merrimack%' and state_abbreviation='NH') 
where county='Merrimack' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Rockingham%' and state_abbreviation='NH') 
where county='Rockingham' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Strafford%' and state_abbreviation='NH') 
where county='Strafford' and state_abbreviation='NH';
update primary_results set fips=(select fips from county_facts where area_name like 'Sullivan%' and state_abbreviation='NH') 
where county='Sullivan' and state_abbreviation='NH';