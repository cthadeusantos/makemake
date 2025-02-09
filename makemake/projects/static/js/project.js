var selectCounterSite = 0;  // Inicializa um contador para IDs únicos
var selectCounterMember = 0;  // Inicializa um contador para IDs únicos
var selectCounterStakeholder = 0;  // Inicializa um contador para IDs únicos
var selectCounterAuthSubmit = 0;  // Inicializa um contador para IDs únicos - ativa ou desativa o botão submit na página

// A SER USADO FUTURAMENTE
//const plusString = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
//  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
//</svg>`;

//const minusString = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
//  <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14" />
//</svg>
//`;

// Main JS Code

// Seleciona todos os elementos <select> na página
const selects = document.querySelectorAll('select');
    
// Verifica se existem elementos com o padrão de name esperado
selects.forEach((select) => {
    const name = select.getAttribute('name');
    
    // Verifica se o name corresponde ao padrão "form-X-building"
    if (/^form-\d+-building$/.test(name)) {
    selectCounterAuthSubmit = 1;  // Inicializa um contador para IDs únicos
    var sendFormButton = document.getElementById('send-form');
    sendFormButton.disabled = false;
    }
});

// JS - jquery auxiliaries functions

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

// Apaga os campos HTML select building quando houver mais de um
document.addEventListener('DOMContentLoaded', function () {
    var previousValue = document.getElementById('id_site').value;  // Valor inicial do select
    var selectElement = document.getElementById('id_site');
    var addSelectButton = document.getElementById('add-select');
    var sendFormButton = document.getElementById('send-form');
    var selectContainer = document.getElementById('select-container');

    if (selectElement) {
        // Adicione um ouvinte de eventos para a mudança no valor do select
        selectElement.addEventListener('change', function () {

            // Lógica a ser executada quando o select for alterado
            console.log('Select alterado! Novo valor:', selectElement.value);

            // Verificar se o valor do select é vazio
            if (selectElement.value === '') {
                // Limpar os selects se a string for vazia
                while (selectContainer.firstChild) {
                    selectContainer.removeChild(selectContainer.firstChild);
                }

                // Se vazio, desativar o botão
                addSelectButton.disabled = true;

                // Desabilita botão submit
                sendFormButton.disabled = true;

            } else {
                selectElement.addEventListener('change', function () {
                    var currentValue = this.value;  // Valor atual do select após a mudança

                    // Comparar o valor anterior com o valor atual
                    if (currentValue !== previousValue) {
                        // A mudança ocorreu
                        console.log('O select teve uma mudança. Valor anterior:', previousValue, 'Novo valor:', currentValue);

                        // Faça algo aqui após a mudança no select

                        // Limpar os selects se a string for vazia
                        while (selectContainer.firstChild) {
                            selectContainer.removeChild(selectContainer.firstChild);
                        }

                        // Desabilita botão submit
                        sendFormButton.disabled = true;

                        // Atualizar o valor anterior para o valor atual
                        previousValue = currentValue;
                    } else {
                        // Nenhuma mudança ocorreu
                        console.log('O select não teve mudanças.');
                    }
                });

                // Se não vazio, ativar o botão
                //addSelectButton.disabled = false;
                addSelectButton && (addSelectButton.disabled = false);

                // Ativar o botão após o primeiro select ser adicionado
                //addSelectButton.removeAttribute('disabled');
            }
        });
    }
});

//
// Adiciona novos membros
//
// Função async para lidar com a lógica
async function addSelectMember() {
    try {
        // Busca os dados do servidor usando fetch
        var response = await fetch("/projects/get-select-users/");
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.statusText);
        }

        var data = await response.json();

        // Incrementa o contador para criar IDs únicos
        if (typeof selectCounterMember === 'undefined') {
            window.selectCounterMember = 0; // Declara globalmente se não existir
        }
        selectCounterMember++;

        // Cria um contêiner exclusivo para o select e o botão de remoção
        var selectContainerId = `select-container-member-${selectCounterMember}`;
        var selectContainer = document.createElement('div');
        selectContainer.id = selectContainerId;
        selectContainer.classList.add('flex', 'items-center', 'gap-2', 'mb-2'); // Adiciona classes de estilo

        // Cria o select
        var selectHtml = `
            <select name="dynamic_selects_members_${selectCounterMember}" 
                    class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
                ${data.options.map(option => `<option value="${option.value}">${option.label}</option>`).join('')}
            </select>
        `;

        // Cria o botão de remoção
        var removeButtonHtml = `
            <button type="button" 
                    class="text-red-500 border border-red-500 rounded px-2 py-1 hover:bg-red-500 hover:text-white"
                    onclick="removeDynamicSelect('${selectContainerId}', 0)">
                Remover
            </button>
        `;

        // Adiciona o select e o botão ao contêiner
        selectContainer.innerHTML = selectHtml + removeButtonHtml;

        // Adiciona o contêiner ao elemento principal
        document.getElementById('select-container-member').appendChild(selectContainer);

        // Habilita o botão de envio
        //var sendFormButton = document.getElementById('send-form');
        //sendFormButton.disabled = false;
    } catch (error) {
        console.log('Erro ao obter opções do select:', error);
    }
}


//
// Adiciona novos stakeholders
//
// Função async para lidar com a lógica
async function addSelectStakeholder() {
    try {

        // Busca os dados do servidor usando fetch
        var response = await fetch("/projects/get-select-users/");
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.statusText);
        }

        var data = await response.json();

        // Incrementa o contador para criar IDs únicos
        if (typeof selectCounterStakeholder === 'undefined') {
            window.selectCounterStakeholder = 0; // Declara globalmente se não existir
        }
        selectCounterStakeholder++;

        // Cria um contêiner exclusivo para o select e o botão de remoção
        var selectContainerId = `select-container-stakeholder-${selectCounterStakeholder}`;
        var selectContainer = document.createElement('div');
        selectContainer.id = selectContainerId;
        selectContainer.classList.add('flex', 'items-center', 'gap-2', 'mb-2'); // Adiciona classes de estilo

        // Cria o select
        var selectHtml = `
            <select name="dynamic_selects_stakeholders_${selectCounterStakeholder}" 
                    class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
                ${data.options.map(option => `<option value="${option.value}">${option.label}</option>`).join('')}
            </select>
        `;

        // Cria o botão de remoção
        var removeButtonHtml = `
            <button type="button" 
                    class="text-red-500 border border-red-500 rounded px-2 py-1 hover:bg-red-500 hover:text-white"
                    onclick="removeDynamicSelect('${selectContainerId}', 0)">
                Remover
            </button>
        `;

        // Adiciona o select e o botão ao contêiner
        selectContainer.innerHTML = selectHtml + removeButtonHtml;

        // Adiciona o contêiner ao elemento principal
        document.getElementById('select-container-stakeholder').appendChild(selectContainer);

        // Habilita o botão de envio
        //var sendFormButton = document.getElementById('send-form');
        //sendFormButton.disabled = false;
    } catch (error) {
        console.log('Erro ao obter opções do select:', error);
    }
}

// Função para adicionar novo formset
function addFormset(e, formsetContainer, addFormsetButton, tab, totalForms, formsetNum, type) {
    e.preventDefault();


    // Verificar se formsetContainer[0] não existe
    // NEW sendo executado
    if (formsetContainer[0] === undefined){

        switch (type){
            //
            // Adiciona novos prédios
            //
            case 'building':
                (async function handleDynamicSelect() {
                    try {
                        // Obtém o ID do site
                        var siteId = document.getElementById('id_site').value;
                
                        // Busca os dados do servidor usando fetch
                        var response = await fetch("/projects/get-select-options/" + siteId + "/");
                        if (!response.ok) {
                            throw new Error('Erro na requisição: ' + response.statusText);
                        }
                        var data = await response.json();

                        if (data.options.length > 0){

                            // Incrementa o contador para criar IDs únicos
                            if (typeof selectCounterSite === 'undefined') {
                                window.selectCounterSite = 0; // Declara globalmente se não existir
                            }
                            selectCounterSite++;
                            selectCounterAuthSubmit++;

                            if (selectCounterAuthSubmit > 0) {
                                // Habilita o elemento select
                                //document.getElementById('send-form').disabled = false;
                                var sendFormButton = document.getElementById('send-form');
                                sendFormButton.disabled = false;
                            }                
                            // Cria um contêiner exclusivo para o select e o botão de remoção
                            var selectContainerId = `select-container-site-${selectCounterSite}`;
                            var selectContainer = document.createElement('div');
                            selectContainer.id = selectContainerId;
                            selectContainer.classList.add('flex', 'items-center', 'gap-2', 'mb-2'); // Adiciona classes de estilo (opcional)
                    
                            // Cria o select
                            var selectHtml = `
                                <select name="dynamic_selects_${selectCounterSite}" 
                                        class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
                                    ${data.options.map(option => `<option value="${option.value}">${option.label}</option>`).join('')}
                                </select>
                            `;
                    
                            // Cria o botão de remoção
                            var removeButtonHtml = `
                                <button type="button" class="text-red-500 border border-red-500 rounded px-2 py-1 hover:bg-red-500 hover:text-white"
                                        onclick="removeDynamicSelect('${selectContainerId}', 1)">
                                    Remover
                                </button>
                            `;
                    
                            // Adiciona o select e o botão ao contêiner
                            selectContainer.innerHTML = selectHtml + removeButtonHtml;
                    
                            // Adiciona o contêiner ao elemento principal
                            document.getElementById('select-container').appendChild(selectContainer);
                    
                            // Habilita o botão de envio
                            //var sendFormButton = document.getElementById('send-form');
                            //sendFormButton.disabled = false;

                        } else { // ELSE DO DATA.OPTIONS
                            window.alert("Selected SITE does not have registered BUILDINGS!");
                        } // ENDIF DO DATA.OPTIONS

                    } catch (error) {
                        console.log('Error getting SELECT options:', error);
                    }
                })();
                
                break;

            //
            // Adiciona novos membros
            //
            case 'member':
                (async function handleDynamicSelect() {
                    try {
                        var data = await fetchData("/projects/get-select-users/");
                        
                        // Incrementa o contador para criar IDs únicos
                        selectCounterMember++;
                
                        // Criar um contêiner exclusivo para o select e o botão de remoção
                        var selectContainerId = `select-container-member-${selectCounterMember}`;
                        var selectContainer = document.createElement('div');
                        selectContainer.id = selectContainerId;
                        selectContainer.classList.add('flex', 'items-center', 'gap-2', 'mb-2'); // Adiciona classes de estilo (opcional)
                
                        // Criar o select
                        var selectHtml = `
                            <select name="dynamic_selects_members_${selectCounterMember}" 
                                    class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
                                ${data.options.map(option => `<option value="${option.value}">${option.label}</option>`).join('')}
                            </select>
                        `;
                
                        // Criar o botão de remoção
                        var removeButtonHtml = `
                            <button type="button" class="text-red-500 border border-red-500 rounded px-2 py-1 hover:bg-red-500 hover:text-white"
                                    onclick="removeDynamicSelect('${selectContainerId}', 0)">
                                Remover
                            </button>
                        `;
                
                        // Adicionar o select e o botão ao contêiner
                        selectContainer.innerHTML = selectHtml + removeButtonHtml;
                
                        // Adicionar o contêiner ao elemento principal
                        document.getElementById('select-container-member').appendChild(selectContainer);
                
                        // Desabilitar o botão de envio (se necessário)
                        //var sendFormButton = document.getElementById('send-form');
                        //sendFormButton.disabled = false;
                        
                        // GAMBIARRA - DO IT A MACGYVER
                        // Busca os dados do servidor usando fetch 
                        // Forma fácil de ativar ou desativar o botão submit
                        // Não estou a fim de pensar - domingão de manhã e com um sol da porra e um calor do c*******
                        // Obtém o ID do site
                        var siteId = document.getElementById('id_site').value;
                        var response = await fetch("/projects/get-select-options/" + siteId + "/");
                        if (!response.ok) {
                            throw new Error('Erro na requisição: ' + response.statusText);
                        }
                        var data = await response.json();

                        if (data.options.length > 0){
                            var sendFormButton = document.getElementById('send-form');
                            sendFormButton.disabled = false;                            
                        } else {
                            var sendFormButton = document.getElementById('send-form');
                            sendFormButton.disabled = true;
                        }
                        
                    } catch (error) {
                        console.log('Erro ao obter opções do select', error);
                    }
                })();                
                break;

            //
            // Adiciona novos stakeholders
            //
            case 'stakeholder':
                (async function handleDynamicSelect() {
                    try {
                        // Busca os dados do servidor
                        var data = await fetchData("/projects/get-select-users/");
                
                        // Incrementa o contador para criar IDs únicos
                        selectCounterStakeholder++;
                
                        // Cria um contêiner exclusivo para o select e o botão de remoção
                        var selectContainerId = `select-container-stakeholder-${selectCounterStakeholder}`;
                        var selectContainer = document.createElement('div');
                        selectContainer.id = selectContainerId;
                        selectContainer.classList.add('flex', 'items-center', 'gap-2', 'mb-2'); // Adiciona classes de estilo (opcional)
                
                        // Cria o select
                        var selectHtml = `
                            <select name="dynamic_selects_stakeholders_${selectCounterStakeholder}" 
                                    class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
                                ${data.options.map(option => `<option value="${option.value}">${option.label}</option>`).join('')}
                            </select>
                        `;
                
                        // Cria o botão de remoção
                        var removeButtonHtml = `
                            <button type="button" class="text-red-500 border border-red-500 rounded px-2 py-1 hover:bg-red-500 hover:text-white"
                                    onclick="removeDynamicSelect('${selectContainerId}', 0)">
                                Remover
                            </button>
                        `;
                
                        // Adiciona o select e o botão ao contêiner
                        selectContainer.innerHTML = selectHtml + removeButtonHtml;
                
                        // Adiciona o contêiner ao elemento principal
                        document.getElementById('select-container-stakeholder').appendChild(selectContainer);
                
                        // Habilita o botão de envio
                        //var sendFormButton = document.getElementById('send-form');
                        //sendFormButton.disabled = false;
                                                // GAMBIARRA - DO IT A MACGYVER
                        // Busca os dados do servidor usando fetch 
                        // Forma fácil de ativar ou desativar o botão submit
                        // Não estou a fim de pensar - domingão de manhã e com um sol da porra e um calor do c*******
                        // Obtém o ID do site
                        var siteId = document.getElementById('id_site').value;
                        var response = await fetch("/projects/get-select-options/" + siteId + "/");
                        if (!response.ok) {
                            throw new Error('Erro na requisição: ' + response.statusText);
                        }
                        var data = await response.json();

                        if (data.options.length > 0){
                            var sendFormButton = document.getElementById('send-form');
                            sendFormButton.disabled = false;                            
                        } else {
                            var sendFormButton = document.getElementById('send-form');
                            sendFormButton.disabled = true;
                        }
                        
                    } catch (error) {
                        console.log('Erro ao obter opções do select', error);
                    }
                })();             
                break;
        }
    
    } else {

        // Verificar se formsetContainer[0] não contém elementos úteis
        // EDIT sendo executado
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

}

// Função para remover o contêiner do select 
// Por enquanto funcionando no NEW
function removeDynamicSelect(containerId, action) {
    var container = document.getElementById(containerId);
    if (container) {
        container.remove();
        if (action === 1){
            selectCounterAuthSubmit--;
            if (selectCounterAuthSubmit <= 0){
                selectCounterAuthSubmit = 0;
                // Desabilita o elemento select
                var sendFormButton = document.getElementById('send-form');
                sendFormButton.disabled = true;
            }
        }
    }
}

// New buildings
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

// New members
let formsetContainerMember = document.querySelectorAll('#id-member-selector'),
    addFormsetButtonMember = document.querySelector('#add-formset2'),
    tab3 = document.querySelector('#tab3'),
    totalFormsMember = document.querySelector('#id_form-TOTAL_FORMS'),
    formsetNumMember = formsetContainerMember.length - 1;

addFormsetButtonMember.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerMember, addFormsetButtonMember, tab3, totalFormsMember, formsetNumMember, 'member')
);

// New stakeholders
let formsetContainerStakeholder = document.querySelectorAll('#id-stakeholder-selector'),
    addFormsetButtonStakeholder = document.querySelector('#add-formset3'),
    tab4 = document.querySelector('#tab4'),
    totalFormsStakeholder = document.querySelector('#id_form-TOTAL_FORMS'),
    formsetNumStakeholder = formsetContainerStakeholder.length - 1;

addFormsetButtonStakeholder.addEventListener(
    'click',
    (e) => addFormset(e, formsetContainerStakeholder, addFormsetButtonStakeholder, tab4, totalFormsStakeholder, formsetNumStakeholder, 'stakeholder')
);

// Remove formset (deprecated)
// Delete select option and button remove
// document.addEventListener('click', function (e) {
//     if (e.target.classList.contains('remove-formset')) {
//         e.preventDefault();
//         e.target.parentElement.remove();
//     }
// });

// Remove formset
// Delete select option and button remove
// Adjust for new condition , select and button are removed
const removeButtons = document.querySelectorAll('.remove-formset');
removeButtons.forEach(button => {
    button.addEventListener('click', function() {
        const parentDiv = this.closest('.formset-container'); 
        parentDiv.remove(); 
    });
});