select * from uok.pgd_admis_yr_mstr order by id
-- check the admission year is present or not based on that add an entry

select * from uok.pgd_batch order by id
-- check the batch is present or not based on that add an entry
uok.auth_user
select * from uok.pgd_univ_reg_mstr order by id desc

select * from uok.pgd_schm_mstr order by id desc
select * from uok.pgd_syllb_mstr order by id desc

uok.auth_group
select * from uok.pgd_univ_reg_mstr where candidate_code = '654269521255'
uok.pgd_stud_colg_prgm_semuok.pgd_univ_reg_mstr
uok.pgd_stud_details
SELECT table_schema, column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'pgd_univ_reg_mstr' AND column_name = 'regulation_year';

SELECT table_schema, column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'pgd_univ_reg_mstr' AND column_name = 'regulation_year';

SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE column_name = 'regulation_year';
uok.user_login_logs
select * from uok.user_login_logs order by id desc
uok.pgd_std_tsfr_req
SELECT * FROM uok.user_login_logs where user_id in(2)
select * from uok.pgd_univ_reg_param order by id desc

delete FROM uok.user_login_logs where id in(6)


uok.auth_group
uok.auth_user_groups
uok.auth_group_permissions
select * from uok.auth_user where username in ('5390')
64	2	39
54389	30923	39
62040	31337	39

20371	16573	10
25096	16573	22
select * from uok.auth_user_groups where user_id in(16573)
select * from uok.auth_group where name in('Section Officer')
select * from uok.pgd_std_tsfr_req order by id desc
uok.pgd_std_tsfr_req
select * from uok.pgd_stud_colg_prgm_sem order by id desc
select * from uok.pgd_dfm_deletion_status order by id desc
select * from uok.pgd_dfm_deletion_status where candidate_code in('47322551096')

uok.pgd_dfm_deletion_status
uok.uok.pgd_dfm_deletion_statuspgd_stud_details
select * from uok.pgd_stud_details where status_id in('5')
select * from uok.pgd_stud_colg_prgm_sem where status_id in('5')
uok.pgd_dfm_deletion_status
uok.pgd_stud_colg_prgm_sem

select * from uok.pgd_univ_reg_schm_prg order by id desc
select * from uok.pgd_univ_reg_schm_prg where programme_id in('23')
select * from uok.pgd_univ_reg_mstr where id in('8')
select * from uok.pgd_schm_mstr order by id desc
uok.pgd_schm_mstr
delete from uok.pgd_schm_mstr where id in(2) and name in('2027')

select * from uok.pgd_prg where code in('474')
uok.pgd_colg_prgm_cours
uok.pgd_prg
select * from uok.pgd_syllb_mstr order by id desc
SELECT setval(
    pg_get_serial_sequence('uok.pgd_schm_mstr', 'id'),
    (SELECT MAX(id) FROM uok.pgd_schm_mstr)
);
pgd_syllb_mstr



select * from uok.pgd_prg_cours_mstr where programme_semester_id = '419'
select * from uok.pgd_colg_prgm_cours order by id desc
select * from uok.pgd_colg_prgm_cours order by id desc
select * from uok.pgd_schm_mstr order by id desc
uok.pgd_cour_prg_class
pgd_cors_mstr
419
uok.pgd_prg_cours_mstr






pgd_cors_mstr 


select * from uok.pgd_cors_mstr where code = 'CS-541'
select * from uok.pgd_cors_mstr where id = '18299'

23375
select * from uok.pgd_prg_cours_mstr where course_id in(23375)
select * from uok.pgd_prg_cours_mstr where id in(29184,29185,29186,29187,29188,29183)
select * from uok.pgd_prg_cours_mstr where id in(23375)
select * from uok.pgd_prg_cours_mstr where programme_semester_id = '338'

29183
select * from uok.pgd_colg_prgm_cours where prgm_cors_sem_id = '29183'
INSERT INTO uok.pgd_schm_mstr (scheme_id) VALUES (15);
select * from uok.pgd_prg_cours_mstr where id in(23375)
UPDATE uok.pgd_prg_cours_mstr 
SET scheme_id = 15 
WHERE id in(29184,29185,29186,29187,29188,29183) ;

pgd_schm_mstr



-- 615 , 620 , 650 , 505
select * from uok.pgd_prg where code like '%913%'
461
select * from uok.pgd_schm_mstr order by id
16
select * from uok.pgd_univ_reg_mstr order by id desc
select * from uok.pgd_univ_reg_schm_prg order by id desc

select * from uok.user_login_logs where user_id in()


uok.user_login_logs
select * from uok.pgd_univ_reg_schm_prg where programme_id = 70
-- add an entry , if new scheme
443

select * from uok.pgd_syllb_mstr where programme_id in(461)
327
select * from uok.pgd_schm_syllb_yr where admission_year_id = 9 and scheme_id = 16 and syllabus_id in(327)
-- add an entry , if new scheme or new admission year is present



-- Query for pgm_sem_cors_id

select pp.id,pp.name,pcm.id,pcm.name,pcm.code,ppcm.id as ppcm,psm.id as sem_id,psm.title as sem_title
from uok.pgd_prg as pp
join uok.pgd_prg_class_mstr as pgcm
on pp.programme_class_id=pgcm.id
join uok.pgd_prgm_sem_mapping as ppsm
on ppsm.programme_id = pp.id
join uok.pgd_sem_mstr as psm
on psm.id=ppsm.semester_id
join uok.pgd_prg_cours_mstr as ppcm
on ppcm.programme_semester_id = ppsm.id
join uok.pgd_cors_mstr as pcm
on pcm.id = ppcm.course_id
where pp.id in (select id from uok.pgd_prg where code = '913') and psm.id in (1)

select * from uok.pgd_prg_cours_mstr where id in(28946,28947,28948,28949,28950,28951,28952)
-- Fill the scheme_id

select * from uok.pgd_syllb_details where programme_course_semester_id in(28946,28947,28948,28949,28950,28951,28952)



insert into uok.pgd_syllb_details
(created_on,updated_on,comments, created_by_id,programme_course_semester_id,
status_id,syllabus_id,updated_by_id)
select distinct CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
prgcrs.comments,prgcrs.created_by_id,prgcrs.id, sylb.status_id,sylb.id,sylb.updated_by_id
--uok.pgd_syllb_details
from
uok.pgd_syllb_mstr as sylb,
uok.pgd_prg as prg,
uok.pgd_prgm_sem_mapping as prgsem,
uok.pgd_prg_cours_mstr as prgcrs,
--uok.pgd_cors_mstr as crs,
uok.pgd_univ_reg_schm_prg as prgregsc
where prg.id= sylb.programme_id and prg.id=prgsem.programme_id and prgcrs.programme_semester_id=prgsem.id
and prg.code in ('913') and prgsem.semester_id=1 and
prgregsc.programme_id=prg.id and prgcrs.scheme_id in(16)
and sylb.id = 327



select * from uok.pgd_sem_reg where programme_semester_id in(select id from uok.pgd_prgm_sem_mapping where programme_id in(
select id from uok.pgd_prg where code ='913') and semester_id in(1))
3144
select * from uok.pgd_prg_cours_mstr where programme_semester_id in(1497)

select * from uok.pgd_schm_syllb_yr where admission_year_id = 9 and scheme_id = 16 and syllabus_id in(327)


-- After all these steps , Do the data migration.

-- ADD THIS NEW PROGRAMME TO CORRESPONDING SECTION



-- NEW SCHEME PROGRAMMES
-- 615 , 620 , 650 , 505
select * from uok.pgd_prg where code like '%913%'
8
select * from uok.pgd_schm_mstr order by id
16 -- 2025 scheme
select * from uok.pgd_univ_reg_mstr where id in(103) order by id
1 , -- if needed , add entry
select * from uok.pgd_univ_reg_schm_prg where programme_id = 461
-- add an entry
439
2025-12-31 11:59:34.865573+05:30

-- Query for pgm_sem_cors_id

select pp.id,pp.name,pcm.id,pcm.name,pcm.code,ppcm.id as ppcm,psm.id as sem_id,psm.title as sem_title
from uok.pgd_prg as pp
join uok.pgd_prg_class_mstr as pgcm
on pp.programme_class_id=pgcm.id
join uok.pgd_prgm_sem_mapping as ppsm
on ppsm.programme_id = pp.id
join uok.pgd_sem_mstr as psm
on psm.id=ppsm.semester_id
join uok.pgd_prg_cours_mstr as ppcm
on ppcm.programme_semester_id = ppsm.id
join uok.pgd_cors_mstr as pcm
on pcm.id = ppcm.course_id
where pp.id in (select id from uok.pgd_prg where code = '913') and psm.id in (1)

select * from uok.pgd_prg_cours_mstr where id in(28946,28947,28948,28949,28950,28951,28952)
-- Fill the scheme_id

select * from uok.pgd_syllb_details where programme_course_semester_id in(28946,28947,28948,28949,28950,28951,28952)

select * from uok.pgd_syllb_mstr where programme_id in(select id from uok.pgd_prg where code in ('913'))
7,323 -- add new entry for new schemes
2025-12-31 11:59:34.865573+05:30

insert into uok.pgd_syllb_details
(created_on,updated_on,comments, created_by_id,programme_course_semester_id,
status_id,syllabus_id,updated_by_id)
select '',CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
prgcrs.comments,prgcrs.created_by_id,prgcrs.id, sylb.status_id,sylb.id,sylb.updated_by_id
--uok.pgd_syllb_details
from
uok.pgd_syllb_mstr as sylb,
uok.pgd_prg as prg,
uok.pgd_prgm_sem_mapping as prgsem,
uok.pgd_prg_cours_mstr as prgcrs,
--uok.pgd_cors_mstr as crs,
uok.pgd_univ_reg_schm_prg as prgregsc
where prg.id= sylb.programme_id and prg.id=prgsem.programme_id and prgcrs.programme_semester_id=prgsem.id
and prg.code in ('634') and prgsem.semester_id=1 and
prgregsc.programme_id=prg.id
and sylb.id in(323)
and prgcrs.id in(1140,28586,28587,28588,1138,1139)





--------------------------------------------------------------------------
-- NEW ADMISSION YEAR PROGRAMMES
'606','590','505','635'
"634",
'510','512','513','514','515','517','518','520','525','529','530','535','540','541','546','550','555','560','575','576','577','578','579','580','584','605','608','610','615','620','625','630','636','638','639','645','650','651','654','655','656','657','658','659','906','915'
"626","542","591","631","632","649","916","551","646"
SELECT DISTINCT ON (pp.code)
ssy.id,
'2026-01-01 11:39:46.305579+05:30'::timestamptz AS created_on,
'2026-01-01 11:39:46.305579+05:30'::timestamptz AS updated_on,
'Bulk inserted on 01.01.2025' AS comments,
9 AS admission_year_id,
2 AS created_by_id,
ssy.scheme_id,
ssy.status_id,
ssy.syllabus_id,
2 AS updated_by_id
FROM uok.pgd_schm_syllb_yr ssy

JOIN uok.pgd_prg_cours_mstr ppcm
ON ppcm.scheme_id = ssy.scheme_id

JOIN uok.pgd_prgm_sem_mapping ppsm
ON ppsm.id = ppcm.programme_semester_id

JOIN uok.pgd_prg pp
ON pp.id = ppsm.programme_id

JOIN uok.pgd_sem_mstr psm
ON psm.id = ppsm.semester_id

JOIN uok.pgd_syllb_mstr sm
ON sm.id = ssy.syllabus_id
AND sm.programme_id = pp.id

WHERE pp.code IN (
'514','515','517','518','520','525','529','530','535','540','541','546','550','555','560',
'575','576','577','578','579','580','584','605','608','610','615','620','625','630','638',
'645','650','651','654','655','656','657','658','659','906','915','626','542','591','631',
'632','649','916','551','646'
)
AND psm.id = 1

ORDER BY
pp.code,
ssy.id DESC;



--OR
select pp.id,pp.name,pcm.id,pcm.name,pcm.code,ppcm.id as ppcm,psm.id as sem_id,psm.title as sem_title
from uok.pgd_prg as pp
join uok.pgd_prg_class_mstr as pgcm
on pp.programme_class_id=pgcm.id
join uok.pgd_prgm_sem_mapping as ppsm
on ppsm.programme_id = pp.id
join uok.pgd_sem_mstr as psm
on psm.id=ppsm.semester_id
join uok.pgd_prg_cours_mstr as ppcm
on ppcm.programme_semester_id = ppsm.id
join uok.pgd_cors_mstr as pcm
on pcm.id = ppcm.course_id
where pp.id in (select id from uok.pgd_prg where code = '634') and psm.id in (1)

select * from uok.pgd_prg_cours_mstr where id in(1140,28586,28587,28588,30,31,32,1138,1139)

select * from uok.pgd_syllb_mstr where programme_id in(select id from uok.pgd_prg where code in ('634'))

select * from uok.pgd_schm_syllb_yr where scheme_id in(1,16) and syllabus_id in(7,323)
-- add new entry
2025-12-31 11:59:34.865573+05:30

-------------------------------------------------------------------------------------------------------------------

select * from uok.pgd_syllb_details where programme_course_semester_id in (27006,27007,27008,27009,27010,27011,27012,4208,4209,4210,4211,4212)
select * from uok.pgd_syllb_mstr where programme_id in(select id from uok.pgd_prg where code in ('590'))
48
193


-- Query for pgm_sem_cors_id

select pp.id,pp.name,pcm.id,pcm.name,pcm.code,ppcm.id as ppcm,psm.id as sem_id,psm.title as sem_title
from uok.pgd_prg as pp
join uok.pgd_prg_class_mstr as pgcm
on pp.programme_class_id=pgcm.id
join uok.pgd_prgm_sem_mapping as ppsm
on ppsm.programme_id = pp.id
join uok.pgd_sem_mstr as psm
on psm.id=ppsm.semester_id
join uok.pgd_prg_cours_mstr as ppcm
on ppcm.programme_semester_id = ppsm.id
join uok.pgd_cors_mstr as pcm
on pcm.id = ppcm.course_id
where pp.id in (select id from uok.pgd_prg where code = '597') and psm.id in (4)




select * from uok.pgd_sem_reg where programme_semester_id in(select id from uok.pgd_prgm_sem_mapping where programme_id in(
select id from uok.pgd_prg where code ='606') and semester_id in(1))
2227
select * from uok.pgd_prg_cours_mstr where programme_semester_id in(246)

select * from uok.pgd_schm_syllb_yr where admission_year_id in(9) and scheme_id = 1 and syllabus_id in(51)

select * from uok.pgd_schm_syllb_yr where scheme_id = 8 and syllabus_id in(48)

select * from uok.pgd_syllb_mstr where id in(92,91,78,189,321,193)

select * from uok.pgd_prg where id in(80,93,94,362,53,56)

606,590
select * from uok.pgd_prg where programme_group_id in(4) and programme_type_id in(7)
id in(56)

select * from uok.pgd_prg_class_mstr order by id

select * from uok.pgd_prg_typ_mstr order by id