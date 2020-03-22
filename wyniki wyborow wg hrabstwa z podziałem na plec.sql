-- KOBIETY

-- wyniki wyborow wg hrabstwa z podzia�em na p�e� - tutaj woman
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * SEX255214/100) woman,
PST045214 -  (PST045214 * (SEX255214/100)) man,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where state is not null 
and county is not null
group by (pr.state, pr.county, PST045214, SEX255214)
order by state;

--MʯCZY�NI

-- wyniki wyborow wg hrabstwa z podzia�em na p�e� - tutaj man
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * SEX255214/100) woman,
PST045214 -  (PST045214 * (SEX255214/100)) man,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where state is not null 
and county is not null
group by (pr.state, pr.county, PST045214, SEX255214)
order by state;

-- POR�WNANIE
-- Ilo�ci osobno przez kobiety i m�czyzn

-- wyniki wyborow wg hrabstwa z podzia�em na p�e� - tutaj man
-- przewaga ilo�ci g�osuj�cych m�czyzn
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * SEX255214/100) woman,
PST045214 -  (PST045214 * (SEX255214/100)) man,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where PST045214 -  (PST045214 * (SEX255214/100)) > (PST045214 * SEX255214/100)
and state is not null 
and county is not null
group by (pr.state, pr.county, PST045214, SEX255214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na p�e� - tutaj man
-- przewaga ilo�ci g�osuj�cych kobiet
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * SEX255214/100) woman,
PST045214 -  (PST045214 * (SEX255214/100)) man,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where PST045214 -  (PST045214 * (SEX255214/100)) < (PST045214 * SEX255214/100)
and state is not null 
and county is not null
group by (pr.state, pr.county, PST045214, SEX255214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na p�e� - tutaj man
-- r�wnowaga ilo�ci g�osuj�cych kobiet i m�czyzn
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * SEX255214/100) woman,
PST045214 -  (PST045214 * (SEX255214/100)) man,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where PST045214 -  (PST045214 * (SEX255214/100)) = (PST045214 * SEX255214/100)
and state is not null 
and county is not null
group by (pr.state, pr.county, PST045214, SEX255214)
order by state;

