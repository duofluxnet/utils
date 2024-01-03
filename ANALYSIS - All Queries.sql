select # 'distinct' should not be needed here!
 p.name,
 r.name as requires,
 r1.name,
 r2.name,
 r3.name,
 r4.name
from
 slackbuilds.package p 
 left join slackbuilds.requires r  on r.package_name = p.name 
 left join slackbuilds.requires r1 on r1.package_name  = r.name 
 left join slackbuilds.requires r2 on r2.package_name  = r1.name
 left join slackbuilds.requires r3 on r3.package_name  = r2.name
 left join slackbuilds.requires r4 on r4.package_name  = r3.name
where
 p.name in ('mongodb')
order BY 
 p.name,
 1, 2, 3, 4, 5, 6
;

select * from package where
   trim(coalesce(maintainer_name , '')) = ''
or trim(coalesce(maintainer_email, '')) = ''
or trim(coalesce(website_url, '')) 		= ''
;

select 
name,
LENGTH(maintainer_name),
LENGTH(maintainer_email),
LENGTH(website_url)
from package
group by name
order by 4  DESC 
;

select name, maintainer_name, maintainer_email, website_url  from package where name in ( 
'mag',
'pixma',
'yar',
'mod_bw',
'hunspell-pl',
'gqrx-sdr',
'pcp',
'spek',
'qt6'
);



select
 p.name,
 p.version,
 p.description,
 p.location,
 t.name as tag_name,
 r.name as requires,
 f.url 
from
 slackbuilds.package p 
 left join slackbuilds.tag t on t.package_name  = p.name 
 left join slackbuilds.requires r on r.package_name = p.name 
 left join slackbuilds.file f on f.package_name = p.name
where
 p.name in ('mongodb')
order BY 
 p.name,
 p.version,
 t.name,
 r.name,
 f.url 
;


SELECT * FROM slackbuilds.package r 	WHERE r.name 			= 'mongodb';
SELECT * FROM slackbuilds.requires r 	WHERE r.package_name 	= 'mongodb';
SELECT * FROM slackbuilds.tag r 		WHERE r.package_name 	= 'mongodb';
SELECT * FROM slackbuilds.file r 		WHERE r.package_name 	= 'mongodb';

select * from package where trim(coalesce(name, '')) = '';
select * from tag where trim(coalesce(name, '')) = '';
select * from requires where trim(coalesce(name, '')) = '';
select * from file where trim(coalesce(url, '')) = '';

delete from tag where trim(coalesce(name, '')) = '';
commit;


with dup as (
select name, count(*) as cnt from package group by name having count(*) > 1
)
select * from package where name in (select name from dup) order by 1, 2, 3, 4
;

SELECT LENGTH(r.name) as len, count(*) as cnt FROM slackbuilds.tag r group by LENGTH(r.name)
order by 1 asc

select LENGTH(t.name), t.* from slackbuilds.tag t where LENGTH(t.name) > 15 order by 1 desc  



select 
 p.location,
 t.name,
 p.version,
 p.name
from
 slackbuilds.package p 
 inner join slackbuilds.tag t on t.package_name = p.name
WHERE
     p.location in ('python')
 and t.name 	in ('rpython')
order BY 
 p.location,
 t.name,
 p.name 
;



select 
 p.maintainer_name ,
 p.maintainer_email ,
 count(distinct p.name) as pack_cnt,
 count(distinct p.location) as loc_uniq_cnt

from 
 package p 
group by
 p.maintainer_name ,
 p.maintainer_email
 order BY  
  3 desc
 ;
 
 