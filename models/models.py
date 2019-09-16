from mongoengine import *
connect('ProjectDB')

class Category(Document):
    title = StringField()
    sub_category = ListField(ReferenceField('self'))
    is_parent = BooleanField()
    lang = StringField(max_length=3)

    # @classmethod
    # def get_or_create(cls):
    #     cat = cls.objects

class Additing(Document):
    tele_user = IntField()
    category = ReferenceField(Category)
    stage = StringField()

    @classmethod
    def get_or_create(cls, tele_user):
        add = cls.objects.filter(tele_user=tele_user).first()
        if not add:
            add = cls(tele_user=tele_user, stage='start')
            cat = Category()
            add.category = cat
            cat.save()
            add.save()
        return add
