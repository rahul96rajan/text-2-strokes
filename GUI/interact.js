const electron = require('electron');
const ipc = electron.ipcRenderer;

var submitBtn = document.getElementById('submit');

submitBtn.addEventListener('click', function(){
	// let initCommand = "cd ../../../..";
	let command = ("cd .. && python3 generate.py --char_seq '"
					+ document.getElementById('inputBox').value + "' --style " +
					+ document.getElementById('fontStyle').value +
					" --save_img");
	let regexString = /results[/]gen_img.*.png/;
	let imagePath = "";
	
	const { exec } = require("child_process");
	// exec(initCommand, (getter) => {if(getter) {}});
	exec(command, (error, data, getter) => {
		console.log(command);
		if(error){
			console.log("error",error.message);
			return;
		}
		if(getter){
			console.log(data);
			return;
		}
		imagePath = data.match(regexString)[0];
	});


	(function wait() {
		if ( imagePath !== "" ) {
			console.log("Image Path: " + imagePath);
			var src = document.getElementById("showImage");
			src.innerHTML="";

			// to display the newly generated image
			var img = document.createElement("img");
			
			img.src = "../"+imagePath;
			src.appendChild(img).style.cssText = 'width: 95%; margin-left: auto; margin-right: auto; display: block;';
			console.log("added new image");
		} else {
			setTimeout( wait, 500 );
		}
	})();
});
