// Este javascript tem o objetivo de monitorar as alterações nos selectboxes referentes a categoria
// Se o selectbox sofrer uma alteração a variavel global referente a categoria será atribuída
// Ao próximo selectbox fazendo com que o usuário precise fazer menos alterações no selectbox

// Variável global para armazenar o valor alterado
let valorSelecionadoGlobal = null; // Define qual categoria será selecionada criar um selectbox

// Adiciona o listener ao documento (ou a um elemento pai comum)
document.addEventListener('change', function(event) {
    const elemento = event.target;
    
    // Verifica se o elemento é um <select> com ID no formato "caixa-X" e exclui "meuID"
    // if (elemento.tagName === 'SELECT' && 
    //     elemento.id.startsWith('select-option-') && 
    //     elemento.id !== 'meuID') {
    if (elemento.id.startsWith('select-option-')) {    
        
        // Atualiza a variável global com o valor selecionado
        valorSelecionadoGlobal = elemento.value;
        
        // Opcional: Para depuração, você pode ver o valor atualizado no console
        console.log(`Valor selecionado na ${elemento.id}: ${valorSelecionadoGlobal}`);
    }
});