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
app.get('/search', (req, res) => {
    var search = req.query.search; // saves user input
    var url = 'https://itunes.apple.com/search?term=' // the saved api link
    console.log
    axios.all(([axios.get(url+search),
    axios.get(`http://127.0.0.1:5000/rand`)]))// inserts the user input into api url to get he data
      .then(axios.spread((firstResponse, secondResponse)  => {
      var results = firstResponse.data?.results; // gets the results from the api in the apporiate format
      var len= results.length;
      var number = secondResponse.data;
      if (len < number)
          obj = results[-1].trackName
          else 
          obj= results[number].trackName
      const tagline = "Search away!";
      //console.log(results);
      console.log(results);
      console.log(len);
      console.log(obj);
      res.render('pages/index', { //renders the index page where the results are as well as tagline
        results: results,
        tagline: tagline,
        random: obj
      });
      }))
      });


app.get('/randint', function(req, res) {
  var search = req.query.search; // saves user input
    var url = 'https://itunes.apple.com/search?term=' // the saved api link
    console.log
    axios.all(([axios.get(url+search),
    axios.get(`http://127.0.0.1:5000/rand`)]))// inserts the user input into api url to get he data
      .then(axios.spread((firstResponse, secondResponse)  => {
      var results = firstResponse.data?.results; // gets the results from the api in the apporiate format
      var len= results.length;
      var number = secondResponse.data;
      if (len < number)
          obj = results[-1].trackName
          else 
          obj= results[number].trackName
      const tagline = "Search away!";
      //console.log(results);
      console.log(results);
      console.log(len);
      console.log(obj);
      res.render('pages/rand', { //renders the index page where the results are as well as tagline
        
        random: obj
      });
      }))
      });



app.listen(8080);

console.log('8080 is the magic port');