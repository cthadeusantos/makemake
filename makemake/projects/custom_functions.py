import re
from auditlog.models import LogEntry

# Funcao ainda inacabada
def log_m2m_changes(instance, items, action, user=None):
    """
    Função de callback para registrar alterações no campo ManyToMany.

    Parâmetros:
    - instance: a instância do modelo principal (ex.: Project).
    - field_name: nome do campo ManyToMany modificado.
    - items: IDs das instâncias adicionadas/removidas.
    - action: a ação executada (post_add, post_remove, post_clear).
    """

    # Mapeamento correto das ações para os valores do auditlog
    action_map = {
        "post_add": 0,   
        "post_update": 1, 
        "post_remove": 2, 
        "post_clear": 3,  
    }

    #if field_name:
    if action == action_map["post_add"]:
        # Registrar a adição de itens
        changes = {}
        for field_name in items:
            counter = 1
            for valor in items[field_name]:
                chave = f'{field_name}{counter}'
                changes[chave] = [None, str(valor)]
                counter += 1
        LogEntry.objects.log_create(
                    instance=instance,
                    action=action,
                    changes=changes,
                    actor=user,
                )
    elif action == action_map["post_remove"]:
        changes = {}
        for item in items:
            counter = 1
            for item in items:
                chave = f'{field_name}{counter}'
                changes[chave] = [None, str(item)]
                counter += 1
        # Registrar a remoção de itens
        # for item in items:
        #     LogEntry.objects.log_create(
        #         instance=instance,
        #         action=LogEntry.Action.DELETE,
        #         changes={'field': field_name, 'new': f'Removed {model.__name__} with ID {pk}'}
        #     )
        LogEntry.objects.log_create(
            instance=instance,
            action=action,
            changes=changes
        )
            
    # elif action == "post_clear":
    #     # Registrar a limpeza de todos os itens
    #     LogEntry.objects.log_create(
    #         instance=instance,
    #         action=LogEntry.Action.DELETE,
    #         changes={'field': field_name, 'new': 'All items cleared'}
    #     )

"""
Deprecated
"""
# def filter_dynamic_keys(prefix, category, model, request, dict_auxiliary):
#     # dinamic_keys are elements starts with (prefix) in request.POST
#     dynamic_keys = [
#         key for key in request.POST.keys()
#         if re.match(rf'{prefix}_\d+', key)
#     ]
#     keys = set()    # Stores the value obtained from POST in the keys variable
#     for key in dynamic_keys:    # Iterates through the filtered keys
#         value = request.POST.get(key)
#         if value and value not in keys: # Avoid the possibility of save repeated values
#             keys.add(value)
#             dict_auxiliary[category].append(model.objects.get(pk=value))

# def filter_dynamic_keys(prefixes, category, model, request, dict_auxiliary):
#     """
#     Captura e processa chaves dinâmicas no request.POST com base nos prefixos fornecidos.
    
#     :param prefixes: Lista de prefixos a serem filtrados (ex: ["dynamic_selects", "form-X"])
#     :param category: Categoria correspondente no dicionário auxiliar
#     :param model: Modelo Django para buscar os objetos correspondentes
#     :param request: Objeto request contendo os dados POST
#     :param dict_auxiliary: Dicionário onde os objetos filtrados serão armazenados
#     """
#     # Construir um padrão regex que capture os diferentes prefixos fornecidos
#     pattern = re.compile(rf'({"|".join(prefixes)})_(?:\d+)(?:_[a-zA-Z]+)?$')

#     dynamic_keys = [
#         key for key in request.POST.keys()
#         if pattern.match(key)
#     ]

#     keys = set()  # Para evitar valores duplicados
#     for key in dynamic_keys:
#         value = request.POST.get(key)
#         if value and value not in keys:
#             keys.add(value)
#             dict_auxiliary[category].append(model.objects.get(pk=value))

def filter_dynamic_keys(pattern, category, model, request, dict_auxiliary):
    """
    Captura e processa chaves dinâmicas no request.POST com base no padrão fornecido.

    :param pattern: Expressão regular para capturar as chaves desejadas
    :param category: Categoria correspondente no dicionário auxiliar
    :param model: Modelo Django para buscar os objetos correspondentes
    :param request: Objeto request contendo os dados POST
    :param dict_auxiliary: Dicionário onde os objetos filtrados serão armazenados
    """
    dynamic_keys = [
        key for key in request.POST.keys()
        if re.match(pattern, key)
    ]

    keys = set()  # Para evitar valores duplicados
    for key in dynamic_keys:
        value = request.POST.get(key)
        if value and value not in keys:
            keys.add(value)
            dict_auxiliary[category].append(model.objects.get(pk=value))

def save_m2m_relationships(instance, m2m_fields, user=None):
    if m2m_fields:
        log_m2m_changes(instance, m2m_fields, LogEntry.Action.CREATE, user)
        for field, items in m2m_fields.items():
            getattr(instance, field).add(*items)
