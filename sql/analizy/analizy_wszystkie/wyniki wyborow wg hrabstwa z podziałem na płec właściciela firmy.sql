-- wyniki wyborow wg hrabstwa z podzia³em na p³ec w³aœciciela firmy - tutaj women
-- wynikiem s¹ hrabstwo Camas w stanie Idaho (republikanie), oraz hrabstwo Jefferson w stanie Missisippi (demokraci)
select distinct pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO015207/100) women,
SBO001207 - (SBO001207 * SBO015207/100) men,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO015207/100) > SBO001207 - (SBO001207 * SBO015207/100)
and state is not null 
and county is not null
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by state;

-- wyniki wyborow wg hrabstwa z podzia³em na p³ec w³aœciciela firmy - tutaj men
-- wiêkszoœæ hrabstw jest efektem tego zapytania
select pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO015207/100) women,
SBO001207 - (SBO001207 * SBO015207/100) men,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO015207/100) < SBO001207 - (SBO001207 * SBO015207/100)
and state is not null 
and county is not null

group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207, pr.party)
having pr.party = 'Democrat'
order by state;

