import sys, os
from flask_restful import Resource, reqparse
from flask import render_template, make_response
from weasyprint import HTML

class GeneratePdf(Resource):
    def get(self):
        #html_string = render_template('your_template.html', data=your_data)
        try:
            html_string = """
            <html>
            <body>
                <h1>Hola, Mundo!</h1>
                <p>Este es un PDF generado desde HTML con WeasyPrint.</p>
            </body>
            </html>
            """
            pdf = HTML(string=html_string).write_pdf()
            
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=documento.pdf'
            return response
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
                return {'mensaje': str(msj) }, 500