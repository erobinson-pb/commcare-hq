# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from mock.mock import MagicMock

from custom.yeksi_naa_reports.tests.utils import YeksiTestCase
from custom.yeksi_naa_reports.reports import Dashboard3Report


class TestDashboard3(YeksiTestCase):

    def test_satisfaction_rate_after_delivery_data_report(self):
        mock = MagicMock()
        mock.couch_user = self.user
        mock.GET = {
            'location_id': '',
            'month_start': '10',
            'year_start': '2017',
            'month_end': '3',
            'year_end': '2018',
        }

        dashboard3_report = Dashboard3Report(request=mock, domain='test-pna')

        satisfaction_rate_after_delivery_data_report = \
            dashboard3_report.report_context['reports'][0]['report_table']
        headers = satisfaction_rate_after_delivery_data_report['headers'].as_export_table[0]
        rows = satisfaction_rate_after_delivery_data_report['rows']
        total_row = satisfaction_rate_after_delivery_data_report['total_row']

        self.assertEqual(
            headers,
            ['Produit', 'Octobre 2017', 'Novembre 2017', 'Décembre 2017', 'Janvier 2018',
             'Février 2018', 'Mars 2018']
        )
        self.assertEqual(
            sorted(rows, key=lambda x: x[0]),
            sorted([
                [u'RIFAMPICINE+ISONIAZIDE+PYRAZINAMIDE+ETHAMBUTOL (150+75+400+2', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'pas de données', u'100.00%'],
                [u'NEVIRAPINE 200MG CP.', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'93.30%'],
                [u'ACETATE DE MEDROXY PROGESTERONE 104MG/0.65ML INJ. (SAYANA PRESS)', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'pas de données', u'100.00%'],
                [u'ACT ADULTE', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'100.00%'],
                [u'Produit A', u'97.63%', u'94.86%', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données'],
                [u'Produit 10', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'87.10%', u'96.30%'],
                [u'Produit 12', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données'],
                [u'LAMIVUDINE+NEVIRAPINE+ZIDOVUDINE (30+50+60)MG CP.', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'100.00%'],
                [u'DISPOSITIF INTRA UTERIN (TCU 380 A) - DIU', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'1462.40%'],
                [u'PARACETAMOL 500MG CP.', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données'],
                [u'EFAVIRENZ 600MG CP.', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'80.77%'],
                [u'RIFAMPICINE+ISONIAZIDE (150+75)MG CP.', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'101.21%'],
                [u'Produit 15', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'100.00%'],
                [u'Test Product 1', u'518.75%', u'592.86%', u'691.67%', u'345.83%', u'129.69%', u'98.44%'],
                [u'Produit 14', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'90.00%'],
                [u'ACETATE DE MEDROXY PROGESTERONE 150MG/ML+S A B KIT (1+1) (DEPO-PROVERA)', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'pas de données', u'150.00%'],
                [u'Produit 2', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'100.00%'],
                [u'ACT PETIT ENFANT', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'100.00%'],
                [u'Produit 1', u'pas de données', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données'],
                [u'ALBENDAZOL 4% SB.', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'100.00%'],
                [u'LEVONORGESTREL+ETHYNILESTRADIOL+FER (0.15+0.03+75)MG (MICROGYNON)', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'pas de données', u'222.22%'],
                [u'Produit C', u'93.88%', u'93.28%', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données'],
                [u'RIFAMPICINE+ISONIAZIDE+PYRAZINAMIDE (60+30+150)MG CP. DISPER', u'pas de données',
                 u'pas de données', u'pas de données', u'pas de données', u'pas de données', u'100.00%'],
                [u'TEST RAPIDE HIV 1/2 (SD BIOLINE)', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données', u'pas de données', u'100.00%'],
                [u'Produit B', u'98.28%', u'98.94%', u'pas de données', u'pas de données', u'pas de données',
                 u'pas de données']
            ], key=lambda x: x[0])
        )
        self.assertEqual(
            total_row,
            ['Total (CFA)', '104.01%', '104.28%', '691.67%', '345.83%', '99.54%', '188.90%']
        )

    def test_valuation_of_pna_stock_per_product_data_report(self):
        mock = MagicMock()
        mock.couch_user = self.user
        mock.GET = {
            'location_id': '',
            'month_start': '10',
            'year_start': '2017',
            'month_end': '3',
            'year_end': '2018',
        }

        dashboard3_report = Dashboard3Report(request=mock, domain='test-pna')

        valuation_of_pna_stock_per_product_data_report = \
            dashboard3_report.report_context['reports'][1]['report_table']
        headers = valuation_of_pna_stock_per_product_data_report['headers'].as_export_table[0]
        rows = valuation_of_pna_stock_per_product_data_report['rows']
        total_row = valuation_of_pna_stock_per_product_data_report['total_row']

        self.assertEqual(
            headers,
            ['Produit', 'Octobre 2017', 'Novembre 2017', 'Décembre 2017', 'Janvier 2018',
             'Février 2018', 'Mars 2018']
        )
        self.assertItemsEqual(
            sorted(rows, key=lambda x: x[0]),
            sorted([
                ['RIFAMPICINE+ISONIAZIDE+PYRAZINAMIDE+ETHAMBUTOL (150+75+400+2', '0.00', '0.00', '0.00',
                 '0.00', '0.00', '0.00'],
                ['NEVIRAPINE 200MG CP.', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['ACETATE DE MEDROXY PROGESTERONE 104MG/0.65ML INJ. (SAYANA PRESS)', '0.00', '0.00', '0.00',
                 '0.00', '0.00', '0.00'], ['ACT ADULTE', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['Produit A', '442500.00', '717500.00', '0.00', '0.00', '0.00', '0.00'],
                ['Produit 10', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['Produit 12', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['LAMIVUDINE+NEVIRAPINE+ZIDOVUDINE (30+50+60)MG CP.', '0.00', '0.00', '0.00', '0.00', '0.00',
                 '0.00'],
                ['DISPOSITIF INTRA UTERIN (TCU 380 A) - DIU', '0.00', '0.00', '0.00', '0.00', '0.00',
                 '0.00'], ['PARACETAMOL 500MG CP.', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['EFAVIRENZ 600MG CP.', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['RIFAMPICINE+ISONIAZIDE (150+75)MG CP.', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['Produit 15', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['Test Product 1', '455000.00', '455000.00', '455000.00', '455000.00', '455000.00',
                 '455000.00'], ['Produit 14', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['ACETATE DE MEDROXY PROGESTERONE 150MG/ML+S A B KIT (1+1) (DEPO-PROVERA)', '0.00', '0.00',
                 '0.00', '0.00', '0.00', '0.00'],
                ['Produit 2', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['ACT PETIT ENFANT', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['Produit 1', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['ALBENDAZOL 4% SB.', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['LEVONORGESTREL+ETHYNILESTRADIOL+FER (0.15+0.03+75)MG (MICROGYNON)', '0.00', '0.00', '0.00',
                 '0.00', '0.00', '0.00'],
                ['Produit C', '198000.00', '386400.00', '0.00', '0.00', '0.00', '0.00'],
                ['RIFAMPICINE+ISONIAZIDE+PYRAZINAMIDE (60+30+150)MG CP. DISPER', '0.00', '0.00', '0.00',
                 '0.00', '0.00', '0.00'],
                ['TEST RAPIDE HIV 1/2 (SD BIOLINE)', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'],
                ['Produit B', '336000.00', '558000.00', '0.00', '0.00', '0.00', '0.00']
            ], key=lambda x: x[0])
        )
        self.assertEqual(
            total_row,
            ['Total (CFA)', '1431500.00', '2116900.00', '455000.00', '455000.00', '455000.00', '455000.00']
        )
