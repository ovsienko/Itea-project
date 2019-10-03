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
    _price = IntField()
    quantity = IntField()
    photo = FileField()

    @property
    def price(self):
        return self._price / 100

    @price.setter
    def price(self, value):
        self._price = value


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


class Cart(Document):
    user = ReferenceField(User, required=True)
    items = ListField(ReferenceField(Item))
    is_archived = BooleanField(default=False)

    @property
    def get_sum(self):
        cart_sum = 0
        for i in self.items:
            cart_sum += i.price
        return cart_sum

    @classmethod
    def create_or_append_to_cart(cls, item, user):
        user_cart = cls.objects.filter(user=user).first()
        if user_cart and not user_cart.is_archived:
            user_cart.items.append(item)
            user_cart.save()
        else:
            cls(user=user, items=[item]).save()

    def clean_cart(self):
        self.items = []
        self.save()
#
# tx = Text(title='addtocart',
#           text='Додати в кошик',
#           lang='🇺🇦')
# tx.save()
# # 🇺🇸
# 🇺🇦
# mn = Menu(name='main', title='Кошик', callb='cart', lang='🇺🇦')
# mn.save()
# #
#
