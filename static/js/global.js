// Description: Global JavaScript functions.

// Enable all fields in a form.
function enableAllFields() {
    document.querySelectorAll('[disabled], [readonly]').forEach(el => {
        el.removeAttribute('disabled');
        el.removeAttribute('readonly');
    });
  }