
select * from uok.user_login_logs where user_id in(select id from uok.auth_user where username = ('5057'))

SELECT setval(
    pg_get_serial_sequence('uok.user_login_logs', 'id'),
    (SELECT MAX(id) FROM uok.user_login_logs)
);
SELECT last_value FROM uok.user_login_logs_id_seq;
select * from uok.auth_user where id = 89924
SELECT MAX(id) FROM uok.user_login_logs;


uok.pgd_bund_mstr
uok.pgd_staff_base
select * from uok.pgd_staff_base ORDER by id desc 

select * from uok.auth_user where username in('47323557024')
uok.pgd_camp_master
select * from uok.pgd_camp_role_allocation ORDER by id desc limit 10
uok.pgd_camp_sub_mstr
select * from uok.pgd_camp_sub_mstr ORDER by id desc 
select * from uok.pgd_camp_sub_addr ORDER by id desc 
uok.pgd_camp_sub_addr
select * from uok.pgd_camp_mstr_addr
pgd_camp_sub_mstr
select * from uok.pgd_camp_master ORDER by id desc 

select * from uok.pgd_camp_schedule_course ORDER by id desc
select * from uok.pgd_sem_mstr ORDER by id desc 

uok.pgd_sem_mstr
uok.pgd_district
select * from uok.pgd_camp_schedule ORDER by id desc 
select * from uok.pgd_desig_hierarchy ORDER by id desc 
select * from uok.pgd_camp_role_allocation ORDER by id desc 
uok.pgd_camp_schedule_course
pgd_camp_schedule
pgd_desig_hierarchy
pgd_camp_role_allocation
uok.pgd_stud_details
select * from uok.pgd_stud_details where candidate_code in('47324553010')

47324553010

47323557024