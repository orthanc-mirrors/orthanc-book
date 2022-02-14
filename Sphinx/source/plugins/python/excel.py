import StringIO
import json
import orthanc
import xlwt

def CreateExcelReport(output, uri, **request):
    if request['method'] != 'GET' :
        output.SendMethodNotAllowed('GET')
    else:
        # Create an Excel writer
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('Studies')

        # Loop over the studies stored in Orthanc
        row = 0
        studies = orthanc.RestApiGet('/studies?expand')
        for study in json.loads(studies):
            sheet.write(row, 0, study['PatientMainDicomTags'].get('PatientID'))
            sheet.write(row, 1, study['PatientMainDicomTags'].get('PatientName'))
            sheet.write(row, 2, study['MainDicomTags'].get('StudyDescription'))
            row += 1

        # Serialize the Excel workbook to a string, and return it to the caller
        # https://stackoverflow.com/a/15649139/881731
        b = StringIO.StringIO()
        excel.save(b)
        output.AnswerBuffer(b.getvalue(), 'application/vnd.ms-excel')

orthanc.RegisterRestCallback('/report.xls', CreateExcelReport)
