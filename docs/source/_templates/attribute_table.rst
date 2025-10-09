.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Name
     - Description
   {% for member in members %}
   * - {{ member.name }}
     - {{ member.docstring }}
   {% endfor %}
