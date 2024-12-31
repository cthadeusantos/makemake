let timeout = null;

document.getElementById('small-input').addEventListener('input', function () {
    const query = this.value;

    clearTimeout(timeout);
    timeout = setTimeout(() => {
        fetchResults(query);
    }, 2000); // Delay of 2 seconds
});

async function fetchResults(query) {
    if (query.trim().length === 0) {
    //if (query.replace("/^\s+|\s+$/gm", '').length === 0) {
        clearDropdown();
        return;
    }

    try {
        const response = await fetch(`/compositions/search_components?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        updateDropdown(data);
    } catch (error) {
        console.error('Error fetching results:', error);
    }
}

function updateDropdown(data) {
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
                code: item.code
        };

        // Adiciona os data-atributes
        for (const [key, value] of Object.entries(dataAttributes || {})) {
            option.setAttribute(`data-${key}`, value);
        }

        selectComponent.appendChild(option);
    });
}

function clearDropdown() {
    const selectComponent = document.getElementById('select-component');
    selectComponent.innerHTML = '<option value="" selected disabled>Select component...</option>';
}