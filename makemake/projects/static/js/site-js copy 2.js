// Função para adicionar novo formset
function addFormset(e, formsetContainer, addFormsetButton, tab, totalForms, formsetNum) {
    e.preventDefault();
    let newForm = formsetContainer[0].cloneNode(true),
        formRegex = RegExp(`form-(\\d){1}-`, 'g');
    formsetNum++;
    newForm.innerHTML = newForm.innerHTML.replace(
        formRegex,
        `form-${formsetNum}-`
    );
    newForm.innerHTML = newForm.innerHTML.replace(
        "disabled=\"\"",
        ""
    );
    tab.insertBefore(newForm, addFormsetButton); // Ponto principal de inserção
    totalForms.setAttribute(
        'value',
        `${formsetContainer.length}`
    );
}

// Novos buildings
const formsetContainerBuilding = document.querySelectorAll('#id-building-selector'),
    formBuilding = document.querySelector('#form'),
    addFormsetButtonBuilding = document.querySelector('#add-formset1'),
    totalFormsBuilding = document.querySelector('#id_form-TOTAL_FORMS'),
    tab1 = document.querySelector('#tab1'),
    formsetNumBuilding = formsetContainerBuilding.length - 1;

addFormsetButtonBuilding.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerBuilding, addFormsetButtonBuilding, tab1, totalFormsBuilding, formsetNumBuilding)
);

// Novos members
const formsetContainerMember = document.querySelectorAll('#id-member-selector'),
    addFormsetButtonMember = document.querySelector('#add-formset2'),
    tab2 = document.querySelector('#tab2'),
    totalFormsMember = document.querySelector('#id_form-TOTAL_FORMS'),
    formsetNumMember = formsetContainerMember.length - 1;

addFormsetButtonMember.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerMember, addFormsetButtonMember, tab2, totalFormsMember, formsetNumMember)
);

// Novos stakeholders
const formsetContainerStakeholder = document.querySelectorAll('#id-stakeholder-selector'),
    addFormsetButtonStakeholder = document.querySelector('#add-formset3'),
    tab3 = document.querySelector('#tab3'),
    totalFormsStakeholder = document.querySelector('#id_form-TOTAL_FORMS'),
    formsetNumStakeholder = formsetContainerStakeholder.length - 1;

addFormsetButtonStakeholder.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerStakeholder, addFormsetButtonStakeholder, tab3, totalFormsStakeholder, formsetNumStakeholder)
);
