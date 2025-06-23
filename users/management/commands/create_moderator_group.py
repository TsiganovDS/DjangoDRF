from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт группу модераторов с нужными правами"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Модераторы")
        perms = [
            "view_lesson",
            "change_lesson",
            "view_course",
            "change_course",
        ]
        for perm_codename in perms:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Permission {perm_codename} не найдено!")
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"Группа 'Модераторы' "
                f"{'создана' if created else 'уже существует'} и права добавлены!"
            )
        )
