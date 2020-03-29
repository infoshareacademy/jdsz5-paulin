--------------------------------------------------
wskazniki as(
select unnest(
percentile_disc(array[0.90,0.95,0.97,0.99])
within group (order by df2.udzial_czarnych_firm)) as
kwantyl_udzial_czarnych_firm
from df2)
select* from wskazniki
--------------------------------------------------
with df1 as (
	select pr.state,pr.county,pr.votes,pr.party,cf.SBO315207/100 as udzial_czarnych_firm,
	cf.SBO001207 as totall_ilo_firm
	from primary_results pr
	join county_facts cf on pr.fips = cf.fips
	where pr.state not in ('Colodrado', 'North Dakota', 'Maine')
	group by pr.state, pr.county, pr.votes, pr.party,cf.SBO001207,cf.SBO315207),
df2 as
(
select df1.county,
case 
when df1.udzial_czarnych_firm<=0.05 then '1) bardzo_malo_firm'
when df1.udzial_czarnych_firm<=0.2 then '2) malo_firm'
when df1.udzial_czarnych_firm<=0.4 then '3) umiarkowanie_firm'
when df1.udzial_czarnych_firm>0.4 then '4) duzo_firm'
end as kategoria,
case when sum(case when df1.party like 'Repub%'then df1.votes end)>sum(case when df1.party like 'Democ%' then df1.votes end) then 1 else 0 end republikanie,
case when sum(case when df1.party like 'Repub%'then df1.votes end)<sum(case when df1.party like 'Democ%' then df1.votes end) then 1 else 0 end demokraci
from df1
group by df1.county,kategoria
),
df3 as
(
select kategoria, count(county) ilo_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci  
from df2
where republikanie<>0 or demokraci<>0
group by kategoria
order by kategoria
),
df4 as
(
select *,
republikanie/sum(republikanie) over()::numeric d_republikanie,
demokraci/sum(demokraci) over()::numeric d_demokraci
from df3
),
df5 as
(select *,
ln(d_republikanie/d_demokraci) woe,
d_republikanie-d_demokraci dr_minus_dd
from df4),
df6 as
(select *, woe*dr_minus_dd  iv from df5)

select *, sum(iv) over() suma_iv from df6
