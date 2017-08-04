;(function() {

  // Require express node module
  var express = require('express');
  // Access environment variables in Node.js
  // In Heroku, it will be defined by Heroku
  // If no port specified, fallback to 9000 (Localhost case)
  const PORT = process.env.PORT || 9000;

  // New express app
  var app = express();

  // Express Middleware:
  // Route everything to http only
  app.use(function(req, res, next) {
    // Fixing Localhost: Use check redirect only on https, not http
    if (req.headers['x-forwarded-proto'] === 'https') {
      res.redirect('http://' + req.hostname + req.url); // Redirect https to http.
    }
    else next();
  });

  // Express Middleware:
  // Static serving
  app.use(express.static('.'));

  // Start server: PORT || 9000
  app.listen(PORT, function() {
    console.log("Express server is up on port " + PORT);
  });
})();