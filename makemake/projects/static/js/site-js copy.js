// Novos buildings
let formsetContainerBuilding = document.querySelectorAll(
    '#id-building-selector'
    ),
    formBuilding = document.querySelector('#form'),
    addFormsetButtonBuilding = document.querySelector(
    '#add-formset1'
    ),
    totalFormsBuilding = document.querySelector(
    '#id_form-TOTAL_FORMS'
    ),
    formsetNumBuilding = formsetContainerBuilding.length - 1;

addFormsetButtonBuilding.addEventListener(
    'click', 
    $addFormsetBuilding
    );

// Adiciona novo usuario(member) 
// tab1
function $addFormsetBuilding(e) {
    e.preventDefault();
    let newForm = formsetContainerBuilding[0].cloneNode(true),
    formRegex = RegExp(`form-(\\d){1}-`,'g');
    formsetNum++
    newForm.innerHTML = newForm.innerHTML.replace(
    formRegex, 
    'form-${formsetNum}-'
    );
    newForm.innerHTML = newForm.innerHTML.replace(
        "disabled=\"\"", 
        ''
        );
    tab1.insertBefore(newForm, addFormsetButtonBuilding); // Principal ponto para inserir
    totalForms.setAttribute(
    'value', 
    '${formsetNumBuilding + 1}'
    );
    }

// Novos members
let formsetContainerMember = document.querySelectorAll(
    '#id-member-selector'
    ),
    form = document.querySelector('#form'),
    addFormsetButtonMember = document.querySelector(
    '#add-formset2'
    ),
    totalForms = document.querySelector(
    '#id_form-TOTAL_FORMS'
    ),
    formsetNum = formsetContainerMember.length - 1;

addFormsetButtonMember.addEventListener(
    'click', 
    $addFormsetMember
    );

// Adiciona novo usuario(member) 
// tab2
function $addFormsetMember(e) {
    e.preventDefault();
    let newForm = formsetContainerMember[0].cloneNode(true),
    formRegex = RegExp(`form-(\\d){1}-`,'g');
    formsetNum++
    newForm.innerHTML = newForm.innerHTML.replace(
    formRegex, 
    'form-${formsetNum}-'
    );
    newForm.innerHTML = newForm.innerHTML.replace(
        "disabled=\"\"", 
        ''
        );
    tab2.insertBefore(newForm, addFormsetButtonMember); // Principal ponto para inserir
    totalForms.setAttribute(
    'value', 
    '${formsetNum + 1}'
    );
    }

    // Novos stakeholders
    let formsetContainerStakeholder = document.querySelectorAll(
        '#id-stakeholder-selector'
        ),
        formStakeholder = document.querySelector('#form'),
        addFormsetButtonStakeholder = document.querySelector(
        '#add-formset3'
        ),
        totalFormsStakeholder = document.querySelector(
        '#id_form-TOTAL_FORMS'
        ),
        formsetNumStakeholder = formsetContainerStakeholder.length - 1;
    
    addFormsetButtonStakeholder.addEventListener(
        'click', 
        $addFormsetStakeholder
        );
    
    // Adiciona novo usuario(member) 
    // tab2
    function $addFormsetStakeholder(e) {
        e.preventDefault();
        let newForm = formsetContainerStakeholder[0].cloneNode(true),
        formRegex = RegExp(`form-(\\d){1}-`,'g');
        formsetNumStakeholder++
        newForm.innerHTML = newForm.innerHTML.replace(
        formRegex, 
        'form-${formsetNumStakeholder}-'
        );
        newForm.innerHTML = newForm.innerHTML.replace(
            "disabled=\"\"", 
            ''
            );
        tab3.insertBefore(newForm, addFormsetButtonStakeholder); // Principal ponto para inserir
        totalFormsStakeholder.setAttribute(
        'value', 
        '${formsetNumStakeholder + 1}'
        );
        }