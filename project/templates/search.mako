<%inherit file="base.mako"/>

<h1>Flying Fist</h1>

<p>
  Search for places:
  <form action="/search" method="get" autocomplete="off">
    <input type="text" id="q" name="q" value="${query_raw}" />
    <input type="submit" value="Search" />
  </form>
</p>

% if search:

<h2>Search results for "${query}" (${hits}):</h2>

<ul>

  % for geoname_id, label, score in places:
  <li>
    [${geoname_id}]: ${label}
  </li>
  % endfor

</ul>

% endif
