from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from online_evaluation import (
    answersheet_allocate,
    answersheet_distribution,
    answersheet_list,
    answersheet_upload,
    as_upload_report,
    automatic_mapping,
    markentry,
    qp_upload_report,
    selections,
    smpmark,
    upload_online_qp,
    onscreen_distribution_list,
)

urlpatterns = [
    path(
        "oe-ans-upload",
        answersheet_upload.AnswersheetUpload.as_view(),
        name="oe-ans-upload",
    ),
    path(
        "file_upload",
        answersheet_upload.FileUploadList.as_view(),
        name="file_upload",
    ),
    path(
        "answersheet-list",
        answersheet_list.AnswersheetList.as_view(),
        name="answersheet-list",
    ),
    path(
        "manual_mapping",
        answersheet_list.ManualMapping.as_view(),
        name="manual_mapping",
    ),
    path(
        "encrypted", answersheet_list.ManualMapping.as_view(), name="encrypted"
    ),
    path(
        "delete_ans",
        answersheet_list.DeleteAnswersheet.as_view(),
        name="delete_ans",
    ),
    path(
        "answersheet-distribution",
        answersheet_distribution.AnswersheetDistribution.as_view(),
        name="answersheet-distribution",
    ),
    path(
        "fetch-online-qp",
        upload_online_qp.FetchQpDetails.as_view(),
        name="fetch-online-qp",
    ),
    path(
        "upload-online-qp",
        upload_online_qp.UploadQpDetails.as_view(),
        name="upload-online-qp",
    ),
    # ******************************
    path(
        "examdet",
        answersheet_distribution.ExamDetails.as_view(),
        name="examdet",
    ),
    path(
        "examiners-list",
        answersheet_distribution.ExaminersList.as_view(),
        name="examiners-list",
    ),
    path(
        "courselist",
        answersheet_distribution.CourseList.as_view(),
        name="courselist",
    ),
    path("pgmlist", selections.PgmList.as_view(), name="pgmlist"),
    path("semlist", selections.SemList.as_view(), name="semlist"),
    path("schemelist", selections.SchemeList.as_view(), name="schemelist"),
    path(
        "examclist", selections.PgmWiseExamcodeList.as_view(), name="examclist"
    ),
    path(
        "ecollegelist",
        selections.EcodewiseCollegeList.as_view(),
        name="ecollegelist",
    ),
    path(
        "ebundlelist",
        selections.CollegewiseBundlesList.as_view(),
        name="ebundlelist",
    ),
    # path('oexamlist',selections.PgmWiseExamcodeList.as_view(),name='oexamlist'),
    path(
        "odistrictlist",
        selections.DistrictList.as_view(),
        name="odistrictlist",
    ),
    path(
        "ocollegelist",
        selections.DisPgmWiseCollege.as_view(),
        name="ocollegelist",
    ),
    path("qpclist", selections.QpcodeList.as_view(), name="qpclist"),
    path(
        "verify_answersheet",
        answersheet_list.VerifyAnswerSheetList.as_view(),
        name="verify_answersheet",
    ),
    path(
        "allocate-ans",
        answersheet_allocate.ExaminerProgram.as_view(),
        name="allocate-ans",
    ),
    path(
        "camp-list",
        answersheet_allocate.ExaminerCamp.as_view(),
        name="camp-list",
    ),
    path(
        "allo-course",
        answersheet_allocate.ExaminerCourse.as_view(),
        name="allo-course",
    ),
    path(
        "alloqp", answersheet_allocate.Examinerqpcode.as_view(), name="alloqp"
    ),
    path(
        "subans",
        answersheet_allocate.Submitanswersheet.as_view(),
        name="subans",
    ),
    path("marksmp", smpmark.Smpbutton.as_view(), name="marksmp"),
    path(
        "mark-entry-view",
        markentry.Examinerqpcode.as_view(),
        name="mark-entry-view",
    ),
    path("onscreen-mark-upload", markentry.Markupload.as_view(), name="onscreen-mark-upload"),
    path("project-onscreen-mark-upload", markentry.ProjectMarkupload.as_view(), name="project-onscreen-mark-upload"),
    path("mark-update", markentry.Markupdate.as_view(), name="mark-update"),
    path("fetch-file", markentry.ServeFile.as_view(), name="fetch-file"),
    path("smpl", markentry.Smpl.as_view(), name="smpl"),
    path(
        "automatic-mapping",
        automatic_mapping.AutomaticMapping.as_view(),
        name="automatic-mapping",
    ),
    path(
        "bundle-return",
        answersheet_allocate.BundleReturn.as_view(),
        name="bundle-return",
    ),
    path(
        "answersheet-distribution-second",
        answersheet_distribution.AnswersheetDistributionSecond.as_view(),
        name="answersheet-distribution-second",
    ),
    path(
        "answersheet-distribution-third",
        answersheet_distribution.AnswersheetDistributionThird.as_view(),
        name="answersheet-distribution-third",
    ),
    path(
        "as-upload-report",
        as_upload_report.ASUpploadQPList.as_view(),
        name="as-upload-report",
    ),
    path(
        "as-upload-report-list",
        as_upload_report.ASReportList.as_view(),
        name="as-upload-report-list",
    ),
    path(
        "qp-upload-report",
        qp_upload_report.QPUploadReport.as_view(),
        name="qp-upload-report",
    ),

    path(
        "onscreen_distribution_list/",
        onscreen_distribution_list.AnswerSheetDistributionList.as_view(),
        name="onscreen_distribution_list",
    ),


    path(
        "onscreen_distribution_filterlist/",
        onscreen_distribution_list.OnscreenDistributionFilterList.as_view(),
        name="onscreen_distribution_filterlist",
    ),

    path(
    "onscreen-distribution-bundle-view/",
    onscreen_distribution_list.OnScreenDistributionBundleView.as_view(),
    name="onscreen-distbn-bundle-view",
    ),
    


    ####================================================ ON SCREEN REVALUATION ===================================================#####
    path("on-screen-revaluation-examiner-valuation",answersheet_allocate.RevaluationExaminerProgram.as_view(),name="on-screen-revaluation-examiner-valuation"),
    path("on-screen-revaluation-examiner-answer-sheet",answersheet_allocate.RevaluationAnswersheetSubmit.as_view(),name="on-screen-revaluation-examiner-answer-sheet"),
    path("on-screen-revaluation-examiner-mark-update",markentry.OnscreenRevaluationMarkUpdate.as_view(),name="on-screen-revaluation-examiner-mark-update"),
    path("on-screen-revaluation-examiner-mark-upload",markentry.OnscreenRevaluationMarkUpload.as_view(),name="on-screen-revaluation-examiner-mark-upload"),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
