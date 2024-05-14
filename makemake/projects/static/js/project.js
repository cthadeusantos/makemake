var selectCounterSite = 0;  // Inicializa um contador para IDs únicos
var selectCounterMember = 0;  // Inicializa um contador para IDs únicos
var selectCounterStakeholder = 0;  // Inicializa um contador para IDs únicos

//
// Adiciona novos prédios
//
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-select').addEventListener('click', async function () {
        try {
            var siteId = document.getElementById('id_site').value;
            var data = await fetchData("/projects/get-select-options/" + siteId + "/");
            //var selectCounterSite = 0;

            // Incrementa o contador para criar IDs únicos
            selectCounterSite++;

            // Criar um novo select com ID único
            //var selectHtml = '<p><select name="dynamic_selects_' + selectCounterSite + '" class="form-select form-select-sm" >';
            var selectHtml = '<p><select name="dynamic_selects_' + selectCounterSite + '" class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer" >';
            for (var i = 0; i < data.options.length; i++) {
                selectHtml += '<option value="' + data.options[i].value + '">' + data.options[i].label + '</option>';
            }
            selectHtml += '</select></p>';

            // Adicionar ao contêiner
            document.getElementById('select-container').insertAdjacentHTML('beforeend', selectHtml);

            // Desabilita botão submit
            var sendFormButton = document.getElementById('send-form');
            sendFormButton.disabled = false;
        } catch (error) {
            console.log('Erro ao obter opções do select', error);
        }
    });
});

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
                addSelectButton.disabled = false;
                // Ativar o botão após o primeiro select ser adicionado
                //addSelectButton.removeAttribute('disabled');
            }
        });
    }
});


//
// Adiciona novos membros
//
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-select-member').addEventListener('click', async function () {
        try {
            var data = await fetchData("/projects/get-select-users/");
            //var selectCounterSite = 0;

            // Incrementa o contador para criar IDs únicos
            selectCounterMember++;

            // Criar um novo select com ID único
            //var selectHtml = '<p><select name="dynamic_selects_members_' + selectCounterMember + '" class="form-select form-select-sm">';
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
    });
});

//
// Adiciona novos stakeholders
//
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-select-stakeholder').addEventListener('click', async function () {
        try {
            var data = await fetchData("/projects/get-select-users/");
            //var selectCounterSite = 0;

            // Incrementa o contador para criar IDs únicos
            selectCounterStakeholder++;

            // Criar um novo select com ID único
            //var selectHtml = '<p><select name="dynamic_selects_stakeholders_' + selectCounterStakeholder + '" class="form-select form-select-sm">';
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
    });
});