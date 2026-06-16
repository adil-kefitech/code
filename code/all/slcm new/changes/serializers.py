# from asyncio import exceptions
import base64
import datetime
import json
from datetime import datetime as dt
from dis import code_info
from functools import reduce
from select import select

# from .constants import*
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import F, Q
from django.http import JsonResponse
from django.utils import timezone
from django.utils.encoding import (
    DjangoUnicodeDecodeError,
    force_str,
    smart_bytes,
    smart_str,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from util.constants import *
from util.models import *
from util.serializers import (
    ProgrammeClassSerializer,
    ProgrammeGroupSerializer,
    ProgrammeTypeMasterSerializers,
)

from .models import *  # importing modeles we created
from urllib.parse import urljoin



# from file_storage import FileStorage
class PgmSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Programme
        fields = ["id", "title"]

    def get_title(self, obj):
        try:
            title = obj.name + "(" + obj.code + ")"
            return title
        except:
            return "NA"


# class SemListSerializer(serializers.ModelSerializer):
#     #id=serializers.SerializerMethodField()
#     #name=serializers.SerializerMethodField()
#     class Meta:
#         model=ProgrammeSemester
#         fields=['id','code']

#     def get_code(self,obj):
#         try:
#             name=SemesterMaster.objects.filter(id=obj.semester_id).all().code
#             return name
#         except:
#             return 'NA'

#     def get_code(self,obj):
#         try:
#             name=SemesterMaster.objects.filter(id=obj.semester_id).all().id
#             return name
#         except:
#             return 'NA'


class ExamcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = ["id", "code"]


class DisctrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "title"]


class SASerializer(serializers.ModelSerializer):
    sqno = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    answersheet_url = serializers.SerializerMethodField()

    class Meta:
        model = ScannedAnswersheet
        fields = ["id", "sqno", "answersheet_url", "status"]

    def get_sqno(self, obj):
        try:
            print(f"{obj.dfm_id=}")
            i = (
                BundleCandidateMapper.objects.filter(
                    digital_false_no_id=obj.dfm_id
                )
                .first()
                .sequence_no
            )
            return i
        except:
            return "NA"

    def get_status(self, obj):
        try:
            i = obj.status.label
            return i
        except:
            return "NA"

    def get_answersheet_url(self, obj):

        if settings.BASE_FILE_PATH:
            base_path = settings.BASE_FILE_PATH.rstrip("/")  # Remove trailing slash if any
            answer_url = obj.answersheet_url.url.lstrip("/")  # Remove leading slash if any

            final_url = f"{base_path}/{answer_url}"
            return final_url
        else:
            return f"{obj.answersheet_url.url}"

    # def get_link(self,obj):
    #     try:
    #         sqno=obj.answersheet_url
    #         return sqno
    #     except:
    #         return 'NA'
    # def get_status(self,obj):
    #     try:
    #         sqno=obj.status_id
    #         return sqno
    #     except:
    #         return 'NA'


class QPCourseSerializer(serializers.ModelSerializer):
    cname = serializers.SerializerMethodField()
    pgmcourseid = serializers.SerializerMethodField()
    pgmname = serializers.SerializerMethodField()

    class Meta:

        model = QuestionPaperExamMapper

        fields = ["id", "cname", "pgmcourseid", "pgmname"]

        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }

    def get_cname(self, obj):
        if obj.qp.qp_pattern.sub_course:
            return (
                obj.qp.qp_pattern.course.name
                + " ("
                + obj.qp.qp_pattern.sub_course.name
                + ")"
                + " ("
                + obj.qp.qp_pattern.course.code
                + ")"
            )
        else:
            return (
                obj.qp.qp_pattern.course.name
                + " ("
                + obj.qp.qp_pattern.course.code
                + ")"
            )

    def get_pgmcourseid(self, obj):  # pgmcourseID
        try:
            examprgsem = ExamProgrammeSemesterMapping.objects.filter(
                exam=obj.exam
            ).first()

            prg_course = ProgrammeCourseSemester.objects.filter(
                sub_course=obj.qp.qp_pattern.sub_course,
                course=obj.qp.qp_pattern.course,
                programme_semester=examprgsem.programme_semester,
            ).first()

            return prg_course.id
        except Exception as e :
            logger.error(e,exc_info=True)
            return "NA"

    def get_pgmname(self, obj):
        examprgsem = ExamProgrammeSemesterMapping.objects.filter(
            exam=obj.exam
        ).first()
        prgtitle = (
            examprgsem.programme_semester.programme.programme_class.title
            + " "
            + examprgsem.programme_semester.programme.name
        )
        return prgtitle


class CampRoleAllocationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    userid = serializers.IntegerField(source="camp_user.id")

    class Meta:

        model = CampRoleAllocation

        fields = ["id", "username", "userid"]

        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }

    def get_username(self, obj):
        user = User.objects.filter(id=obj.camp_user.id).first()
        return user.get_full_name()


class AnswersheetExaminationScheduleSerializer(serializers.ModelSerializer):
    examtitle = serializers.CharField(source="exam.title")
    examid = serializers.IntegerField(source="exam.id")
    courseid = serializers.IntegerField(source="programme_semester_course.id")
    examcode = serializers.CharField(source="exam.code")
    coursecode = serializers.CharField(
        source="programme_semester_course.course.code"
    )
    start_date = serializers.DateField(format="%d-%m-%Y")

    coursetitle = serializers.SerializerMethodField()

    class Meta:

        model = ExaminationSchedule

        fields = [
            "examtitle",
            "examid",
            "courseid",
            "coursetitle",
            "examcode",
            "coursecode",
            "start_date",
        ]

        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }

    def get_coursetitle(self, obj):
        try:
            if obj.programme_semester_course.sub_course:
                return (
                    obj.programme_semester_course.course.name
                    + " ("
                    + obj.programme_semester_course.sub_course.name
                    + ")"
                )
            else:
                return obj.programme_semester_course.course.name
        except:
            return "NA"


class ProgrammeCourseSemesterNew(serializers.ModelSerializer):
    prgm_course_sem_id = serializers.CharField(source="id")
    course_id = serializers.CharField(source="course.id")
    course_name = serializers.CharField(source="course.name")
    course_type_code = serializers.CharField(source="course.course_type.code")
    duaration = serializers.SerializerMethodField()

    class Meta:
        model = ProgrammeCourseSemester

        fields = [
            "prgm_course_sem_id",
            "course_id",
            "course_name",
            "course_type_code",
            "duaration",
        ]

        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }


class SemesterwiseCourse(serializers.ModelSerializer):
    sem_id = serializers.CharField(source="semester.id")
    sem_title = serializers.CharField(source="semester.title")
    prgm_id = serializers.CharField(source="programme.id")
    # sem_code=serializers.CharField(source='semester.code')
    prgm_cours = ProgrammeCourseSemesterNew(many=True)
    # course_list=CourseSerializer(many=True)
    prgm_course_order = serializers.SerializerMethodField()

    class Meta:
        model = ProgrammeSemester

        fields = [
            "id",
            "sem_id",
            "prgm_id",
            "sem_title",
            "prgm_cours",
            "prgm_course_order",
        ]

        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }

    def get_prgm_course_order(self, obj):

        course_id = []
        course_data_id = []
        course_type_id = [13]
        prgm_course_order = ProgrammeCourseSemester.objects.filter(
            programme_semester=obj
        ).order_by("course_order")

        for prg_cour in prgm_course_order:
            cour_id = prg_cour.course.id
            course_data_id.append(cour_id)
        course_data = CourseMaster.objects.filter(
            id__in=course_data_id
        ).filter(~Q(course_type__in=course_type_id))

        prgm_sem_cour_final = ProgrammeCourseSemester.objects.filter(
            programme_semester=obj, course__in=course_data
        ).order_by("course_order")

        prgm_course_order_serl = ProgrammeCourseSemesterNew(
            prgm_sem_cour_final, many=True
        )

        return prgm_course_order_serl.data


class Smplr(serializers.ModelSerializer):
    class Meta:
        model = SmpReasonMaster
        fields = ["name"]


class BundleDisTypeSer(serializers.ModelSerializer):
    class Meta:
        model = BundleDistributionType
        fields = ["id", "name", "code"]


class PgmCourseSer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    sub_course = serializers.SerializerMethodField()
    pgmcosid = serializers.SerializerMethodField()
    pgmsemid = serializers.SerializerMethodField()

    class Meta:
        model = ProgrammeCourseSemester
        fields = ["id", "title", "code", "sub_course", "pgmcosid", "pgmsemid"]

    def get_title(self, o):
        try:
            id = CourseMaster.objects.get(id=o.course_id).title
            return id
        except:
            return "NA"

    def get_code(self, o):
        try:
            code = CourseMaster.objects.get(id=o.course_id).code
            return code
        except:
            return "NA"

    def get_sub_course(self, o):
        try:
            id = o.sub_course
            return id
        except:
            return "NA"

    def get_pgmcosid(self, o):
        try:
            id = o.id
            return id
        except:
            return "NA"

    def get_pgmsemid(self, o):
        try:
            id = o.programme_semester_id
            return id
        except:
            return "NA"

    def get_id(self, o):
        try:
            id = o.course_id
            return id
        except:
            return "NA"


class Courseserializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaster
        fields = ["id", "title","code"]


class Qpcodeserializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPaper
        fields = ["qp_code"]


class QpcodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleMaster
        fields = ["qp_code"]
        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }


class SubSectionSerializer(serializers.ModelSerializer):
    pgmt = serializers.SerializerMethodField()
    pgmg = serializers.SerializerMethodField()
    pgmc = serializers.SerializerMethodField()

    class Meta:
        model = SubsectionProgramme
        fields = ["pgmt", "pgmg", "pgmc"]

    def get_pgmt(self, obj):

        program_type = obj.programme.programme_type
        data = ProgrammeTypeMasterSerializers(program_type).data
        return data

    def get_pgmg(self, obj):

        program_type = obj.programme.programme_group
        data = ProgrammeGroupSerializer(program_type).data
        return data

    def get_pgmc(self, obj):

        program_type = obj.programme.programme_class
        data = ProgrammeClassSerializer(program_type).data
        return data


class QPUploadSerializer(serializers.ModelSerializer):
    qp_code = serializers.CharField(source="qp.qp_code", default="NA")
    course_name = serializers.SerializerMethodField()
    status = serializers.CharField(source="status.label", default="NA")

    qp_url = serializers.SerializerMethodField()

    ans_key_url = serializers.SerializerMethodField()
    ans_template = serializers.SerializerMethodField()

    class Meta:

        model = QuestionPaperExamMapper
        fields = (
            "qp_code",
            "course_name",
            "status",
            "qp_url",
            "ans_key_url",
            "ans_template",
        )

    def get_course_name(self, obj):
        if obj.qp.qp_pattern.sub_course:
            return (
                obj.qp.qp_pattern.course.name
                + " ("
                + obj.qp.qp_pattern.sub_course.name
                + ")"
                + " ("
                + obj.qp.qp_pattern.course.code
                + ")"
            )
        else:
            return (
                obj.qp.qp_pattern.course.name
                + " ("
                + obj.qp.qp_pattern.course.code
                + ")"
            )

    def get_ans_template(self, obj):
        qp_palette = obj.qp.questionpaperpalette_set.first()
        ans_form = " "
        if qp_palette:
            ans_form_url = qp_palette.ans_form
            ans_form = (
                f"{settings.BASE_FILE_PATH}media/{ans_form_url.strip()[0:]}"
            )

        return ans_form

    def get_qp_url(self, obj):
        qp_url = " "
        if obj.qp:
            url = obj.qp.question_paper_url
            if url:
                qp_url = f"{settings.BASE_FILE_PATH}media/{url.strip()[0:]}"
        return qp_url

    def get_ans_key_url(self, obj):
        ans_key_url = " "
        if obj.qp:
            url = obj.qp.answer_key_url
            if url:
                ans_key_url = (
                    f"{settings.BASE_FILE_PATH}media/{url.strip()[0:]}"
                )
        return ans_key_url




class OnscreenDistributionFilterView(serializers.ModelSerializer):
    qp_code = serializers.SerializerMethodField()
    bundle_code = serializers.SerializerMethodField()
    examiner = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    status = serializers.CharField(source="status.label")
    total_no_of_answersheet = serializers.SerializerMethodField()
    bundle = serializers.SerializerMethodField()
    examiner_id = serializers.SerializerMethodField()
    evaluvationtype = serializers.SerializerMethodField()
    evaluated_no_of_answersheet = serializers.SerializerMethodField()

    class Meta:
        model = BundleExaminer
        fields = [
            "id",
            "qp_code",
            "bundle_code",
            "bundle",
            "examiner",
            "examiner_id",
            "course_name",
            "status",
            "total_no_of_answersheet",
            "evaluvationtype",
            "evaluated_no_of_answersheet",
        ]
        extra_kwargs = {
            "created_on": {"write_only": True},
            "updated_on": {"write_only": True},
            "created_by": {"write_only": True},
            "updated_by": {"write_only": True},
        }

    def get_qp_code(self, obj):
        BundleCampobj = BundleCamp.objects.filter(
            id=obj.bundle_camp.id
        ).first()
        bundleid = BundleCampobj.bundle.id
        BundleMasterobj = BundleMaster.objects.filter(id=bundleid).first()
        qpcode = BundleMasterobj.qp_code
        return qpcode

    def get_bundle_code(self, obj):
        BundleCampobj = BundleCamp.objects.filter(
            id=obj.bundle_camp.id
        ).first()
        bundleid = BundleCampobj.bundle.id
        BundleMasterobj = BundleMaster.objects.filter(id=bundleid).first()
        bundlecode = BundleMasterobj.bundle_code
        return bundlecode

    def get_bundle(self, obj):
        BundleCampobj = BundleCamp.objects.filter(
            id=obj.bundle_camp.id
        ).first()
        bundleid = BundleCampobj.bundle.id
        BundleMasterobj = BundleMaster.objects.filter(id=bundleid).first()
        bundleid = BundleMasterobj.id
        return bundleid

    def get_examiner(self, obj):
        CampRoleAllocationobj = CampRoleAllocation.objects.filter(
            id=obj.camp_rol_allo.id
        ).first()
        camp_user = CampRoleAllocationobj.camp_user.id
        user = UserProfiles.objects.filter(user_id=camp_user).first()
        return user.full_name

    def get_examiner_id(self, obj):
        CampRoleAllocationobj = CampRoleAllocation.objects.filter(
            id=obj.camp_rol_allo.id
        ).first()
        camp_user = CampRoleAllocationobj.camp_user.id
        return camp_user

    def get_course_name(self, obj):

        bundlemaster = BundleMaster.objects.filter(
            id=obj.bundle_camp.bundle.id
        ).first()
        programme_course_semester_id = (
            bundlemaster.programme_course_semester.id
        )

        ProgrammeCourseSemesterobj = ProgrammeCourseSemester.objects.filter(
            id=programme_course_semester_id
        ).first()
        if ProgrammeCourseSemesterobj.sub_course:
            return (
                ProgrammeCourseSemesterobj.course.name
                + " ("
                + ProgrammeCourseSemesterobj.sub_course.name
                + ")"
                + " ("
                + ProgrammeCourseSemesterobj.course.code
                + ")"
            )
        else:
            return (
                ProgrammeCourseSemesterobj.course.name
                + " ("
                + ProgrammeCourseSemesterobj.course.code
                + ")"
            )

    def get_total_no_of_answersheet(self, obj):
        BundleCampobj = BundleCamp.objects.filter(
            id=obj.bundle_camp.id
        ).first()
        bundleid = BundleCampobj.bundle.id
        total = BundleCandidateMapper.objects.filter(
            bundle_id=bundleid, status_id=ACTIVE_STATE
        ).count()
        return total

    def get_evaluvationtype(self, obj):
        try:
            return obj.evaluation_type.name
        except:
            return "NA"
        
    def get_evaluated_no_of_answersheet(self, obj):
        BundleCampobj = BundleCamp.objects.filter(
            id=obj.bundle_camp.id
        ).first()
        bundleid = BundleCampobj.bundle.id
        print("bundleidbundleidbundleidbundleidbundleid",bundleid)
        bundle_candidate_dfm=BundleCandidateMapper.objects.filter(bundle_id=bundleid).values_list('digital_false_no_id',flat=True)
        print("bundle_candidate_dfmbundle_candidate_dfmbundle_candidate_dfmbundle_candidate_dfm",bundle_candidate_dfm)
        # bundleExaminer = 
        evaluated = ExaminerFalseNumber.objects.filter(
           digital_false_no__in=bundle_candidate_dfm, status_id=EVALUATED,bundle_examiner_id=obj.id).count()
        print("evaluatedevaluatedevaluatedevaluatedevaluated",evaluated)
        # total = BundleCandidateMapper.objects.filter(
        #     bundle_id=bundleid, status_id=ACTIVE_STATE
        # ).count()
        return evaluated

class OnScreenBundleDetailsSerializer(serializers.ModelSerializer):
    """
    Safe replacement for BundleDetailsSerializer for OE bundles.
    Fetches exam info from DB relationships, NOT from slip_data JSON
    (OE bundles have empty/invalid slip_data so json.loads fails).
    """
    exam               = serializers.SerializerMethodField()
    examCode           = serializers.SerializerMethodField()
    course             = serializers.SerializerMethodField()
    courseCode         = serializers.SerializerMethodField()
    dateOfExam         = serializers.SerializerMethodField()
    qpCode             = serializers.SerializerMethodField()
    examiner           = serializers.SerializerMethodField()
    username           = serializers.SerializerMethodField()
    emailId            = serializers.SerializerMethodField()
    mobileNum          = serializers.SerializerMethodField()
    bundleDistributionType = serializers.SerializerMethodField()
    dateOfDistribution = serializers.SerializerMethodField()
    totalNoOfAnswersheet = serializers.SerializerMethodField()
    noEvaluvated       = serializers.SerializerMethodField()
    noOfAsReturn       = serializers.SerializerMethodField()
    status             = serializers.SerializerMethodField()

    class Meta:
        model = BundleExaminer
        fields = [
            'exam', 'examCode', 'course', 'courseCode', 'dateOfExam',
            'qpCode', 'examiner', 'username', 'emailId', 'mobileNum',
            'bundleDistributionType', 'dateOfDistribution',
            'totalNoOfAnswersheet', 'noEvaluvated', 'noOfAsReturn', 'status',
        ]

    def _get_exam_schedule(self, obj):
        """Helper — fetch ExaminationSchedule once, reused by multiple fields."""
        try:
            pcs = obj.bundle_camp.bundle.programme_course_semester
            return ExaminationSchedule.objects.filter(
                programme_semester_course=pcs,
                status_id=ACTIVE_STATE,
            ).first()
        except Exception:
            return None

    def get_exam(self, obj):
        try:
            sch = self._get_exam_schedule(obj)
            return sch.exam.title if sch else "NA"
        except Exception:
            return "NA"

    def get_examCode(self, obj):
        try:
            sch = self._get_exam_schedule(obj)
            return sch.exam.code if sch else "NA"
        except Exception:
            return "NA"

    def get_course(self, obj):
        try:
            pcs = obj.bundle_camp.bundle.programme_course_semester
            if pcs.sub_course:
                return (
                    pcs.course.name
                    + " (" + pcs.sub_course.name + ")"
                    + " (" + pcs.course.code + ")"
                )
            return pcs.course.name + " (" + pcs.course.code + ")"
        except Exception:
            return "NA"

    def get_courseCode(self, obj):
        try:
            return obj.bundle_camp.bundle.programme_course_semester.course.code
        except Exception:
            return "NA"

    def get_dateOfExam(self, obj):
        try:
            sch = self._get_exam_schedule(obj)
            return sch.start_date.strftime("%d-%m-%Y") if sch else "NA"
        except Exception:
            return "NA"

    def get_qpCode(self, obj):
        try:
            return obj.bundle_camp.bundle.qp_code
        except Exception:
            return "NA"

    def get_examiner(self, obj):
        try:
            return obj.camp_rol_allo.camp_user.get_full_name()
        except Exception:
            return "NA"

    def get_username(self, obj):
        try:
            return obj.camp_rol_allo.camp_user.username
        except Exception:
            return "NA"

    def get_emailId(self, obj):
        try:
            return obj.camp_rol_allo.camp_user.email
        except Exception:
            return "NA"

    def get_mobileNum(self, obj):
        try:
            profile = UserProfiles.objects.filter(
                user=obj.camp_rol_allo.camp_user
            ).first()
            return profile.mobile_number if profile else "NA"
        except Exception:
            return "NA"

    def get_bundleDistributionType(self, obj):
        try:
            return obj.bundle_distribution_type.name
        except Exception:
            return "NA"

    def get_dateOfDistribution(self, obj):
        try:
            return obj.created_on.strftime("%d-%m-%Y")
        except Exception:
            return "NA"

    def get_totalNoOfAnswersheet(self, obj):
        try:
            return BundleCandidateMapper.objects.filter(
                bundle=obj.bundle_camp.bundle,
                status_id=ACTIVE_STATE,
            ).count()
        except Exception:
            return 0

    def get_noEvaluvated(self, obj):
        try:
            dfm_ids = BundleCandidateMapper.objects.filter(
                bundle=obj.bundle_camp.bundle
            ).values_list('digital_false_no_id', flat=True)

            return ExaminerFalseNumber.objects.filter(
                digital_false_no_id__in=dfm_ids,
                status_id=EVALUATED,
                bundle_examiner=obj,
            ).count()
        except Exception:
            return 0

    def get_noOfAsReturn(self, obj):
        try:
            ret = BundleReturnStatement.objects.filter(
                bundle_examiner=obj
            ).first()
            return ret.no_of_as_return if ret else "NA"
        except Exception:
            return "NA"

    def get_status(self, obj):
        try:
            return obj.status.label
        except Exception:
            return "NA"