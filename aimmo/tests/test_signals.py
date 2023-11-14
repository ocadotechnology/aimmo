from common.models import UserProfile
from django.contrib.auth.models import User
from django.test import TestCase

from ..models import WorksheetBadge


class TestSignals(TestCase):
    def test_pre_save___user_profile__create_worksheet_badge(self):
        user = User.objects.create_user(
            "JDoe",
            "john.doe@codeforlife.com",
            "password",
        )

        user_profile = UserProfile.objects.create(user=user)
        assert not WorksheetBadge.objects.exists()

        def assert_worksheet_badges():
            worksheet_badges = [
                WorksheetBadge(
                    user=user,
                    worksheet_id=1,
                    badge_id=1,
                ),
                WorksheetBadge(
                    user=user,
                    worksheet_id=1,
                    badge_id=2,
                ),
            ]
            assert len(worksheet_badges) == WorksheetBadge.objects.count()
            for worksheet_badge, expected_worksheet_badge in zip(WorksheetBadge.objects.all(), worksheet_badges):
                assert (
                    worksheet_badge.user == expected_worksheet_badge.user
                    and worksheet_badge.worksheet_id == expected_worksheet_badge.worksheet_id
                    and worksheet_badge.badge_id == expected_worksheet_badge.badge_id
                )

        user_profile.aimmo_badges = "1:1,1:2"
        user_profile.save()
        assert_worksheet_badges()

        user_profile.save()
        assert_worksheet_badges()
