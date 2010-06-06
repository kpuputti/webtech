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
