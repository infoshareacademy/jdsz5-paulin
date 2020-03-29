-- SBO001207	Total number of firms, 2007
--
-- SBO315207	Black-owned firms, percent, 2007
-- SBO115207	American Indian- and Alaska Native-owned firms, percent, 2007
-- SBO215207	Asian-owned firms, percent, 2007
-- SBO515207	Native Hawaiian- and Other Pacific Islander-owned firms, percent, 2007
-- SBO415207	Hispanic-owned firms, percent, 2007
-- SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100)	other-owned
--
-- SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207

-- wyniki wyborow wg hrabstwa z podzia³em na firmê - tutaj black_owned

--- najwiêkszy idzia³ w wyborach czarnoskórzy przedsiêbiorcy mieli w stanie Alabama (kilka hrabstw)
-- oraz w hrabstwie Hancock w stanie Georgia 
-- wiêkszoœc odda³a swoje g³osy na republikanów, jedynym wyj¹tkiem by³ohrabstwo Wilcox w stanie Alabama
select distinct pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO315207/100) black_owned,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO315207/100) > (SBO001207 * SBO115207/100)
and (SBO001207 * SBO315207/100) > (SBO001207 * SBO215207/100)
and (SBO001207 * SBO315207/100) > (SBO001207 * SBO515207/100)
and (SBO001207 * SBO315207/100) > (SBO001207 * SBO415207/100)
and (SBO001207 * SBO315207/100) > (SBO001207 * SBO015207/100)
and (SBO001207 * SBO315207/100) > SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - 
(SBO001207 * SBO215207/100) - (SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100))
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by state;

-- wyniki wyborow wg hrabstwa z podzia³em na firmê - tutaj indian owned -- brak wyników
select distinct pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO115207/100) indian_owned,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO115207/100) > (SBO001207 * SBO315207/100)
and (SBO001207 * SBO115207/100) > (SBO001207 * SBO215207/100)
and (SBO001207 * SBO115207/100) > (SBO001207 * SBO515207/100)
and (SBO001207 * SBO115207/100) > (SBO001207 * SBO415207/100)
and (SBO001207 * SBO115207/100) > (SBO001207 * SBO015207/100)
and (SBO001207 * SBO115207/100) > SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - 
(SBO001207 * SBO215207/100) - (SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100))
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by state;

-- wyniki wyborow wg hrabstwa z podzia³em na firmê - tutaj asian owned -- brak wyników
select distinct pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO215207/100) asian_owned,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO215207/100) > (SBO001207 * SBO115207/100)
and (SBO001207 * SBO215207/100) > (SBO001207 * SBO315207/100)
and (SBO001207 * SBO215207/100) > (SBO001207 * SBO515207/100)
and (SBO001207 * SBO215207/100) > (SBO001207 * SBO415207/100)
and (SBO001207 * SBO215207/100) > (SBO001207 * SBO015207/100)
and (SBO001207 * SBO215207/100) > SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - 
(SBO001207 * SBO215207/100) - (SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100))
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by state;

-- wyniki wyborow wg hrabstwa z podzia³em na firmê - tutaj hawaii owned -- brak wyników
select distinct pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO515207/100) hawaii_owned,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO515207/100) > (SBO001207 * SBO115207/100)
and (SBO001207 * SBO515207/100) > (SBO001207 * SBO215207/100)
and (SBO001207 * SBO515207/100) > (SBO001207 * SBO315207/100)
and (SBO001207 * SBO515207/100) > (SBO001207 * SBO415207/100)
and (SBO001207 * SBO515207/100) > (SBO001207 * SBO015207/100)
and (SBO001207 * SBO515207/100) > SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - 
(SBO001207 * SBO215207/100) - (SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100))
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by state;

-- wyniki wyborow wg hrabstwa z podzia³em na firmê - hispanic -- brak wyników
select distinct pr.state, pr.county,
SBO001207 total, 
(SBO001207 * SBO415207/100) hispanic_owned,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (SBO001207 * SBO415207/100) > (SBO001207 * SBO115207/100)
and (SBO001207 * SBO415207/100) > (SBO001207 * SBO215207/100)
and (SBO001207 * SBO415207/100) > (SBO001207 * SBO515207/100)
and (SBO001207 * SBO415207/100) > (SBO001207 * SBO315207/100)
and (SBO001207 * SBO415207/100) > (SBO001207 * SBO015207/100)
and (SBO001207 * SBO415207/100) > SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - 
(SBO001207 * SBO215207/100) - (SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100))
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by state;

-- wyniki wyborow wg hrabstwa z podzia³em na firmê - tutaj other-owner
-- tutaj znalaz³y siê wszystkie firmy pozosta³ych w³aœcicieli, prawdopodobnie wiêkszoœæ z tych firm
-- prowadz¹ ludzie koloru skóry bia³ej lub 'mieszanej'
select distinct pr.state, pr.county,
SBO001207 total, 
SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - (SBO001207 * SBO215207/100) - 
(SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100)) other,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - (SBO001207 * SBO215207/100) - 
(SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100)) 
> (SBO001207 * SBO315207/100)
and SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - (SBO001207 * SBO215207/100) - 
(SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100)) 
> (SBO001207 * SBO115207/100)
and SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - (SBO001207 * SBO215207/100) - 
(SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100)) 
> (SBO001207 * SBO215207/100)
and SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - (SBO001207 * SBO215207/100) - 
(SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100)) 
> (SBO001207 * SBO515207/100)
and SBO001207 - ((SBO001207 * SBO315207/100) - (SBO001207 * SBO115207/100) - (SBO001207 * SBO215207/100) - 
(SBO001207 * SBO515207/100) - (SBO001207 * SBO415207/100)) 
> (SBO001207 * SBO415207/100)
and state is not null 
and county is not null
group by (pr.state, pr.county, SBO315207, SBO115207, SBO215207, SBO515207, SBO415207, SBO015207, SBO001207)
order by wynik;