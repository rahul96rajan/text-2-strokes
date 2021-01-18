const { app, Menu, MenuItem } = require("electron");

const isMac = process.platform === "darwin";

// win menu
const winMenuTemplate = [
	{
		label: "App name",
			submenu: [
				{
					label: "About app name",
        	// click: openAbout(),
				},
				{
					label: 'Quit',
						accelerator: 'Ctrl+Q',
						// click: () => {getModals.quitWindow();}
				}
			]
	},
	{
		label: "File",
		submenu: [
			{
				label: "Open new window",
			},
			{
				label: "Hide app name",
				role: "hide",
			},
			{
				label: "Close window",
				role: "quit"
			}
		]
	},
];



// mac menu
const macMenuTemplate = [
	{
		label: "App name",
    	submenu: [
    		{
        	label: "About app name",
        	// click: openAbout(),
      	},
				{
					label: 'Quit',
					accelerator: 'Command+Q',
					// click: () => {getModals.quitWindow();}
				}
			]
	},
	{
		label: "File",
			submenu: [
				{
					label: "Open new window",
				},
				{
					label: "Hide app name",
					role: "hide"
				},
				{
					label: "Close window",
					role: "quit"
				}
			]
	},
	{
		label: "Edit",
			submenu: [
				{
					label: "Undo",
					accelerator: 'Command+Z',
					role: "undo"
				},
				{
					label: "Redo",
					accelerator: 'Command+Shift+Z',
					role: "redo"
				},
				{
					label: "Cut",
					accelerator: 'Command+X',
					role: "cut"
				},
				{
					label: "Copy",
					accelerator: 'Command+C',
					role: "copy"
				},
			
				{
					label: "Paste",
					accelerator: 'Command+P',
					role: "paste"
				},
				{
					label: "Select All",
					accelerator: 'Command+A',
					role: "selectAll"
				},
				{
					label: "Redo",
					accelerator: 'Command+Shift+Z',
					role: "redo"
				},
			]
	},
	{
		label: "View",
			submenu: [
				{
					label: "Reload",
					role: "reload"
				},
				{
					label: "Enter Full Screen",
					role: "togglefullscreen"
				},
			]
	},
	{
		label: "Window",
			submenu: [
				{
					label: "Minimize",
					role: "minimize"
				},
			]
	},
	{
		label: "Help",
			submenu: [
				{
					label: "Report an issue",
				},
				{
					label: "Feedback",
				}
			]
	} 
];


 module.exports = {macMenuTemplate, winMenuTemplate};