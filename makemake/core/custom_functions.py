import re

def left_pad(number=0, digits=4, char='0'):
    assert (number >= 0), "Sorry, no numbers below zero"
    assert (len(str(number)) <= digits), ' '.join(("Sorry, number of digits exceeds", str(digits), "."))
    assert (len(char) < 2), "Sorry, number of characters exceeds 1."
    string = char * digits
    number = str(number)
    stop = digits - len(number)
    return ''.join((string[:stop], number))

def get_text_choices(value, choices):
    for key, text in choices:
        if key == value:
            return text
    return ''

"""
Extrai o nome do arquivo da string informada
"""
def extract_filename(url):
    return url.split('/')[-1]

"""
Verifica se é uma lista vazia
"""
def is_list_empty(lista):
    return not bool(lista)
"""
Divide as palavras de uma string de acordo com & e |, mantendo o espaço no início e no fim das palavras se existir
"""
def separar_valores_com_espaco(string):
    # Verifica se a string contém '&' ou '|'
    if '&' in string and '|' in string:
        # Caso existam ambos, separamos por '&'
        lista1 = re.findall(r'[^&|]+(?=&)', string)
        lista2 = re.findall(r'[^&|]+(?=\|)', string)
    elif '&' in string:
        # Se existirem apenas '&', separamos por '&'
        lista1 = re.findall(r'[^&]+', string)
        lista2 = []
    elif '|' in string:
        # Se existirem apenas '|', separamos por '|'
        lista1 = []
        lista2 = re.findall(r'[^|]+', string)
    else:
        # Se não houver '&' ou '|', retornamos listas vazias
        lista1 = []
        lista2 = []
    
    return lista1, lista2

"""
Divide as palavras de uma string de acordo com & e |, remove espaços do início e fim das palavras
"""
# def separar_valores_sem_espaco(string):
#     # Verifica se a string contém '&' ou '|'
#     if '&' in string and '|' in string:
#         # Caso existam ambos, separamos por '&'
#         lista1 = [valor.strip() for valor in re.findall(r'[^&|]+(?=&)', string)]
#         lista2 = [valor.strip() for valor in re.findall(r'[^&|]+(?=\|)', string)]
#     elif '&' in string:
#         # Se existirem apenas '&', separamos por '&'
#         lista1 = [valor.strip() for valor in re.findall(r'[^&]+', string)]
#         lista2 = []
#     elif '|' in string:
#         # Se existirem apenas '|', separamos por '|'
#         lista1 = []
#         lista2 = [valor.strip() for valor in re.findall(r'[^|]+', string)]
#     elif ' ' in string:
#         lista1 = string.split(' ')
#         lista2 = []
#     else:
#         # Se não houver '&' ou '|', retornamos listas vazias
#         #lista1 = string.split(' ')
#         lista1 = []
#         lista2 = []
    
#     return lista1, lista2

def separar_valores_sem_espaco(string):
    # Remove dois ou mais espaços consecutivos da string
    string = re.sub(r'\s{2,}', ' ', string).strip()
    
    # Verifica se a string contém '&' ou '|'
    if '&' in string and '|' in string:
        # Caso existam ambos, separamos por '&'
        lista1 = [valor.strip() for valor in re.findall(r'[^&|]+(?=&)', string)]
        lista2 = [valor.strip() for valor in re.findall(r'[^&|]+(?=\|)', string)]
    elif '&' in string:
        # Se existirem apenas '&', separamos por '&'
        lista1 = [valor.strip() for valor in re.findall(r'[^&]+', string)]
        lista2 = []
    elif '|' in string:
        # Se existirem apenas '|', separamos por '|'
        lista1 = []
        lista2 = [valor.strip() for valor in re.findall(r'[^|]+', string)]
    elif ' ' in string:
        # Se existirem espaços, separamos por espaços ignorando múltiplos espaços
        lista1 = [valor for valor in string.split(' ') if valor.strip()]
        lista2 = []
    elif string != '':
        lista1 = [valor for valor in string.split(' ') if valor.strip()]
        lista2 = []
    else:
        # Se não houver '&' ou '|', retornamos listas vazias
        lista1 = []
        lista2 = []

    return lista1, lista2

"""
Valida CNPJ e CPF
"""
def valida_cnpj_cpf(numero):
    # Remover caracteres não numéricos
    numero = ''.join(filter(str.isdigit, numero))
    
    # Verificar se o número tem 14 dígitos (CNPJ)
    if len(numero) == 14:
        cnpj = numero
        # Validar CNPJ
        if valida_cnpj(cnpj):
            return "CNPJ válido: " + cnpj
        else:
            return "CNPJ inválido"
    # Verificar se o número tem 11 dígitos (CPF)
    elif len(numero) == 11:
        cpf = numero
        # Validar CPF
        if valida_cpf(cpf):
            return "CPF válido: " + cpf
        else:
            return "CPF inválido"
    # Caso contrário, não é um CNPJ nem um CPF válido
    else:
        return "Número não tem 11 ou 14 dígitos, não é CNPJ nem CPF válido"

"""
Checa CNPJ
"""
def valida_cnpj(cnpj):
    # Algoritmo de validação de CNPJ
    multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    cnpj = [int(c) for c in cnpj]
    # Verifica o primeiro dígito verificador
    soma = sum(a * b for a, b in zip(cnpj[:12], multiplicadores_1))
    resto = soma % 11
    digito_verificador_1 = 0 if resto < 2 else 11 - resto
    if digito_verificador_1 != cnpj[12]:
        return False
    # Verifica o segundo dígito verificador
    soma = sum(a * b for a, b in zip(cnpj[:13], multiplicadores_2))
    resto = soma % 11
    digito_verificador_2 = 0 if resto < 2 else 11 - resto
    if digito_verificador_2 != cnpj[13]:
        return False
    return True

"""
Checa CPF
"""
def valida_cpf(cpf):
    # Algoritmo de validação de CPF
    if len(set(cpf)) == 1:
        return False
    cpf = [int(d) for d in cpf]
    soma = sum(a * b for a, b in zip(cpf[:9], range(10, 1, -1)))
    digito_verificador_1 = 11 - (soma % 11)
    digito_verificador_1 = digito_verificador_1 if digito_verificador_1 < 10 else 0
    if digito_verificador_1 != cpf[9]:
        return False
    soma = sum(a * b for a, b in zip(cpf[:10], range(11, 1, -1)))
    digito_verificador_2 = 11 - (soma % 11)
    digito_verificador_2 = digito_verificador_2 if digito_verificador_2 < 10 else 0
    if digito_verificador_2 != cpf[10]:
        return False
    return True

