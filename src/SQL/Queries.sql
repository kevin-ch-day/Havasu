-- Query records by sample families
SELECT * FROM malware_samples WHERE family = 'Xenomorph';

-- family and # of samples
select family, count(*)
from malware_samples
where family is not null
GROUP by Family

select *
from malware_samples
where Kaspersky_Label like '%Anubis%'
order by id;

-- Dataset Label
SELECT id, Kaspersky_Label, Microsoft_Label
FROM malware_samples WHERE family = 'BlackRock'

-- MobSF Security Scorecard
SELECT id, security_score, grade, trackers_detections, high_risks, medium_risk
FROM mobfs_analysis
WHERE id in (75, 76, 77)