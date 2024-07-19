from django.db import models
from user.models import User
from quote.models import Quote
from tags.models import Tag
from django.urls import reverse
from language.models import Language


class News(models.Model):
    class CATEGORYS:
        NEWS = 'News'
        POLICY = 'Policy'
        SOCIETY = 'Society'
        ADVERTISING = 'Advertising'
        BY_EAR = 'By hearing'

        CATEGORY_CHOICES = (
            (NEWS, 'Новости'),
            (POLICY, 'Политика'),
            (SOCIETY, 'Общество'),
            (ADVERTISING, 'Реклама'),
            (BY_EAR, 'На слуху'),
        )

    class SUBCATEGORYS:
        KAZAKHSTAN_NEWS = 'Kazakhstan News'
        MANGYSTAU_NEWS = 'Mangystau News'
        WORLD_NEWS = 'World News'
        PRESIDENT = 'President'
        MEETINGS = 'Meetings'
        ECONOMY = 'Economy'
        SPORT = 'Sport'
        ECOLOGY = 'Ecology'
        MEDICINE = 'Medicine'
        EDUCATION = 'Education'
        CULTURE = 'Culture'
        TRUTH = 'True'
        YOUTH = 'Youth'

        SUBCATEGORY_CHOICES = (
            (KAZAKHSTAN_NEWS, 'Новости Казахстана'),
            (MANGYSTAU_NEWS, 'Новости Мангистау'),
            (WORLD_NEWS, 'Мировые новости'),
            (PRESIDENT, 'Президент'),
            (MEETINGS, 'Встречи'),
            (ECONOMY, 'Экономика'),
            (SPORT, 'Спорт'),
            (ECOLOGY, 'Экология'),
            (MEDICINE, 'Медицина'),
            (EDUCATION, 'Образование'),
            (CULTURE, 'Культура'),
            (TRUTH, 'Правда'),
            (YOUTH, 'Молодежь'),
        )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, through='NewsTag', related_name='news_tags')
    category = models.CharField(max_length=20, choices=CATEGORYS.CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORYS.SUBCATEGORY_CHOICES, blank=True, null=True)
    exclusive = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Новость {self.id}"

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    class Meta:
        ordering = ["id"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class NewsTranslation(models.Model):
    news = models.ForeignKey(News, related_name='translations', on_delete=models.CASCADE)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        unique_together = ('news', 'lang')
        ordering = ["id"]
        verbose_name = "Перевод новости"
        verbose_name_plural = "Переводы новостей"

    def __str__(self):
        return f"{self.title} ({self.lang})"


class NewsTag(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'tag')
        ordering = ["id"]
        verbose_name = "Тег новости"
        verbose_name_plural = "Теги новостей"

    def __str__(self):
        return f"Новость {self.news.id} - Тег {self.tag.tag_name}"


class Comment(models.Model):
    comment = models.TextField()
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коммента́рий {self.id} на новость {self.news.id}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Коммента́рий"
        verbose_name_plural = "Коммента́рии"


class VoteComment(models.Model):
    VOTE_TYPES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )

    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vote")
    comment = models.ForeignKey(Comment, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]
        verbose_name = "Голос за комментарий"
        verbose_name_plural = "Голоса за комментарии"

    def __str__(self):
        return f"{self.vote_type} от {self.user_id} Голос за комментарий {self.comment.id}"


class Link(models.Model):
    new_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name="links")
    facebook = models.URLField(verbose_name="Facebook URL", blank=True, null=True)
    whatsapp = models.URLField(verbose_name="WhatsApp URL", blank=True, null=True)
    telegram = models.URLField(verbose_name="Telegram URL", blank=True, null=True)
    vk = models.URLField(verbose_name="Vk URL", blank=True, null=True)
    twitter = models.URLField(verbose_name="Twitter URL", blank=True, null=True)
    threads = models.URLField(verbose_name="Threads URL", blank=True, null=True)
    instagram = models.URLField(verbose_name="Instagram URL", blank=True, null=True)
    linkedin = models.URLField(verbose_name="LinkedIn URL", blank=True, null=True)
    youtube = models.URLField(verbose_name="YouTube URL", blank=True, null=True)
    tiktok = models.URLField(verbose_name="TikTok URL", blank=True, null=True)

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["id"]
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
