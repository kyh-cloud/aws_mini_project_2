from django.db import models


class Board(models.Model):
    b_number = models.AutoField(db_column='b_number', primary_key=True)
    title = models.CharField(db_column='title', max_length=225, blank=True, null=True)
    b_context = models.CharField(db_column='b_context', max_length=10000, blank=True, null=True)
    b_datetime = models.DateTimeField(db_column='b_datetime', blank=True, null=True)
    id = models.ForeignKey('Users', models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'board'

        def __str__(self):
            return "제목 : " + self.b_title + ", 작성자 : " + self.b_writer


class Comment(models.Model):
    c_number = models.AutoField(db_column='c_number', primary_key=True)
    c_context = models.CharField(db_column='c_context', max_length=10000, blank=True, null=True)
    c_datetime = models.DateTimeField(db_column='c_datetime', blank=True, null=True)
    b_number = models.ForeignKey('Board', models.DO_NOTHING, db_column='b_number')
    id = models.ForeignKey('Users', models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'comment'


class Users(models.Model):
    id = models.CharField(db_column='id', primary_key=True, max_length=225)
    pw = models.CharField(db_column='pw', max_length=225, blank=True, null=True)
    name = models.CharField(db_column='name', max_length=225)
    nickname = models.CharField(db_column='nickname', max_length=225)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name;
