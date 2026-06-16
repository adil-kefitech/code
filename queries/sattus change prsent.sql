uok.pgd_attds_stud


select * from uok.pgd_exam_reg_cors_mapping ORDER by id desc limit 100

select * from uok.pgd_stud_prgm_sem_cours ORDER by id desc limit 100

select * from uok.pgd_qp_pattern_mstr ORDER by id desc
uok.pgd_qp_exam
select * from uok.pgd_qp where qp_pattern_id in(4774)
uok.pgd_qp
select * from uok.pgd_qp_exam ORDER by id desc

uok.pgd_exam_reg_cors_mapping
uok.pgd_stud_prgm_sem_cours

date -- 04/06/2026
59023141010  --candidate code
59018407  --exam code

uok.pgd_qp_exam
uok.pgd_qp_pattern_mstr

select * from uok.pgd_qp_pattern_mstr where course_id in(2456)






select * from uok.river_state where id in(25,26,24)
select * from uok.auth_user where username = '59023141010'
-- take id, 37978

select * from uok.pgd_exam where code like '%59018407%'
-- take id, 3905

select * from uok.pgd_exam_schdl where exam_id in(3905) and start_date = '2026-06-04'
-- take programme_semester_course_id, 2978,2972


select * from uok.pgd_exam_reg where created_by_id in(37978) and exam_id in(3905)
-- id, 295183
-- take student_semester_id, 308259
select * from uok.pgd_stud_prgm_sem_cours where student_semester_id = 308259 and prgm_sem_course_id in(2978,2972,2979,2973,2980,2974,2975,2976,2977,2977,2976)
-- take id, 1340430
-- take prgm_sem_course_id, 2972

select * from uok.pgd_prg_cours_mstr where id in(2972)
-- take course_id, 2456

select * from uok.pgd_qp_pattern_mstr where course_id in(2456)
-- take id, 2702

select * from uok.pgd_qp where qp_pattern_id in(2702)
-- take ids,2875,5809,8423,10775

select * from uok.pgd_qp_exam where qp_id in(2875,5809,8423,10775) and exam_id in(3905)
-- take qp_id

select * from uok.pgd_qp where id in(10775)
-- We get the qp_code as 'Y 5317'



select * from uok.pgd_exam_reg_cors_mapping where student_semester_course_id in(1340431,1340433,1340434,1340435,1340430,1340432)


select * from uok.pgd_exam_reg_cors_mapping where student_semester_course_id in(1340431,1340433,1340434,1340435,1340430,1340432)

select * from uok.auth_user where username = '59023141010' --user_id = 37978

select * from uok.pgd_exam where code like '%59018407%'  -- take id, 3905
select * from uok.pgd_exam_schdl where exam_id in(3905) and start_date = '2026-06-04'
-- take programme_semester_course_id, 2978,2972


select * from uok.pgd_exam_reg_cors_mapping where student_semester_course_id in(select id from uok.pgd_stud_prgm_sem_cours where student_semester_id in(select student_semester_id from uok.pgd_exam_reg where created_by_id in(select id from uok.auth_user where username = '59023141010') and exam_id in(select id from uok.pgd_exam where code like '%59018407%')) and prgm_sem_course_id in(select programme_semester_course_id from uok.pgd_exam_schdl where exam_id in(select id from uok.pgd_exam where code like '%59018407%')))

select id from uok.pgd_exam where code like '%59018407%' --exam_id
select id from uok.auth_user where username = '59023141010' --user_id
select programme_semster_course_id from uok.pgd_exam_schdl where exam_id in(select id from uok.pgd_exam where code like '%59018407%') --prgm_sem_course_id

select * from uok.pgd_exam_schdl where exam_id in(select id from uok.pgd_exam where code like '%59018407%') --prgm_sem_course_id
select student_semester_id from uok.pgd_exam_reg where created_by_id in(select id from uok.auth_user where username = '59023141010') and exam_id in(select id from uok.pgd_exam where code like '%59018407%')
--student_semester_id
select * from uok.pgd_stud_prgm_sem_cours where student_semester_id in(select student_semester_id from uok.pgd_exam_reg where created_by_id in(select id from uok.auth_user where username = '59023141010') and exam_id in(select id from uok.pgd_exam where code like '%59018407%')) and prgm_sem_course_id in(select programme_semester_course_id from uok.pgd_exam_schdl where exam_id in(select id from uok.pgd_exam where code like '%59018407%'))
-- take id, 1340430
select id from uok.pgd_prg_cours_mstr where id in(2972) -- take course_id, 2456




SELECT DISTINCT ercm.*
FROM uok.pgd_exam_reg_cors_mapping ercm
JOIN uok.pgd_stud_prgm_sem_cours spsc 
    ON ercm.student_semester_course_id = spsc.id
JOIN uok.pgd_exam_reg er 
    ON spsc.student_semester_id = er.student_semester_id
JOIN uok.auth_user au 
    ON er.created_by_id = au.id
JOIN uok.pgd_exam e_reg 
    ON er.exam_id = e_reg.id
JOIN uok.pgd_exam_schdl es 
    ON spsc.prgm_sem_course_id = es.programme_semester_course_id
JOIN uok.pgd_exam e_schdl 
    ON es.exam_id = e_schdl.id
WHERE au.username = '59023141010'
  AND e_reg.code LIKE '%59018407%'
  AND e_schdl.code LIKE '%59018407%'


select * from uok.pgd_exam_reg_cors_mapping where student_semester_course_id in(select id from uok.pgd_stud_prgm_sem_cours where student_semester_id in(select student_semester_id from uok.pgd_exam_reg where created_by_id in(select id from uok.auth_user where username = '59023141010') and exam_id in(select id from uok.pgd_exam where code like '%59018407%')) and prgm_sem_course_id in(select programme_semester_course_id from uok.pgd_exam_schdl where exam_id in(select id from uok.pgd_exam where code like '%59018407%')))


select * from uok.pgd_exam_reg_cors_mapping where exam_registration_id in(
select id from uok.pgd_exam_reg where created_by_id in(select id from uok.auth_user
where username = '47122554006') and exam_id in(select id from uok.pgd_exam where code like '%47120504%'))
59023141010  --candidate code
59018407  --exam code
SELECT * FROM uok.pgd_cors_mstr where id in(76,36,302)
select * from uok.pgd_qp where qp_code = 'W 5448'
select * from uok.pgd_qp_exam where exam_id in(3618) and qp_id in(9968)
--13103,13104,13106,13721,13719,13105
select * from uok.pgd_exam where code in('50523103') --3618


22486
select * from uok.pgd_qp_pattern_mstr where id in(3578)
												  2554006
47120504

select * from uok.pgd_cors_mstr where name like 'Logic' --4116
select * from uok.pgd_prg_cours_mstr where course_id in(4116) --5294
-- take course_id, 2456

select * from uok.pgd_qp_pattern_mstr where course_id in(4116)
-- take id, 2702

select * from uok.pgd_qp where qp_pattern_id in(3578)
-- take ids,2875,5809,8423,10775

select * from uok.pgd_qp_exam where qp_id in(2875,5809,8423,10775) and exam_id in(3905)
-- take qp_id

select * from uok.pgd_qp where id in(10775)
-- We get the qp_code as 'Y 5317'










select * from uok.pgd_exam_reg_cors_mapping where exam_registration_id in(208603)

select * from uok.pgd_digital_false_no ORDER by id desc limit 100
select * from uok.pgd_smp_history_updation ORDER by id desc limit 100
select * from uok.pgd_res_wh ORDER by id desc limit 100
select * from uok.pgd_res_wh_cours ORDER by id desc limit 100






SELECT id, code, title, status_id 
FROM uok.pgd_exam 
WHERE code = '50523103';

SELECT id, name, code 
FROM uok.pgd_cors_mstr 
WHERE name ILIKE 'Logic';


SELECT qp.id, qp.qp_code, qp.status_id AS qp_status,
       qpem.id AS mapper_id, qpem.status_id AS mapper_status,
       c.name AS course_name, c.code AS course_code,
       sc.name AS sub_course_name
FROM uok.pgd_qp_exam qpem
JOIN uok.pgd_qp qp ON qp.id = qpem.qp_id
JOIN uok.pgd_exam e ON e.id = qpem.exam_id
JOIN uok.pgd_qp_pattern_mstr qpp ON qpp.id = qp.qp_pattern_id
JOIN uok.pgd_cors_mstr c ON c.id = qpp.course_id
LEFT JOIN uok.pgd_crs_sub_mstr sc ON sc.id = qpp.sub_course_id
WHERE e.code = '50523103'
  AND c.name ILIKE 'Logic';


SELECT qp.id, qp.qp_code, qp.status_id AS qp_status,
       qpem.id AS mapper_id, qpem.status_id AS mapper_status,
       c.name AS course_name,
       sc.name AS sub_course_name,
       es.id AS schedule_id,
       pcs.id AS pcs_id
FROM uok.pgd_qp_exam qpem
JOIN uok.pgd_qp qp ON qp.id = qpem.qp_id
JOIN uok.pgd_exam e ON e.id = qpem.exam_id
JOIN uok.pgd_qp_pattern_mstr qpp ON qpp.id = qp.qp_pattern_id
JOIN uok.pgd_cors_mstr c ON c.id = qpp.course_id
LEFT JOIN uok.pgd_crs_sub_mstr sc ON sc.id = qpp.sub_course_id
JOIN uok.pgd_exam_schdl es ON es.exam_id = e.id
JOIN uok.pgd_prg_cours_mstr pcs ON pcs.id = es.programme_semester_course_id
    AND pcs.course_id = qpp.course_id
WHERE e.code = '50523103'
  AND c.name ILIKE '%Logic%';
  
  
SELECT ehas.id AS student_allotment_id,
       sd.candidate_code,
       up.full_name AS student_name,
       eh.name AS hall_name,
       ac.name AS college_name,
       ac.code AS college_code
FROM uok.pgd_exam_hal_alotmnt_stdnt ehas
JOIN uok.pgd_exam_hal_alotmnt_cors_tchr ehact ON ehact.id = ehas.exam_hal_alotmnt_cors_tchr_id
JOIN uok.pgd_exam_hal_alotmnt_cors ehac ON ehac.id = ehact.exam_hal_alotmnt_cors_id
JOIN uok.pgd_exam_hal_alotmnt eha ON eha.id = ehac.exam_hal_alotmnt_id
JOIN uok.pgd_exam_hall eh ON eh.id = eha.exam_hall_id
JOIN uok.pgd_exam_cntr ec ON ec.id = eh.exam_center_id
JOIN uok.pgd_collgs ac ON ac.id = ec."College_id"
JOIN uok.pgd_exam_schdl es ON es.id = ehac.exam_schedule_id
JOIN uok.pgd_exam e ON e.id = es.exam_id
JOIN uok.pgd_prg_cours_mstr pcs ON pcs.id = es.programme_semester_course_id
JOIN uok.pgd_cors_mstr c ON c.id = pcs.course_id
JOIN uok.pgd_stud_details sd ON sd.id = ehas.student_details_id
JOIN uok.pgd_stud_base sb ON sb.id = sd.student_id
JOIN uok.pgd_profl up ON up.user_id = sb.user_id
WHERE e.code = '50523103'
  AND c.name ILIKE '%Logic%'
  AND ehac.status_id = 1
  AND ehact.status_id = 1
  AND ehas.status_id = 1
ORDER BY eh.name, ehas.id;


select * from uok.pgd_exam_cntr 


SELECT es.id AS examsch_id,
       e.code AS exam_code,
       c.name AS course_name,
       es.status_id
FROM uok.pgd_exam_schdl es
JOIN uok.pgd_exam e ON e.id = es.exam_id
JOIN uok.pgd_prg_cours_mstr pcs ON pcs.id = es.programme_semester_course_id
JOIN uok.pgd_cors_mstr c ON c.id = pcs.course_id
WHERE e.code = '50523103'
  AND c.name ILIKE '%Logic%'
  AND es.status_id = 1;

select * from uok.pgd_exam where code in('50523103') --3618
select * from uok.pgd_exam_schdl where exam_id in(3618)
56281


select * from uok.river_state 
