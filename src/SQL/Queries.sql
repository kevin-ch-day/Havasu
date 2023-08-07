-- Query records by sample families
SELECT *
FROM malware_samples
WHERE family = 'Anubis';

-- family and # of samples
select family, count(*)
from malware_samples
where family is not null
GROUP by Family

select *
from malware_samples
where Kaspersky_Label like '%Anubis%'
order by id;