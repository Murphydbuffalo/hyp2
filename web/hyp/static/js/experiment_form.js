document.onreadystatechange = function(_event) {
  let currentNumForms = parseInt(document.querySelector("#id_variant_set-TOTAL_FORMS").value);
  const minNumForms = parseInt(document.querySelector("#id_variant_set-MIN_NUM_FORMS").value);
  const maxNumForms = parseInt(document.querySelector("#id_variant_set-MAX_NUM_FORMS").value);

  document.querySelector(".newExperimentForm-addVariant").onclick = function(event) {
    event.preventDefault();
    currentNumForms++;

    const clonedInput = document.querySelector(".newExperimentForm-emptyVariantForm .newVariantInputContainer").cloneNode(true);
    const newInputHTML = clonedInput.outerHTML.replace(/__prefix__/g, currentNumForms - 1);
    document.querySelector(".newExperimentForm-variantFormFields").insertAdjacentHTML("beforeend", newInputHTML);
    document.querySelector("#id_variant_set-TOTAL_FORMS").value = currentNumForms;

    if (currentNumForms === maxNumForms - 1) {
      event.currentTarget.classList.add("hidden");
    }
  }
}
