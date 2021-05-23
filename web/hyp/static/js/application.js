// TODO: only load this on the relevant page...
document.onreadystatechange = function(_event) {
  let hiddenVariantIndex = 2;

  document.querySelector(".add-variant").onclick = function(event) {
    event.preventDefault();
    let nextVariantInputs = document.querySelectorAll(`#variant-${hiddenVariantIndex} .hidden`)
    nextVariantInputs.forEach((element) => element.classList.remove("hidden"));

    hiddenVariantIndex++;

    nextVariantInputs = document.querySelectorAll(`#variant-${hiddenVariantIndex} .hidden`)

    if (nextVariantInputs.length === 0) {
      event.currentTarget.classList.add("hidden");
    }
  }
}