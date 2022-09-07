from django.contrib import admin
from django.contrib.admin.decorators import display
from django_resized import forms
from myapp.models import *
# Register your models here.
# admin.site.register(Account)
# admin.site.register(Cat)


class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('id', 'name', 'phone', 'add_date')


admin.site.register(Group, GroupAdmin)

# class ItemAdmin(admin.ModelAdmin):
    # model = Item
    # list_display = ['id', 'barcode', 'group', 'name',
    #                 # 'price',
    #                 # 'addprice',
    #                 'finalprice',
    #                 # 'stock',
    #                 'mawe',
    #                 # 'deleted',
    #                 'quantity'
    #                 ]
    # # list_editable = ['group', 'price', 'addprice', 'stock', 'deleted']
    # # list_editable = ['quantity']
    # list_filter = ['group', 'deleted']
    # list_max_show_all = False


# admin.site.register(Item, ItemAdmin)


# class LocalCompanyAdmin(admin.ModelAdmin):
#     model = LocalCompany
#     list_display = ['id', 'name', 'code', 'region',
#                     'phone', 'owner_name', 'exchange', 'totallSell', 'totallPay', 'mawe']
#     list_filter = ['region']
#     list_max_show_all = False


# admin.site.register(LocalCompany, LocalCompanyAdmin)

class RegionAdmin(admin.ModelAdmin):
    model = Region
    list_display = ('id', 'name', 'code')
    forms = ['id']

admin.site.register(Region,RegionAdmin)

admin.site.register(Vendor)


class BankAdmin(admin.ModelAdmin):
    model = Bank
    list_display = ('id', 'group', 'income', 'loan')
    list_filter = ['group', 'date']


admin.site.register(Bank, BankAdmin)


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ('id', 'group', 'local', 'bank', 'date')
    list_filter = ['group', 'date']


admin.site.register(Payment, PaymentAdmin)

admin.site.register(Transport)
admin.site.register(Dliver)
admin.site.register(Motors)


class OldAcctAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ('id', 'group', 'local', 'income', 'loan', 'date')
    list_filter = ['group', 'date']
admin.site.register(OldAcc,OldAcctAdmin)
# admin.site.register(Sell)
admin.site.register(TradeCompany)
admin.site.register(ReSell)


class SelldetailAdmin(admin.TabularInline):
    model = SellDetail
    # list = ('sell', 'item','quantity','price')
    # readonly_fields = ['finalprice','mawe']


class SellAdmin(admin.ModelAdmin):
    model = Sell
    # list_display = ['vendor', 'group', 'local',
    #                 'discount', 'date', 'status']
    # list_editable = ['status']
    # list_filter = ['group', 'date']
    # inlines = [SelldetailAdmin]


admin.site.register(Sell, SellAdmin)


class OrderdetailAdmin(admin.TabularInline):
    model = OrderDetail


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id','trader']
    # inlines = [OrderdetailAdmin]


admin.site.register(Order, OrderAdmin)


class SellDetailAdmin(admin.ModelAdmin):
    model = SellDetail
    # list_display = ['id','sell', 'item', 'quantity',
    #                 'price', 'total', 'date', 'status']
    # list_editable = ['price', 'quantity', 'status']
    # list_filter = ['item', 'date']
    # list_max_show_all = False


admin.site.register(SellDetail, SellDetailAdmin)


# class ItemDetailAdmin(admin.TabularInline):
#     model = Item

# class GroupAdmin(admin.ModelAdmin):
#     model = Group
#     inlines = [ItemDetailAdmin]

# admin.site.register(Group, GroupAdmin)

# class TradeCompanyAdmin(admin.ModelAdmin):
#     model = TradeCompany
#     inlines = [ItemDetailAdmin]

# admin.site.register(TradeCompany, TradeCompanyAdmin)
