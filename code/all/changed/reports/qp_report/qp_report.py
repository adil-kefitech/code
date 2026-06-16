from datetime import date
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from util.models import (
    Examination,
    ExaminationSchedule,
    ProgrammeCourseSemester,
    CourseMaster,
    QuestionPaper,
    QuestionPaperExamMapper,
    QuestionPaperBluePrintMaster,
)
from util.constants import BAD_GATEWAY, BAD_GATEWAY_ERROR_CODE, FETCH_SUCCESS_MSG
from util.pagination import format_response

import logging

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
#  FEATURE 1 ─ QP Report by Exam Code
#  GET  → renders the template (page load)
#  POST → accepts { "exam_code": "..." } and returns course + QP code table
# ─────────────────────────────────────────────────────────────────────────────

class QPReportByExamCode(APIView):
    def get(self, request):
        return format_response(
            True,
            "success",
            {},
            status_code=status.HTTP_200_OK,
            template_name="qp_report.html",
        )
        
    def post(self, request):
        try:
            exam_code = request.data.get("exam_code", "").strip()
            if not exam_code:
                return format_response(
                    False,
                    "Exam code is required.",
                    {},
                    "EXAM_CODE_REQUIRED",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # ── 1. Resolve Examination ────────────────────────────────────────
            exam = Examination.objects.filter(code=exam_code).first()
            if not exam:
                return format_response(
                    False,
                    "Invalid Exam Code. No examination found.",
                    {},
                    "INVALID_EXAM_CODE",
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            today = date.today()

            ended_schedules = (
                ExaminationSchedule.objects.filter(exam=exam, end_date__lt=today)
                .select_related(
                    "programme_semester_course__course",
                    "programme_semester_course__programme_semester__programme",
                )
            )

            if not ended_schedules.exists():
                return format_response(
                    True,
                    "No ended exam schedules found for this examination.",
                    {
                        "exam_title": exam.title,
                        "exam_code": exam.code,
                        "course_data": [],
                    },
                    status_code=status.HTTP_200_OK,
                )

            seen_pcs_ids = set()
            course_data = []

            for schedule in ended_schedules:
                pcs = schedule.programme_semester_course
                if pcs.id in seen_pcs_ids:
                    continue
                seen_pcs_ids.add(pcs.id)
                course = pcs.course  
                qp_mappers = QuestionPaperExamMapper.objects.filter(
                    exam=exam,
                    qp__qp_pattern__course=course,
                ).select_related("qp")
                qp_codes = list(
                    dict.fromkeys(  # preserves order, removes duplicates
                        m.qp.qp_code for m in qp_mappers
                    )
                )
                course_data.append(
                    {
                        "course_name": course.name,
                        "course_code": course.code,
                        "exam_end_date": str(schedule.end_date),
                        "qp_codes": qp_codes if qp_codes else [],
                        "qp_codes_display": ", ".join(qp_codes) if qp_codes else "N/A",
                    }
                )
            course_data.sort(key=lambda x: x["course_code"])

            return format_response(
                True,
                FETCH_SUCCESS_MSG,
                {
                    "exam_title": exam.title,
                    "exam_code": exam.code,
                    "course_data": course_data,
                },
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(e, exc_info=True)
            return format_response(
                False,
                BAD_GATEWAY,
                {},
                BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ─────────────────────────────────────────────────────────────────────────────
#  FEATURE 2 ─ QP Report by QP Code
#  GET  → renders the template (handled in same template as Feature 1)
#  POST → accepts { "qp_code": "..." } and returns exam codes + course codes
# ─────────────────────────────────────────────────────────────────────────────

class QPReportByQPCode(APIView):
    def post(self, request):
        try:
            qp_code = request.data.get("qp_code", "").strip()
            if not qp_code:
                return format_response(
                    False, "QP Code is required.", {}, "QP_CODE_REQUIRED",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            qp_paper_ids = list(QuestionPaper.objects.filter(qp_code=qp_code).values_list('id', flat=True))
            
            if not qp_paper_ids:
                return format_response(
                    False, "No Question Paper found with this QP Code.", {},
                    "QP_CODE_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND
                )
            qp_exam_mappers = (
                QuestionPaperExamMapper.objects.filter(qp_id__in=qp_paper_ids)
                .select_related("exam")
            )
            if not qp_exam_mappers.exists():
                return format_response(
                    True, "This QP Code has not been mapped to any examination.",
                    {"qp_code": qp_code, "exam_data": []},
                    status_code=status.HTTP_200_OK
                )
            seen_exam_ids = set()
            exam_data = []
            for mapper in qp_exam_mappers:
                exam = mapper.exam
                if not exam or exam.id in seen_exam_ids:
                    continue
                seen_exam_ids.add(exam.id)

                valid_course_ids = list(QuestionPaper.objects.filter(
                    qp_code=qp_code
                ).values_list('qp_pattern__course_id', flat=True))

                schedules = ExaminationSchedule.objects.filter(
                    exam=exam,
                    programme_semester_course__course_id__in=valid_course_ids
                ).select_related("programme_semester_course__course")

                seen_course_ids = set()
                courses = []
                for sch in schedules:
                    course = sch.programme_semester_course.course
                    if course and course.id not in seen_course_ids:
                        seen_course_ids.add(course.id)
                        courses.append({
                            "course_code": course.code,
                            "course_name": course.name,
                        })

                courses.sort(key=lambda c: c["course_code"])

                exam_data.append({ 
                    "exam_code": exam.code,
                    "exam_title": exam.title,
                    "courses": courses,
                    "course_codes_display": ", ".join(c["course_code"] for c in courses) if courses else "N/A",
                })

            exam_data.sort(key=lambda x: x["exam_code"])

            return format_response(
                True, FETCH_SUCCESS_MSG,
                {"qp_code": qp_code, "exam_data": exam_data},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(e, exc_info=True)
            return format_response(
                False, BAD_GATEWAY, {}, BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


