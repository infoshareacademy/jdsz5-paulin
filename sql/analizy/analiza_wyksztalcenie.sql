--golne zestawienie danych badanych, gdzie
--EDU635213 to High school graduate or higher, percent of persons age 25+, 2009-2013
-- EDU685213 to Bachelor's degree or higher, percent of persons age 25+, 2009-2013

--zalozenia: wiek 25=18, tak aby można było podzielić spleczenstwo na niewyksztalcone i wyksztalcone w wieku "nieszkolenym"
with demography as (
    select pr.state,
           pr.county,
           pr.fips,
           pr.state_abbreviation                                                                      as abv,
           cf.pst045214                                                                               as population,
           (cf.AGE295214 / 100) * cf.PST045214                                                        as school_age,
           (cf.AGE775214 / 100) * cf.PST045214                                                        as retire_age,
           cf.PST045214 - ((cf.AGE295214 / 100) * cf.PST045214 + (cf.AGE775214 / 100) * cf.PST045214) as productive_age
    from primary_results pr
             join county_facts cf on pr.fips = cf.fips
    group by pr.state, pr.county, pr.fips, cf.pst045214, cf.age295214, cf.age775214
),
--nie uzgledniono ososb w wieku 18+ ktore nie posiadaja nizszego wyksztalcenia niz high school,brak danych
     education as (
         select demography.state,
                demography.county,
                demography.abv,
                sum(demography.productive_age + demography.retire_age)              as voters,
                (demography.productive_age + demography.retire_age) *
                (cf2.EDU685213 / 100)                                               as super_educated,
                (demography.productive_age + demography.retire_age) *
                ((cf2.EDU635213 - cf2.EDU685213) / 100)                             as middle_educated,
                (demography.productive_age + demography.retire_age) *
                (1 - (cf2.EDU685213 / 100 + (cf2.EDU635213 - cf2.EDU685213) / 100)) as primary_non_educated
         from demography
                  join county_facts cf2 on demography.fips = cf2.fips
         group by demography.state, demography.county, cf2.edu685213, cf2.edu635213, demography.productive_age,
                  demography.retire_age
     ),

     podzial as (
         select edu.state,
                edu.county,
                case
                    when edu.super_educated / edu.voters >= edu.middle_educated / edu.voters and
                         edu.super_educated / edu.voters >= edu.primary_non_educated / edu.voters then 'super'
                    when edu.middle_educated / edu.voters > edu.super_educated / edu.voters and
                         edu.middle_educated / edu.voters > edu.primary_non_educated / edu.voters then 'srenio'
                    when edu.primary_non_educated / edu.voters > edu.super_educated / edu.voters and
                         edu.primary_non_educated / edu.voters > edu.middle_educated / edu.voters then 'slabo'
                    end       as                                        poziom_edu,
                sum(pr.votes) as                                        liczba_glosow,
                sum(case when pr.party like 'Repub%' then pr.votes end) republikanie,
                sum(case when pr.party like 'Democ%' then pr.votes end) demokraci
         from education as edu
                  join primary_results pr on edu.county = pr.county
                  join county_facts cf on pr.fips = cf.fips
         where edu.state not in ('Colodrado', 'North Dakota', 'Maine')
         group by poziom_edu, edu.state, edu.county),

     udzial as
         (select *,
                 republikanie / sum(republikanie) over ()::numeric d_republikanie,
                 demokraci / sum(demokraci) over ()::numeric       d_demokraci
          from podzial
         ),

     wsp as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from udzial),

     wsp2 as
             (select *, woe * dr_minus_dd iv from wsp)

select *, sum(iv) over () suma_iv
from wsp2





