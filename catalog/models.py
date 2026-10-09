from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("Адрес", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})


class Service(models.Model):
    class Format(models.TextChoices):
        ONLINE = "online", "Онлайн-встреча"
        FILE = "file", "Файл-результат"
        ACCESS = "access", "Доступ к сервису"

    # PROTECT: a category that still has services cannot be deleted
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="services",
        verbose_name="Категория",
    )
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Адрес", max_length=200, unique=True)
    short_description = models.CharField("Кратко", max_length=300, blank=True)
    description = models.TextField("Описание", blank=True)
    # Money: always DecimalField, never FloatField
    price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=2)
    duration_days = models.PositiveSmallIntegerField("Срок, дней", default=3)
    delivery_format = models.CharField(
        "Формат выдачи", max_length=10, choices=Format.choices, default=Format.FILE
    )
    cover = models.ImageField("Обложка", upload_to="services/%Y/%m/", blank=True)
    is_active = models.BooleanField("Опубликована", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "price"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.price} ₽)"

    def get_absolute_url(self):
        return reverse("catalog:service_detail", kwargs={"slug": self.slug})