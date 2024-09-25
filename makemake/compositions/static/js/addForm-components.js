function addForm() {
    const formsetDiv = document.getElementById('add-form');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const currentFormCount = formsetDiv.children.length;
    const newFormCount = parseInt(totalForms.value);

    // Clone the empty form
    const newForm = formsetDiv.children[0].cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replace(/form-\d+-/g, `form-${newFormCount}-`);

    // Clear the input value
    const inputs = newForm.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].value = '';
    }

    // Append the new form
    formsetDiv.appendChild(newForm);

    // Update the number of total forms
    totalForms.value = newFormCount + 1;
}