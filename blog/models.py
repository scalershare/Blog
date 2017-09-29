from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100)


class PublishedManage(models.Manager):
    """创建发布日期管理器"""
    def get_queryset(self):
        return super(PublishedManage,
                     self).get_queryset().filter(status='发布')


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章模型"""
    STATUS_CHOICES = (('草稿', '草稿'),
                      ('发布', '发布'))
    category = models.ForeignKey(Category, related_name='post_category')
    title = models.CharField(u'标题', max_length=150)
    body = models.TextField()
    author = models.ForeignKey(User,
                               related_name='author')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='草稿')
    summary = models.CharField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = models.Manager()
    published = PublishedManage()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.id])
