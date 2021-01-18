var inputField = document.querySelector('#inputBox')
var submitBtn = document.querySelector('#submit')

function updateBtnStatus(str) {
    let textEnteredLength = str.length;
    console.log(textEnteredLength)
    let disabled = true
    if (textEnteredLength >= 5 && textEnteredLength <= 50) disabled = false;
    
    if (disabled) {
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.style.cssText = 'color:rgba(255, 255, 255, 0.412); background-color:rgba(0, 0, 136, 0.412);';
    } else {
        submitBtn.removeAttribute('disabled');
        submitBtn.style.cssText = 'color:white; background-color:rgba(0, 0, 136, 0.938);';
    }
}