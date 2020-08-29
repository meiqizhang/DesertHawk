from django.db import models

# Create your models here.
"""
CREATE TABLE `t_article_index` (
  `score` float DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `content` mediumtext,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` int DEFAULT NULL,
  FULLTEXT KEY `fulltext_title_content` (`title`,`content`) /*!50100 WITH PARSER `ngram` */ ,
  FULLTEXT KEY `title_indx` (`title`) /*!50100 WITH PARSER `ngram` */ ,
  FULLTEXT KEY `title_index` (`title`) /*!50100 WITH PARSER `ngram` */ ,
  FULLTEXT KEY `content_index` (`content`) /*!50100 WITH PARSER `ngram` */ 
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC

"""


class ArticleIndex(models.Model):
    title = models.CharField(max_length=128, verbose_name='文章标题')
    content = models.TextField(max_length=1024*1024*4, verbose_name='文章内容')

    class Meta:
        db_table = 't_article_index'
        verbose_name = '文章索引'
        verbose_name_plural = verbose_name
