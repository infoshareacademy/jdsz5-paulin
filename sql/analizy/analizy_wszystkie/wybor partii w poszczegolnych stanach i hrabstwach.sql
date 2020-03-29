-- wybór partii w danym stanie
select pr.state,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.state = pr.state and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.state = pr.state and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from primary_results pr
group by pr.state
order by pr.state;

-- wybór partii w danym hrabstwie
select  distinct pr.state, pr.county,
case
when (select sum(pr1.votes) from primary_results pr1 where pr1.county = pr.county and pr1.party = 'Republican')
> (select sum(pr2.votes) from primary_results pr2 where pr2.county = pr.county and pr2.party = 'Democrat') then 'republican'
else 'democrat'
end as wynik
from primary_results pr
group by pr.county, pr.state, pr.party
order by pr.state 