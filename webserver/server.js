const socketIO = require('socket.io');
const path = require('path');
const INDEX = path.join(__dirname, '/public/index.html');
const SUBMIT = path.join(__dirname, '/public/index.html');

const PORT = process.env.PORT || 3000;

var express = require('express');
var bodyParser = require('body-parser');
var multer = require('multer')
let {PythonShell} = require('python-shell')
var app = express();
var fs = require('fs');
var filepath = "./webserver/public/images/";
var urlencodedParser = bodyParser.urlencoded({ extended: false })



app.get('/', function (req, res) {
    res.sendFile(INDEX)
})

app.post('/contact', urlencodedParser, function (req, res) {
    console.log(req.body);
    filepath = "./webserver/public/images/";
    var result = JSON.stringify(req.body)
    var ar = result.split(",");
    var store = ar[0];
    var nameArr = store.split(":");
    var name = nameArr[1];
    var filename = "./json/" + name.slice(1, -1) + ".json"
    var string = "{" + name + ": [{"
    console.log(string);
    for( var i = 1; i < ar.length; ++i ) {
        string = string + ar[i] + ",";
    }
    string = string.slice(0, -1);
    string = string + "]}";
    fs.writeFile(filename, string, function(err) {
        if(err) {
            return console.log(err);
        }
        console.log("The file was saved!");
    });
    filepath = filepath + name.slice(1, -1);
    if (!fs.existsSync(filepath)){
            fs.mkdirSync(filepath);
    } 
    res.redirect('submit.html');
})

var Storage = multer.diskStorage({
    destination: function(req, file, callback) {
        callback(null, filepath);
    },
    filename: function(req, file, callback) {
        callback(null, Date.now() + "_" + file.originalname);
    }
});

var upload = multer({
    storage: Storage
}).array("imgUploader", 3); //Field name and max count

app.post("/api/Upload", function(req, res) {
     upload(req, res, function(err) {
         if (err) {
             return res.end("Something went wrong! Please navigate back to the previous page and try again");
         };
         return res.redirect('../../complete.html');  
     });
 });

app.post("/complete", function(req, res) {
    PythonShell.run('./webserver/facial.py', null, function (err){
        if (err) throw err;
        console.log('finished');
    })
    res.redirect('index.html');
});

 
app.use(express.static(__dirname + '/public'))
app.listen(3000, '0.0.0.0', function() {
    console.log('Listening to port:  ' + 3000);
});



