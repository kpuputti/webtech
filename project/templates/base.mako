<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>${self.title()} | Flying Fist</title>
    <link rel="stylesheet" type="text/css" href="/static/css/styles.css" />
    <link rel="stylesheet" type="text/css" href="/static/js/lib/jquery-ui/css/black-tie/jquery-ui-1.8.1.custom.css" />
</head>
<body>
  <div id="container">
    ${self.body()}
  </div>
  <script type="text/javascript" src="/static/js/lib/jquery-1.4.2.min.js"></script>
  <script type="text/javascript" src="/static/js/lib/jquery-ui/js/jquery-ui-1.8.1.custom.min.js"></script>
  <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
  <script type="text/javascript" src="/static/js/scripts.js"></script>
  ${self.footer()}
</body>
</html>

<%def name="title()">Main</%def>
<%def name="footer()"></%def>
