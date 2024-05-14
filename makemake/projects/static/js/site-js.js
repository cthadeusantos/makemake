var selectCounterSite = 0;  // Inicializa um contador para IDs únicos
var selectCounterMember = 0;  // Inicializa um contador para IDs únicos
var selectCounterStakeholder = 0;  // Inicializa um contador para IDs únicos


async function fetchData(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
            } else {
                reject('Erro ao obter dados');
            }
        };

        xhr.onerror = function () {
            reject('Erro ao fazer a requisição');
        };

        xhr.send();
    });
}


async function addSelectMember() {
    try {
        var data = await fetchData("/projects/get-select-users/");
        //var selectCounterSite = 0;

        // Incrementa o contador para criar IDs únicos
        selectCounterMember++;

        // Criar um novo select com ID único
        var selectHtml = '<p><select name="dynamic_selects_members_' + selectCounterMember + '" class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">';
        for (var i = 0; i < data.options.length; i++) {
            selectHtml += '<option value="' + data.options[i].value + '">' + data.options[i].label + '</option>';
        }
        selectHtml += '</select></p>';

        // Adicionar ao contêiner
        document.getElementById('select-container-member').insertAdjacentHTML('beforeend', selectHtml);

        // Desabilita botão submit
        var sendFormButton = document.getElementById('send-form');
        sendFormButton.disabled = false;
    } catch (error) {
        console.log('Erro ao obter opções do select', error);
    }
}

async function addSelectStakeholder() {
    try {
        var data = await fetchData("/projects/get-select-users/");
        //var selectCounterSite = 0;

        // Incrementa o contador para criar IDs únicos
        selectCounterStakeholder++;

        // Criar um novo select com ID único
        var selectHtml = '<p><select name="dynamic_selects_stakeholders_' + selectCounterStakeholder + '" class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">';
        for (var i = 0; i < data.options.length; i++) {
            selectHtml += '<option value="' + data.options[i].value + '">' + data.options[i].label + '</option>';
        }
        selectHtml += '</select></p>';

        // Adicionar ao contêiner
        document.getElementById('select-container-stakeholder').insertAdjacentHTML('beforeend', selectHtml);

        // Desabilita botão submit
        var sendFormButton = document.getElementById('send-form');
        sendFormButton.disabled = false;
    } catch (error) {
        console.log('Erro ao obter opções do select', error);
    }
}

// Função para adicionar novo formset
function addFormset(e, formsetContainer, addFormsetButton, tab, totalForms, formsetNum, type) {
    e.preventDefault();

    // Verificar se formsetContainer[0] não contém elementos úteis
    if (formsetContainer[0].childElementCount === 0) {
        // Faça alguma coisa aqui, como retornar ou lançar um erro
        switch (type) {
            case 'building':
                
                break;
            case 'member':
                // Chame a função quando o DOM estiver carregado
                addSelectMember();
                break;
            case 'stakeholder':
                addSelectStakeholder();
                break;
            default:
                break;
        }
        return;
    }

    //Se formsetContainer[0] contém elementos úteis
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


