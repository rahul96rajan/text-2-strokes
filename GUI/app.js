const { app, BrowserWindow, ipcMain, Menu, dialog } = require("electron");
const path = require("path");
const customMenu = require("./menu");

let mainWindow;

const isWindows = process.platform === 'win32';
const isMac = process.platform === "darwin";

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 500,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: true,
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