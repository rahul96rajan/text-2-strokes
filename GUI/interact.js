const electron = require('electron');
const ipc = electron.ipcRenderer;

var submitBtn = document.getElementById('submit');

submitBtn.addEventListener('click', function(){
	// console.log(document.getElementById('inputText').value);		// to retreive the value introduced in the input field
	// ipc.send('buttonClicked');  
	
	// let spawn = require("child_process").spawn;

	// let bat = spawn("python ", [
	// 		"hello.py",          // Argument for cmd.exe to carry out the specified script
	// 		 "/Users/lowkey/Git repo's/python_project", // Path to your file
	// 		"1",   // First argument
	// 		"2"    // n-th argument
	// ]);
	// let initCommand = "cd ../../../..";
	let command = "cd .. && python3 generate.py --char_seq '"+ document.getElementById('inputBox').value + "' --save_img";
	
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
		console.log(data);
	});

	// add delay to wait for the pyhton program to execute and generate the gen_image.png file
	setTimeout(function() {

	// to remove the last generated image
	var src = document.getElementById("showImage");
	src.innerHTML="";
	// src.removeChild(src.childNodes[0]);
	// console.log(src.childNode);
	// console.log(src.childNodes.length);
	// if (src.childNodes.length > 0) {
	// 	for (let i = 0; i < src.childNodes.length; i++) {
	// 		src.removeChild(src.childNodes[i]);
	// 		console.log(i);
	// 	}		
		
	// }

	// to display the newly generated image
	var img = document.createElement("img");
	var regexString = "results/gen_img1610883803.332347.png";
	console.log(data.match(regexString));
	img.src = "../results/gen_img.png"; //http://www.google.com/intl/en_com/images/logo_plain.png";
	
	src.appendChild(img).style.width='600px';
	console.log("added new image");
	}, 10000);

});

// var img = document.createElement("img");
// 	img.src = "./image.png"; //http://www.google.com/intl/en_com/images/logo_plain.png";
// 	var src = document.getElementById("showImage");
// 	src.appendChild(img).style.width='200px';	

// document.getElementById('showImage').innerHTML
// var para = document.createElement('<img src="./image.png" />');
// document.getElementById('showImage').innerHTML.element.appendChile(para);




