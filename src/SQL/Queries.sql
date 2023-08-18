-- Query records by sample families
SELECT *
FROM malware_samples
WHERE family = 'Xenomorph';

-- family and # of samples
select family, count(*)
from malware_samples
where family is not null
GROUP by Family

-- Dataset Label
SELECT x.id,
    x.Kaspersky_Label Kaspersky,
    x.Microsoft_Label Microsoft
FROM x.malware_samples
WHERE x.family = 'BlackRock'

-- MobSF Security Scorecard by family
SELECT y.id,
	y.security_score score,
    y.grade,
    y.trackers_detections tracker,
    y.high_risks,
    y.medium_risks
FROM malware_samples x
	JOIN mobfs_analysis y
    	ON y.id = x.id
WHERE x.family = 'brata';

-- static analysis chart
select x.id,
	x.size,
	y.activities,
    y.services,
    y.receivers,
    y.providers
from malware_samples x
	join mobfs_analysis y
		on y.id = x.id
where x.family = 'brata'
order by x.id;

-- Dangerous Permissions
SELECT x.permission_id,
	x.permission_name
FROM android_permissions x
where x.permission_status = 'Dangerous'
order by x.permission_name asc;

-- non-dangerous permissions
SELECT x.permission_id,
	x.permission_name
FROM android_permissions x
where not x.permission_status = 'Dangerous'
order by x.permission_name asc;

-- normal permissions
SELECT x.permission_id,
	x.permission_name
FROM android_permissions x
where x.permission_status = 'Normal'
order by x.permission_name asc;

SELECT x.permission_id,
	x.permission_name
FROM android_permissions x
where x.permission_status = 'Not for use by third-party apps.'
order by x.permission_name asc;