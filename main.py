from flask import Flask, render_template, request, send_file, jsonify
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
from flask_cors import CORS

#app = Flask(__name__)
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

class PDF(FPDF):
    #Conversão dos meses para extenso
    meses = {'01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
             '04': 'Abril', '05': 'Maio', '06': 'Junho',
             '07': 'Julho', '08': 'Agosto', '09': 'Setembro',
             '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'}
    
    def __init__(self, dados):
        super().__init__('P', 'mm', 'A5')
        self.dados = dados

    #Printa as informações do médico e paciente
    def header(self):
        self.image('oxemed.png', 10, 8, 60)

        self.set_y(14)
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 0, self.dados["medico"]["nome"], align='R')

        self.set_y(19)
        self.set_font('helvetica', '', 10)
        self.cell(0, 0, self.dados["medico"]["crm"], align='R')

        self.ln(20)

        self.set_font('helvetica', 'B', 14)
        self.cell(0,0, self.dados["paciente"], align='C')
        self.ln(15)
    
    #Printa os itens presentes no receituário
    def adicionar_receituario(self):
        self.set_font('courier', '', 14)
        for item in self.dados["receituario"]:
            self.multi_cell(0, 5, f'{item}\n', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    #Printa a data de emissão do receituário e a imagem do OxeMed
    def footer(self):
        self.image('oxemed_bg.png', -8, 78, 165)
        
        data = datetime.now()
        formatData = f"{data.strftime('%d')} de {self.meses[data.strftime('%m')]} de {data.strftime('%Y')}"

        self.set_y(-15)
        self.set_x(-30)
        self.set_font('helvetica', '', 10)
        self.cell(0, 0, formatData, align='R')
        
@app.route('/rota2')
def imprimir():
    return jsonify({"Olá": "Mundo"})

@app.route('/receituario', methods=['POST'])
def gerar_pdf():
    # Obter os dados do formulário
    data = request.get_json()
    print(data)

    if data is None:
        return jsonify({"error": "No JSON data received"}), 400 

    # Criar PDF com os dados
    form = PDF(data)
    form.set_auto_page_break(auto=True, margin=35)
    form.add_page()

    form.set_font('courier', '', 14)

    form.adicionar_receituario()

    # Salvar PDF temporariamente
    pdf_temp = 'temp.pdf'
    form.output(pdf_temp)

    filename = '_'.join(data['paciente'].split(' '))

    # Enviar o arquivo PDF como resposta
    return send_file(pdf_temp, as_attachment=True, attachment_filename=f'{filename}.pdf')
    #form.output('receituario_1.pdf')
#return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
