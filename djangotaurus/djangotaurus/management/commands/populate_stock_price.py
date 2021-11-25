from django.core.management.base import BaseCommand
from djangotaurus.models import Stock, StockPriceCurrent

class Command(BaseCommand):
    help = 'Populates the StockPriceCurrent table with initial stocks'

    def _populate_db(self):
        stock_list = Stock.objects.all()
        for stock in stock_list:
            stock_price = StockPriceCurrent()
            stock_price.stock = stock
            stock_price.save()

    def handle(self, *args, **options):
        self._populate_db()


