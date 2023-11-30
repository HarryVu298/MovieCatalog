select distinct rating from movies.amazon
union
select distinct rating from movies.disney
union
select distinct rating from movies.hulu
union
select distinct rating from movies.netflix;