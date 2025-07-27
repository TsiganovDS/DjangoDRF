from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CourseSubscribeAPIView,
    CourseViewSet,
    CreateCheckoutSessionView,
    CreatePaymentView,
    CreatePriceView,
    CreateProductView,
    LessonViewSet,
    StripeSessionStatusView,
    UpdateCourseView,
    HomePageView,
)

app_name = "lms"


router = SimpleRouter()
router.register("courses", CourseViewSet)
router.register("lessons", LessonViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "courses/subscribe/", CourseSubscribeAPIView.as_view(), name="course-subscribe"
    ),
    path("create-payment/", CreatePaymentView.as_view(), name="create-payment"),
    path("create-product/", CreateProductView.as_view(), name="create-product"),
    path("create-price/", CreatePriceView.as_view(), name="create-price"),
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "stripe/session-status/<str:session_id>/",
        StripeSessionStatusView.as_view(),
        name="stripe-session-status",
    ),
    path(
        "course/update/<int:course_id>/",
        UpdateCourseView.as_view(),
        name="update_course",
    ),
    path("", HomePageView.as_view(), name="index"),
]
