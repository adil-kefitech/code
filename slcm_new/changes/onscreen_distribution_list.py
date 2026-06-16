import datetime
import json
import logging
logger = logging.getLogger(__name__)

import traceback
from datetime import date, datetime
from re import template

import cryptography
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Q
from django.http import Http404, HttpResponse  # witten httpresponse
from django.shortcuts import get_object_or_404  # 404 if object is not exists
from django.shortcuts import redirect, render
from django.utils import timezone
from iteration_utilities import unique_everseen  # for remove dict
from rest_framework import status  # basically sent back status
from rest_framework import generics, permissions
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import (
    Response,
)  # get a perticular response every thing is okey then give 200 response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView  # normal view can written API data
from river.utils.exceptions import RiverException
from simple_history.utils import (
    bulk_create_with_history,
    bulk_update_with_history,
)

from util.constants import *
from util.models import *
from util.pagination import *
from util.serializers import *
from datetime import datetime as dt


from .serializers import *

from camp_mgmt.serializers import *
from rest_framework.permissions import IsAuthenticated



class AnswerSheetDistributionList(APIView):
    def get(self, request):
        try:
           
            user = request.user.id
            CampRoleListReqDate=dt.now()
            CampRoleAllocationobj = CampRoleAllocation.objects.filter(
                camp_user_id=user,
                 camp_schedule__start_date__lte=CampRoleListReqDate,
                 camp_schedule__end_date__gte=CampRoleListReqDate,
                camp_group__group__name__in=[CAMP_OFFICER],
                status_id=ACTIVE_STATE,
            ).all()
            campschl = [i.camp_schedule.id for i in CampRoleAllocationobj]
            print("____________________________________________________________________________")
            print(campschl)
            
            CampScheduleobj = CampSchedule.objects.filter(id__in=campschl,status_id=ACTIVE_STATE).all()

            sub_camp_list=[i.sub_camp.id for i in CampScheduleobj]

            print("_______________________________sub_camp_list_____________________________________________")
            print(sub_camp_list)

            BundleCampobj = BundleCamp.objects.filter(
                sub_camp_id__in=sub_camp_list,
               bundle__comments__icontains= "OEBundle created",
                ).all()
            
            print("____________________________________________________________________________")

            print(BundleCampobj)
           
            BundleExaminerobj = BundleExaminer.objects.filter(
                bundle_camp__in=BundleCampobj,
                status_id__in=[EVALUATED, ALLOCATED, RECEIVED],
            ).order_by("-created_on").all()


            bundlelist = []
            for i in BundleCampobj:
                bundlelist.append(i.bundle.id)
            BundleMasterobj = BundleMaster.objects.filter(
                id__in=bundlelist,
                comments__icontains="oebundle created",
            ).all()
            qpcode_list_serializer = QpcodeListSerializer(
                BundleMasterobj, many=True
            )
            templist = list(unique_everseen(qpcode_list_serializer.data))
            answersheet_distrbtn_list_serializer = (
                AnswerSheetDistributionFilterView(BundleExaminerobj, many=True)
            )
            return format_response(
                True,
                "success",
                data={
                    # "answersheet_distribution_list": answersheet_distrbtn_list_serializer.data,
                    "qp_code_list": templist,
                },
                status_code=status.HTTP_201_CREATED,
                template_name="onscreen_distribution_list.html",
            )
        except Exception as e:
            return format_response(
                False,
                BAD_GATEWAY,
                {},
                BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    # def post(self,request):
    #     try:
           
    #         qpcode = request.data["qpcode"]
           
    #         campallobj=CampRoleAllocation.objects.filter(

    #         camp_user=request.user,
    #         camp_group__group__name__in=[CAMP_OFFICER],
    #         status_id=ACTIVE_STATE,

    #         camp_schedule__sub_camp__bundlecamp__bundle__qp_code=qpcode).all()
          

    #         campp=[]

            

    #         for camp in campallobj:

    #             camp_id=camp.camp_schedule.id
                

    #             camp=camp.camp_schedule.camp_display_name  

    #             campp.append({"camp_id":camp_id,"camp":camp})

    #         camp=unique_everseen(campp)
          
    #         return format_response(
    #             True,
    #             "success",
    #             data={
    #                  "camp": camp,
    #             },
                
    #             status_code=status.HTTP_201_CREATED,
    #             template_name="onscreen_distribution_list.html",
    #         )
            
    #     except Exception as e:
    #         return format_response(
    #             False,
    #             BAD_GATEWAY,
    #             {},
    #             BAD_GATEWAY_ERROR_CODE,
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             template_name="500.html",
    #         )






class OnscreenDistributionFilterList(APIView):
    def post(self, request):
        try:
            user = request.user.id
           
            srch = request.data.get("search",[])
           
            # dates = request.data.get("dates",[])
            # camp = request.data.get("camp",[])
         
            print("hgfjhgfjhgf...............",srch)
           
            queryset = BundleExaminer.objects.filter(

                bundle_camp__sub_camp__campschedule__camproleallocation__camp_user=user,
                bundle_camp__sub_camp__campschedule__camproleallocation__camp_group__group__name=CAMP_OFFICER,
               
                status_id__in=[EVALUATED, ALLOCATED, RECEIVED],
            ).order_by("-created_on")
            print(queryset.count())
           
            # for d in dates:

            #     query = d
               
            #     if query != None:
            #         queryset = queryset.filter(
            #             Q(created_on__date=query)
            #         ).distinct()
                   
            for n in srch:

                query = n
               
                if query != None:
                    queryset = queryset.filter(
                        Q(bundle_camp__bundle__qp_code=query)
                    ).distinct()
            # for c in camp:


                # sub_camp_list= CampSchedule.objects.filter(id=camp).all()
            
                # sub_camp_list=[i.sub_camp.id for i in sub_camp_list]
          
            
                # BundleCampobj = BundleCamp.objects.filter(
                #     sub_camp_id__in=sub_camp_list).all()
                
                # bundlecamp_id =[i.id for i in BundleCampobj]
                # query = c
                # print(queryset.first().bundle_camp.camp_id)
                # if query != None:
                #     queryset = queryset.filter(
                #         Q(bundle_camp__sub_camp__campschedule__id=query)
                #     ).distinct()



            print("Chumma.........................")
            onscreen_distrbtn_list_serializer = (
                OnscreenDistributionFilterView(queryset, many=True)
            )
            
            print("serial data...................:",onscreen_distrbtn_list_serializer.data)
          
            
            return format_response(
                True,
                "success",
                data={
                    "answersheet_distribution_list": onscreen_distrbtn_list_serializer.data
                },
                status_code=status.HTTP_201_CREATED,
                template_name="answersheet_dist/answer_sheet_distribution_list.html",
            )
        except Exception as e:
            logger.error(e,exc_info=True)
            return format_response(
                False,
                BAD_GATEWAY,
                {},
                BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_400_BAD_REQUEST,
                template_name="500.html",
            )


class OnScreenDistributionBundleView(APIView):
    permission_classes = [IsAuthenticated]
    """
    GET → returns full bundle details for the View modal on the
          On-Screen Distribution List page.
    Called by: view_button click (AJAX GET with ?bundle_id=<id>)
    """
    def get(self, request):
        try:
            bundle_examiner_id = request.GET.get("bundle_id")

            # Revaluation bundles may use RevaluationExaminerFalseNumber id
            try:
                rev_obj = RevaluationExaminerFalseNumber.objects.get(
                    id=bundle_examiner_id
                )
                bundle_examiner = BundleExaminer.objects.filter(
                    id=rev_obj.bundle_examiner.id
                ).first()
            except RevaluationExaminerFalseNumber.DoesNotExist:
                bundle_examiner = BundleExaminer.objects.filter(
                    id=bundle_examiner_id
                ).first()

            if not bundle_examiner:
                return format_response(
                    False,
                    "Bundle examiner not found",
                    {},
                    BAD_GATEWAY_ERROR_CODE,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            serializer = OnScreenBundleDetailsSerializer(bundle_examiner)

            return format_response(
                True,
                "success",
                data={
                    "answersheetDistributionBundleView": serializer.data
                },
                status_code=status.HTTP_200_OK,
                template_name="onscreen_distribution_list.html",
            )

        except Exception as e:
            logger.error(e, exc_info=True)
            return format_response(
                False,
                BAD_GATEWAY,
                {},
                BAD_GATEWAY_ERROR_CODE,
                status_code=status.HTTP_400_BAD_REQUEST,
            )