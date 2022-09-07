import datetime
import decimal
from tokenize import group
from django.db import models
from django.db.models.aggregates import Avg, Sum
from django.db.models.expressions import F
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_resized import ResizedImageField
from django.conf import settings
from dateutil.relativedelta import relativedelta
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name_plural = "هه‌ژمار"


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Group(models.Model):
    name = models.CharField(verbose_name="ناوی بنکە", max_length=250)
    phone = models.CharField(verbose_name="ژ.موبایل",
                             max_length=250, blank=True, null=True)
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    status = models.BooleanField(default=False)
    
    @property
    def paymentByMonth(self):
        if self.payment_group.all:
            grouptotallSells = {}
            MongtotallSells = {}
            for i in range(0, 10):
                paylaon = 0
                date = (datetime.date.today() +
                    relativedelta(months=-i))
                for pay in self.payment_group.filter(date__year=date.year, date__month=date.month):
                    paylaon = paylaon + (pay.bank.income - pay.bank.loan)
                    paylaon = decimal.Decimal(paylaon)
                    MongtotallSells[date.strftime('%Y-%m')] = paylaon
            grouptotallSells = MongtotallSells
        return grouptotallSells
    
    @property
    def items(self):
        items = 0
        if self.item_group.count:
            for totall in self.item_group.filter(deleted=False):
                items = items + (totall.mawe * totall.price)
            return items
        return items

    @property
    def vendors(self):
        items = self.vendor_group.count
        return items

    @property
    def totallSellMonthly(self):
        # today = datetime.date.today()
        totalls = 0
        for totall in self.sell_group.filter(date__month=datetime.date.today().month, status=True):
            totalls = totalls + (totall.totallint - totall.totalback)
        return str(float('{:.2f}'.format(totalls)))

    @property
    def totallSell(self):
        # today = datetime.date.today()
        totalls = 0
        for totall in self.sell_group.filter(status=True):
            totalls = totalls + (totall.totallint - totall.totalback)
        return str(float('{:.2f}'.format(totalls)))
    
    
    @property
    def totallOrder(self):
        totalls = 0
        for totall in self.order_group.all():
            totalls = totalls + (totall.totallint)
        return str(float('{:.2f}'.format(totalls)))

    @property
    def paymentsMonthly(self):
        if self.payment_group.count:
            paylaon = 0
            for pay in self.payment_group.filter(date__month=datetime.date.today().month):
                paylaon = paylaon + (pay.bank.income - pay.bank.loan)
            return paylaon

    @property
    def payments(self):
        if self.payment_group.count:
            paylaon = 0
            for pay in self.payment_group.all():
                paylaon = paylaon + (pay.bank.income - pay.bank.loan)
            return paylaon

    @property
    def oldAccs(self):
        if self.oldacc_group.count:
            paylaon = 0
            for laon in self.oldacc_group.all():
                paylaon = paylaon + (laon.loan - laon.income)
            return paylaon
    #

    @property
    def loans(self):
        if self.loan_group.count:
            paylaon = 0
            for laon in self.loan_group.all():
                paylaon = paylaon + (laon.bank.income - laon.bank.loan)
            return paylaon

    @property
    def buys(self):
        items = self.buy_group.count
        return items

    @property
    def totallBuy(self):
        totalls = 0
        if self.order_group.count():
            for totall in self.order_group.all():
                totalls = totalls + totall.totallint
        return totalls

    @property
    def banks(self):
        items = self.bank_group.count
        return items

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "بنکەکان"


class Epmploye(models.Model):
    name = models.CharField(verbose_name="ناوی کرێکار", max_length=250)
    phone = models.CharField(verbose_name="ژ.موبایل",
                             max_length=250, blank=True, null=True)
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "کارمەندان"


class Region(models.Model):
    name = models.CharField(verbose_name="ناوچە", max_length=250)
    code = models.CharField("کۆدی ناوچە", max_length=150)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "ناوچەکان"


class Vendor(models.Model):
    name = models.CharField(verbose_name="ناوی مەندوب", max_length=250)
    phone = models.CharField(verbose_name="ژ.موبایل",
                             max_length=250, blank=True, null=True)
    group = models.ForeignKey("Group", verbose_name="ناو بنکە",
                              on_delete=models.CASCADE, related_name="vendor_group", null=True)
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    status = models.BooleanField(default=False)

    @property
    def totallSell(self):
        groups = Group.objects.all()

        if self.sell_vendor.all:
            grouptotallSells = {}
            for group in groups:
                MongtotallSells = {}
                for i in range(0, 10):
                    totallSells = 0
                    date = (datetime.date.today() +
                            relativedelta(months=-i))
                    for totall in self.sell_vendor.filter(date__year=date.year, date__month=date.month, group=group.id):
                        totallSells = totallSells + \
                            (totall.totallint - totall.totalback)
                        totallSells = decimal.Decimal(totallSells)
                        MongtotallSells[date.strftime('%Y-%m')] = totallSells
                if(MongtotallSells) : grouptotallSells[group.name] = MongtotallSells 
        return grouptotallSells

    @property
    def totallSellGroup(self):
        groups = Group.objects.all()
        grouptotallSells = {}
        for group in groups:
            if self.sell_vendor.all:
                totallSells = 0
                for totall in self.sell_vendor.filter(date__month=datetime.date.today().month, group=group.id):
                    totallSells = totallSells + \
                        (totall.totallint - totall.totalback)
                    totallSells = decimal.Decimal(totallSells)
                grouptotallSells[group.id] = totallSells
        return grouptotallSells

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "فرۆشیاران-مەندوب"


class TradeCompany(models.Model):
    name = models.CharField(verbose_name="ناوی کۆمپانیا", max_length=250)
    code = models.CharField("کۆدی کۆمپانیا یا ژ.موبایل", max_length=150)
    address = models.CharField(
        verbose_name="ناونیشان", max_length=150, blank=True, null=True)
    phone = models.CharField(verbose_name="ژ.موبایل",
                             max_length=150, blank=True, null=True)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="trader_group")
    exchange = models.DecimalField(
        verbose_name="qarz yakam jar", max_digits=22, decimal_places=2, default="0.0")
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    @property
    def mawe(self):
        paylaon = 0
        buy = 0
        if(self.loan_compnay.all()):
            for pay in self.loan_compnay.all():
                paylaon = paylaon + (pay.bank.loan - pay.bank.income)

        if(self.order_compnay.all()):
            for laon in self.order_compnay.all():
                buy = buy + laon.totallint

        return (buy - paylaon) + self.exchange

    @property
    def totallLoan(self):
        totalls = 0
        for pay in self.loan_compnay.all():
            totalls = totalls + (pay.bank.loan - pay.bank.income)
        return str(float('{:.2f}'.format(totalls)))

    @property
    def totallBuy(self):
        totalls = 0
        for totall in self.order_compnay.all():
            totalls = totalls + totall.totallint
        return str(float('{:.2f}'.format(totalls)))

    class Meta:
        verbose_name_plural = "کۆمپانیا"


class LocalCompany(models.Model):
    name = models.CharField(verbose_name="ناوی کڕیار", max_length=250)
    code = models.CharField("کۆدی کڕیار", max_length=150)
    region = models.ForeignKey("Region", verbose_name="ناوچە",
                               on_delete=models.CASCADE, related_name="local_region")
    address = models.CharField(
        verbose_name="ناونیشان", max_length=150, blank=True, null=True)
    phone = models.CharField(verbose_name="ژ.موبایل",
                             max_length=150, blank=True, null=True)
    owner_name = models.CharField(
        verbose_name="ناوی خاوەنکار", max_length=250, blank=True, null=True)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    exchange = models.DecimalField(
        verbose_name="قەرزی یەکەمجار", max_digits=22, decimal_places=2, default="0.0")
    location = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True)
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    status = models.BooleanField(default=False)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    # @property
    # def mawe(self):
    #     groups = Group.objects.all()
    #     groupmawe = {}
    #     for group in groups:
    #         paylaon = 0
    #         buy = 0
    #         oldass = 0
    #         if(self.payment_compnay.filter(group=group.id)):
    #             for pay in self.payment_compnay.filter(group=group.id):
    #                 paylaon = paylaon + (pay.bank.income - pay.bank.loan)

    #         if(self.sell_compnay.filter(group=group.id, status=True)):
    #             for laon in self.sell_compnay.filter(group=group.id, status=True):
    #                 buy = buy + laon.totallint

    #         if(self.oldacc_compnay.filter(group=group.id)):
    #             for laon in self.oldacc_compnay.filter(group=group.id):
    #                 oldass = oldass + (laon.loan - laon.income)

    #         groupmawe[group.id] = (
    #             buy - paylaon) + self.exchange - decimal.Decimal(self.totallSellback[group.id]) + oldass
    #     return groupmawe
    
    # @property
    # def alarm(self):
    #     groups = Group.objects.all()
    #     groupmawe = {}
    #     for group in groups:
    #         paylaon = 0
    #         buy = 0
    #         oldass = 0
    #         if(self.payment_compnay.filter(group=group.id)):
    #             for pay in self.payment_compnay.filter(group=group.id):
    #                 paylaon = paylaon + (pay.bank.income - pay.bank.loan)

    #         if(self.sell_compnay.filter(group=group.id, status=True)):
    #             for laon in self.sell_compnay.filter(date__month=datetime.date.today().month, group=group.id, status=True):
    #                 buy = buy + laon.totallint

    #         if(self.oldacc_compnay.filter(group=group.id)):
    #             for laon in self.oldacc_compnay.filter(group=group.id):
    #                 oldass = oldass + (laon.loan - laon.income)
    #         if ( (buy - paylaon) + self.exchange - decimal.Decimal(self.totallSellback[group.id]) + oldass > 0.0 ):
    #             groupmawe[group.id] = (
    #                 buy - paylaon) + self.exchange - decimal.Decimal(self.totallSellback[group.id]) + oldass
    #         else : groupmawe[group.id] = 0.0
    #     return groupmawe

    # @property
    # def totallOld(self):
    #     groups = Group.objects.all()
    #     totallOlds = {}
    #     for group in groups:
    #         oldass = 0
    #         for laon in self.oldacc_compnay.filter(group=group.id):
    #             oldass = oldass + (laon.loan - laon.income)
    #         totallOlds[group.id] = decimal.Decimal(oldass)
    #     return totallOlds

    # @property
    # def totallOldloan(self):
    #     groups = Group.objects.all()
    #     totallOlds = {}
    #     for group in groups:
    #         oldass = 0
    #         for laon in self.oldacc_compnay.filter(group=group.id):
    #             oldass = oldass + (laon.loan)
    #         totallOlds[group.id] = decimal.Decimal(oldass)
    #     return totallOlds

    # @property
    # def totallOldincome(self):
    #     groups = Group.objects.all()
    #     totallOlds = {}
    #     for group in groups:
    #         oldass = 0
    #         for laon in self.oldacc_compnay.filter(group=group.id):
    #             oldass = oldass + (laon.income)
    #         totallOlds[group.id] = decimal.Decimal(oldass)
    #     return totallOlds

    # @property
    # def totallPay(self):
    #     groups = Group.objects.all()
    #     totallPays = {}
    #     for group in groups:
    #         totalls = 0
    #         for pay in self.payment_compnay.filter(group=group.id):
    #             totalls = totalls + pay.bank.income
    #         totallPays[group.id] = decimal.Decimal(totalls)
    #     return totallPays

    # @property
    # def totallSell(self):
    #     groups = Group.objects.all()
    #     totallSells = {}
    #     for group in groups:
    #         totalls = 0
    #         for totall in self.sell_compnay.filter(group=group.id):
    #             totalls = totalls + totall.totallint
    #         totallSells[group.id] = decimal.Decimal(totalls)
    #     return totallSells

    # @property
    # def totallSellback(self):
    #     groups = Group.objects.all()
    #     totallSells = {}
    #     for group in groups:
    #         totalls = 0
    #         for totall in self.sell_compnay.filter(group=group.id):
    #             totalls = totalls + totall.totalback
    #         totallSells[group.id] = decimal.Decimal(totalls)
    #     return totallSells

    class Meta:
        verbose_name_plural = "کڕیارەکان"


class Cat(models.Model):
    name = models.CharField(verbose_name="ناوی مەواد", max_length=250)
    image = ResizedImageField(size=[400, 400], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name='وێنه‌')
    deleted = models.BooleanField(default=False)
    date_added = models.DateField(
        verbose_name='ریكه‌وتی دانان', auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "جۆره‌كانی خواردن"


class Item(models.Model):
    category = models.ForeignKey(
        "Cat", related_name='item_category', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="item_group")
    name = models.CharField(verbose_name="ناوی مەواد", max_length=250)
    bag = models.CharField(verbose_name="جۆری مەواد", max_length=250)
    wight = models.DecimalField(
        verbose_name="کێشی کاڵا", max_digits=22, decimal_places=2, default=0)
    price = models.DecimalField(
        verbose_name="نرخی کڕین", max_digits=22, decimal_places=4)
    addprice = models.DecimalField(
        verbose_name="رءژەی قازانژ", max_digits=22, decimal_places=4)
    quantity = models.IntegerField(verbose_name=" دانە")
    barcode = models.CharField("کۆدی مەواد", max_length=150)
    trader = models.ForeignKey("TradeCompany", verbose_name="کۆمپانیا",
                               on_delete=models.CASCADE, related_name="item_compnay")
    stock = models.IntegerField(verbose_name=" مانەوەی یەکەم جار", default=0)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    image = ResizedImageField(size=[400, 400], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name="وێنه‌")
    add_date = models.DateTimeField(verbose_name='رێکەوت', auto_now=True)
    deleted = models.BooleanField(default=False)
    # mawe = models.IntegerField(default='0')

    def __str__(self):
        return self.name

    # @property
    # def popularity(self):
    #     likes = 0
    #     if(self.item_sell.aggregate(Sum('quantity'))['quantity__sum']):
    #         likes = self.item_sell.aggregate(Sum('quantity'))['quantity__sum']
    #     return likes

    # @property
    # def ordered(self):
    #     krin = 0
    #     if(self.item_order.aggregate(Sum('quantity'))['quantity__sum']):
    #         krin = self.item_order.aggregate(Sum('quantity'))['quantity__sum']
    #     return krin

    @property
    def finalprice(self):
        price = self.price + (self.price * self.addprice)
        return str(float('{:.2f}'.format(price)))

    # @property
    # def mawe(self):
    #     krin = 0
    #     frosh = 0
    #     gerawe = 0
    #     if(self.item_order.aggregate(Sum('quantity'))['quantity__sum']):
    #         krin = self.item_order.aggregate(Sum('quantity'))['quantity__sum']

    #     frosh = 0
    #     if(self.item_sell.aggregate(Sum('quantity'))['quantity__sum']):
    #         frosh = self.item_sell.aggregate(Sum('quantity'))['quantity__sum']

    #     if self.ReSell_item.aggregate(Sum('quantity'))['quantity__sum']:
    #         gerawe = self.ReSell_item.aggregate(
    #             Sum('quantity'))['quantity__sum']

    #     return (krin - frosh) + (self.stock) + (gerawe)

    class Meta:
        verbose_name_plural = "کاڵاکان"


class Pricing(models.Model):
    item = models.ForeignKey(
        "Item", related_name='item_price', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    price = models.DecimalField(
        verbose_name="نرخی کڕین", max_digits=22, decimal_places=2)
    addprice = models.DecimalField(
        verbose_name="رءژەی قازانژ", max_digits=22, decimal_places=2)
    status = models.BooleanField(default=False)
    date_added = models.DateField(verbose_name='date added', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "نرخەکان"


class Sell(models.Model):
    vendor = models.ForeignKey("Vendor", verbose_name="فرۆشیار",
                               on_delete=models.CASCADE, related_name="sell_vendor")
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="sell_group")
    local = models.ForeignKey("LocalCompany", verbose_name="کڕیار",
                              on_delete=models.CASCADE, related_name="sell_compnay")
    discount = models.DecimalField(
        verbose_name="dashkan", max_digits=22, decimal_places=2, blank=True, default=0.0)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "wasl " + str(self.id)

    @property
    def totallBar(self):
        total = 0
        if len(self.sell_detail.all()):
            total = self.sell_detail.aggregate(Sum('quantity'))[
                'quantity__sum']
        return str(total)

    @property
    def totall(self):
        total = 0
        if len(self.sell_detail.all()):
            total = float('{:.2f}'.format(self.sell_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']))
        return str(total)

    @property
    def totalback(self):
        tot = 0
        if len(self.ReSell_detail.all()):
            tot = self.ReSell_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']
        return tot

    @property
    def totallint(self):
        tot = 0
        if len(self.sell_detail.all()):
            tot = self.sell_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total'] - self.discount
        return tot

    class Meta:
        verbose_name_plural = "فرۆشتنەکان"


class SellDetail(models.Model):
    sell = models.ForeignKey("Sell", verbose_name="وەسڵ",
                             on_delete=models.CASCADE, related_name="sell_detail")
    item = models.ForeignKey("Item", verbose_name="کاڵا",
                             on_delete=models.CASCADE, related_name="item_sell")
    quantity = models.IntegerField(verbose_name="دانە")
    price = models.DecimalField(
        verbose_name="نرخ", max_digits=22, decimal_places=2)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)
    status = models.BooleanField(default=False)

    def item_image(self):
        if self.item.image:
            return self.item.image.url
        else:
            return 'null'

    def allwight(self):
        return self.item.wight * self.quantity

    def total(self):
        return self.price * self.quantity

    def finalprice(self):
        return self.item.finalprice

    def stock(self):
        return self.item.stock

    def __str__(self):
        return "forsh kala " + str(self.id)

    class Meta:
        verbose_name_plural = "کاڵای دەرچوو"

# // mewady hawt nek order


class Order(models.Model):
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="order_group")
    trader = models.ForeignKey("TradeCompany", verbose_name="کۆمپانیا",
                               on_delete=models.CASCADE, related_name="order_compnay")
    code = models.CharField(verbose_name="ژمارەی وەسڵ",
                            max_length=250, blank=True, default="")
    discount = models.DecimalField(
        verbose_name="داشکاندن", max_digits=22, decimal_places=2, blank=True, default="0.0")
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)

    def __str__(self):
        return "wasl dawakary" + str(self.id)

    @property
    def totall(self):
        total = 0
        if len(self.order_detail.all()):
            total = float('{:.2f}'.format(self.order_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']))
        return str(total)

    @property
    def totallQ(self):
        total = 0
        if len(self.order_detail.all()):
            total = float('{:.2f}'.format(self.order_detail.annotate(
                answer=F('quantity')).aggregate(total=Sum('answer'))['total']))
        return str(total)

    @property
    def totallint(self):
        tot = 0
        if len(self.order_detail.all()):
            tot = self.order_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total'] - self.discount
        return tot

    class Meta:
        verbose_name_plural = "کڕین"


class OrderDetail(models.Model):
    order = models.ForeignKey("Order", verbose_name="wasl",
                              on_delete=models.CASCADE, related_name="order_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="item_order")
    quantity = models.IntegerField(verbose_name=" دانە")
    price = models.DecimalField(
        verbose_name="nrx", max_digits=22, decimal_places=2)
    date = models.DateField(verbose_name="بەروار", auto_now_add=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)

    @property
    def total(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = "کالای هاتوو"


class Payment(models.Model):
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="payment_group")
    local = models.ForeignKey("LocalCompany", verbose_name="کڕیار",
                              on_delete=models.CASCADE, related_name="payment_compnay")
    bank = models.ForeignKey("Bank", verbose_name="قاسە",
                             on_delete=models.CASCADE, related_name="payment_bank")
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)
    
    class Meta:
        verbose_name_plural = "پارەدان"


class OldAcc(models.Model):
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="oldacc_group")
    local = models.ForeignKey("LocalCompany", verbose_name="کڕیار",
                              on_delete=models.CASCADE, related_name="oldacc_compnay")
    income = models.DecimalField(
        verbose_name="هاتوو", max_digits=22, decimal_places=2)
    loan = models.DecimalField(
        verbose_name="دەرچووو", max_digits=22, decimal_places=2)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "کۆن"


class Payloan(models.Model):
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="loan_group")
    trader = models.ForeignKey("TradeCompany", verbose_name="کڕیار",
                               on_delete=models.CASCADE, related_name="loan_compnay")
    bank = models.ForeignKey("Bank", verbose_name="قاسە",
                             on_delete=models.CASCADE, related_name="loan_bank")
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "قەرزدان"


class buy(models.Model):
    name = models.CharField(verbose_name="هۆکار", max_length=250, blank=True)
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="buy_group")
    bank = models.ForeignKey("Bank", verbose_name="قاسە",
                             on_delete=models.CASCADE, related_name="buy_bank")
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)


class Paysalary(models.Model):
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="salary_group")
    bank = models.ForeignKey("Bank", verbose_name="قاسە",
                             on_delete=models.CASCADE, related_name="salary_bank")
    employee = models.ForeignKey("Epmploye", verbose_name="کارمەند",
                                 on_delete=models.CASCADE, related_name="salary_employee")
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)


class Bank(models.Model):
    group = models.ForeignKey("Group", verbose_name="ناوی بنکە",
                              on_delete=models.CASCADE, related_name="bank_group")
    income = models.DecimalField(
        verbose_name="هاتوو", max_digits=22, decimal_places=2)
    loan = models.DecimalField(
        verbose_name="دەرچووو", max_digits=22, decimal_places=2)
    date = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)


class ReSell(models.Model):
    sell = models.ForeignKey("Sell", verbose_name="داواکاری",
                             on_delete=models.CASCADE, related_name="ReSell_detail")
    item = models.ForeignKey("Item", verbose_name="کاڵا",
                             on_delete=models.CASCADE, related_name="ReSell_item")
    quantity = models.IntegerField(verbose_name="دانە")
    price = models.DecimalField(
        verbose_name="نرخ", max_digits=22, decimal_places=2)
    date = models.DateField(verbose_name="بەروار", auto_now_add=True)
    datetime = models.DateTimeField(
        verbose_name="رێکەوت", auto_now_add=True, blank=True)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.pk)

    def __unicode__(self):
        return


class Motors(models.Model):
    title = models.CharField(max_length=110, blank=True, null=True)
    number = models.CharField(max_length=11, blank=True, null=True)
    image = ResizedImageField(size=[300, 300], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name="وێنه‌")
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "Motors"


class Dliver(models.Model):
    name = models.CharField(max_length=110, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    motor = models.ForeignKey(
        Motors, related_name='owed_motor', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    phoneId = models.CharField(max_length=110, blank=True, null=True)
    image = ResizedImageField(size=[200, 200], quality=50,
                              upload_to='images/', blank=True, null=True, verbose_name="وێنه‌")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "شۆفێر"


class Transport(models.Model):
    dliver = models.ForeignKey(Dliver, on_delete=models.CASCADE)
    # request = models.ForeignKey(Sell, on_delete=models.CASCADE)
    request = models.ManyToManyField('Sell', related_name="bar_sell")
    start_date = models.DateTimeField(verbose_name='start date')
    end_date = models.DateTimeField(verbose_name='end date')
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.request)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "باركراو"


class BnkaUser(models.Model):
    bnka = models.ForeignKey(
        Group, related_name='BnkaUser', on_delete=models.CASCADE)
    user = models.ForeignKey(
        Account, related_name='BnkasUser', on_delete=models.CASCADE)
    date_added = models.DateField(verbose_name='date added', auto_now_add=True)

    def __str__(self):
        return str(self.bnka) + " " + str(self.user)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "بنکەو بەکارهێنەر"


class VendorUser(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name='VendorUser', on_delete=models.CASCADE)
    user = models.ForeignKey(
        Account, related_name='VendosUser', on_delete=models.CASCADE)
    date_added = models.DateField(verbose_name='date added', auto_now_add=True)

    def __str__(self):
        return str(self.vendor) + " " + str(self.user)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "مەندوب بەکارهێنەر"


class RequestOrder(models.Model):
    customer = models.ForeignKey(
        TradeCompany, related_name='reqtrader', on_delete=models.CASCADE, default=1)
    request_detail = models.ManyToManyField('RequestDetail')
    totalprice = models.CharField(max_length=11)
    date_added = models.DateField(verbose_name='date added', auto_now_add=True)
    last_edit = models.DateTimeField(verbose_name='last edit', auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "داواكاریه‌كان"


class RequestSell(models.Model):
    local = models.ForeignKey(
        LocalCompany, related_name='reqtlocal', on_delete=models.CASCADE, default=1)
    request_detail = models.ManyToManyField('RequestDetail')
    totalprice = models.CharField(max_length=11)
    date_added = models.DateField(verbose_name='date added', auto_now_add=True)
    last_edit = models.DateTimeField(verbose_name='last edit', auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "داواكاریه‌كان"


class RequestDetail(models.Model):
    item = models.ForeignKey(
        Item, related_name='req_item', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=11)
    price = models.CharField(max_length=11)
    date_added = models.DateField(
        verbose_name='date added', auto_now_add=True)
    last_edit = models.DateTimeField(verbose_name='last edit', auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.food.title + str(self.total_price)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "ورده‌كاری داواكاری"
