select * from uok.pgd_exam where code = '33620406' --4032

select * from uok.pgd_qp where qp_code = 'Y 5412' --10933

select * from uok.pgd_qp_exam where qp_id in(10933) --14061

select * from uok.pgd_qp where qp_pattern_id in(1041)
select * from uok.pgd_qp order by id desc limit 100
select * from uok.pgd_cors_mstr where code = 'COA 1431' --1049

select * from uok.pgd_qp_pattern_mstr where course_id = '1049'  --1041

select * from uok.pgd_exam where code = ''

exam schedule id by vaishakh bro