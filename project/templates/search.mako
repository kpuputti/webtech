<%inherit file="base.mako"/>

<h1>Flying Fist</h1>

<p>
  Search for places:
  <form id="search" action="/search" method="get" autocomplete="off">
    <input type="text" id="q" name="q" value="${query_raw}" />
    <input type="submit" value="Search" />
  </form>
</p>

% if search:

<h2>Found ${hits} results for "${query}":</h2>

<ul>

  % for geoname_id, label, label_highlighted, score in places:
  <li>
    <a href="/flyingfist/${geoname_id}">${label_highlighted}</a>
  </li>
  % endfor

</ul>

% endif
