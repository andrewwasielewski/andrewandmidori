# andrewandmidori
----------

Wedding website hosted on AWS ([andrewandmidori.com](http://andrewandmidori.com))
 - Uses S3 to host static pages
 - RSVP POST requests are made to Amazon API Gateway
 - Lambda w/ proxy integration parses the POST payload and writes the relevant information to Google Sheets
