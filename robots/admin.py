from django.contrib import admin
from django.http import HttpResponse
import xlsxwriter
from datetime import datetime, timedelta

from robots.models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('model', 'version', 'created')
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):

        one_week_ago = datetime.now() - timedelta(days=7)

        queryset = queryset.filter(created__gte=one_week_ago)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})

        self.create_excel_sheet(workbook, queryset, 'R2', 'R2_robots', ['Модель', 'Версия', 'Количество'])
        self.create_excel_sheet(workbook, queryset, '13', '13_robots', ['Модель', 'Версия', 'Количество'])
        self.create_excel_sheet(workbook, queryset, 'X5', 'X5_robots', ['Модель', 'Версия', 'Количество'])

        workbook.close()
        return response

    def create_excel_sheet(self, workbook, queryset, model, sheet_name, headers):
        worksheet = workbook.add_worksheet(sheet_name)

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        model_queryset = queryset.filter(model=model)
        versions = model_queryset.values_list('version', flat=True).distinct()

        row_num = 1
        versions_dict = {}

        for version in versions:
            count = model_queryset.filter(version=version).count()

            if version not in versions_dict:
                versions_dict[version] = True

                worksheet.write(row_num, 0, model)
                worksheet.write(row_num, 1, version)
                worksheet.write(row_num, 2, count)

                row_num += 1

    export_to_excel.short_description = 'Export to Excel'

