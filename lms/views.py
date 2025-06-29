import stripe
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.management.commands.stripe_service import (
    create_checkout_session,
    create_price,
    create_product,
)
from users.permissions import IsModeratorReadOnly
from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PriceSerializer,
    ProductSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsModeratorReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.all()
        if user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsModeratorReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.all()
        if user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=user)


class CourseSubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


@method_decorator(csrf_exempt, name="dispatch")
class CreatePaymentView(View):
    def post(self, request):
        name = request.POST.get("name")
        amount = float(request.POST.get("amount"))
        try:
            product_id = create_product(name)
            price_id = create_price(product_id, amount)
            checkout_url = create_checkout_session(price_id)
            return redirect(checkout_url)
        except Exception as e:
            return render(request, "lms/index.html", {"error": str(e)})

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        stripe_product_id = create_product(payment)
        price_id = create_price(payment, stripe_product_id)
        session_id, payment_link = create_checkout_session(price_id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class CreateProductView(APIView):
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                "Product Created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"product_id": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            )
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = create_product(serializer.validated_data["name"])
            return Response({"product_id": product_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePriceView(APIView):
    @swagger_auto_schema(
        request_body=PriceSerializer,
        responses={
            201: openapi.Response(
                "Price Created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"price_id": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            )
        },
    )
    def post(self, request):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            price_id = create_price(
                serializer.validated_data["product_id"],
                serializer.validated_data["amount"],
                serializer.validated_data["currency"],
            )
            return Response({"price_id": price_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSessionView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["price_id", "success_url", "cancel_url"],
            properties={
                "price_id": openapi.Schema(type=openapi.TYPE_STRING),
                "success_url": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                ),
                "cancel_url": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                ),
            },
            example={
                "price_id": "price123",
                "success_url": "https://site.com/success",
                "cancel_url": "https://site.com/cancel",
            },
        ),
        responses={
            201: openapi.Response(
                "Session Created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "session_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "url": openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                        ),
                    },
                ),
            )
        },
    )
    def post(self, request):
        price_id = request.data.get("price_id")
        success_url = request.data.get("success_url")
        cancel_url = request.data.get("cancel_url")
        if price_id and success_url and cancel_url:
            session_id, session_url = create_checkout_session(
                price_id, success_url, cancel_url
            )
            return Response(
                {"session_id": session_id, "url": session_url},
                status=status.HTTP_201_CREATED,
            )
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class StripeSessionStatusView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "session_id",
                openapi.IN_PATH,
                description="Stripe Session ID",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                "Session Info",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING),
                        "payment_status": openapi.Schema(type=openapi.TYPE_STRING),
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "amount_total": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "currency": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            404: "Session not found or ID incorrect.",
        },
    )
    def get(self, session_id):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return Response(
                {
                    "id": session.id,
                    "payment_status": session.payment_status,
                    "status": session.status,
                    "amount_total": session.amount_total,
                    "currency": session.currency,
                }
            )
        except stripe.error.InvalidRequestError:
            return Response(
                {"error": "Session not found or ID incorrect."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
