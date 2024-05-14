// Função para habilitar todos os selects desabilitados
function habilitarSelects() {
    // Selecione todos os elementos select desabilitados
    var selects = document.querySelectorAll('select[disabled]');
    
    // Itere sobre os selects desabilitados
    selects.forEach(function(select) {
        // Remova o atributo disabled
        select.removeAttribute('disabled');
    });
}