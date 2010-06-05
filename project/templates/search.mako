<%inherit file="base.mako"/>

<h1>Flying Fist</h1>
<h2>Search results for "${query}" (${hits}):</h2>

<ul>

  % for geoname_id, label, score in places:
  <li>
    [${geoname_id}]: ${label}
  </li>
  % endfor

</ul>
