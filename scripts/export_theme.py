from qt_material import export_theme

extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'monoespace',
    'font_size': '13px',
    'line_height': '13px',

    # Density Scale
    'density_scale': '0',

}

export_theme(theme='dark_blue.xml', 
             qss='src/compas_view2/app/theme/dark_blue.qss', 
             rcc='src/compas_view2/app/theme/resources.rcc',
             output='src/compas_view2/app/theme/resources', 
             prefix='icon:/', 
             invert_secondary=False, 
             extra=extra,
            )