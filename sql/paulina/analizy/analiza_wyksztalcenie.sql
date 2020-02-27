--golne zestawienie danych badanych, gdzie
--EDU635213 to High school graduate or higher, percent of persons age 25+, 2009-2013
-- EDU685213 to Bachelor's degree or higher, percent of persons age 25+, 2009-2013

--zalozenia: wiek 25=18, tak aby można było podzielić spleczenstwo na niewyksztalcone i wyksztalcone w wieku "nieszkolenym"
with demography as (
select pr.state,pr.county,pr.fips,cf.pst045214,(cf.AGE295214/100)*cf.PST045214 as school_age,
(cf.AGE775214/100)*cf.PST045214 as retire_age,
cf.PST045214-((cf.AGE295214/100)*cf.PST045214+(cf.AGE775214/100)*cf.PST045214) as productive_age
from primary_results pr 
join county_facts cf on pr.fips =cf.fips
group by pr.state,pr.county,pr.fips,cf.pst045214 ,cf.age295214,cf.age775214
),
--nie uzgledniono ososb w wieku 18+ ktore nie posiadaja nizszego wyksztalcenia niz high school,brak danych
education as(
select demography.state, demography.county,sum(demography.productive_age+demography.retire_age) as voters,
(demography.productive_age+demography.retire_age)*(cf2.EDU685213/100) as super_educated,
(demography.productive_age+demography.retire_age)*((cf2. EDU635213-cf2.EDU685213)/100) as primary_educated
from demography
join county_facts cf2 on demography.fips=cf2.fips 
group by demography.state,demography.county,cf2.edu685213,cf2.edu635213,demography.productive_age,demography.retire_age
)
select * from education



