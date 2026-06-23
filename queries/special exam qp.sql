select * from uok.pgd_exam where code = '33620406' --4032

select * from uok.pgd_qp where qp_code = 'Y 5412' --10933

select * from uok.pgd_qp_exam where qp_id in(10933) --14061

select * from uok.pgd_qp where qp_pattern_id in(1041)
select * from uok.pgd_qp order by id desc limit 100

select * from uok.pgd_cors_mstr where code = 'LW 1645' --22896
select * from uok.pgd_cors_mstr where code = 'LW- 1644' --22898

select * from uok.pgd_cors_mstr where code = 'LW- 1644' --22898

select * from uok.pgd_qp_pattern_mstr where course_id = 22896 --4430
select * from uok.pgd_qp_pattern_mstr where course_id = 22898 --4431

select * from uok.pgd_qp where qp_pattern_id in(4430,4431)
select * from uok.pgd_qp where qp_pattern_id in(4431)


select * from uok.pgd_qp where id in(9309,9310,9312,9313)
select * from uok.pgd_qp_exam where exam_id in(3280) and status_id in(78)


select * from uok.pgd_qp_exam where qp_id in(9313)
select * from uok.pgd_qp_exam where exam_id in(3280) and status_id in(78) --9309,9310,9312
select * from uok.pgd_exam_schdl where id in(57036,57037,57039,57040)

uok.pgd_exam_schdl
uok.pgd_qp_exam
9313


select * from uok.pgd_exam where code = ''

exam schedule id by vaishakh bro























































































