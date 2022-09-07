from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import viewsets
from .models import *
from .serializer import *
# Create your views here.


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocalViewSet(viewsets.ModelViewSet):
    queryset = LocalCompany.objects
    serializer_class = LocalSerializer


# class LocalXViewSet(viewsets.ModelViewSet):
#     queryset = LocalCompany.objects.all().order_by('id')
#     serializer_class = LocalXSerializer


class TraderViewSet(viewsets.ModelViewSet):
    queryset = TradeCompany.objects.all()
    serializer_class = TraderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

class TraderXViewSet(viewsets.ModelViewSet):
    queryset = TradeCompany.objects.all()
    serializer_class = TraderXSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(deleted=False).order_by('id')
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer

class GroupXViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupXSerializer


class ItemXViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemXSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'deleted']


class SellDetailViewSet(viewsets.ModelViewSet):
    queryset = SellDetail.objects.all()
    serializer_class = SellDetailSerializer


class SellXDetailViewSet(viewsets.ModelViewSet):
    queryset = SellDetail.objects.all().order_by('-datetime')
    serializer_class = SellXDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['item']


class SellViewSet(viewsets.ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']


class SellXViewSet(viewsets.ModelViewSet):
    queryset = Sell.objects.order_by('-datetime')
    serializer_class = SellXSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group','local_id','status']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

class OldAccrViewSet(viewsets.ModelViewSet):
    queryset = OldAcc.objects.all()
    serializer_class =OldAccSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group','local']

class OrderXViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-datetime')
    serializer_class = OrderXSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']


class OrderedViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderedSerializer


class TransportsViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all().order_by('-id')
    serializer_class = TransportsSerializer

class TransportsXViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all().order_by('-id')
    serializer_class = TransportsXSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all().order_by('id')
    serializer_class = RegionSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorXViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorXSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all().order_by('-datetime')
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

class PayViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-datetime')
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['local']

class BuyViewSet(viewsets.ModelViewSet):
    queryset = buy.objects.all()
    serializer_class = BuySerializer

class PayLoanViewSet(viewsets.ModelViewSet):
    queryset = Payloan.objects.all()
    serializer_class = PayLoanSerializer

class ReSellViewSet(viewsets.ModelViewSet):
    queryset = ReSell.objects.all()
    serializer_class = ReSellSerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PriceSerializer

class EmployeViewSet(viewsets.ModelViewSet):
    queryset = Epmploye.objects.all()
    serializer_class = EmployeSerializer

class PaySalaryViewSet(viewsets.ModelViewSet):
    queryset = Epmploye.objects.all()
    serializer_class = PaySalarySerializer


class OrderedXViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderedXSerializer
    
def mycompany(request):
    response_data = {}
    response_data['company'] = 'زەندەر'
    return JsonResponse(response_data)

# class LocalXSerializer(serializers.ModelSerializer):
#     region = serializers.ReadOnlyField(source='region.name')
#     totallSell = serializers.ReadOnlyField()
#     attempts = serializers.SerializerMethodField()
#     # oldacc_compnay = OldAccSerializer(read_only=True, many=True)
#     # payment_company = PaySerializer(read_only=True, many=True)

#     class Meta:
#         model = LocalCompany
#         fields = ['id', 'name', 'phone', 'code', 'region', 'location', 'image', 'add_date', 'status', 'zip_code', 'state', 'country',
#                   'owner_name', 'totallSell', 'mawe', 'totallPay', 'exchange', 'totallSellback', 'attempts', 'date']

#     def get_attempts(self, obj):
#         quiztakers = Sell.objects.filter(local=obj)
#         return SellSerializer(quiztakers, many=True).data