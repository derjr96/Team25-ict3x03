# NOTE: This script may take up to 2 hours to run

from django.core.management.base import BaseCommand
from djangotaurus.models import Stock
from djangotaurus.validation import Validation_Functions
import yfinance as yf
import csv

class Command(BaseCommand):
    help = 'Populates the Stock table with the yfinance API'

    def _populate_db(self):
        symbols_list = ''
        symbol_suffix = 'SI'

        with open('data/SGX.txt', newline='') as symbols:
            csv_reader = csv.reader(symbols, delimiter='\t')
            headers = next(csv_reader)
            for symbol in csv_reader:
                symbols_list += f'{symbol[0]}.{symbol_suffix} '

        Stock.objects.all().delete()

        tickers = yf.Tickers(symbols_list)

        for symbol, ticker in tickers.tickers.items():
            company_name = ticker.info.get('longName')
            if company_name:
                print(f'Inserting {company_name}...')
                if (Validation_Functions.validate_yfinance(symbol, ticker.info)):
                    stock = Stock()
                    stock.company_name = company_name
                    stock.image_url = ticker.info.get('logo_url')
                    stock.stock_symbol = symbol
                    stock.sector = ticker.info.get('sector')
                    stock.industry = ticker.info.get('industry')
                    stock.company_desc = ticker.info.get('longBusinessSummary')
                    stock.save()
                else:
                    print(f'{symbol}: API validation error, skipping symbol')
        print(f'Stocks Insertion Complete')

    def handle(self, *args, **options):
        self._populate_db()
