<%inherit file="base.mako"/>

<%def name="title()">${label}</%def>

<%def name="header()">
<form id="search" action="/search" method="get" autocomplete="off">
  <input type="text" id="q" name="q" />
  <input type="submit" value="Search" />
</form>
</%def>

<%
if 'type' in info:
   ptype = info['type']['objectLabel']
else:
   ptype = 'unknown'
%>

<h1 class="place-header">${label}<br />
  <span class="place-type">(${ptype})</span>
</h1>

% if 'latitude' in info and 'longitude' in info:
<p id="toggle-wikipedia">
  <strong>Show on map</strong>:
  <input type="checkbox" />Wikipedia pages
</p>
<div id="map"></div>
% endif

<script type="text/javascript">
  var PLACE = ${info_str};
</script>

% if weather:

% if 'stationName' in weather:
<h3>Current weather conditions in weather station ${weather['stationName']}:</h3>
% else:
<h3>Current weather conditions:</h3>
% endif

<ul id="weather">

  % for k, v in weather:
  <li>
    <strong>${k}</strong>: ${v}
  </li>
  % endfor

</ul>

% endif

<h3>Properties:</h3>

<ul id="place-properties">

  % for key in sorted_keys:
  <li>

    <% prop = info[key] %>

    <strong>${prop['predicateLabel']}</strong>:

    % if prop['isLiteral']:
      % if prop['predicateLabel'] == 'alternate names':
        ${prop['object'].replace(',', ', ')}
      % else:
        ${prop['object']}
      % endif
    % elif prop['isLocal']:
      <a href="${prop['object']}">${prop['objectLabel']}</a>
    % else:
      label

    % endif

  </li>
  % endfor

</ul>

% if related:

<h3>Related places:</h3>

<ul>

  % for uri, clabel, plabel in related:

  <li>
    <a href="${uri}">${clabel}</a> as ${plabel}
  </li>

  % endfor

</ul>

% endif
