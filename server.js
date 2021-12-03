// load the items needed to continue
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

var selectedID = "";
app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// home page 


app.get('/', function(req, res){
    res.render('pages/home'); // renders the home page
    });

    
    
// search page that contains api to get information and to display

app.get('/users', (req, res) => {
   
    console.log
    axios.get('http://127.0.0.1:5000/api/users/all')// inserts the user input into api url to get he data
        .then(response => {
        var results =response.data?.results; // gets the results from the api in the apporiate format
        
        console.log(results);
        res.render('pages/index', { //renders the index page where the results are as well as tagline
            results: results
          });
        })
      });
    


  

app.listen(8080);

console.log('8080 is the magic port');