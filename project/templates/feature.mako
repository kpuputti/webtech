<%inherit file="base.mako"/>

<h1>${label} (${uri})</h1>

<ul>
  % for predicate, tobject in data:
  <li>

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
