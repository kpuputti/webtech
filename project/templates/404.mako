<%inherit file="base.mako"/>

<%def name="title()">${status}</%def>

<h1>Resource not found.</h1>

<p>Message: "<em>${message}"</em></p>

<%def name="header()">
<form id="search" action="/search" method="get" autocomplete="off">
  <input type="text" id="q" name="q" />
  <input type="submit" value="Search" />
</form>
</%def>
