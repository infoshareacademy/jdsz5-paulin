select * from county_facts cf ;
select * from county_facts_dictionary cfd ;
select * from primary_results pr 

select distinct candidate from primary_results pr 

select 
corr (fraction_votes, RHI125214) as ws_vs_bialy,
corr (fraction_votes, RHI225214) as ws_vs_czarny,
corr (fraction_votes, RHI325214) as ws_vs_indianin,
corr (fraction_votes, RHI425214) as ws_vs_azjata,
corr (fraction_votes, RHI525214) as ws_vs_hawajczyk,
corr (fraction_votes, RHI625214) as ws_vs_dwie_rasy,
corr (fraction_votes, RHI725214) as ws_vs_latynos,
corr (fraction_votes, RHI825214) as ws_vs_bialy_nie_latynos

from primary_results pr 
left join county_facts cf on cf.fips = pr.fips
where party ilike '%demo%'

-- korelacja narodowosci i wyksztalcenia -- wyroznia sie korelacja bialy nie latynos
select 
corr (EDU635213, RHI125214) as bialy,
corr (EDU635213, RHI225214) as czarny,
corr (EDU635213, RHI325214) as indianin,
corr (EDU635213, RHI425214) as azjata,
corr (EDU635213, RHI525214) as hawajczyk,
corr (EDU635213, RHI625214) as dwie_rasy,
corr (EDU635213, RHI725214) as latynos,
corr (EDU635213, RHI825214) as bialy_nie_latynos

from county_facts cf2 
 -- korelacja narodowosci i wyksztalcenia 2 -- wyroznia sie korelacja z azjatami
select 
corr (RHI125214, EDU685213) as bialy,
corr (RHI225214, EDU685213) as czarny,
corr (EDU685213, RHI325214) as indianin,
corr (EDU685213, RHI425214) as azjata,
corr (EDU685213, RHI525214) as hawajczyk,
corr (EDU685213, RHI625214) as dwie_rasy,
corr (EDU685213, RHI725214) as latynos,
corr (EDU685213, RHI825214) as bialy_nie_latynos

from county_facts cf2 

-- korelacja narodowosci i wlascicieli firm -- wyrazne korelacje
select 

corr (SBO315207, RHI225214) as czarny,
corr (SBO115207, RHI325214) as indianin,
corr (SBO215207, RHI425214) as azjata,
corr (SBO515207, RHI525214) as hawajczyk,
corr (SBO415207, RHI725214) as latynos,
corr(
(SBO001207 - SBO315207 + SBO115207 + SBO215207 + SBO515207 + SBO415207), RHI125214) as bialy --??
from county_facts cf 

--
select 
corr (PVY020213, RHI125214) as bialy,
corr (PVY020213, RHI225214) as czarny,
corr (PVY020213, RHI325214) as indianin,
corr (PVY020213, RHI425214) as azjata,
corr (PVY020213, RHI525214) as hawajczyk,
corr (PVY020213, RHI625214) as dwie_rasy,
corr (PVY020213, RHI725214) as latynos,
corr (PVY020213, RHI825214) as bialy_nie_latynos
from county_facts cf2

