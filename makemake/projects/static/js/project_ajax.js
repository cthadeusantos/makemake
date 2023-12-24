$(document).ready(function () {
    var selectCounter = 0;  // Inicializa um contador para IDs únicos
    $('#add-select').on('click', function () {
        $.ajax({
            url: "/projects/get-select-options/" + document.getElementById('id_site').value +"/",
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Incrementa o contador para criar IDs únicos
                selectCounter++;

                // Criar um novo select com ID único
                var selectHtml = '<p><select name="dynamic_selects_' + selectCounter + '">';
                for (var i = 0; i < data.options.length; i++) {
                    selectHtml += '<option value="' + data.options[i].value + '">' + data.options[i].label + '</option>';
                }
                selectHtml += '</select></p>';

                // Adicionar ao contêiner
                $('#select-container').append(selectHtml);

                // Desabilita botão submit
                var sendFormButton = document.getElementById('send-form');
                sendFormButton.disabled = false;
            },
            error: function () {
                console.log('Erro ao obter opções do select');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var previousValue = $('#id_site').val();  // Valor inicial do select
    var selectElement = document.getElementById('id_site');

    if (selectElement) {
        // Adicione um ouvinte de eventos para a mudança no valor do select
        selectElement.addEventListener('change', function () {

            // Lógica a ser executada quando o select for alterado
            console.log('Select alterado! Novo valor:', selectElement.value);

            // Supondo que você já tem uma referência ao botão
            var addSelectButton = document.getElementById('add-select');

            // Verificar se o valor do select é vazio

            if (selectElement.value === '') {
                var selectContainer = $('#select-container');

                // Limpar os selects se a string for vazia
                selectContainer.empty();

                // Se vazio, desativar o botão
                addSelectButton.disabled = true;

                // Desabilita botão submit
                var sendFormButton = document.getElementById('send-form');
                sendFormButton.disabled = true;

            } else {

                $('#id_site').on('change', function () {
                    var currentValue = $(this).val();  // Valor atual do select após a mudança

                    // Comparar o valor anterior com o valor atual
                    if (currentValue !== previousValue) {
                        // A mudança ocorreu
                        console.log('O select teve uma mudança. Valor anterior:', previousValue, 'Novo valor:', currentValue);

                        // Faça algo aqui após a mudança no select
                        var selectContainer = $('#select-container');

                        // Limpar os selects se a string for vazia
                        selectContainer.empty();

                        // Desabilita botão submit
                        var sendFormButton = document.getElementById('send-form');
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