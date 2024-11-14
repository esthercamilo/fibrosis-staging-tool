import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import pdfplumber
import re
from django.db import IntegrityError
from api.models import Skill
from core.settings import BASE_DIR


def extract_code_and_text_EM(file_path):
    data = []

    # Expressão regular para capturar o código e o texto
    pattern = re.compile( r'(EM\d{2}[A-Z]{2,3}\d{3})(.*?)(?=EM\d{2}[A-Z]{2,3}\d{3}|\Z)', re.DOTALL)

    # Abrir o PDF
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                # Procurar todas as correspondências no texto da página
                matches = pattern.findall(text)

                for match in matches:
                    code = match[0].strip()
                    description = " ".join(match[1].split()).strip()
                    data.append((code, description))

                    try:
                        skill = Skill(code=code, description=description)
                        skill.save()
                        print(f"Skill {code} salvo com sucesso!")
                    except IntegrityError as e:
                        print(f"Erro ao salvar {code}: {str(e)}")

    return data


if __name__ == '__main__':
    # Exemplo de uso
    # file_path = r'C:\scripts\BNCC.pdf'
    file_path = os.path.join(BASE_DIR,  'data', 'BNCC_EI_EF_110518_versaofinal.pdf')
    extracted_data = extract_code_and_text_EM(file_path)

    # Exibindo os códigos e descrições extraídas
    for code, description in extracted_data:
        print(f"Código: {code}")
        print(f"Descrição: {description}")
        print("-" * 50)