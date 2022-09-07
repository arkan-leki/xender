# Serializers define the API representation.
from urllib import request
from django.db.models import fields
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'


class TraderXSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeCompany
        fields = ['id', 'name', 'code', 'exchange', 'group', 'image', 'add_date', 'status',
                  'exchange', 'totallLoan', 'date', 'totallBuy', 'address', 'phone']


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeCompany
        fields = '__all__'


class SellDetailSerializer(serializers.ModelSerializer):
    sell_vendorID = serializers.ReadOnlyField(source='sell.vendor.id')

    class Meta:
        model = SellDetail
        fields = '__all__'


class OldAccSerializer(serializers.ModelSerializer):
    local_name = serializers.ReadOnlyField(source='local.name')
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = OldAcc
        fields = '__all__'


class SellXDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    item_wight = serializers.ReadOnlyField(source='item.wight')
    # item_image = serializers.ReadOnlyField(source='item.image')
    item_code = serializers.ReadOnlyField(source='item.barcode')
    # item_bag = serializers.ReadOnlyField(source='item.bag')
    item_group = serializers.ReadOnlyField(source='item.group.id')
    item_price = serializers.ReadOnlyField(source='item.price')
    sell_local = serializers.ReadOnlyField(source='sell.local.name')
    sell_vendor = serializers.ReadOnlyField(source='sell.vendor.name')
    sell_vendorID = serializers.ReadOnlyField(source='sell.vendor.id')
    item_group_name = serializers.ReadOnlyField(source='item.group.name')

    class Meta:
        model = SellDetail
        fields = ['id', 'item', 'item_name', 'item_code', 'datetime', 'stock', 'finalprice', 'total', 'item_group', 'item_price',
                  'quantity', 'price', 'sell', 'sell_local', 'sell_vendor', 'sell_vendorID', 'date', 'total', 'status', 'item_group_name', 'item_wight', 'allwight', 'item_image']


class LocalSerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    # exchange = serializers.ReadOnlyField()

    class Meta:
        model = LocalCompany
        fields = '__all__'


class ReSellSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='sell.group.id')
    group_name = serializers.ReadOnlyField(source='sell.group.name')
    local = serializers.ReadOnlyField(source='sell.local.id')
    local_name = serializers.ReadOnlyField(source='sell.local.name')
    item_name = serializers.ReadOnlyField(source='item.name')
    item_barcode = serializers.ReadOnlyField(source='item.barcode')
    # item_image = serializers.ReadOnlyField(source='item.image')

    class Meta:
        model = ReSell
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epmploye
        fields = '__all__'


class SellXSerializer(serializers.ModelSerializer):
    local_name = serializers.ReadOnlyField(source='local.name')
    owner_name = serializers.ReadOnlyField(source='local.owner_name')
    local_code = serializers.ReadOnlyField(source='local.code')
    local_phone = serializers.ReadOnlyField(source='local.phone')
    local_exchange = serializers.ReadOnlyField(source='local.exchange')
    local_region = serializers.ReadOnlyField(source='local.region.name')
    group_name = serializers.ReadOnlyField(source='group.name')
    vendor_name = serializers.ReadOnlyField(source='vendor.name')
    group_phone = serializers.ReadOnlyField(source='group.phone')
    vendor_phone = serializers.ReadOnlyField(source='vendor.phone')
    sell_detail = SellXDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Sell
        fields = ['id', 'local', 'local_name', 'local_code', 'owner_name', 'sell_detail', 'date', 'datetime', 'totall', 'totallint', 'totalback', 'status',
                  'discount', 'group_name', 'group', 'vendor', 'vendor_name', 'group_phone', 'vendor_phone', 'local_phone', 'local_exchange', 'local_region', 'totallBar']


class GroupXSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name', 'phone', 'image', 'add_date', 'status', 'items', 'vendors', 'totallSellMonthly', 'oldAccs',  'paymentByMonth',
                  'totallSell', 'totallOrder', 'payments', 'paymentsMonthly', 'loans', 'buys', 'banks', 'totallBuy', 'items']


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'


class BuySerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    bank_loan = serializers.ReadOnlyField(source='bank.loan')
    bank_income = serializers.ReadOnlyField(source='bank.income')

    class Meta:
        model = buy
        fields = '__all__'


class PaySalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Paysalary
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = '__all__'


class VendorXSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'totallSell', 'totallSellGroup', 'status']


class BankSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Bank
        fields = ['id', 'income', 'loan', 'group',
                  'group_name', 'datetime', 'date']


class PaySerializer(serializers.ModelSerializer):
    local_name = serializers.ReadOnlyField(source='local.name')
    local_code = serializers.ReadOnlyField(source='local.code')
    local_region = serializers.ReadOnlyField(source='local.region.name')
    local_phone = serializers.ReadOnlyField(source='local.phone')
    group_name = serializers.ReadOnlyField(source='group.name')
    bank_loan = serializers.ReadOnlyField(source='bank.loan')
    bank_income = serializers.ReadOnlyField(source='bank.income')
    payment_bank = BankSerializer(read_only=True, many=True)

    class Meta:
        model = Payment
        fields = ['id', 'date', 'datetime', 'local', 'group', 'bank', 'local_name',
                  'group_name', 'bank_loan', 'bank_income', 'payment_bank', 'local_code', 'local_region', 'local_phone']


class PayLoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payloan
        fields = '__all__'


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class TransportsSerializer(serializers.ModelSerializer):
    dliver_name = serializers.ReadOnlyField(source='dliver.name')

    class Meta:
        model = Transport
        fields = '__all__'


class TransportsXSerializer(serializers.ModelSerializer):
    request = SellXSerializer(read_only=True, many=True)

    class Meta:
        model = Transport
        fields = '__all__'


class OrderedSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderedXSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    item_price = serializers.ReadOnlyField(source='item.price')
    item_wight = serializers.ReadOnlyField(source='item.wight')
    item_quantity = serializers.ReadOnlyField(source='item.quantity')
    item_wightAll = serializers.ReadOnlyField(source='item.wightAll')
    item_code = serializers.ReadOnlyField(source='item.barcode')
    item_bag = serializers.ReadOnlyField(source='item.bag')
    sell = serializers.ReadOnlyField(source='sell.id')
    item_deleted = serializers.ReadOnlyField(source='item.deleted')

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderXSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    trader_name = serializers.ReadOnlyField(source='trader.name')
    trader_exchange = serializers.ReadOnlyField(source='trader.exchange')
    order_detail = OrderedXSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'group', 'trader', 'code', 'totallQ',
                  'discount', 'date', 'order_detail', 'group_name', 'trader_name', 'totallint', 'totall', 'trader_exchange', 'datetime']


class ItemXSerializer(serializers.ModelSerializer):
    # group_name = serializers.ReadOnlyField(source='group.name')
    # trader = serializers.ReadOnlyField(source='trader.name')
    # category_name = serializers.ReadOnlyField(source='category.name')
    item_sell = SellDetailSerializer(read_only=True, many=True)
    ReSell_item = ReSellSerializer(read_only=True, many=True)
    finalprice = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class KashHasb(serializers.ModelSerializer):
    sell_group = SellXSerializer(read_only=True, many=True)
    item_group = ItemXSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'url', 'name', 'phone', 'sell_group', 'item_group']


# class LocalXSerializer(serializers.ModelSerializer):
#     region_name = serializers.ReadOnlyField(source='region.name')
#     totallSell = serializers.ReadOnlyField()
#     # attempts = serializers.SerializerMethodField()
#     # payment_compnay = PaySerializer(read_only=True, many=True)
#     # oldacc_compnay = OldAccSerializer(read_only=True, many=True)

#     class Meta:
#         model = LocalCompany
#         fields = ['id', 'name', 'phone', 'code', 'region', 'region_name', 'location', 'image', 'add_date', 'status', 'zip_code', 'state', 'country',  'alarm',
#                   'owner_name', 'totallSell', 'exchange', 'totallPay', 'totallOld', 'totallOldloan', 'totallOldincome', 'exchange', 'totallSellback', 'date']
#         # fields = ['id', 'name', 'phone', 'code', 'region', 'location', 'image', 'add_date', 'status', 'zip_code', 'state', 'country',
#         #           'owner_name', 'totallSell', 'exchange', 'totallPay', 'exchange', 'totallSellback', 'attempts', 'date', 'payment_compnay', 'oldacc_compnay']

#     # def get_attempts(self, obj):
#     #     quiztakers = Sell.objects.filter(local=obj)
#     #     return SellXSerializer(quiztakers, many=True).data
