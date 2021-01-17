const { app, BrowserWindow, ipcMain, Menu, dialog } = require("electron");
const path = require("path");
const customMenu = require("./menu");

let mainWindow;

const isWindows = process.platform === 'win32';
const isMac = process.platform === "darwin";

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      // (NOT RECOMMENDED)
      // If true, we can skip attaching functions from ./menu-functions.js to window object in preload.js.
      // And, instead, we can use electron APIs directly in renderer.js
      // From Electron v5, nodeIntegration is set to false by default. And it is recommended to use preload.js to get access to only required Node.js apis.
      nodeIntegration: true
    },
    frame: isWindows ? false : true //Remove frame to hide default menu
  });
  

  // const menu = isMac?Menu.buildFromTemplate(customMenu.macMenuTemplate):Menu.buildFromTemplate(customMenu.winMenuTemplate);
  // Menu.setApplicationMenu(menu);
  
  mainWindow.loadFile("index.html");
	
  mainWindow.on("closed", function() {
    mainWindow = null;
  });
}

app.on('ready', function(){
  createWindow();
})


app.on("window-all-closed", function() {
	if (process.platform !== "darwin") app.quit();
});

// app.on("activate", function() {
//   if (mainWindow === null) createWindow();
// });



// Register an event listener. When ipcRenderer sends mouse click co-ordinates, show menu at that point.
// ipcMain.on(`display-app-menu`, function(e, args) {
//   if (mainWindow) {
//     menu.popup({
//       window: mainWindow,
//       x: args.x,
//       y: args.y
//     });
//   }
// });


ipcMain.on('buttonClicked', function(event) {
  // alert('hi');
  dialog.showErrorBox('error msg', 'demo of an error msg');
}) 
