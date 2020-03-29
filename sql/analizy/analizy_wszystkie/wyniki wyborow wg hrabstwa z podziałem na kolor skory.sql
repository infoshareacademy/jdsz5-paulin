-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj white (w por�wnaniu z pozosta�ymi)
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI125214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj white
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI125214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI125214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj black ( w por�wnaniu z pozosta�ymi)
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI225214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj black
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI225214/100) black,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI225214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI225214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj indian (w por�wnaniu w pozosta�ymi)
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI325214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI825214/100)
and state is not null 
and county is not null
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj indian
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI325214/100) indian,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI325214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI325214/100) > (PST045214 * RHI825214/100)
and state is not null 
and county is not null
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj asian (w por�wnaniu z pozosta�ymi)
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI425214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI825214/100)
and state is not null 
and county is not null
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj asian
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI425214/100) asian,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI425214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI425214/100) > (PST045214 * RHI825214/100)
and state is not null 
and county is not null
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj hawaii (w por�wnaniu z pozosta�ymi) - brak wynik�w
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI525214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI525214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI525214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI525214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI525214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI525214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI525214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj two or more races (w por�wnaniu z pozosta�ymi) - brak wynik�w
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI625214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI625214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI625214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI625214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI625214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI625214/100) > (PST045214 * RHI725214/100)
and (PST045214 * RHI625214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj hispanic (w por�wnaniu z pozosta�ymi)
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI725214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj hispanic
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI725214/100) hispanic,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI725214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI725214/100) > (PST045214 * RHI825214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;

-- wyniki wyborow wg hrabstwa z podzia�em na kolor sk�ry - tutaj white alone (w por�wnaniu z z pozosta�ymi) - brak wynik�w
select distinct pr.state, pr.county,
PST045214 total, 
(PST045214 * RHI125214/100) white,
(PST045214 * RHI225214/100) black,
(PST045214 * RHI325214/100) indian,
(PST045214 * RHI425214/100) asian,
(PST045214 * RHI525214/100) hawaii,
(PST045214 * RHI625214/100) two_or_more,
(PST045214 * RHI725214/100) hispanic,
(PST045214 * RHI825214/100) white_alone,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * RHI825214/100) > (PST045214 * RHI125214/100)
and (PST045214 * RHI825214/100) > (PST045214 * RHI225214/100)
and (PST045214 * RHI825214/100) > (PST045214 * RHI325214/100)
and (PST045214 * RHI825214/100) > (PST045214 * RHI425214/100)
and (PST045214 * RHI825214/100) > (PST045214 * RHI525214/100)
and (PST045214 * RHI825214/100) > (PST045214 * RHI625214/100)
and (PST045214 * RHI825214/100) > (PST045214 * RHI725214/100)
group by (pr.state, PST045214, pr.county, RHI125214, RHI225214, RHI325214, RHI425214, RHI525214, RHI625214, RHI725214, RHI825214)
order by state;