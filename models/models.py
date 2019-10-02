from mongoengine import *
connect('ProjectDB')


class Category(Document):
    title = StringField()
    title_en = StringField()

    def __str__(self):
        return self.title

    def delete_all(self):
        Item.objects.filter(category=self).delete()
        self.delete()

    def get_card(self, lang):
        if lang == '🇺🇦':
            return self.title
        elif lang == '🇺🇸':
            return self.title_en


class AddCat(Document):
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


class Item(Document):
    title = StringField()
    title_en = StringField()
    category = ReferenceField(Category)
    desc = StringField()
    desc_en = StringField()
    price = IntField()
    quantity = IntField()
    photo = FileField()


class AddItem(Document):
    tele_user = IntField()
    item = ReferenceField(Item)
    stage = StringField()

    @classmethod
    def get_or_create(cls, tele_user):
        add = cls.objects.filter(tele_user=tele_user)
        if not add:
            add = cls(tele_user=tele_user, stage='start',)
            itm = Item()
            itm.save()
            add.item = itm
            add.save()
        return add


class User(Document):
    user_id = IntField()
    name = StringField()
    surname = StringField()
    nickname = StringField()
    user_state = IntField()
    lang = StringField()

    @classmethod
    def get_or_create_user(cls, message):
        user = cls.objects.filter(user_id=message.from_user.id).first()
        if user:
            return user
        else:
            return cls(user_id=message.from_user.id,
                       name=message.from_user.first_name,
                       surname=message.from_user.last_name,

                       nickname=message.from_user.username).save()


class Text(Document):
    title = StringField()
    text = StringField()
    lang = StringField()


class Menu(Document):
    title = StringField()
    callb = StringField()
    lang = StringField()
    name = StringField()


#
# tx = Text(title='cat_list',
#           text='Список категорій',
#           lang='🇺🇦')
# tx.save()
# # 🇺🇸
# 🇺🇦
# mn = Menu(name='main', title='Категорії', callb='cats', lang='🇺🇦')
# mn.save()
#
#
