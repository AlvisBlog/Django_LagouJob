from django.db import models

# Create your models here.


class DataModel(models.Model):
    company_name = models.CharField(verbose_name = '公司名称', max_length = 256)
    zhiwei = models.CharField(verbose_name = '职位', max_length = 256)
    position = models.CharField(verbose_name = '地理位置', max_length = 256)
    money = models.CharField(verbose_name = '薪资范围', max_length = 256)
    exp = models.CharField(verbose_name = '经验', max_length = 256)
    xueli = models.CharField(verbose_name = "学历", max_length = 10)
    industry = models.CharField(verbose_name = '行业', max_length = 256)
    rongzi = models.CharField(verbose_name = "融资阶段", max_length = 10)
    skill_type = models.IntegerField(verbose_name = '技术类型', choices = ((0,"后端开发"),
                                                                       (1, "移动开发"),
                                                                       (2, "前端开发"),
                                                                       (3, "人工智能"),
                                                                       (4, "测试"),
                                                                       (5, "运维"),
                                                                       (6, "数据库")
                                                                      ))
    sort = models.IntegerField(verbose_name = "类型", choices = ((0, "java"), (1, "c++"), (2, "php"),(3, 'python'),
                                                               (4, "HTML5"), (5, "android"), (6, "ios"), (7, "wp"),
                                                               (8, "web前端"), (9, "Flash"), (10, "html5"), (11, "javascript"),
                                                               (12, "深度学习"), (13, "机器学习"), (14, "图像处理"), (15, "图像识别"),
                                                               (16, "测试工程师"), (17, "自动化测试"), (18, "功能测试"), (19, "性能测试"),
                                                               (20, "运维工程师"), (21, "运维开发工程师"), (22, "网络工程师"), (23, "系统工程师"),
                                                               (24, "mysql"), (25, "sqlserver"), (26, "oracle"), (27, "DB2")
                                                               ))