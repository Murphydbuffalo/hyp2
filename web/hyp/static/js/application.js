// TODO: only load this on the relevant page...
document.onreadystatechange = function(_event) {
  let variantIndex = 0;

  document.querySelector(".add-variant").onclick = function(event) {
    event.preventDefault();
    variantIndex = variantIndex + 1;

    const nextVariantInputs = document.querySelectorAll(`#variant-${variantIndex + 1} .hidden`)

    if (nextVariantInputs.length > 0) {
      nextVariantInputs.forEach((element) => element.classList.remove("hidden"));
    } else {
      event.currentTarget.classList.add("hidden");
    }
  }
}