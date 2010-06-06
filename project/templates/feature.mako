<%inherit file="base.mako"/>

<%def name="title()">${label}</%def>

<div id="header">

  <h1>${label}<br />
    <span class="place-type">(${info['type']['objectLabel']})</span>
  </h1>

  <form id="search" action="/search" method="get" autocomplete="off">
    <input type="text" id="q" name="q" />
    <input type="submit" value="Search" />
  </form>

</div>

% if 'latitude' in info and 'longitude' in info:
<div id="map"></div>
% endif

<script type="text/javascript">
  var PLACE = ${info_str};
</script>

<ul id="place-properties">

  % for key in sorted_keys:
  <li>

    <% prop = info[key] %>

    <strong>${prop['predicateLabel']}</strong>:

    % if prop['isLiteral']:
    ${prop['object']}
    % elif prop['isLocal']:
    <a href="${prop['object']}">${prop['objectLabel']}</a>
    % else:
    ${prop['objectLabel']}
    % endif

  </li>
  % endfor

</ul>
