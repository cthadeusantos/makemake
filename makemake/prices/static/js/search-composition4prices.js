let timeout = null;

document.getElementById('small-input').addEventListener('input', function () {
    const query = this.value;

    clearTimeout(timeout);
    timeout = setTimeout(() => {
        fetchResults1(query);
    }, 2000); // Delay of 2 seconds
});

async function fetchResults1(query) {
    if (query.trim().length === 0) {
        clearDropdown1();
        return;
    }

    try {
        const response = await fetch(`/compositions/search_components?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        updateDropdown1(data);
    } catch (error) {
        console.error('Error fetching results:', error);
    }
}

function updateDropdown1(data) {
    const selectComponent = document.getElementById('select-component');
    selectComponent.innerHTML = '<option value="" selected disabled>Select component...</option>'; // Clear previous options

    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id; // Assuming the data items have 'value' and 'text' properties
        option.textContent = item.description;
        if (item.iscomposition){
            option.textContent = '* '+ item.description + ' *';
        } 

        var dataAttributes = {
                dbtype: item.dbtype,
                code: item.code,
                unit: item.unit,
        };

        // Adiciona os data-atributes
        // Procurar por material para aprender sobre como e porque isto é feito,
        // pois aprendi isso aqui com o chatgpt
        for (const [key, value] of Object.entries(dataAttributes || {})) {
            option.setAttribute(`data-${key}`, value);
        }

        selectComponent.appendChild(option);
    });
}

function clearDropdown1() {
    const selectComponent = document.getElementById('select-component');
    selectComponent.innerHTML = '<option value="" selected disabled>Select component...</option>';
}


// Funcoes que buscam os PriceLabels
async function fetchResultsPriceLabel(selectOption) {
    // if (query.length === 0) {
    //     clearDropdownCategory();
    //     return;
    // }

    try {
        const response = await fetch(`/prices/search-prices-labels`);
        const data = await response.json();
        updateDropdownPriceLabel(data, selectOption);
    } catch (error) {
        console.error('Error fetching results:', error);
    }
}

function updateDropdownPriceLabel(data, selectedOption) {
    const selectComponent = document.getElementById(selectedOption);
    //selectComponent.innerHTML = '<option value="" selected disabled>Select component...</option>'; // Clear previous options

    // Verifica se o elemento com esse ID existe
    if (!selectComponent) {
        console.error(`Elemento com ID '${selectedOption}' não foi encontrado.`);
        return;
    }

    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id; // Assuming the data items have 'value' and 'text' properties
        option.textContent = item.name;
        if (item.id == valorSelecionadoGlobal){
            option.selected = true;
        }
        selectComponent.appendChild(option);
    });
}

function clearDropdownPriceLabel() {
    const selectComponent = document.getElementById('select-component');
    selectComponent.innerHTML = '<option value="" selected disabled>Select component...</option>';
}