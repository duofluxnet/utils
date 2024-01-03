with loc_tag as (
	select 
	 p.location, 
	 t.name as tag_name,
	 count(distinct p.name) as uniq_pack_cnt 
	 #count(*) as cnt,
	 #count(*) - count(distinct p.name) as delta
	from
	 slackbuilds.package p 
	 inner join slackbuilds.tag t on t.package_name = p.name 
	group by 
	 p.location, 
	 t.name 
	having 
	 p.location <> t.name 
	order by
	 p.location asc, 
	 count(*) desc
)
, loc_tag_pb as (
	select 
	 location,
	 tag_name,
	 uniq_pack_cnt,
	 sum(uniq_pack_cnt) over (partition by location) as loc_grp_cnt 
	FROM
	 loc_tag
	order by
	 location,
	 uniq_pack_cnt desc
), tag_db as (
	select 
	 location,
	 tag_name,
	 uniq_pack_cnt,
	 loc_grp_cnt,
	 (uniq_pack_cnt / loc_grp_cnt) * 100.00 as tag_pc_in_loc_grp,
	 round(log(2, (uniq_pack_cnt / loc_grp_cnt) * 100.00) * 10, 1) as tag_power_db
	FROM 
	 loc_tag_pb
	order by
	 location, 
	 uniq_pack_cnt desc
)
select
 location,
 case
	 # filter-in only tag w/ power gt 3 dB (cut-off)! muhuahuaa
	 when tag_power_db > 3 then tag_name else 'NOISE' 
 end as tag_name,
 avg(tag_power_db) as avg_tag_power_db
from
 tag_db
group by
 location,
 2
order by
 location,
 3 desc
;
