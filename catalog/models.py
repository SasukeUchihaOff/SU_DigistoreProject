from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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

class Review(models.Model):
    # CASCADE: reviews make no sense without their service
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Услуга",
    )
    # SET_NULL: the review stays when the user is deleted (needs null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews",
        verbose_name="Автор",
    )
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField("Текст", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        ordering = ["-created_at"]
        constraints = [
            # One review per author for each service
            models.UniqueConstraint(fields=["service", "author"], name="uniq_review"),
        ]

    def __str__(self):
        return f"{self.service} - {self.rating}/5"
    
class ServicePlan(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name="Услуга",
    )
    name = models.CharField("Название тарифа", max_length=100)  # Basic / Standard / Premium
    price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=2)
    duration_days = models.PositiveSmallIntegerField("Срок, дней", default=3)
    # List of included options, e.g. ["3 правки", "Исходники"]
    options = models.JSONField("Опции", default=list, blank=True)
    is_recommended = models.BooleanField("Рекомендуемый", default=False)

    class Meta:
        verbose_name = "тариф"
        verbose_name_plural = "тарифы"
        ordering = ["price"]
        constraints = [
            models.UniqueConstraint(fields=["service", "name"], name="uniq_plan_name"),
        ]

    def __str__(self):
        return f"{self.service.title} - {self.name}"