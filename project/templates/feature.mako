<%inherit file="base.mako"/>

<%def name="title()">${label}</%def>

<h1>${label} (${uri})</h1>

<h2>As a subject:</h2>

<ul>
  % for subject, predicate, tobject in subject_data:
  <li>

    <strong>${label}</strong>

    -

    % if predicate['local']:
      <a href="${predicate['uri']}">${predicate['label']}</a>
    % else:
      ${predicate['label']}
    % endif

    -

    % if tobject.get('text', False):
      ${tobject['text']}
    % elif tobject['local']:
      <a href="${tobject['uri']}">${tobject['label']}</a>
    % else:
      ${tobject['label']}
    % endif

  </li>
  % endfor
</ul>

<h2>As an object:</h2>

<ul>
  % for subject, predicate, tobject in object_data:
  <li>

    % if subject['local']:
      <a href="${subject['uri']}">${subject['label']}</a>
    % else:
      ${subject['uri']}
    % endif

    -

    % if predicate['local']:
      <a href="${predicate['uri']}">${predicate['label']}</a>
    % else:
      ${predicate['label']}
    % endif

    -

    <strong>${label}</strong>

  </li>
  % endfor
</ul>
