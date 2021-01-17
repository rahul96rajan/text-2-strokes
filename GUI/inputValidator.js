var inputField = document.querySelector('#inputBox')
var submitBtn = document.querySelector('#submit')


function changeButtonColor(textEnteredLength, disabled) {
    if (textEnteredLength >= 4 && textEnteredLength < 50) disabled = false;
    if (disabled) {
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.style.cssText = 'color:red; background-color:green;';
    } else {
        submitBtn.removeAttribute('disabled');
        submitBtn.style.cssText = 'color:white; background-color:blue;';
    }
}


inputField.addEventListener('keydown', function(e) {
    var disabled = true;

    const key = event.key;
    let textEnteredLength = inputField.value.length;

    if (key === "Backspace" || key === "Delete") {textEnteredLength = inputField.value.length; changeButtonColor(textEnteredLength, disabled);}

    console.log(inputField.value.length)
    if (textEnteredLength >= 4 && textEnteredLength < 50) {disabled = false; changeButtonColor(textEnteredLength, disabled);};
})