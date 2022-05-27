import os
import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as DjangoUserModel
from django.conf import settings
from django.db import connection


def get_report_month_year(request):
    try:
        req_date = request.GET['report_date']
    except KeyError:
        req_date = None

    if not req_date:
        req_month, req_year = datetime.datetime.now().strftime("%m-%Y").split("-")
    else:
        req_year, req_month, _ = req_date.split("-")

    if req_month[0] == "0":
        req_month = req_month[1]

    return req_month, req_year


class Reports(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        report_id = kwargs['report_id']
        return getattr(self, "report_%d" % (report_id))(request)

    def report_1(self, request):
        req_month, req_year = get_report_month_year(request)
        sql = self.get_sql_report(1)
        r = self.execute_query(sql, (req_month, req_year, ))
        return render(request, "report_1.html", {'count': 0 if not r else r['count']})

    def report_2(self, request):
        sql = self.get_sql_report(2)
        result = self.execute_query(sql, one_row=False)
        return render(request, "report_2.html", {
            'results': [
                (item['operation_name'], item['active_count'], )
                for item in result
            ]
        })

    def report_3(self, request):
        sql = self.get_sql_report(3)
        results = self.execute_query(sql, one_row=False)
        return render(request, "report_3.html", {'results': results})

    def report_4(self, request):
        sql = self.get_sql_report(4)
        results = self.execute_query(sql, one_row=False)
        return render(request, "report_4.html", {'results': results})

    def report_5(self, request):
        req_month, req_year = get_report_month_year(request)
        sql = self.get_sql_report(5)
        results = self.execute_query(sql, (req_month, req_year, ), one_row=False)
        return render(request, "report_5.html", {'results': results})

    @staticmethod
    def execute_query(sql, args=(), one_row=True):
        cursor = connection.cursor()
        cursor.execute(sql, args)

        results = [dict(
            zip(
                [d[0] for d in cursor.description],
                row
            )
        ) for row in cursor.fetchall()]

        cursor.close()
        return None if not results else results[0] if one_row else results

    @staticmethod
    def get_sql_report(report_id):
        sql_path = os.path.join(settings.BASE_DIR, "sql_reports", "report_%d.sql" % (report_id, ))
        with open(sql_path) as f:
            sql = f.read()
            return sql.strip()
