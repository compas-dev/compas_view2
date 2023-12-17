{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block methods %}
    .. rubric:: Methods

    .. autosummary::
        :toctree:
        :nosignatures:
    {% for item in methods %}
    {% if item not in inherited_members %}
        ~{{ name }}.{{ item }}
    {% endif %}
    {%- endfor %}

    {% endblock %}
