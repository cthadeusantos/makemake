// Função para adicionar novo formset
function addFormset(e, formsetContainer, addFormsetButton, tab, totalForms, formsetNum, type) {
    e.preventDefault();
    let newForm = formsetContainer[0].cloneNode(true),
        formRegex = RegExp(`form-(\\d){1}-`, 'g');
    formsetNum++;
    newForm.innerHTML = newForm.innerHTML.replace(
        formRegex,
        `form-${formsetNum}-`
    );

    //Remove all disabled attributes:
    newForm.innerHTML = removerDisabled(newForm.innerHTML);

    //Remove all disabled attributes:
    newForm.innerHTML = removerHidden(newForm.innerHTML);
    
    tab.insertBefore(newForm, addFormsetButton); // Ponto principal de inserção
    totalForms.setAttribute(
        'value',
        `${formsetContainer.length}`
    );

    // Atribuir formsetNum à variável correspondente com base no tipo de formset
    switch (type) {
        case 'building':
            formsetNumBuilding = formsetNum;
            break;
        case 'member':
            formsetNumMember = formsetNum;
            break;
        case 'stakeholder':
            formsetNumStakeholder = formsetNum;
            break;
        default:
            break;
    }
}

// Novos buildings
let formsetContainerBuilding = document.querySelectorAll('#id-building-selector'),
    formBuilding = document.querySelector('#form'),
    addFormsetButtonBuilding = document.querySelector('#add-formset1'),
    totalFormsBuilding = document.querySelector('#id_form-TOTAL_FORMS'),
    tab2 = document.querySelector('#tab2'),
    formsetNumBuilding = formsetContainerBuilding.length - 1;

addFormsetButtonBuilding.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerBuilding, addFormsetButtonBuilding, tab2, totalFormsBuilding, formsetNumBuilding, 'building')
);

// Novos members
let formsetContainerMember = document.querySelectorAll('#id-member-selector'),
    addFormsetButtonMember = document.querySelector('#add-formset2'),
    tab3 = document.querySelector('#tab3'),
    totalFormsMember = document.querySelector('#id_form-TOTAL_FORMS'),
    formsetNumMember = formsetContainerMember.length - 1;

addFormsetButtonMember.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerMember, addFormsetButtonMember, tab3, totalFormsMember, formsetNumMember, 'member')
);

// Novos stakeholders
let formsetContainerStakeholder = document.querySelectorAll('#id-stakeholder-selector'),
    addFormsetButtonStakeholder = document.querySelector('#add-formset3'),
    tab4 = document.querySelector('#tab4'),
    totalFormsStakeholder = document.querySelector('#id_form-TOTAL_FORMS'),
    formsetNumStakeholder = formsetContainerStakeholder.length - 1;

addFormsetButtonStakeholder.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerStakeholder, addFormsetButtonStakeholder, tab4, totalFormsStakeholder, formsetNumStakeholder, 'stakeholder')
);

// Remove formset 
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('remove-formset')) {
        e.preventDefault();
        e.target.parentElement.remove();
    }
});


// Função para remover todos os atributos 'disabled' de um elemento HTML
function removerDisabled(htmlString) {
    return htmlString.replace(/disabled=""/g, '');
}

// Função para remover todos os atributos 'disabled' de um elemento HTML
function removerHidden(htmlString) {
    return htmlString.replace(/hidden=""/g, '');
}


