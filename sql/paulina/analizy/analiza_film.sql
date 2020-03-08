--okreslenie poziomow bezrobocia
wskazniki as(
select unnest(
percentile_disc(array[0.25, 0.5,0.80,0.9,0.95,0.96,0.98,0.99])
within group (order by wsad.zmiana_zatrudnienia_nierol_rok)) as
kwantyl_zmiana_zatrudnienia,
unnest(array[0.25, 0.5,0.80,0.9,0.95,0.96,0.98,0.99])
as rzad_kwantylu
from wsad)
--------------------------------------------------------------------------------
--analiza firm -nierolniczych
--------------------------------------------------------------------------------
with wsad as 
(select pr.state,pr.county,pr.votes,pr.party,cf.BZA010213 as ilo_firm_nierol, cf.BZA110213 as zatrudnienia_nierol,
case when cf.BZA010213>0 then cf.SBO001207-cf.BZA010213
when cf.BZA010213=0 then 0 end as ilo_firm_rol,
cf.BZA115213 as zmiana_zatrudnienia_nierol_rok, cf.SBO001207 as ilo_firm,
case when cf.SBO001207>0 then cf.BZA010213/cf.SBO001207
when cf.SBO001207=0 then 0 end::numeric as udzial_nierol_firm,
cf.BZA110213/cf.BZA010213 as os_na_firma_nierol,
cf.PST045214-((cf.AGE295214/100)*cf.PST045214+(cf.AGE775214/100)*cf.PST045214) as productive_age,
((cf.BZA110213/cf.BZA010213)*((cf.PST045214-((cf.AGE295214/100)*cf.PST045214+(cf.AGE775214/100)*cf.PST045214))/cf.PST045214))/100 as udzial_zatrudnienia_nierol
from primary_results pr 
join county_facts cf on pr.fips =cf.fips
group  by pr.state, pr.county,pr.votes,pr.party,cf.pst045214,cf.age295214,cf.age775214,cf.BZA010213,
cf.BZA110213 ,cf.BZA115213,cf.SBO001207),
--pogrupowanie hrabstw wzg.zmian zatrudnienia 
zmiany as (
select case 
when w.zmiana_zatrudnienia_nierol_rok<0 then 'spadek'
when w.zmiana_zatrudnienia_nierol_rok<=1.3 then 'powolny_wzrost'
when w.zmiana_zatrudnienia_nierol_rok<=5 then 'umiarkowany_wzrost'
when w.zmiana_zatrudnienia_nierol_rok>=8.8 then 'szybki_wzrost'
when w.zmiana_zatrudnienia_nierol_rok<8.8 then 'hiper_wzrost' end as zmiany_zatrudnienia_nierol,
sum(w.votes) as liczba_glosow,
sum(case when w.party like 'Repub%'then w.votes end) republikanie,
sum(case when w.party like 'Democ%' then w.votes end) demokraci
from wsad as w
where w.state not in ('Colodrado', 'North Dakota', 'Maine')
group by zmiany_zatrudnienia_nierol
order by zmiany_zatrudnienia_nierol
),
k2 as 
(select *,
z.republikanie/sum(z.republikanie) over()::numeric d_republikanie,
z.demokraci/sum(z.demokraci) over()::numeric d_demokraci
from zmiany as z
),
k3 as
(select *,
ln(d_republikanie/d_demokraci) woe,
d_republikanie-d_demokraci dr_minus_dd
from k2),
k4 as
(select *, woe*dr_minus_dd  iv from k3)

select *, sum(iv) over() suma_iv from k4
--w wyliczen "spadek" jest jedynym ŚREDNIM PREDYKTOREM


--jako sprawdzenie poprawności podziału kwantyli
wskazniki2 as (
select z.*,stddev(z.liczba_glosow) as std_zmian_gosp
from zmiany as z
group by z.liczba_glosow,z.zmiany_zatrudnienia,z.republikanie
)
select * from wskazniki2

---------------------------------------------------------------
--analiza bezrobocia i biedy
---------------------------------------------------------------
--do wyznaczeni przedzialow
wskaz as(
select unnest(
percentile_disc(array[0.1,0.75,1])
within group (order by udzial_bezrobocie)) as
kwantyl_bezrobocie,
unnest(array[0.1,0.75,1])
as rzad_kwantylu_b,
unnest(
percentile_disc(array[0.0005,0.01,0.05, 0.5,0.99])
within group (order by poziom_ubustwa)) as
kwantyl_ubustwa,
unnest(array[0.0005,0.01,0.05, 0.5,0.99])
as rzad_kwantylu_u
from df1)
-------------------------------------------------
--analiza
-------------------------------------------------

with df1 as 
(select pr.state,pr.county,pr.votes,pr.party, 
cf.NES010213/(cf.PST045214-((cf.AGE295214/100)*cf.PST045214+(cf.AGE775214/100)*cf.PST045214)) as udzial_bezrobocia, 
(cf.PST045214-((cf.AGE295214/100)*cf.PST045214+(cf.AGE775214/100)*cf.PST045214))-cf.NES010213 as pracujacy,
cf.SBO001207 as ilo_firm,cf.PVY020213 as poziom_ubustwa
from primary_results pr 
join county_facts cf on pr.fips =cf.fips
group  by pr.state, pr.county,pr.votes,pr.party,cf.nes010213,cf.pst045214,cf.pvy020213,cf.age295214,cf.age775214,cf.SBO001207
),

zmiany as (
select df1.state,case 
when df1.udzial_bezrobocia <=0.08 then 'niskie_bezrobocie'
when df1.udzial_bezrobocia <=0.10 then 'umiarkowane_bezrobocie'
when df1.udzial_bezrobocia >0.1 then 'wysokie_bezrobocie' end as poziom_bezrobocia,
case 
when df1.poziom_ubustwa <=8 then 'bardzo_niskie_ubustwo'
when df1.poziom_ubustwa <=13 then 'niskie_ubustwo'
when df1.poziom_ubustwa <=20 then 'umiarkowane_ubustwo'
when df1.poziom_ubustwa <=29 then 'wysokie_ubustwo'
when df1.poziom_ubustwa >20 then 'bardzo_wysokie_ubustwo'
end as poziom_ubustwa,
sum(df1.votes) as liczba_glosow,
sum(case when df1.party like 'Repub%'then df1.votes end) republikanie,
sum(case when df1.party like 'Democ%' then df1.votes end) demokraci
from df1
where df1.state not in ('Colodrado', 'North Dakota', 'Maine')
group by df1.state,df1.udzial_bezrobocia,df1.poziom_ubustwa
--order by zmiany_zatrudnienia_nierol
),
k2 as 
(select *,
z.republikanie/sum(z.republikanie) over()::numeric d_republikanie,
z.demokraci/sum(z.demokraci) over()::numeric d_demokraci
from zmiany as z
),
k3 as
(select *,
ln(d_republikanie/d_demokraci) woe,
d_republikanie-d_demokraci dr_minus_dd
from k2),
k4 as
(select *, woe*dr_minus_dd  iv from k3)

select *, sum(iv) over() suma_iv from k4
--w wyliczen "spadek" jest jedynym ŚREDNIM PREDYKTOREM
----------------------------------------------------------
--analiza_firm_ze_wzgledu_na narodowości
-------------------------------------------------------
with base as(
select pr.state, pr.county,sum(pr.votes) as ilo_glosow,pr.party, SBO001207 as ilo_firm, SBO315207 as udzial_czarnych_wl,SBO115207 as udzial_native_wl,
SBO215207 as udzial_asian_wl, SBO515207 as udzial_pacyfic_island_wl,
SBO415207 as udzial_spain_wl, SBO015207 as udzial_female_wl,
(cf.PST045214-((cf.AGE295214/100)*cf.PST045214+(cf.AGE775214/100)*cf.PST045214))-cf.NES010213 as pracujacy
from primary_results pr 
join county_facts cf on pr.fips =cf.fips
group  by pr.state, pr.county,pr.party,cf.sbo001207,cf.sbo315207,cf.sbo115207,cf.sbo215207,cf.sbo515207,
cf.sbo415207,cf.sbo015207,cf.pst045214,cf.age295214,cf.age775214,cf.nes010213
),
--udzial_czarnych właścicieli w firmach z podziałem dla republikan i demokratów (tutaj uwzględnić jeszcz pozostałe nacje)
df1 as (
select base.state, base.county,1-(base.udzial_czarnych_wl/100) as udzial_czarnych_firm,
1-(base.udzial_native_wl/100) as udzial_native_firm,
1-(base.udzial_asian_wl/100) as udzial_asian_firm,
1-(base.udzial_pacyfic_island_wl/100) as udzial_pacific_firm,
1-(base.udzial_spain_wl/100) as udzial_spain_firm,
sum(case when base.party like 'Repub%'then base.ilo_glosow end) republikanie,
sum(case when base.party like 'Democ%' then base.ilo_glosow end) demokraci
from base
group by base.state, base.county,base.udzial_czarnych_wl,base.ilo_firm,base.ilo_glosow,
base.udzial_native_wl,base.udzial_asian_wl,base.udzial_pacyfic_island_wl,base.udzial_spain_wl

)
select * from df1




