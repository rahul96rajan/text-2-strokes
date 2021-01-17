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
	let command = "cd .. && python3 generate.py --char_seq '"+ document.getElementById('inputText').value + "' --save_img";
	
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

	setTimeout(function() {
	var img = document.createElement("img");
	img.src = "../results/gen_img.png"; //http://www.google.com/intl/en_com/images/logo_plain.png";
	var src = document.getElementById("showImage");
	src.appendChild(img).style.width='200px';	
	}, 10000);

});

// var img = document.createElement("img");
// 	img.src = "./image.png"; //http://www.google.com/intl/en_com/images/logo_plain.png";
// 	var src = document.getElementById("showImage");
// 	src.appendChild(img).style.width='200px';	

// document.getElementById('showImage').innerHTML
// var para = document.createElement('<img src="./image.png" />');
// document.getElementById('showImage').innerHTML.element.appendChile(para);




