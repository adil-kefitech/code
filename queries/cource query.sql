select * from uok.pgd_cors_mstr where code in('654')
select * from uok.pgd_cors_mstr where code in('EN 1111')
select * from uok.pgd_prg_cours_mstr where course_id in(381)
61523402
uok.pgd_colg_prgm_cours
select * from uok.pgd_colg_prgm_cours order by id desc
select * from uok.pgd_colg_batch_prgm_sem order by id desc
select * from uok.pgd_colg_batch_prgm order by id desc
select * from uok.pgd_colg_prgm where programme_id=('70')
select * from uok.pgd_colg_prgm order by id desc

select * from uok.pgd_prg order by id desc

select * from uok.pgd_prg where code=('654')

uok.pgd_colg_prgmuok.pgd_prg
uok.pgd_colg_batch_prgm
uok.pgd_colg_batch_prgm_sem
uok.pgd_prg_cours_mstr
select * from uok.pgd_prg_cours_mstr order by id desc 
select count(*),status_id from uok.pgd_prg_cours_mstr group by status_id  

select * from uok.pgd_prg_cours_mstr where course_id in(381)

select * from uok.pgd_cour_prg_grp order by id desc
select * from uok.pgd_cour_prg_class order by id desc

select * from uok.river_state order by id desc 
uok.river_state
select * from uok.pgd_schm_mstr order by id desc
uok.pgd_schm_mstr

select * from uok.pgd_menu order by id desc
select * from uok.pgd_menu where redirect_url = 'answer-sheet-printing'

uok.pgd_menu

select * from uok.auth_permission order by id desc
uok.auth_permission

select * from uok.auth_group_permissions where group_id in(39,10) order by id desc
uok.auth_group_permissions
select * from uok.auth_user_groups where group_id in(10)

select * from uok.auth_user where id in(442,450,466,446,454,459,469,476,1298,16693,16748,16691,9892,10126,10110,10115,16239,2537,16548,16573,16574,16575,16589,17842,17195,17223,17224,17845,17225,17226,17227,17228,17176,17944,1165,19454,22447,19455,19456,22473,22474,16226,17192,30659,28456,28470,28479,30142,30143,28238,2,30765,30784,30923,31331,31337,40254,40257,40287,42495,43277,43284,58057,29953,63888,452,31104,70354,22475,77148,77149,77150,77469,79083,79273,457,70766,79462,79609,79040,30263,80170,89827,89834,89842,16228,89859,89868,463,83345,89878,89894,89922,28241,89969)
select * from uok.auth_user where is_superuser = true
uok.auth_user_groups
uok.auth_group
select * from uok.auth_group order by id desc

uok.pgd_menu_permision
select * from uok.pgd_menu_permision order by id desc

uok.django_content_type
select * from uok.django_content_type order by id desc

select * from uok.django_content_type where id in(502)

uok.pgd_menu_typ
select * from uok.pgd_menu_typ order by id desc

SELECT setval(
    pg_get_serial_sequence('uok.pgd_menu', 'id'), 
    (SELECT MAX(id) FROM uok.pgd_menu)
);




select * from uok.pgd_schm_mstr order by id desc
select * from uok.pgd_syllb_mstr order by id desc

uok.pgd_syllb_mstr
uok.pgd_schm_mstr



uok.pgd_bund_mstr
select * from uok.pgd_bund_mstr where bundle_code in('W 12670056')

select * from uok.pgd_bund_examiner where bundle_camp_id in(90620)
uok.pgd_bund_examiner
SELECT 
    b.qp_code,
    sc.id AS sub_camp_id,
    sc.display_name AS sub_camp_name,
    COUNT(DISTINCT sa.id) AS unallocated_sheets,
    g.name AS required_distribution_type
FROM uok.pgd_on_val_scn_as sa
JOIN uok.pgd_bund_mstr b ON sa.bundle_id = b.id
JOIN uok.pgd_exam_schdl es ON sa.exam_schedule_id = es.id
JOIN uok.river_state s ON sa.status_id = s.id
LEFT JOIN uok.pgd_on_val_exr_scn_as esa ON sa.id = esa.answersheet_id

JOIN uok.pgd_camp_schedule_course csc ON csc.exam_schedule_id = es.id
JOIN uok.pgd_camp_schedule cs ON csc.camp_schedule_id = cs.id
JOIN uok.pgd_camp_sub_mstr sc ON cs.sub_camp_id = sc.id

JOIN uok.pgd_camp_role_allocation cra ON cra.camp_course_id = csc.id
JOIN uok.pgd_desig_hierarchy dh ON cra.camp_group_id = dh.id
JOIN uok.auth_group g ON dh.group_id = g.id
JOIN uok.river_state cra_s ON cra.status_id = cra_s.id
WHERE 
                           
    sa.dfm_id IS NOT NULL                 
    AND esa.id IS NULL                        
    AND sc.id IN (529, 515, 564, 614, 643)    
    AND cra_s.label = 'ACTIVE'                
    AND (g.name ILIKE '%Additional Examiner%' OR g.name ILIKE '%Chief Examiner%')
GROUP BY 
    b.qp_code, sc.id, sc.display_name, g.name
ORDER BY 
    unallocated_sheets DESC;
	
	
	
	
	uok.pgd_schm_mstr
select * from uok.auth_user where username in('5928')
25380614
select * from uok.user_login_logs where user_id in(89858)

delete from uok.user_login_logs where id in(12)





select * from uok.pgd_cors_mstr where programme_id in(59) and course_type_code in(206)

SELECT
    cm.id          AS course_id,
    cm.code        AS course_code,
    cm.title       AS course_title,
    ctm.code       AS course_type_code,
    ctm.title      AS course_type_title,
    p.id           AS programme_id,
    p.title        AS programme_title,
    sm.id          AS semester_id,
    sm.title       AS semester_title,
    es.start_date  AS exam_start_date,
    es.end_date    AS exam_end_date
FROM uok.pgd_exam e

JOIN uok.pgd_exam_prgm_sem    eps ON eps.exam_id               = e.id
JOIN uok.pgd_prgm_sem_mapping psm ON psm.id                    = eps.programme_semester_id
JOIN uok.pgd_prg              p   ON p.id                      = psm.programme_id
JOIN uok.pgd_sem_mstr         sm  ON sm.id                     = psm.semester_id

JOIN uok.pgd_prg_cours_mstr   pcs ON pcs.programme_semester_id = psm.id
JOIN uok.pgd_cors_mstr        cm  ON cm.id                     = pcs.course_id
JOIN uok.pgd_cors_typ_mastr   ctm ON ctm.id                    = cm.course_type_id

-- Join exam schedule to get dates
JOIN uok.pgd_exam_schdl       es  ON es.programme_semester_course_id = pcs.id
                                  AND es.exam_id                     = e.id

WHERE e.code = '61523402';

select * from uok.pgd_cors_mstr where id in(22522,22523,22524,22525,22527,22568,22526)
select * from uok.pgd_prg_cours_mstr where course_id in(22522,22523)
select * from uok.pgd_prg_cours_mstr where programme_semester_id in(294)

pgd_prg_cours_mstr




-- Find duplicate courses in ProgrammeCourseSemester for the specific exam
SELECT
    pcs.id                          AS pcs_id,
    pcs.course_id,
    cm.code                         AS course_code,
    cm.title                        AS course_title,
    pcs.programme_semester_id,
    p.title                         AS programme_title,
    sm.title                        AS semester_title,
    sm.id                           AS semester_id,
    sc.title                        AS scheme_title,
    sc.code                         AS scheme_code,
    es.id                           AS schedule_id,
    es.start_date,
    es.end_date
    --es.status                       AS schedule_status
FROM uok.pgd_prg_cours_mstr       pcs
JOIN uok.pgd_cors_mstr             cm  ON cm.id  = pcs.course_id
JOIN uok.pgd_cors_typ_mastr        ctm ON ctm.id = cm.course_type_id
JOIN uok.pgd_prgm_sem_mapping      psm ON psm.id = pcs.programme_semester_id
JOIN uok.pgd_prg                   p   ON p.id   = psm.programme_id
JOIN uok.pgd_sem_mstr              sm  ON sm.id  = psm.semester_id
LEFT JOIN uok.pgd_schm_mstr        sc  ON sc.id  = pcs.scheme_id
LEFT JOIN uok.pgd_exam_schdl       es  ON es.programme_semester_course_id = pcs.id
                                       AND es.exam_id = 3946

WHERE ctm.code IN ('7')   -- replace with your PROJECT_COURSE_CODE
  AND pcs.programme_semester_id = 294                      -- from your log
  AND psm.semester_id  = 7                       -- from your log
select * from uok.pgd_prg_cours_mstr where course_id in(22526)
ORDER BY pcs.course_id, pcs.id;

select * from uok.pgd_cors_typ_mastr


SELECT
    course_id,
    programme_semester_id,
    COUNT(*)        AS duplicate_count,
    array_agg(id)   AS pcs_ids,
    array_agg(scheme_id) AS scheme_ids
FROM uok.pgd_prg_cours_mstr
GROUP BY course_id, programme_semester_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;