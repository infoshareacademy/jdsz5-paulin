with black_or_african_alone_a as
         (
             select r.fips,
                    case
                        when f.RHI225214 < 20 then '1.1) niski udział czarnoskorych'
                        when f.RHI225214 < 40 then '1.2) sredni udział czarnoskorych'
                        else '1.3) wysoki udział czarnoskorych'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    0              demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) >
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
             limit 1050
         ),
     black_or_african_alone_b as
         (
             select r.fips,
                    case
                        when f.RHI225214 < 20 then '1.1) niski udział czarnoskorych'
                        when f.RHI225214 < 40 then '1.2) sredni udział czarnoskorych'
                        else '1.3) wysoki udział czarnoskorych'
                        end as     kategoria,
                    0              republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) <
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
         ),
     black_or_african_alone_1 as
         (
             select *
             from black_or_african_alone_a
             union
             select *
             from black_or_african_alone_b
         ),
     black_or_african_alone_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from black_or_african_alone_1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
         ),
     black_or_african_alone_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from black_or_african_alone_2
         ),
     black_or_african_alone_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from black_or_african_alone_3),
     black_or_african_alone_5 as
             (select *, woe * dr_minus_dd iv from black_or_african_alone_4),
     payment_a as
         (
             select r.fips,
                    case
                        when f.inc910213 < 20000 then '2.1) niskie dochody'
                        when f.inc910213 < 30000 then '2.2) srednie dochody'
                        else '2.3) wysokie dochody'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    0              demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) >
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
             limit 1050
         ),
     payment_b as
         (
             select r.fips,
                    case
                        when f.inc910213 < 20000 then '2.1) niskie dochody'
                        when f.inc910213 < 30000 then '2.2) srednie dochody'
                        else '2.3) wysokie dochody'
                        end as     kategoria,
                    0              republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) <
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
         ),
     payment_1 as
         (
             select *
             from payment_a
             union
             select *
             from payment_b
         ),
     payment_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from payment_1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
         ),
     payment_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from payment_2
         ),
     payment_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from payment_3),
     payment_5 as
             (select *, woe * dr_minus_dd iv from payment_4),
     immigrants_a as
         (
             select r.fips,
                    case
                        when f.POP645213 < 5 then '3.1) niski udzial imigrantow'
                        when f.POP645213 < 10 then '3.2) sredni udzial imigrantow'
                        when f.POP645213 < 20 then '3.3) wysoki udzial imigrantow'
                        else '3.4) bardzo wysoki udzial imigrantow'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    0              demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) >
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
             limit 1050
         ),
     immigrants_b as
         (
             select r.fips,
                    case
                        when f.POP645213 < 5 then '3.1) niski udzial imigrantow'
                        when f.POP645213 < 10 then '3.2) sredni udzial imigrantow'
                        when f.POP645213 < 20 then '3.3) wysoki udzial imigrantow'
                        else '3.4) bardzo wysoki udzial imigrantow'
                        end as     kategoria,
                    0              republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) <
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
         ),
     immigrants_1 as
         (
             select *
             from immigrants_a
             union
             select *
             from immigrants_b
         ),
     immigrants_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from immigrants_1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
         ),
     immigrants_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from immigrants_2
         ),
     immigrants_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from immigrants_3),
     immigrants_5 as
             (select *, woe * dr_minus_dd iv from immigrants_4),
     home_owners_1 as
         (
             select r.fips,
                    case
                        when f.HSG445213 < 60 then '4.1) odsetek osob posiadajacych dom na wlasnosc do 60%'
                        when f.HSG445213 < 70 then '4.2) odsetek osob posiadajacych dom na wlasnosc do 70%'
                        when f.HSG445213 < 75 then '4.3) odsetek osob posiadajacych dom na wlasnosc do 75%'
                        when f.HSG445213 < 80 then '4.4) odsetek osob posiadajacych dom na wlasnosc do 80%'
                        else '4.5) odsetek osob posiadajacych dom na wlasnosc 80% i wiecej'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
         ),
     home_owners_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from home_owners_1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
         ),
     home_owners_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from home_owners_2
         ),
     home_owners_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from home_owners_3),
     home_owners_5 as
             (select *, woe * dr_minus_dd iv from home_owners_4),
     woman_population_1 as
         (
             select r.fips,
                    case
                        when f.sex255214::numeric / 100 < 0.50 then '5.1) mniej niż połowa populacji stanowią kobiety'
                        else '5.2) więcej niż połowa populacji stanowią kobiety'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             where r.state not in ('Colodrado', 'North Dakota', 'Maine')
             group by r.fips, kategoria
         ),
     woman_population_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from woman_population_1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
         ),
     woman_population_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from woman_population_2
         ),
     woman_population_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from woman_population_3),
     woman_population_5 as
             (select *, woe * dr_minus_dd iv from woman_population_4),
     veterans_1 as
         (
             select r.fips,
                    case
                        when (VET605213 * 100) / POP010210::numeric < 6 then '6.1) udzial weteranow do 6%'
                        when (VET605213 * 100) / POP010210::numeric < 8 then '6.2) udzial weteranow do 8%'
                        when (VET605213 * 100) / POP010210::numeric < 10 then '6.3) udzial weteranow do 10%'
                        else '6.4) udzial weteranow pow 10%'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             where r.state not in ('Colodrado', 'North Dakota', 'Maine')
             group by r.fips, kategoria
         ),
     veterans_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from veterans_1
             where republikanie is not null
                or demokraci is not null
             group by kategoria
         ),
     veterans_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from veterans_2
         ),
     veterans_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from veterans_3),
     veterans_5 as
             (select *, woe * dr_minus_dd iv from veterans_4),
     age_a as
         (
             select r.fips,
                    case
                        when age775214 <= 15 then '7.1) niski udzial starszych osob'
                        when age775214 <= 20 then '7.2) sredni udzial'
                        else '7.3) bardzo wysoki'
                        end as     kategoria,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) >
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end republikanie,
                    0              demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) >
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
             limit 1050
         ),
     age_b as
         (
             select r.fips,
                    case
                        when age775214 <= 15 then '7.1) niski udzial starszych osob'
                        when age775214 <= 20 then '7.2) sredni udzial'
                        else '7.3) bardzo wysoki'
                        end as     kategoria,
                    0              republikanie,
                    case
                        when sum(case when r.party like 'Repub%' then r.votes end) <
                             sum(case when r.party like 'Democ%' then r.votes end) then 1
                        else 0 end demokraci
             from primary_results r
                      join county_facts f on r.fips = f.fips
             group by r.fips, kategoria
             having (case
                         when sum(case when r.party like 'Repub%' then r.votes end) <
                              sum(case when r.party like 'Democ%' then r.votes end) then 1
                         else 0 end) = 1
         ),
     age_1 as
         (
             select *
             from age_a
             union
             select *
             from age_b
         ),
     age_2 as
         (
             select kategoria, count(fips) liczba_hrabstw, sum(republikanie) republikanie, sum(demokraci) demokraci
             from age_1
             where republikanie <> 0
                or demokraci <> 0
             group by kategoria
         ),
     age_3 as
         (
             select *,
                    republikanie / sum(republikanie) over ()::numeric d_republikanie,
                    demokraci / sum(demokraci) over ()::numeric       d_demokraci
             from age_2
         ),
     age_4 as
         (select *,
                 ln(d_republikanie / d_demokraci) woe,
                 d_republikanie - d_demokraci     dr_minus_dd
          from age_3),
     age_5 as
             (select *, woe * dr_minus_dd iv from age_4),
     black_or_african_alone as (select *, sum(iv) over () suma_iv
                                from black_or_african_alone_5),
     payment as (select *, sum(iv) over () suma_iv
                 from payment_5),
     immigrants as (select *, sum(iv) over () suma_iv
                    from immigrants_5),
     home_owners as (select *, sum(iv) over () suma_iv
                     from home_owners_5),
     woman_population as (select *, sum(iv) over () suma_iv
                          from woman_population_5),
     veterans as (select *, sum(iv) over () suma_iv
                  from veterans_5),
     age as (select *, sum(iv) over () suma_iv
             from age_5)
select *
from black_or_african_alone
union
select *
from payment
union
select *
from immigrants
union
select *
from home_owners
union
select *
from woman_population
union
select *
from veterans
union
select *
from age
order by kategoria;



-- select *, sum(iv) over () suma_iv
-- from black_or_african_alone_5;
-- select *, sum(iv) over () suma_iv
-- from payment_5;
-- select *, sum(iv) over () suma_iv
-- from immigrants_5
-- select *, sum(iv) over () suma_iv
-- from home_owners_5
-- select *, sum(iv) over () suma_iv
-- from woman_population_5;
-- select *, sum(iv) over () suma_iv
-- from veterans_5;
-- select *, sum(iv) over () suma_iv
-- from age_5;











