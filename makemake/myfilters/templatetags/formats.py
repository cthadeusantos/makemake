from django import template

register = template.Library()

# def formata_numero(value, max_digits=13, decimal_separator='.', thousands_separator=','):
#     # Lógica de formatação mais flexível, considerando parâmetros
#     # ...
#     return formatted_value

def format_cnpj_cpf(value, max_digits=14,):
    if len(str(value)) == 11:
        return f'{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}'
    elif len(str(value)) == 14:
        return f'{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}'
    else:
        return value  # Retorna o valor original caso não tenha 11 ou 13 dígitos

register.filter('format_cnpj_cpf', format_cnpj_cpf)