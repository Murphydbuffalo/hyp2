document.onreadystatechange = function(_event) {
  const currentNumForms = parseInt(document.querySelector("#id_variant_set-TOTAL_FORMS").value);
  const minNumForms = parseInt(document.querySelector("#id_variant_set-MIN_NUM_FORMS").value);
  const maxNumForms = parseInt(document.querySelector("#id_variant_set-MAX_NUM_FORMS").value);

  document.querySelector("#add-variant").onclick = function(event) {
    event.preventDefault();
    const clonedInput = document.querySelector("#empty-form").cloneNode(true);
    const newInputHTML = clonedInput.outerHTML.replace(/__prefix__/g, currentNumForms);
    document.querySelector("#variant-form-fields").insertAdjacentHTML("beforeend", newInputHTML);
    document.querySelector("#id_variant_set-TOTAL_FORMS").value = currentNumForms + 1;

    if (currentNumForms === maxNumForms) {
      event.currentTarget.classList.add("hidden");
    }
  }
}