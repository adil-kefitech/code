--code to find bundle with user id
select * from uok.pgd_bund_mstr where id in(
	select bundle_id from uok.pgd_bndl_camp where sub_camp_id in(
	select sub_camp_id from uok.pgd_camp_schedule where id in(
	select camp_schedule_id from uok.pgd_camp_role_allocation where camp_user_id in(
	select id from uok.auth_user 
		where username = '5049')))) order by id desc


bineesh-999
pgd_camp_schedule_course


pgd_sem_mstr
select * from uok.pgd_camp_schedule_course ORDER by id desc
select * from uok.pgd_camp_schedule_programmapping ORDER by id desc

pgd_camp_schedule_programmapping

uok.pgd_bund_mstr

select * from uok.pgd_bund_mstr ORDER by id desc
select * from uok.pgd_bund_mstr ORDER by id desc 

70766
select * from uok.auth_user where id in(70766)
select * from uok.pgd_camp_role_allocation where camp_user_id in(select id from uok.auth_user where username = ('7176'))
select * from uok.pgd_camp_sub_mstr ORDER by id desc
S6-APRIL 2024 EMS-TVPM
317
select * from uoS6-APRIL 2024 EMS-TVPMk.pgd_camp_schedule ORDER by id desc 
select * from uok.pgd_camp_schedule_course ORDER by id desc
select * from uok.pgd_exam_schdl ORDER by id desc 
select * from uok.pgd_bndl_camp ORDER by id desc 
select * from uok.pgd_camp_sub_mstr ORDER by id desc

select * from uok.pgd_bndl_camp where bundle_id in(84120)
select * from uok.pgd_bndl_camp where sub_camp_id in(696) --97950
--97950
select * from uok.pgd_bund_mstr where id in(102332,102331,102330)
--code to find bundle with user id
select * from uok.pgd_bund_mstr where id in(select bundle_id from uok.pgd_bndl_camp where sub_camp_id in(select sub_camp_id from uok.pgd_camp_schedule where id in(select camp_schedule_id from uok.pgd_camp_role_allocation where camp_user_id in(70766))))
696

select * from uok.pgd_camp_sub_mstr where id in(552)

select * from uok.pgd_camp_schedule where sub_camp_id in(317) --893
select * from uok.pgd_camp_role_allocation where camp_schedule_id in(1013)
select * from uok.pgd_camp_role_allocation where camp_user_id in(70766)

100515
609
100515
uok.pgd_bndl_camp
uok.pgd_exam_schdl

pgd_camp_schedule_course


select * from uok.auth_user where username = '5905'
-- the the id, Old AO's ID
select * from uok.pgd_camp_role_allocation where camp_user_id = 30142
-- take camp_schedule_ids,
select * from uok.pgd_camp_schedule where id in(574) order by id
select * FROM uok.pgd_bndl_camp where sub_camp_id in(334)
-- take the bundle IDs,
select * from uok.pgd_bund_mstr where id in (53820,50029,50629,50041,51019,51024,50634,51561,50809,50289,50148,50317,51654,50578,49908,50103,50740,51449,51635,50993,51058,49971,50199,51851,49989,50600,50018,50699,50816,51044,51111,53751,53819,53815,53824,53767,53816,53809,53904,53897,53900,53893,53902,50844,53812,53899,54434,54070,54072,54063,53807,56780,53792,53895,57674,57673,57675,53808,58045,57672,58100,57983,58324,58476,58325,58706,54416,58961,58931,59028,59479
and status_id not in(27,37,38,39) and exam_center_id is null
-- just check the condition, Here we try to avoid all the college bundles.
select * from uok.auth_user where username = '6319'
-- New AO's user_id
 
-- update uok.pgd_bund_mstr set created_by_id =70354,updated_by_id = 70354 where id in(54510,48259,54004,48108,41550,49395,48807,41560,41599,53907,48832,48980)

-- and status_id not in(27,37,38,39) and exam_center_id is null

-- Here we update OLD AO's ID with NEW AO's ID
											 
											 
											 
-- 1. Find bundles linked to a specific sub camp via BundleCamp
SELECT bm.id, bm.bundle_code, bm.exam_center_id, bm.status_id, bm.created_by_id
FROM uok.pgd_bund_mstr bm
JOIN uok.pgd_bndl_camp bc ON bc.bundle_id = bm.id
WHERE bc.sub_camp_id = 317
ORDER BY bm.id;


										
-- 2. Preview exactly what your filter would match (the rows that WILL be updated)
SELECT bm.id, bm.bundle_code, bm.exam_center_id, bm.status_id, bm.created_by_id
FROM uok.pgd_bund_mstr bm
JOIN uok.pgd_bndl_camp bc ON bc.bundle_id = bm.id
WHERE bc.sub_camp_id = 696
  AND bm.exam_center_id IS NULL
  AND bm.status_id NOT IN (27, 37, 38, 39);
							
											 
-- 3. Preview rows that will be IGNORED (the ones to skip)
SELECT bm.id, bm.bundle_code, bm.exam_center_id, bm.status_id, bm.created_by_id
FROM uok.pgd_bund_mstr bm
JOIN uok.pgd_bndl_camp bc ON bc.bundle_id = bm.id
WHERE bc.sub_camp_id = 696
  AND (bm.exam_center_id IS not NULL OR bm.status_id IN (27, 37, 38, 39));
											 
											 
											 
											 
											 
											 
											 
											 
											 