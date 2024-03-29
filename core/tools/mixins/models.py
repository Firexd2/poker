from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Manager


class NamedObjMixin(models.Model):
    name = models.TextField("Name", blank=True, null=True)

    class Meta:
        abstract = True


class OnOffMixin(models.Model):
    is_enabled = models.BooleanField("Enabled", default=True, blank=True)

    class Meta:
        abstract = True


class PriorityMixin(models.Model):
    """Миксин, который позволяет в ручную задавать приоритет объектов

    Для объектов, которые могут создаваться и у которых в save_related ModelAdmin идёт добавление связанных объектов,
    потребуется повторный вызов save() для просчета priority
    """
    priority = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)

    # если True, присвоит новому объекту приоритет
    auto_priority_for_new_obj = True

    class Meta:
        abstract = True

    def get_objects_in_view(self):
        """Просчет приоритета объекта следует делать из его "поля видимости". Получаем это поле видимости,
        по факту из qs (чтобы вызвать count(), get() и т.п.)
        Если не переопределить, то будет считать по всем объектам
        """
        return self.__class__.objects

    def save(self, auto_priority=True, *args, **kwargs):
        need_auto_priority = bool(self.id) or self.auto_priority_for_new_obj

        if need_auto_priority and auto_priority:
            objects = self.get_objects_in_view()
            count_objects = objects.count()

            if not self.priority or self.priority > count_objects:
                if self.id:
                    self.priority = count_objects
                else:
                    self.priority = count_objects + 1
            else:
                # вытаскиваем старый приоритет нашего объекта
                old_priority = objects.get(id=self.id).priority
                # присваиваем старый приоритет объекту, который занимает нужный приоритет
                try:
                    old_object = objects.get(priority=self.priority)
                    old_object.priority = old_priority
                    old_object.save(auto_priority=False)
                except self.__class__.DoesNotExist:
                    pass

        super(PriorityMixin, self).save(*args, **kwargs)

    def delete(self, *args):
        """При удалении объекта необходимо всем просчитать priority
        """
        for enum, obj in enumerate(self.get_objects_in_view().exclude(id=self.id), start=1):
            obj.priority = enum
            obj.save(auto_priority=False)
        super(PriorityMixin, self).delete(*args)


class DistinctManager(Manager):
    """Manager, удаляющий дубли
    """
    def get_queryset(self):
        return super(DistinctManager, self).get_queryset().distinct()
