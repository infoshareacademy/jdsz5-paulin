--- wyjsciowe (p)
select pr.state,
       (select sum(pr1.votes) from primary_results pr1 where pr1.state = pr.state and pr1.party = 'Republican') as repu,
       (select sum(pr2.votes) from primary_results pr2 where pr2.state = pr.state and pr2.party = 'Democrat')   as demo
from primary_results pr
group by pr.state;

-- wyb�r patrii w danym stanie (P)
select pr.state,
       case
           when (select sum(pr1.votes) from primary_results pr1 where pr1.state = pr.state and pr1.party = 'Republican')
               > (select sum(pr2.votes) from primary_results pr2 where pr2.state = pr.state and pr2.party = 'Democrat')
               then 'republican'
           else 'democrat'
           end as wynik
from primary_results pr
group by pr.state
order by pr.state;

-- suma os�b g�osuj�cych z podzia�em na stan i wiek
select distinct pr1.state,
                sum(cf1.POP010210 * cf1.AGE135214) as demo_under_5,
                sum(cf1.POP010210 * cf1.AGE295214) as demo_under_18,
                sum(cf1.POP010210 * cf1.AGE775214) as demo_over_65,
                sum(cf1.POP010210 * cf2.AGE135214) as repu_under_5,
                sum(cf1.POP010210 * cf2.AGE295214) as repu_under_18,
                sum(cf1.POP010210 * cf2.AGE775214) as repu_over_65
from county_facts cf1
         left join primary_results pr1 on cf1.fips = pr1.fips
         left join county_facts cf2 on cf1.fips = cf2.fips
         left join primary_results pr2 on cf1.fips = pr2.fips
where pr1.party ilike '%demo%'
  and pr2.party ilike '%repu%'
group by 1;

-- zapytanie ktore pokaze jaka grupa narodowosciowa by�a najliczniejsza w danym stanie
-- liczebnsc narodowosci
select distinct state,
                sum((RHI125214 / 100) * PST045214) as white,
                sum((RHI225214 / 100) * PST045214) as black,
                sum((RHI325214 / 100) * PST045214) as indian,
                sum((RHI425214 / 100) * PST045214) as asian,
                sum((RHI525214 / 100) * PST045214) as hawaii,
                sum((RHI625214 / 100) * PST045214) as two_or_more,
                sum((RHI725214 / 100) * PST045214) as hispanic,
                sum((RHI825214 / 100) * PST045214) as white_alone
from primary_results pr
         left join county_facts cf on cf.fips = pr.fips
group by state
order by state;

-- najwi�ksze argumenty dot. Narodowo�ci
select distinct state,
                greatest(
                        sum((RHI125214 / 100) * PST045214),
                        sum((RHI225214 / 100) * PST045214),
                        sum((RHI325214 / 100) * PST045214),
                        sum((RHI425214 / 100) * PST045214),
                        sum((RHI525214 / 100) * PST045214),
                        sum((RHI625214 / 100) * PST045214),
                        sum((RHI725214 / 100) * PST045214),
                        sum((RHI825214 / 100) * PST045214)
                    )
from primary_results pr
         left join county_facts cf on cf.fips = pr.fips
group by state, RHI125214,
         RHI225214, RHI325214,
         RHI425214, RHI525214,
         RHI625214, RHI725214,
         RHI825214, PST045214
order by state;