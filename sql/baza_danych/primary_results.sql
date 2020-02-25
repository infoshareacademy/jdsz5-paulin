create table primary_results
(
	state varchar,
	state_abbreviation varchar,
	county varchar,
	fips integer,
	party varchar,
	candidate varchar,
	votes integer,
	fraction_votes numeric
);

alter table primary_results owner to postgres;

