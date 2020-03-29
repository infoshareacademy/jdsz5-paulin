-- wyniki wyborow wg stanu z podzia³em na wiek - tutaj pon.18 - brak wyników
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * AGE295214/100) under_18, (PST045214 * AGE775214/100) over_65, 
PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)) between_18_64,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * AGE295214/100) > (PST045214 * AGE775214/100)
and (PST045214 * AGE295214/100) > (PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)))
group by (pr.state, PST045214, AGE295214, AGE775214, pr.county)
order by state;

-- wyniki wyborow wg stanu z podzia³em na wiek - tutaj pow. 65
-- wynikiem jest tylko jedno hrabstwo Sumter w stanie Flodyda, 
-- dane z 2016 r: spo³eczeñstwo pon. 18: 7,1%, 18-64: 36,6%, a pow.65: 56,3%
-- wynik nie powinien dziwiæ ze wzglêdu na tam du¿y procent zamiaszkania ludzi pow. 65 r¿
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * AGE295214/100) under_18, (PST045214 * AGE775214/100) over_65, 
PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)) between_18_64,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * AGE775214/100) > (PST045214 * AGE295214/100)
and (PST045214 * AGE775214/100) > (PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)))
group by (pr.state, PST045214, AGE295214, AGE775214, pr.county)
order by state;

-- wyniki wyborow wg stanu z podzia³em na wiek - tutaj miêdzy 18 a 64 r¿
-- standardowo wiêkszoœæ wyborców by³a z tego przedzia³u wiekowego
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * AGE295214/100) under_18, (PST045214 * AGE775214/100) over_65, 
PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)) between_18_64,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)) > (PST045214 * AGE295214/100)
and PST045214 -  (PST045214 * (AGE775214/100)) - (PST045214 * (AGE295214/100)) > (PST045214 * AGE775214/100)
group by (pr.state, PST045214, AGE295214, AGE775214, pr.county)
order by state;
--------------
select state, 
PST045214 total, (PST045214 * EDU635213/100) high_school, 
(PST045214 * EDU685213/100) degree_or_higher, 
PST045214 -  (PST045214 * (EDU685213/100)) - (PST045214 * (EDU635213/100)) other
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips

-- wyniki wyborow wg stanu z podzia³em na edukacjê - tutaj EDU635213 (LO lub wy¿ej)
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * EDU635213/100) high_school, (PST045214 * EDU685213/100) degree_or_higher, 
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * EDU635213/100) > PST045214 -  (PST045214 * (EDU685213/100)) - (PST045214 * (EDU635213/100)) 
and (PST045214 * EDU635213/100) > (PST045214 * EDU685213/100)
group by (pr.state, PST045214, EDU635213, EDU685213, pr.county)
order by state;

-- wyniki wyborow wg stanu z podzia³em na edukacjê - tutaj EDU685213 (licencjat lub wy¿ej) 
-- brak wyników, mo¿liwe, ¿e powodem tego jest do³aczenie wszystkich do grupy 'EDU635213'
select distinct pr.state, pr.county,
PST045214 total, (PST045214 * EDU635213/100) high_school, (PST045214 * EDU685213/100) degree_or_higher, 
PST045214 -  (PST045214 * (EDU685213/100)) - (PST045214 * (EDU635213/100)) other,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from county_facts cf 
left join primary_results pr on pr.fips = cf.fips
where (PST045214 * EDU685213/100) > PST045214 -  (PST045214 * (EDU685213/100)) - (PST045214 * (EDU635213/100)) 
and (PST045214 * EDU685213/100) > (PST045214 * EDU635213/100)
group by (pr.state, PST045214, EDU635213, EDU685213, pr.county)
order by state;



