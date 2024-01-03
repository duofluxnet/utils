select
 ROW_NUMBER() OVER(),
 
 p.name,
 p.version,
 p.description,
 p.location,
 
 count(distinct r.name) as cnt_requires,
 group_concat(distinct r.name order by r.name SEPARATOR ', ') as requires,
 
 p.readme,
 p.slack_desc,
 
 group_concat(distinct t.name order by t.name SEPARATOR ', ') as tags,
 
 p.maintainer_name,
 p.maintainer_email,
 p.website_url,
 
 count(distinct f.url) as cnt_urls,
 group_concat(distinct f.url  order by f.url  SEPARATOR ', ')  as urls,
 
 p.ts

 
from
 slackbuilds.package p 
 left join slackbuilds.tag t on t.package_name  = p.name 
 left join slackbuilds.requires r on r.package_name = p.name 
 left join slackbuilds.file f on f.package_name = p.name
 
 
where 
    upper(p.name) 				like '%MONGODB%'
 or upper(p.description) 		like '%MONGODB%'
 or upper(p.location)	 		like '%MONGODB%'

 or upper(r.name)		 		like '%MONGODB%'
 
 or upper(p.readme) 			like '%MONGODB%'
 or upper(p.slack_desc)			like '%MONGODB%'
 
 or upper(t.name)		 		like '%MONGODB%'

 or upper(p.maintainer_name)	like '%MONGODB%'
 or upper(p.maintainer_email)	like '%MONGODB%'
 or upper(p.website_url)		like '%MONGODB%'
 
 or upper(f.url)			 	like '%MONGODB%'
 
 
GROUP BY 
 p.name,
 p.version,
 p.description,
 p.location,
 
 p.readme,
 p.slack_desc,
 
 p.maintainer_name,
 p.maintainer_email,
 p.website_url,

 p.ts

order BY 
 p.name,
 p.version,
 p.ts
;