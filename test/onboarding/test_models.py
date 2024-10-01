from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from onboarding.models import OnBoarding
from users.models import User, Applicant
from job_application.models import JobApplication
from job_posting.models import JobPosting
from django.utils import timezone

class OnBoardingModelTest(TestCase):
    # Prepare
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.applicant = Applicant.objects.create(user=self.user)
        self.job_posting = JobPosting.objects.create(job_name="job123", description="description for job123")
        self.job_application = JobApplication.objects.create(
            applicant_id=self.applicant.applicant_id,
            job_id=self.job_posting.id
        )

    # Test for model creation
    def test_onboarding_creation(self):
        # Prepare
        onboarding = OnBoarding.objects.create(
            job_application_id=self.job_application,
            pic_user_id=self.user,
            ktp="1234567890123456",
            bank="Test Bank",
            bpjs="1234567890",
            foto_diri="url/to/photo",
            npwp="0987654321",
            datetime_start=timezone.now(),
            datetime_end=timezone.now(),
            confirm="Yes",
        )

        # Assert
        self.assertEqual(onboarding.ktp, "1234567890123456")
        self.assertEqual(onboarding.bank, "Test Bank")
        self.assertEqual(onboarding.bpjs, "1234567890")
        self.assertEqual(onboarding.npwp, "0987654321")
        self.assertEqual(onboarding.confirm, "Yes")

        self.assertEqual(OnBoarding.objects.count(), 1)

    # Test for default value for confirm attribute
    def test_default_confirm_value(self):
        # Prepare
        onboarding = OnBoarding.objects.create(
            job_application_id=self.job_application,
            pic_user_id=self.user,
        )

        # Assert
        self.assertEqual(onboarding.confirm, "Not Confirm")

    # Test for relationship with different models
    def test_relationships(self):
        # Prepare
        onboarding = OnBoarding.objects.create(
            job_application_id=self.job_application,
            pic_user_id=self.user,
            ktp="1234567890123456",
            bank="Test Bank",
            bpjs="1234567890",
            foto_diri="url/to/photo",
            npwp="0987654321",
            datetime_start=timezone.now(),
            datetime_end=timezone.now(),
            confirm="Yes",
        )

        # Assert
        self.assertEqual(onboarding.job_application_id, self.job_application)
        self.assertEqual(onboarding.pic_user_id, self.user)

    # Test for one to one relationship with job application
    def test_one_to_one_relationship(self):
        # Prepare
        onboarding1 = OnBoarding.objects.create(
            job_application_id=self.job_application,
            pic_user_id=self.user,
            datetime_start=timezone.now() - timezone.timedelta(days=1)
        )

        # Assert
        with self.assertRaises(IntegrityError):
            onboarding2 = OnBoarding.objects.create(
                job_application_id=self.job_application,
                pic_user_id=self.user,
                datetime_start=timezone.now()
            )

    # Test for invalid confirm choice
    def test_confirm_choices(self):
        # Prepare
        onboarding = OnBoarding.objects.create(
            job_application_id=self.job_application,
            pic_user_id=self.user,
            confirm="InvalidChoice"
        )

        # Assert
        with self.assertRaises(ValidationError):
            onboarding.full_clean() # Trigger model field validation

    # Test for onboarding data ordering (based on datetime created)
    def test_list_ordering(self):
        # Prepare
        user1 = User.objects.create(username="testuser2")
        applicant1 = Applicant.objects.create(user=user1)
        job_application1 = JobApplication.objects.create(
            applicant_id=applicant1.applicant_id,
            job_id=self.job_posting.id
        )

        user2 = User.objects.create(username="testuser3")
        applicant2 = Applicant.objects.create(user=user2)
        job_application2 = JobApplication.objects.create(
            applicant_id=applicant2.applicant_id,
            job_id=self.job_posting.id
        )

        onboarding1 = OnBoarding.objects.create(
            job_application_id=self.job_application,
            pic_user_id=self.user,
            datetime_start=timezone.now() - timezone.timedelta(days=1)
        )
        onboarding2 = OnBoarding.objects.create(
            job_application_id=job_application1,
            pic_user_id=self.user,
            datetime_start=timezone.now()
        )
        onboarding3 = OnBoarding.objects.create(
            job_application_id=job_application2,
            pic_user_id=self.user,
            datetime_start=timezone.now()
        )

        onboardings = OnBoarding.objects.all()

        # Assert
        self.assertEqual(onboardings[0], onboarding1)
        self.assertEqual(onboardings[1], onboarding2)
        self.assertEqual(onboardings[2], onboarding3)