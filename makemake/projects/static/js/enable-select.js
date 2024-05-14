// Função para habilitar todos os selects com base no padrão do ID e do nome
function habilitarSelects() {
    // Seleciona todos os elementos que têm um ID começando com "id_form-" e um nome começando com "form-"
    var selects = document.querySelectorAll('[id^="id_form-"][name^="form-"]');
    
    // Itera sobre os selects encontrados
    for (var i = 0; i < selects.length; i++) {
        // Habilita o select atual
        selects[i].removeAttribute('disabled');
    }
}