from django.db import models

# Create your models here.
class Animent_table(models.Model):
    title = models.CharField(max_length=255,unique=True)
    state = models.CharField(max_length=60, null=True)
    type = models.CharField(max_length=50, null=True)
    cover = models.TextField(null=True)
    author = models.CharField(max_length=60, null=True)
    cartoon_voice = models.TextField(null=True)
    synopsis = models.TextField(null=True)
    video_url_list = models.TextField(null=True)
    title_list = models.TextField(null=True)
    uptime = models.DateTimeField(null=True)
    upyear = models.CharField(max_length=30, null=True)
    language = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=60, null=True)
    tag_id = models.CharField(max_length=30, null=True)
    score = models.FloatField(default=0)
    score_nub = models.IntegerField(default=0)
    click_nub = models.IntegerField(default=0)
    disk_number = models.IntegerField(default=1)
    class Meta:
        verbose_name = '动漫'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def to_dict(self):
        dic = {
            '名字': self.title,
            '状态': self.state,
            '动漫类型':self.type.__str__(),
            '封面url':self.cover,
            '视频url':self.video_url_list.__str__(),
            '更新时间':self.uptime,
            '介绍':self.synopsis,
            '声优': self.cartoon_voice,
            '年份': self.upyear,
        }
        return dic

class cartoon_weekUpdate(models.Model):
    week = models.CharField(max_length=50, null=True)
    cartoonTitle = models.TextField(null=True)

# 访问量
class user_visit(models.Model):
    ip = models.CharField(max_length=200)
    area = models.CharField(max_length=60, null=True)
    time = models.DateTimeField(auto_now=True)
    visits_number = models.IntegerField(default=1)
    visits_history = models.TextField(null=True)

# 留言
class leave_word(models.Model):
    from AnimentLoginApi.models import users_table
    ursename = models.CharField(null=True, max_length=200)
    content = models.TextField(null=True)
    reply = models.TextField(null=True)
    urse_img = models.ImageField(null=True)
    time = models.DateTimeField(auto_now=True)
    up_user_message = models.ManyToManyField(users_table, related_name='sendChar')