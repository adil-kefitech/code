from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.utils import timezone

from rest_framework.generics import ListAPIView
from rest_framework import status

from river.models import State

from util.models import (
    StaffBase,
    StaffSection,
    SubsectionProgramme,
    Programme,
    ProgrammeSemester,
    Batch,
    CollegeBatchProgrammeSemester,
    SchemeMaster,
    UniversityRegulationSchemeProgramme,
    ProgrammeCourseSemester,
    CourseMaster,
    CourseTypeMaster,
    CourseProgrammeClass, 
    CourseProgrammeGroup,
    SyllabusMaster,               
    SyllabusDetails,              
    QuestionPaperBluePrintMaster,

   
)
from util.constants import *
from util.loggings import logging

from django.db import transaction
from django.utils.text import slugify

logger = logging.getLogger(__name__)

import json as _json




# ============================================================================
#   PAGE LOAD  –  GET /course-management/
#   Renders the page with all course types for dropdowns.
# ============================================================================

class CourseManagementPageLoad(ListAPIView):

    def get(self, request):
        try:
            from django.db.models import F
            staffbase    = StaffBase.objects.filter(user=request.user).first()
            staffsection = StaffSection.objects.filter(staff=staffbase)
            subsection   = [s.sub_section for s in staffsection]

            subsectionprg = SubsectionProgramme.objects.filter(
                sub_section_id__in=subsection
            ).select_related(
                'programme__programme_type',
                'programme__programme_group',
                'programme__programme_class',
            )

            cascade_data = {}
            dup_typ = set()
            dup_grp = set()

            for sp in subsectionprg:
                prog    = sp.programme
                p_type  = prog.programme_type.title  if prog.programme_type  else "NA"
                p_group = prog.programme_group.title if prog.programme_group else "NA"
                p_class = prog.programme_class.title if prog.programme_class else "NA"
                p_code  = prog.code if prog.code else ""
                p_title = f"{prog.title} - ({p_code})" if p_code else prog.title
                p_id    = prog.id

                if p_type  != "NA": dup_typ.add(p_type)
                if p_group != "NA": dup_grp.add(p_group)

                if p_type  not in cascade_data:
                    cascade_data[p_type] = {}
                if p_group not in cascade_data[p_type]:
                    cascade_data[p_type][p_group] = {}
                if p_class not in cascade_data[p_type][p_group]:
                    cascade_data[p_type][p_group][p_class] = {}
                cascade_data[p_type][p_group][p_class][p_title] = p_id

            programme_type  = [{"prgtyp": t} for t in sorted(dup_typ)]
            programme_group = [{"prggrp": g} for g in sorted(dup_grp)]

            batches = Batch.objects.all().select_related("academic_year").order_by(
                "-academic_year__admission_year", "title"
            )
            batch_list = [
                {
                    "id":            b.id,
                    "title":         b.display_name or b.title,
                    "academic_year": b.academic_year.admission_year,
                }
                for b in batches
            ]

            course_types = list(
                CourseTypeMaster.objects.all().order_by("title").values("id", "title")
            )

            return format_response(
                True, "Success",
                data={
                    "prg_typ":      programme_type,
                    "prg_grp":      programme_group,
                    "batch_list":   batch_list,
                    "cascade_json": _json.dumps(cascade_data),
                    "course_types": course_types,
                },
                status_code=status.HTTP_200_OK,
                template_name="course_management.html",
            )

        except Exception as e:
            import traceback
            traceback.print_exc() 
            logger.error(e, exc_info=True)
            return format_response(
                False, BAD_GATEWAY, {}, BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                template_name="500.html",
            )


# ============================================================================
#   COURSE MANAGEMENT — Fetch Courses
#   POST /course-management/fetch-courses/
#
#   Returns all ProgrammeCourseSemester rows for the selected prgm_sem,
#   filtered by scheme_id.  Each row carries full CourseMaster details.
# ============================================================================
class CourseManagementFetchCourses(ListAPIView):

    def post(self, request):
        try:
            prgm_sem_id = request.data.get("prgm_sem_id")
            scheme_id   = request.data.get("scheme_id")
            batch_id    = request.data.get("batch_id")

            if not prgm_sem_id:
                return JsonResponse(
                    {"success": False, "message": "prgm_sem_id is required.", "data": {}},
                    status=400
                )

            qs = ProgrammeCourseSemester.objects.filter(
                programme_semester_id=prgm_sem_id
            ).select_related(
                "course", "course__course_type", "scheme"
            )

            if scheme_id:
                qs = qs.filter(scheme_id=scheme_id)

            qs = qs.order_by("course_order", "course__code")

            courses = []
            for pcs in qs:
                courses.append({
                    "pcsId":             pcs.id,
                    "courseId":          pcs.course_id,
                    "courseCode":        pcs.course.code,
                    "courseName":        pcs.course.name,
                    "courseTitle":       pcs.course.title,
                    "courseDescription": pcs.course.description or "",
                    "courseType":        pcs.course.course_type.title if pcs.course.course_type else "—",
                    "courseTypeId":      pcs.course.course_type_id,
                    "courseNum":         pcs.course_num,
                    "courseOrder":       pcs.course_order,
                    "schemeTitle":       pcs.scheme.title if pcs.scheme else "—",
                })

            try:
                prgm_sem = ProgrammeSemester.objects.select_related(
                    "programme", "semester"
                ).get(id=prgm_sem_id)
                programme_title = prgm_sem.programme.title
                semester_title  = prgm_sem.semester.code
            except ProgrammeSemester.DoesNotExist:
                programme_title = "—"
                semester_title  = "—"

            batch_title = "—"
            if batch_id:
                try:
                    batch_title = Batch.objects.get(id=batch_id).title
                except Batch.DoesNotExist:
                    pass

            return JsonResponse({
                "success": True, "message": "Success",
                "data": {
                    "courses":        courses,
                    "totalCourses":   len(courses),
                    "programmeTitle": programme_title,
                    "semesterTitle":  semester_title,
                    "batchTitle":     batch_title,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"success": False, "message": str(e), "data": {}}, status=400)


# ============================================================================
#   COURSE MANAGEMENT — Check Code Unique
#   POST /course-management/check-code/
# ===========================================
class CourseManagementCheckCode(ListAPIView):

    def post(self, request):
        try:
            course_code = request.data.get("course_code", "").strip().upper()
            exclude_id  = request.data.get("exclude_id")

            if not course_code:
                return JsonResponse(
                    {"success": False, "message": "course_code is required.", "data": {}},
                    status=400
                )

            qs = CourseMaster.objects.filter(code__iexact=course_code)
            if exclude_id:
                qs = qs.exclude(id=exclude_id)

            return JsonResponse(
                {"success": True, "message": "Success", "data": {"isUnique": not qs.exists()}}
            )

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"success": False, "message": str(e), "data": {}}, status=400)


# ============================================================================
#   COURSE MANAGEMENT — Edcourse-maskit Course
# ============================================================================
class CourseManagementEdit(ListAPIView):

    def post(self, request):
        try:
            pcs_id         = request.data.get("pcs_id")
            name           = request.data.get("name", "").strip()
            title          = request.data.get("title", "").strip()
            description    = request.data.get("description", "").strip()
            course_type_id = request.data.get("course_type_id")
            course_num     = request.data.get("course_num", "").strip()
            course_order   = request.data.get("course_order", 1)
            updated_by     = request.user
            now            = timezone.now()

            if not pcs_id:
                return JsonResponse({"success": False, "message": "pcs_id is required.", "data": {}}, status=400)
            if not name:
                return JsonResponse({"success": False, "message": "Course Name is required.", "data": {}}, status=400)
            if not title:
                return JsonResponse({"success": False, "message": "Short Title is required.", "data": {}}, status=400)
            if not course_type_id:
                return JsonResponse({"success": False, "message": "Course Type is required.", "data": {}}, status=400)

            try:
                pcs = ProgrammeCourseSemester.objects.select_related("course").get(id=pcs_id)
            except ProgrammeCourseSemester.DoesNotExist:
                return JsonResponse({"success": False, "message": "Course mapping not found.", "data": {}}, status=400)

            try:
                course_type = CourseTypeMaster.objects.get(id=course_type_id)
            except CourseTypeMaster.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid Course Type.", "data": {}}, status=400)

            with transaction.atomic():
                # 1. Update CourseMaster 
                course             = pcs.course
                course.name        = name
                course.title       = title
                course.description = description
                course.course_type = course_type
                course.slug        = slugify(title)
                course.updated_by  = updated_by
                course.updated_on  = now
                course.save()

                # 2. Update ProgrammeCourseSemester
                pcs.course_num   = course_num
                pcs.course_order = int(course_order) if course_order else pcs.course_order
                pcs.updated_by   = updated_by
                pcs.updated_on   = now
                pcs.save()

                # 3. Sync the Blueprint name to match the new course name
                QuestionPaperBluePrintMaster.objects.filter(course=course).update(
                    pattern_name=name[:100],
                    updated_by=updated_by,
                    updated_on=now
                )

            return JsonResponse({
                "success": True,
                "message": f'Course "{course.name}" ({course.code}) updated successfully.',
                "data":    {"courseId": course.id, "pcsId": pcs.id},
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"success": False, "message": str(e), "data": {}}, status=400)
        

# ============================================================================
#   COURSE MANAGEMENT — Add New Course With Mapping
# ============================================================================
class CourseManagementAddWithMapping(ListAPIView):

    def post(self, request):
        try:
            code           = request.data.get("code", "").strip().upper()
            name           = request.data.get("name", "").strip()
            title          = request.data.get("title", "").strip()
            description    = request.data.get("description", "").strip()
            course_type_id = request.data.get("course_type_id")
            prgm_sem_id    = request.data.get("prgm_sem_id")
            batch_id       = request.data.get("batch_id")
            course_order   = request.data.get("course_order", 1)
            course_num     = "0" + str(course_order)
            scheme_id      = request.data.get("scheme_id")
            created_by     = request.user
            now            = timezone.now()

            # ── Validate ─────────────────────────────────────────────────
            if not code:
                return JsonResponse({"success": False, "message": "Course Code is required.", "data": {}}, status=400)
            if not name:
                return JsonResponse({"success": False, "message": "Course Name is required.", "data": {}}, status=400)
            if not title:
                return JsonResponse({"success": False, "message": "Short Title is required.", "data": {}}, status=400)
            if not course_type_id:
                return JsonResponse({"success": False, "message": "Course Type is required.", "data": {}}, status=400)
            if not prgm_sem_id:
                return JsonResponse({"success": False, "message": "Semester selection is missing. Please re-fetch.", "data": {}}, status=400)
            if not batch_id:
                return JsonResponse({"success": False, "message": "Batch selection is missing. Please re-fetch.", "data": {}}, status=400)

            # ── Uniqueness check ──────────────────────────────────────────
            if CourseMaster.objects.filter(code__iexact=code).exists():
                return JsonResponse({
                    "success": False,
                    "message": f'Course code "{code}" already exists. Use a different code.',
                    "data": {}
                }, status=400)

            # ── FK lookups ────────────────────────────────────────────────
            try:
                course_type = CourseTypeMaster.objects.get(id=course_type_id)
            except CourseTypeMaster.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid Course Type.", "data": {}}, status=400)

            try:
                prgm_sem = ProgrammeSemester.objects.select_related(
                    'programme__programme_class', 
                    'programme__programme_group'
                ).get(id=prgm_sem_id)
            except ProgrammeSemester.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid Programme Semester.", "data": {}}, status=400)

            scheme = None
            if scheme_id:
                try:
                    scheme = SchemeMaster.objects.get(id=scheme_id)
                except SchemeMaster.DoesNotExist:
                    pass

            # ── Pre-fetch Syllabus and Regulation lookups ─────────────────
            latest_syllabus = SyllabusMaster.objects.filter(
                programme=prgm_sem.programme
            ).order_by('-id').first()

            latest_reg_mapping = None
            latest_regulation = None
            if scheme:
                latest_reg_mapping = UniversityRegulationSchemeProgramme.objects.filter(
                    programme=prgm_sem.programme,
                    scheme=scheme
                ).order_by('-regulation_id').first()
                latest_regulation = latest_reg_mapping.regulation if latest_reg_mapping else None

            try:
                pending_state_id = State.objects.get(label='PENDING').id
            except State.DoesNotExist:
                pending_state_id = 2  

            with transaction.atomic():
                # 1. Create CourseMaster ──────────────────────────────────
                course = CourseMaster.objects.create(
                    name=name,
                    code=code,
                    title=title,
                    description=title,
                    course_type=course_type,
                    slug=slugify(title),
                    created_by=created_by,
                    updated_by=created_by,
                    updated_on=now,
                    status_id=ACTIVE_STATE,
                    comments='Created via Course Management UI'
                )

                # 2. Create ProgrammeCourseSemester ───────────────────────
                pcs = ProgrammeCourseSemester.objects.create(
                    programme_semester=prgm_sem,
                    course=course,
                    course_num=course_num,
                    course_order=int(course_order) if course_order else 1,
                    scheme=scheme,
                    created_by=created_by,
                    updated_by=created_by,
                    updated_on=now,
                    status_id=ACTIVE_STATE,
                    comments='Created via Course Management UI'
                )

                # 3. Create SyllabusDetails ───────────────────────────────
                if latest_syllabus:
                    SyllabusDetails.objects.create(
                        programme_course_semester=pcs,
                        syllabus=latest_syllabus,
                        created_by=created_by,
                        updated_by=created_by,
                        updated_on=now,
                        status_id=ACTIVE_STATE,
                        comments='Mapped via Course Management UI'
                    )

                # 4. Create QuestionPaperBluePrintMaster ──────────────────
                if latest_regulation and scheme:
                    QuestionPaperBluePrintMaster.objects.create(
                        pattern_name=name[:100], 
                        pattern_code=code[:50],
                        regulation=latest_regulation,
                        course=course,
                        scheme=scheme,
                        exam_type_id=2,    
                        maximum_mark='100',  
                        exam_duration='180', 
                        created_by=created_by,
                        updated_by=created_by,
                        updated_on=now,
                        status_id=ACTIVE_STATE,
                        comments='Generated via Course Management UI'
                    )

                # 5. Link Programme Class & Group ─────────────────────────
                if prgm_sem.programme.programme_class:
                    CourseProgrammeClass.objects.create(
                        course=course,
                        programme_class=prgm_sem.programme.programme_class,
                        created_by=created_by,
                        updated_by=created_by,
                        updated_on=now,
                        status_id=ACTIVE_STATE
                    )

                if prgm_sem.programme.programme_group:
                    CourseProgrammeGroup.objects.create(
                        course=course,
                        programme_group=prgm_sem.programme.programme_group,
                        created_by=created_by,
                        updated_by=created_by,
                        updated_on=now,
                        status_id=ACTIVE_STATE
                    )

                # 6. CollegeProgrammeCourse for every college in the batch ─
                # Exclude external examiner college (code 999)
                cbps_qs = CollegeBatchProgrammeSemester.objects.filter(
                    prgm_semester=prgm_sem,
                    college_batch_prgm__batch_id=batch_id,
                ).exclude(
                    college_batch_prgm__college_programm__college_department__college__code='999'
                )

                college_count = 0
                # for cbps in cbps_qs:
                #     CollegeProgrammeCourse.objects.create(
                #         colg_batch_prgm_sem=cbps,
                #         prgm_cors_sem=pcs,
                #         status_id=pending_state_id,
                #         created_by=created_by,
                #         updated_by=created_by,
                #         updated_on=now,
                #         comments='Mapped via Course Management UI'
                #     )
                #     college_count += 1

            return JsonResponse({
                "success": True,
                "message": (
                    f'Course "{name}" ({code}) created and completely mapped. '
                    f'{college_count} college(s) updated.'
                ),
                "data": {
                    "courseId":     course.id,
                    "pcsId":        pcs.id,
                    "courseCode":   course.code,
                    "courseName":   course.name,
                    "courseType":   course_type.title,
                    "courseTypeId": course_type.id,
                    "courseNum":    pcs.course_num,
                    "courseOrder":  pcs.course_order,
                    "schemeTitle":  scheme.title if scheme else "—",
                    "collegeCount": college_count,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"success": False, "message": str(e), "data": {}}, status=400)

# ============================================================================
#   COURSE MANAGEMENT — Course Search
#   POST /course-management/course-search/
# ============================================================================


# ============================================================================
class CourseManagementProgrammeSearch(ListAPIView):

    def post(self, request):
        try:
            from django.db.models import Q
            query = request.data.get("query", "").strip()

            if len(query) < 2:
                return JsonResponse({"success": True, "message": "Success", "data": {"programmes": []}})

            progs = Programme.objects.filter(
                Q(code__icontains=query) | Q(title__icontains=query)
            ).order_by("title")[:25]

            return JsonResponse({
                "success": True, "message": "Success",
                "data": {
                    "programmes": [
                        {"id": p.id, "title": p.title, "code": p.code or ""}
                        for p in progs
                    ]
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"success": False, "message": str(e), "data": {}}, status=400)



# ============================================================================
#   COURSE MANAGEMENT — Add New Course With MULTIPLE Semester Mappings
# ============================================================================
class CourseManagementAddWithMultiMapping(ListAPIView):

    def post(self, request):
        try:
            code           = request.data.get("code", "").strip().upper()
            name           = request.data.get("name", "").strip()
            course_type_id = request.data.get("course_type_id")
            global_order   = int(request.data.get("course_order", 1) or 1)
            mappings       = request.data.get("mappings", [])
            created_by     = request.user
            now            = timezone.now()

            # ── Validate top-level ────────────────────────────────────────
            if not code:
                return JsonResponse({"success": False, "message": "Course Code is required.", "data": {}}, status=400)
            if not name:
                return JsonResponse({"success": False, "message": "Course Name is required.", "data": {}}, status=400)
            if not course_type_id:
                return JsonResponse({"success": False, "message": "Course Type is required.", "data": {}}, status=400)
            if not mappings:
                return JsonResponse({"success": False, "message": "At least one Programme Semester mapping is required.", "data": {}}, status=400)

            # ── Validate each mapping entry ───────────────────────────────
            for idx, m in enumerate(mappings):
                row = idx + 1
                if not m.get("prgm_sem_id"):
                    return JsonResponse({"success": False, "message": f"Row {row}: Semester is required.", "data": {}}, status=400)
                if not m.get("scheme_id"):
                    return JsonResponse({"success": False, "message": f"Row {row}: Scheme is required.", "data": {}}, status=400)

            # ── Course code uniqueness ────────────────────────────────────
            if CourseMaster.objects.filter(code__iexact=code).exists():
                return JsonResponse({
                    "success": False,
                    "message": f'Course code "{code}" already exists. Use a different code.',
                    "data": {}
                }, status=400)

            # ── Course Type FK ────────────────────────────────────────────
            try:
                course_type = CourseTypeMaster.objects.get(id=course_type_id)
            except CourseTypeMaster.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid Course Type.", "data": {}}, status=400)

            # ── Pre-resolve ProgrammeSemester + Scheme for every row ──────
            resolved = []
            for idx, m in enumerate(mappings):
                row = idx + 1
                try:
                    prgm_sem = ProgrammeSemester.objects.select_related(
                        "programme__programme_class",
                        "programme__programme_group",
                        "semester",
                    ).get(id=m["prgm_sem_id"])
                except ProgrammeSemester.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"Row {row}: Programme Semester not found.", "data": {}}, status=400)

                try:
                    scheme = SchemeMaster.objects.get(id=m["scheme_id"])
                except SchemeMaster.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"Row {row}: Scheme not found.", "data": {}}, status=400)

                latest_syllabus = SyllabusMaster.objects.filter(
                    programme=prgm_sem.programme
                ).order_by("-id").first()

                latest_reg_mapping = UniversityRegulationSchemeProgramme.objects.filter(
                    programme=prgm_sem.programme,
                    scheme=scheme,
                ).order_by("-regulation_id").first()
                latest_regulation = latest_reg_mapping.regulation if latest_reg_mapping else None

                row_order  = int(m.get("course_order") or global_order)
                course_num = "0" + str(row_order)

                resolved.append({
                    "prgm_sem":          prgm_sem,
                    "scheme":            scheme,
                    "latest_syllabus":   latest_syllabus,
                    "latest_regulation": latest_regulation,
                    "course_order":      row_order,
                    "course_num":        course_num,
                })

            # ── All validation passed — write atomically ───────────────────
            total_pcs_created = 0
            linked_classes    = set()
            linked_groups     = set()
            linked_syllabuses = set()
            linked_blueprints = set()

            with transaction.atomic():
                # 1. CourseMaster — created once
                course = CourseMaster.objects.create(
                    name=name,
                    code=code,
                    title=name,
                    description=name,
                    course_type=course_type,
                    slug=slugify(name),
                    created_by=created_by,
                    updated_by=created_by,
                    updated_on=now,
                    status_id=ACTIVE_STATE,
                    comments="Created via Course Management UI",
                )

                for r in resolved:
                    prgm_sem = r["prgm_sem"]
                    scheme   = r["scheme"]

                    # 2. ProgrammeCourseSemester
                    pcs, pcs_created = ProgrammeCourseSemester.objects.get_or_create(
                        programme_semester=prgm_sem,
                        course=course,
                        scheme=scheme,
                        defaults={
                            "course_num":   r["course_num"],
                            "course_order": r["course_order"],
                            "created_by":   created_by,
                            "updated_by":   created_by,
                            "updated_on":   now,
                            "status_id":    ACTIVE_STATE,
                            "comments":     "Created via Course Management UI",
                        }
                    )
                    if pcs_created:
                        total_pcs_created += 1

                    # 3. SyllabusDetails — once per unique syllabus
                    if r["latest_syllabus"]:
                        syl_id = r["latest_syllabus"].id
                        if syl_id not in linked_syllabuses:
                            SyllabusDetails.objects.get_or_create(
                                programme_course_semester=pcs,
                                syllabus=r["latest_syllabus"],
                                defaults={
                                    "created_by": created_by,
                                    "updated_by": created_by,
                                    "updated_on": now,
                                    "status_id":  ACTIVE_STATE,
                                    "comments":   "Mapped via Course Management UI",
                                }
                            )
                            linked_syllabuses.add(syl_id)

                    # 4. QuestionPaperBluePrintMaster — once per (scheme, regulation)
                    if r["latest_regulation"] and scheme:
                        bp_key = (scheme.id, r["latest_regulation"].id)
                        if bp_key not in linked_blueprints:
                            QuestionPaperBluePrintMaster.objects.get_or_create(
                                regulation=r["latest_regulation"],
                                course=course,
                                scheme=scheme,
                                defaults={
                                    "pattern_name": name[:100],
                                    "pattern_code": code[:50],
                                    "exam_type_id": 2,
                                    "maximum_mark": "100",
                                    "exam_duration": "180",
                                    "created_by":   created_by,
                                    "updated_by":   created_by,
                                    "updated_on":   now,
                                    "status_id":    ACTIVE_STATE,
                                    "comments":     "Generated via Course Management UI",
                                }
                            )
                            linked_blueprints.add(bp_key)

                    # 5. CourseProgrammeClass — once per unique class
                    prog_class = prgm_sem.programme.programme_class
                    if prog_class and prog_class.id not in linked_classes:
                        CourseProgrammeClass.objects.get_or_create(
                            course=course,
                            programme_class=prog_class,
                            defaults={
                                "created_by": created_by, "updated_by": created_by,
                                "updated_on": now, "status_id": ACTIVE_STATE,
                            },
                        )
                        linked_classes.add(prog_class.id)

                    # 6. CourseProgrammeGroup — once per unique group
                    prog_group = prgm_sem.programme.programme_group
                    if prog_group and prog_group.id not in linked_groups:
                        CourseProgrammeGroup.objects.get_or_create(
                            course=course,
                            programme_group=prog_group,
                            defaults={
                                "created_by": created_by, "updated_by": created_by,
                                "updated_on": now, "status_id": ACTIVE_STATE,
                            },
                        )
                        linked_groups.add(prog_group.id)

                    # CollegeProgrammeCourse intentionally NOT created here.
                    # College mapping is handled separately via Student Mapping workflow.

            return JsonResponse({
                "success": True,
                "message": (
                    f'Course "{name}" ({code}) created and mapped to '
                    f'{total_pcs_created} semester(s) successfully.'
                ),
                "data": {
                    "courseId":   course.id,
                    "courseCode": course.code,
                    "pcsCount":   total_pcs_created,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"success": False, "message": str(e), "data": {}}, status=400)


class CourseManagementCourseSearch(ListAPIView):

    def post(self, request):
        try:
            from django.db.models import Q
            query = request.data.get("query", "").strip()

            if len(query) < 2:
                return JsonResponse(
                    {"success": True, "message": "Success", "data": {"courses": []}})

            qs = CourseMaster.objects.filter(
                Q(code__icontains=query) | Q(name__icontains=query)
            ).select_related("course_type").order_by("code")[:30]

            return JsonResponse({
                "success": True, "message": "Success",
                "data": {
                    "courses": [
                        {
                            "id":           c.id,
                            "code":         c.code,
                            "name":         c.name,
                            "title":        c.title or "",
                            "courseType":   c.course_type.title if c.course_type else "—",
                            "courseTypeId": c.course_type_id,
                        }
                        for c in qs
                    ]
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": str(e), "data": {}}, status=400)


# ============================================================================
#   COURSE MANAGEMENT — Map Existing Course to Multiple Programme Semesters
#   POST /course-management/map-existing/
# ============================================================================
class CourseManagementMapExisting(ListAPIView):

    def post(self, request):
        try:
            course_id  = request.data.get("course_id")
            mappings   = request.data.get("mappings", [])
            created_by = request.user
            now        = timezone.now()

            # ── Validate ──────────────────────────────────────────────────
            if not course_id:
                return JsonResponse(
                    {"success": False, "message": "course_id is required.", "data": {}}, status=400)
            if not mappings:
                return JsonResponse(
                    {"success": False, "message": "At least one Programme Semester mapping is required.", "data": {}}, status=400)

            try:
                course = CourseMaster.objects.select_related("course_type").get(id=course_id)
            except CourseMaster.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Course not found.", "data": {}}, status=400)

            for idx, m in enumerate(mappings):
                row = idx + 1
                if not m.get("prgm_sem_id"):
                    return JsonResponse(
                        {"success": False, "message": f"Row {row}: Semester is required.", "data": {}}, status=400)
                if not m.get("scheme_id"):
                    return JsonResponse(
                        {"success": False, "message": f"Row {row}: Scheme is required.", "data": {}}, status=400)

            # ── Pre-resolve FKs ───────────────────────────────────────────
            resolved = []
            for idx, m in enumerate(mappings):
                row = idx + 1

                try:
                    prgm_sem = ProgrammeSemester.objects.select_related(
                        "programme__programme_class",
                        "programme__programme_group",
                        "semester",
                    ).get(id=m["prgm_sem_id"])
                except ProgrammeSemester.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": f"Row {row}: Programme Semester not found.", "data": {}}, status=400)

                try:
                    scheme = SchemeMaster.objects.get(id=m["scheme_id"])
                except SchemeMaster.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": f"Row {row}: Scheme not found.", "data": {}}, status=400)

                latest_syllabus = SyllabusMaster.objects.filter(
                    programme=prgm_sem.programme
                ).order_by("-id").first()

                latest_reg_mapping = UniversityRegulationSchemeProgramme.objects.filter(
                    programme=prgm_sem.programme,
                    scheme=scheme,
                ).order_by("-regulation_id").first()
                latest_regulation = latest_reg_mapping.regulation if latest_reg_mapping else None

                row_order  = int(m.get("course_order") or 1)
                course_num = "0" + str(row_order)

                resolved.append({
                    "prgm_sem":          prgm_sem,
                    "scheme":            scheme,
                    "latest_syllabus":   latest_syllabus,
                    "latest_regulation": latest_regulation,
                    "course_order":      row_order,
                    "course_num":        course_num,
                })

            # ── Write atomically ──────────────────────────────────────────
            total_pcs_created = 0
            total_skipped     = 0
            linked_classes    = set()
            linked_groups     = set()
            linked_syllabuses = set()
            linked_blueprints = set()

            with transaction.atomic():
                for r in resolved:
                    prgm_sem = r["prgm_sem"]
                    scheme   = r["scheme"]

                    # 1. ProgrammeCourseSemester
                    pcs, pcs_created = ProgrammeCourseSemester.objects.get_or_create(
                        programme_semester=prgm_sem,
                        course=course,
                        scheme=scheme,
                        defaults={
                            "course_num":   r["course_num"],
                            "course_order": r["course_order"],
                            "created_by":   created_by,
                            "updated_by":   created_by,
                            "updated_on":   now,
                            "status_id":    ACTIVE_STATE,
                            "comments":     "Mapped via Course Management UI",
                        }
                    )
                    if pcs_created:
                        total_pcs_created += 1
                    else:
                        total_skipped += 1
                        continue   # already mapped — skip sub-records

                    # 2. SyllabusDetails — once per unique syllabus
                    if r["latest_syllabus"]:
                        syl_id = r["latest_syllabus"].id
                        if syl_id not in linked_syllabuses:
                            SyllabusDetails.objects.get_or_create(
                                programme_course_semester=pcs,
                                syllabus=r["latest_syllabus"],
                                defaults={
                                    "created_by": created_by,
                                    "updated_by": created_by,
                                    "updated_on": now,
                                    "status_id":  ACTIVE_STATE,
                                    "comments":   "Mapped via Course Management UI",
                                }
                            )
                            linked_syllabuses.add(syl_id)

                    # 3. QuestionPaperBluePrintMaster — once per (scheme, regulation)
                    if r["latest_regulation"] and scheme:
                        bp_key = (scheme.id, r["latest_regulation"].id)
                        if bp_key not in linked_blueprints:
                            QuestionPaperBluePrintMaster.objects.get_or_create(
                                regulation=r["latest_regulation"],
                                course=course,
                                scheme=scheme,
                                defaults={
                                    "pattern_name": course.name[:100],
                                    "pattern_code": course.code[:50],
                                    "exam_type_id": 2,
                                    "maximum_mark": "100",
                                    "exam_duration": "180",
                                    "created_by":   created_by,
                                    "updated_by":   created_by,
                                    "updated_on":   now,
                                    "status_id":    ACTIVE_STATE,
                                    "comments":     "Generated via Course Management UI",
                                }
                            )
                            linked_blueprints.add(bp_key)

                    # 4. CourseProgrammeClass — once per unique class
                    prog_class = prgm_sem.programme.programme_class
                    if prog_class and prog_class.id not in linked_classes:
                        CourseProgrammeClass.objects.get_or_create(
                            course=course,
                            programme_class=prog_class,
                            defaults={
                                "created_by": created_by, "updated_by": created_by,
                                "updated_on": now, "status_id": ACTIVE_STATE,
                            },
                        )
                        linked_classes.add(prog_class.id)

                    # 5. CourseProgrammeGroup — once per unique group
                    prog_group = prgm_sem.programme.programme_group
                    if prog_group and prog_group.id not in linked_groups:
                        CourseProgrammeGroup.objects.get_or_create(
                            course=course,
                            programme_group=prog_group,
                            defaults={
                                "created_by": created_by, "updated_by": created_by,
                                "updated_on": now, "status_id": ACTIVE_STATE,
                            },
                        )
                        linked_groups.add(prog_group.id)

                    # CollegeProgrammeCourse intentionally NOT created here.
                    # College mapping is handled separately via Student Mapping workflow.

            skip_note = f" ({total_skipped} already mapped — skipped)." if total_skipped else "."
            return JsonResponse({
                "success": True,
                "message": (
                    f'Course "{course.name}" ({course.code}) mapped to '
                    f'{total_pcs_created} semester(s){skip_note}'
                ),
                "data": {
                    "courseId":   course.id,
                    "courseCode": course.code,
                    "pcsCreated": total_pcs_created,
                    "skipped":    total_skipped,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": str(e), "data": {}}, status=400)




# ============================================================================
#   COURSE MANAGEMENT — Course Current Mappings
#   POST /course-management/course-current-mappings/
# ============================================================================
class CourseManagementCourseCurrentMappings(ListAPIView):

    def post(self, request):
        try:
            course_id = request.data.get("course_id")

            if not course_id:
                return JsonResponse(
                    {"success": False, "message": "course_id is required.", "data": {}},
                    status=400
                )

            try:
                course = CourseMaster.objects.select_related("course_type").get(id=course_id)
            except CourseMaster.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Course not found.", "data": {}},
                    status=400
                )

            pcs_qs = ProgrammeCourseSemester.objects.filter(
                course=course
            ).select_related(
                "programme_semester__programme__programme_type",
                "programme_semester__programme__programme_group",
                "programme_semester__programme__programme_class",
                "programme_semester__semester",
                "scheme",
            ).order_by(
                "programme_semester__programme__title",
                "programme_semester__semester__code",
            )

            mappings = []
            for pcs in pcs_qs:
                ps   = pcs.programme_semester
                prog = ps.programme
                sem  = ps.semester

                mappings.append({
                    "pcsId":          pcs.id,
                    "programmeId":    prog.id,
                    "programme":      prog.title,
                    "programmeCode":  prog.code or "—",
                    "programmeType":  prog.programme_type.title  if prog.programme_type  else "—",
                    "programmeGroup": prog.programme_group.title if prog.programme_group else "—",
                    "programmeClass": prog.programme_class.title if prog.programme_class else "—",
                    "semester":       f"Semester {sem.code}" if sem else "—",
                    "semesterCode":   sem.code if sem else "—",
                    "scheme":         pcs.scheme.title if pcs.scheme else "—",
                    "courseNum":      pcs.course_num  or "—",
                    "courseOrder":    pcs.course_order,
                })

            return JsonResponse({
                "success": True,
                "message": "Success",
                "data": {
                    "mappings":      mappings,
                    "totalMappings": len(mappings),
                    "courseName":    course.name,
                    "courseCode":    course.code,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": str(e), "data": {}}, status=400
            )



# # =============================================================================
# #   GET /course-mask/
# #   Renders course_mask.html — no special data needed (no cascade selects).
# # =============================================================================

class CourseMaskPageLoad(ListAPIView):

    def get(self, request):
        try:
            return format_response(
                True, "Success",
                data={},
                status_code=status.HTTP_200_OK,
                template_name="course_mask.html",
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            return format_response(
                False, BAD_GATEWAY, {}, BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                template_name="500.html",
            )


# =============================================================================
#   2. GET MAPPINGS FOR A COURSE
#   POST /course-mask/mappings/
# =============================================================================
class CourseMaskGetMappings(ListAPIView):

    def post(self, request):
        try:
            course_id = request.data.get("course_id")

            if not course_id:
                return JsonResponse(
                    {"success": False, "message": "course_id is required.", "data": {}},
                    status=400,
                )

            # ── Fetch CourseMaster ──────────────────────────────────────────
            try:
                course = CourseMaster.objects.select_related("course_type").get(id=course_id)
            except CourseMaster.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Course not found.", "data": {}},
                    status=400,
                )

            # ── Fetch all PCS rows for this course ──────────────────────────
            pcs_qs = (
                ProgrammeCourseSemester.objects
                .filter(course=course)
                .select_related(
                    "programme_semester__programme__programme_type",
                    "programme_semester__programme__programme_group",
                    "programme_semester__programme__programme_class",
                    "programme_semester__semester",
                    "scheme",
                )
                .order_by(
                    "programme_semester__programme__title",
                    "programme_semester__semester__code",
                )
            )

            mappings = []
            active_count = 0

            for pcs in pcs_qs:
                ps   = pcs.programme_semester
                prog = ps.programme
                sem  = ps.semester

                is_active = (pcs.status_id != 5)
                if is_active:
                    active_count += 1

                mappings.append({
                    "pcsId":          pcs.id,
                    "pcsStatusId":    pcs.status_id,   # 5 = Masked
                    "programme":      prog.title,
                    "programmeCode":  prog.code or "—",
                    "programmeType":  prog.programme_type.title  if prog.programme_type  else "—",
                    "programmeGroup": prog.programme_group.title if prog.programme_group else "—",
                    "programmeClass": prog.programme_class.title if prog.programme_class else "—",
                    "semester":       f"Semester {sem.code}" if sem else "—",
                    "semesterCode":   sem.code if sem else "—",
                    "scheme":         pcs.scheme.title if pcs.scheme else "—",
                    "courseNum":      pcs.course_num   or "—",
                    "courseOrder":    pcs.course_order,
                })

            return JsonResponse({
                "success": True,
                "message": "Success",
                "data": {
                    "mappings":       mappings,
                    "totalMappings":  len(mappings),
                    "activeMappings": active_count,
                    "courseStatusId": course.status_id,
                    "courseName":     course.name,
                    "courseCode":     course.code,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": str(e), "data": {}},
                status=400,
            )


# =============================================================================
#   3. EXECUTE MASK
#   POST /course-mask/execute/
# =============================================================================
class CourseMaskExecute(ListAPIView):

    def post(self, request):
        try:
            course_id  = request.data.get("course_id")
            pcs_ids    = request.data.get("pcs_ids", [])
            updated_by = request.user
            now        = timezone.now()

            # ── Validate inputs ─────────────────────────────────────────────
            if not course_id:
                return JsonResponse(
                    {"success": False, "message": "course_id is required.", "data": {}},
                    status=400,
                )
            if not pcs_ids or not isinstance(pcs_ids, list) or len(pcs_ids) == 0:
                return JsonResponse(
                    {"success": False, "message": "pcs_ids must be a non-empty list.", "data": {}},
                    status=400,
                )

            # ── Fetch CourseMaster ──────────────────────────────────────────
            try:
                course = CourseMaster.objects.get(id=course_id)
            except CourseMaster.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Course not found.", "data": {}},
                    status=400,
                )

            # ── Perform all writes atomically ────────────────────────────────
            masked_pcs_count = 0
            masked_course    = False

            with transaction.atomic():

                # ── Step 1: Mask each selected PCS row ──────────────────────
                for pcs_id in pcs_ids:
                    try:
                        pcs = ProgrammeCourseSemester.objects.get(
                            id=pcs_id,
                            course_id=course_id,   # security: must belong to this course
                        )
                    except ProgrammeCourseSemester.DoesNotExist:
                        # Skip silently if the row doesn't exist or belongs to another course
                        continue

                    if pcs.status_id == 5:
                        # Already masked — nothing to do
                        continue

                    pcs.status_id  = 5
                    pcs.updated_by = updated_by
                    pcs.updated_on = now
                    pcs.save()
                    masked_pcs_count += 1

                # ── Step 2: Check if any PCS rows are still active ───────────
                still_active = (
                    ProgrammeCourseSemester.objects
                    .filter(course_id=course_id)
                    .exclude(status_id=5)
                    .count()
                )

                # ── Step 3: If none remain active, mask the CourseMaster too ─
                if still_active == 0 and course.status_id != 5:
                    course.status_id  = 5
                    course.updated_by = updated_by
                    course.updated_on = now
                    course.save()
                    masked_course = True

            # ── Build response message ───────────────────────────────────────
            if masked_course:
                message = (
                    f'{masked_pcs_count} mapping(s) masked successfully. '
                    f'All mappings are now masked — '
                    f'Course "{course.name}" ({course.code}) has also been masked.'
                )
            else:
                message = (
                    f'{masked_pcs_count} mapping(s) masked successfully.'
                )

            return JsonResponse({
                "success": True,
                "message": message,
                "data": {
                    "maskedPcsCount": masked_pcs_count,
                    "maskedCourse":   masked_course,
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": str(e), "data": {}},
                status=400,
            )


# =============================================================================
#   4. UNMASK A SINGLE PCS ROW
#   POST /course-mask/unmask/
# =============================================================================
class CourseMaskUnmask(ListAPIView):

    def post(self, request):
        try:
            course_id  = request.data.get("course_id")
            pcs_id     = request.data.get("pcs_id")
            updated_by = request.user
            now        = timezone.now()

            # ── Validate ────────────────────────────────────────────────────
            if not course_id:
                return JsonResponse(
                    {"success": False, "message": "course_id is required.", "data": {}},
                    status=400,
                )
            if not pcs_id:
                return JsonResponse(
                    {"success": False, "message": "pcs_id is required.", "data": {}},
                    status=400,
                )

            # ── Fetch CourseMaster ──────────────────────────────────────────
            try:
                course = CourseMaster.objects.get(id=course_id)
            except CourseMaster.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Course not found.", "data": {}},
                    status=400,
                )

            # ── Fetch PCS (must belong to this course) ───────────────────────
            try:
                pcs = ProgrammeCourseSemester.objects.get(
                    id=pcs_id,
                    course_id=course_id,
                )
            except ProgrammeCourseSemester.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Mapping not found for this course.", "data": {}},
                    status=400,
                )

            # ── Guard: already active ───────────────────────────────────────
            if pcs.status_id != 5:
                return JsonResponse(
                    {"success": False, "message": "This mapping is not masked.", "data": {}},
                    status=400,
                )

            # ── Restore both PCS and CourseMaster atomically ─────────────────
            with transaction.atomic():
                # Unmask the selected PCS row
                pcs.status_id  = ACTIVE_STATE
                pcs.updated_by = updated_by
                pcs.updated_on = now
                pcs.save()

                # Always unmask CourseMaster too — even if other PCS rows are still masked
                course.status_id  = ACTIVE_STATE
                course.updated_by = updated_by
                course.updated_on = now
                course.save()

            return JsonResponse({
                "success": True,
                "message": (
                    f' Unmasked successfully. '
                    f'Course "{course.name}" ({course.code}) '
                    f'has also been restored to Active.'
                ),
                "data": {
                    "pcsId":      pcs.id,
                    "courseId":   course.id,
                    "maskedCourse": True,   # CourseMaster was touched
                },
            })

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": str(e), "data": {}},
                status=400,
            )

