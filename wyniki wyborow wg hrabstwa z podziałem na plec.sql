-- KOBIETY

-- wyniki wyborow wg hrabstwa z podzia³em na p³eæ - tutaj woman
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

--MÊ¯CZYNI

-- wyniki wyborow wg hrabstwa z podzia³em na p³eæ - tutaj man
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

-- PORÓWNANIE
-- Iloœci osobno przez kobiety i mê¿czyzn

-- wyniki wyborow wg hrabstwa z podzia³em na p³eæ - tutaj man
-- przewaga iloœci g³osuj¹cych mê¿czyzn
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

-- wyniki wyborow wg hrabstwa z podzia³em na p³eæ - tutaj man
-- przewaga iloœci g³osuj¹cych kobiet
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

-- wyniki wyborow wg hrabstwa z podzia³em na p³eæ - tutaj man
-- równowaga iloœci g³osuj¹cych kobiet i mê¿czyzn
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

