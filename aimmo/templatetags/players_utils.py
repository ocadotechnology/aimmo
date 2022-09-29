from aimmo.models import Game
from django import template
from common.models import School, Class, Teacher

from common.permissions import logged_in_as_student, logged_in_as_teacher

register = template.Library()


def get_user_playable_games(context, base_url):
    # Only called by teacher to create games table
    user = context.request.user
    teacher = None if not user else user.userprofile.teacher
    if logged_in_as_teacher(user):
        school_id = teacher.school_id
        school = School.objects.get(id=school_id)
        current_school_teachers = Teacher.objects.filter(school=school)
        playable_games = (
            Game.objects.filter(game_class__teacher__in=current_school_teachers, is_archived=False)
            if teacher.is_admin
            else Game.objects.filter(game_class__teacher=teacher, is_archived=False)
        )
        # playable_games = Game.objects.filter(game_class__teacher=user.userprofile.teacher, is_archived=False)
    else:
        pass
        playable_games = Game.objects.none()
    return {
        "user": user,
        "base_url": base_url,
        "open_play_games": playable_games if user.is_authenticated else None,
    }
