// function addForm() {
//     const formsetDiv = document.getElementById('add-form');
//     const totalForms = document.getElementById('id_form-TOTAL_FORMS');
//     const currentFormCount = formsetDiv.children.length;
//     const newFormCount = parseInt(totalForms.value);

//     // Clone the empty form
//     const newFormset = document.getElementById('inlineformset');
//     const newForm = formsetDiv.children[0].cloneNode(true);
//     newForm.innerHTML = newForm.innerHTML.replace(/form-\d+-/g, `form-${newFormCount}-`);

//     // Clear the input value
//     const inputs = newForm.getElementsByTagName('input');
//     for (let i = 0; i < inputs.length; i++) {
//         inputs[i].value = '';
//     }

//     // Append the new form
//     formsetDiv.appendChild(newForm);

//     // Update the number of total forms
//     totalForms.value = newFormCount + 1;
// }

function addForm() {
    const puthere = document.getElementById('putselecthere');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const newFormCount = parseInt(totalForms.value);

    // Clone the empty form with id 'inlineformset'
    const formsetTemplate = document.getElementById('inlineformset');
    const newForm = formsetTemplate.cloneNode(true);

    // Atualiza o id para evitar duplicidade
    newForm.setAttribute('id', `inlineformset-${newFormCount}`);

    // Atualiza os nomes e ids dos campos para corresponder ao novo formulário
    newForm.innerHTML = newForm.innerHTML.replace(/form-\d+-/g, `form-${newFormCount}-`);

    // Limpa os valores dos inputs no novo formulário
    const inputs = newForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.value = '';
        if (input.type === 'checkbox' || input.type === 'radio') {
            input.checked = false;
        }
    });

    // Remove os erros de validação no novo formulário clonado
    const errorSpans = newForm.querySelectorAll('.text-red-500');
    errorSpans.forEach(span => {
        span.innerText = '';
    });

    // Adiciona o novo formulário ao container 'putselecthere'
    puthere.appendChild(newForm);

    // Atualiza o número total de formulários
    totalForms.value = newFormCount + 1;
}
