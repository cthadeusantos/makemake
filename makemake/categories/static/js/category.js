
/*
The code below will added new elements at homepage
Can update too!
*/

function addFormSetCategory() {
    const formsetContainer = document.getElementById('formset-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');

    // Selecionar todos os elementos cujo ID segue o padrão 'form-INPUT-X'
    const formInputs = document.querySelectorAll('[id^="form-INPUT-"]');
    
    // Inicializar o maior índice
    let maxIndex = -1;

    // Iterar pelos IDs dos formulários e encontrar o maior índice X
    formInputs.forEach(function(input) {
        const match = input.id.match(/form-INPUT-(\d+)/);
        if (match && match[1]) {
            const currentIndex = parseInt(match[1]);
            if (currentIndex > maxIndex) {
                maxIndex = currentIndex;
            }
        }
    });

    // O próximo índice será o maior X + 1
    const newIndex = maxIndex + 1;

    // Clonar o último formulário (ou qualquer outro) 
    const newForm = formsetContainer.children[(formInputs.length - 1)].cloneNode(true);

    // Regex para encontrar 'form-INPUT-X' e 'formset-X'
    const regexInput = /form-INPUT-\d+/g;
    const regexFormset = /formset-\d+/g;

    // Substituir a ocorrência no atributo 'name' e 'id' de cada campo
    newForm.innerHTML = newForm.innerHTML.replace(regexInput, `form-INPUT-${newIndex}`);
    newForm.innerHTML = newForm.innerHTML.replace(regexFormset, `formset-${newIndex}`);

    // Limpar os valores dos campos de entrada
    const inputs = newForm.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].type !== 'hidden') {  // Não limpar campos hidden
            inputs[i].value = '';
        }
    }

    // Adicionar o novo formulário ao contêiner
    formsetContainer.appendChild(newForm);

    // Atualizar o número total de formulários
    totalForms.value = newIndex + 1; // Aumenta o total de formulários
    document.getElementById('id_form-TOTAL_FORMS').value = totalForms.value;
}

/*
The code below will delete elements at homepage
*/
function removeFormSet(index) {
    // Seleciona todos os elementos que possuem IDs que correspondem ao padrão 'form-INPUT-X'
    const formItems = document.querySelectorAll('[id^="form-INPUT-"]');

    // Se houver mais de um formulário, permita a remoção
    if (formItems.length > 1) {
        const formsetItem = document.getElementById('formset-' + index);
        if (formsetItem) {
            formsetItem.remove();  // Remove o container que inclui o select e o botão
        }
    } else {
        alert("Você deve ter pelo menos um formulário!");
    }
}
