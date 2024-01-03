WITH RECURSIVE packdep (rn, name, idx, lvl) AS (

	SELECT
	 0 AS rn,
	 r.name AS name,
	 CAST(concat(0) AS VARCHAR(1000)) as idx,
	 CAST(concat(r.name, '') AS VARCHAR(1000)) as lvl
	 
	FROM
	 package r
	 
	WHERE
	 # PARAMETER PACKAGE NAME -----------------------------------------
	 r.name in ('lua')
	 # ----------------------------------------------------------------
	 
 UNION
		
	SELECT
	 p.rn + 1 AS rn,
	 r.name	AS name,
	 CAST(concat(p.idx, '.', p.rn + 1) AS VARCHAR(1000)) as idx,
	 CONCAT(p.lvl, ' -> ', r.name)  AS lvl
	 
	FROM
	 requires r
	 INNER JOIN packdep p ON r.package_name = p.name
	 
)

, depseq AS (

	SELECT
	 p.name,
	 MAX(p.rn) AS seq_no
	 
	FROM
	 packdep p
	 
	GROUP BY
	 p.name
	 
	ORDER BY
	 MAX(p.rn) DESC
	 
)

, cmd_qry AS (
	SELECT
	 d.seq_no,
	 d.name,
	 p.version,
	 p.description,
	 CONCAT('/opt/slackbuilds/15.0/', p.location, '/', p.name, '/', ' ') AS pack_path,
	 CONCAT('cd /opt/slackbuilds/15.0/', p.location, '/', p.name, '/', ' ') AS location_path,
	 f.url,
	 CONCAT('wget ', f.url, ' ') AS url_wget,
	 CONCAT('./', p.name, '.SlackBuild', ' ') AS build_cmd,
	 CONCAT('/tmp/', p.name, '-', p.version, '-x86_64-1_SBo.tgz', ' ') AS tgz,
	 CONCAT('upgradepkg --install-new ', '/tmp/', p.name, '-', p.version, '-x86_64-1_SBo.tgz', ' ') AS tgz_path
	
	FROM
	 depseq d
	 LEFT JOIN package p ON p.name         = d.name 
	 LEFT JOIN file    f ON f.package_name = d.name
	
	ORDER BY 
	 d.seq_no DESC
)


SELECT 
 CONCAT( 
 	'echo "PROCESSING [', name, '] (', version, '): ', pack_path, '"', '\n', 
 	location_path, ' 1>/dev/null\n',
 	'echo "RC" = $?', '\n'
 	'echo "DOWNLOADING [', name, ']: ', url, '"', '\n',
 	url_wget, ' 1>/dev/null\n', 
 	'echo "RC" = $?', '\n'
 	'echo "BUILDING [', name, ']: ', build_cmd, '"', '\n',
 	build_cmd, ' 1>/dev/null\n',
 	'echo "RC" = $?', '\n'
 	'echo "INSTALLING [', name, ']: ', tgz, '"', '\n',
 	tgz_path, ' 1>/dev/null\n',
 	'echo "RC" = $?', '\n'
 	'echo "DONE [', name, ']: ', description, '"', '\n' 	
 ) AS cmd
 
FROM
 cmd_qry
 
ORDER BY
 seq_no DESC
