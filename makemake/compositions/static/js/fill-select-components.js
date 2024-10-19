let inputCounter = 1;
let inputBlockCounter = 0;

document.getElementById('add-input-button').addEventListener('click', function () {
    const selectComponent = document.getElementById('select-component');

    // Here you can also get the selected option and its data attributes if needed
    const selectedOption = selectComponent.options[selectComponent.selectedIndex];
    const dataAttributes = {};
    for (let attr of selectedOption.attributes) {
        if (attr.name.startsWith('data-')) {
            dataAttributes[attr.name] = attr.value;
        }
    }

    // If select components is empty
    if (selectedOption.value===""){
        alert("You must select a component!");
        return; // Interrompe a criação do novo elemento
    }

    // Seleciona todos os elementos
    const allElements = document.querySelectorAll('*');
    // Array para armazenar os elementos com IDs no formato "ID-X"
    const elementsWithIdX = [];
    // Regex para identificar IDs no formato "ID-X"
    const idPattern = /^ID-\d+$/;
    // Loop para verificar os IDs e adicionar os elementos correspondentes ao array
    allElements.forEach(element => {
        if (element.id && idPattern.test(element.id)) {
            elementsWithIdX.push(element);
        }
    });
    //Verificar se o valor do novo select já existe
    for (let i = 0; i < elementsWithIdX.length; i++) {
        if (elementsWithIdX[i].value == selectedOption.value) {
            alert('The element exist!');
            return; // Interrompe a criação do novo elemento
        }
    }
    
    const container = document.getElementById('putselecthere');
    const inputBlock = document.createElement('div');
    inputBlock.className = 'flex mb-3';
    inputBlock.id = 'input-block-' + inputCounter;

    const inputID = document.createElement('input');
    inputID.type = 'text';
    //inputID.id = 'ID-' + inputCounter;
    inputID.id = 'id-' + inputCounter;
    //inputID.name = inputCounter + '-id'; // Add name for Django form submission
    inputID.name = 'id-' + inputCounter; // Add name for Django form submission
    //inputID.placeholder = 'ID';
    inputID.placeholder = 'id';
    inputID.readOnly = true;
    inputID.className = 'w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500';

    const inputDBtype = document.createElement('input');
    inputDBtype.type = 'text';
    inputDBtype.id = 'dbtype-' + inputCounter;
    //inputDBtype.name = inputCounter + '-dbtype'; // Add name for Django form submission
    inputDBtype.name = 'dbtype-' + inputCounter; // Add name for Django form submission
    inputDBtype.placeholder = 'DBtype';
    inputDBtype.readOnly = true;
    inputDBtype.className = 'w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500';

    const inputCode = document.createElement('input');
    inputCode.type = 'text';
    inputCode.id = 'code-' + inputCounter;
    //inputCode.name = inputCounter + '-code'; // Add name for Django form submission
    inputCode.name = 'code-' + inputCounter; // Add name for Django form submission
    inputCode.placeholder = 'Code';
    inputCode.readOnly = true;
    inputCode.className = 'w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500';

    const inputComponent = document.createElement('textarea');
    //inputComponent.id = 'component-' + inputCounter;
    inputComponent.id = 'description-' + inputCounter;
    //inputComponent.name = inputCounter + 'component'; // Add name for Django form submission   
    inputComponent.name = 'description-' + inputCounter; // Add name for Django form submission   
    inputComponent.placeholder = 'Component';
    inputComponent.readOnly = true;
    inputComponent.rows = 1;
    inputComponent.className = 'w-1/2 flex-1 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500';
    
    // Add the select element
    const selectOption = document.createElement('select');
    selectOption.id = 'select-option-' + inputCounter;
    selectOption.name = 'select-option-' + inputCounter;
    selectOption.className = 'w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500';


    // Add options to the select element
    const options = [
        { value: 1, text: 'Allocation factor' },
        { value: 2, text: 'Collected' }
    ];

    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option.value;
        opt.textContent = option.text;
        // Set the first option (value: 1) as selected
        if (option.value === 1) {
            opt.selected = true;
  }
        selectOption.appendChild(opt);
    });

    const inputQty = document.createElement('input');
    inputQty.type = 'text';
    inputQty.id = 'quantity-' + inputCounter;
    inputQty.name = 'quantity-' + inputCounter; // Add name for Django form submission   
    inputQty.placeholder = 'Qty';
    inputQty.className = 'w-1/12 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 text-right';

    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'ml-2 h-8 text-sm px-2 py-2 text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg dark:bg-red-600 dark:hover:bg-red-700 focus:outline-none dark:focus:ring-red-800';
    removeButton.innerHTML = 'Remove';
    removeButton.addEventListener('click', function () {
        container.removeChild(inputBlock);
        inputBlockCounter--;
        if (!inputBlockCounter){
            const checkbox = document.getElementById('id_iscomposition');
            const input = document.getElementById('small-input');
            const button = document.getElementById('add-input-button');
            const select = document.getElementById('select-component');
        
            checkbox.checked = false;
            input.disabled = true;
            input.value = "";
            button.disabled = true;
            select.disabled = true;
        }
    });

    inputBlock.appendChild(inputID);
    inputBlock.appendChild(inputDBtype);
    inputBlock.appendChild(inputCode);
    inputBlock.appendChild(inputComponent);
    inputBlock.appendChild(selectOption); 
    inputBlock.appendChild(inputQty);
    inputBlock.appendChild(removeButton);
    container.appendChild(inputBlock);

    //console.log('PASSEI');
    // Send values to input's
    document.getElementById(inputID.id).value = selectedOption.value;
    document.getElementById(inputDBtype.id).value = dataAttributes['data-dbtype'];
    document.getElementById(inputCode.id).value = dataAttributes['data-code'];
    document.getElementById(inputComponent.id).value = selectedOption.textContent;
    document.getElementById(inputQty.id).value = "1.00";

    inputCounter++;
    inputBlockCounter++;
});