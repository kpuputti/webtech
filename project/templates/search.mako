<%inherit file="base.mako"/>

<h1>Flying Fist place search:</h1>

<p>
  <form id="search" action="/search" method="get" autocomplete="off">
    <input type="text" id="q" name="q" value="${query_raw}" />
    <input type="submit" value="Search" />
  </form>
</p>

% if not search:
<div id="description">
  <p>
    Flying Fist has over 21 000 places within the
    <a href="/flyingfist/2750405">the Kingdom of the
    Netherlands</a>. Just try typing in a place name and the
    autocompletion suggests words that are within the data store.
  </p>
  <p>Some example places to get you started:</p>
  <ul>
    <li><a href="/flyingfist/2750405">the Kingdom of the Netherlands</a></li>
    <li><a href="/flyingfist/2753919">Holland</a></li>
    <li><a href="/flyingfist/2756253">Eindhoven</a></li>
    <li><a href="/flyingfist/2759794">Amsterdam</a></li>
    <li><a href="/flyingfist/7113992">Rioolwaterzuiveringsinstallatie Apeldoorn</a></li>
  </ul>
</div>
% else:

<hr />

<% results = 'result' if hits == 1 else 'results' %>

<h2>Found ${hits} ${results} for "${query}":</h2>

<ul id="search-results">

  % for i, place in enumerate(places):

  % if i == 0:
  <li class="highlight">
  % else:
  <li>
  % endif

    <% info = place['info'] %>

    <a href="/flyingfist/${place['geoname_id']}">${place['label_hi']}</a>

    <span class="place-type">(${info['type']})</span>

    <span class="place-info">

    % if info.get('admin2Code', None) and info.get('admin1Code', None):

    in <a href="${info['admin2Code']}">${info['admin2CodeLabel']}</a>,
    <a href="${info['admin1Code']}">${info['admin1CodeLabel']}</a>

    % elif info.get('admin1Code', None):
    in <a href="${info['admin1Code']}">${info['admin1CodeLabel']}</a>

    % elif info.get('admin2Code', None):
    in <a href="${info['admin2Code']}">${info['admin2CodeLabel']}</a>

    % endif

    % if info.get('population', None):
    <br />population: ${info['population']}
    % endif

    </span>

    % if i == 0 and info.get('latitude', None) and info.get('longitude', None):

    <span class="place-info-map">
      <a href="/flyingfist/${place['geoname_id']}">
        <img src="http://maps.google.com/maps/api/staticmap?sensor=false&zoom=10&size=300x200&center=${info['latitude']},${info['longitude']}" />
      </a>
    </span>

    % endif

  </li>
  % endfor

</ul>

% endif
