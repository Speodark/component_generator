from utilities.db import components_count, get_all_components
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

def add_component_popup():
    return dbc.Modal(
        id='add-component-popup',
        size='lg',
        centered=True,
        children=html.Div(
            className='dashboard__add-component',
            children=[
                # The popup title
                html.Span(
                    className='dashboard__add-component--title',
                    children='Component name'
                ),
                # The input for the component name
                dcc.Input(
                    id='add-component-input',
                    className='dashboard__add-component--input',
                    type="text",
                    value='',
                    autoComplete='off'
                ),
                # If while trying to create a component there's an error this will show the error
                html.Span(
                    id='add-component-not-available',
                    className='dashboard__add-component--warning hide',
                    children=''
                ),
                # Create the component
                html.Button(
                    id='add-component-create-btn',
                    className='btn__blue dashboard__add-component--create-btn',
                    children='Create'
                ),
                # Cancel the component creation
                html.Button(
                    id='add-component-cancel-btn',
                    className='btn__red dashboard__add-component--cancel-btn',
                    children='Cancel'
                )
            ]
        ),
    )


def delete_component_popup():
    return dbc.Modal(
        id='delete-component-popup',
        size='sm',
        centered=True,
        children=html.Div(
            className='dashboard__delete-popup',
            children=[
                html.Span(
                    className='dashboard__delete-popup--title',
                    children='Are you sure you want to delete the component?'
                ),
                html.Span(
                    className='dashboard__delete-popup--warning',
                    children="You won't be able to retrieve the component information!"
                ),
                # Delete the component
                html.Button(
                    id='delete-component-btn',
                    className='btn__red dashboard__delete-popup--delete',
                    children='Delete'
                ),
                # Cancel
                html.Button(
                    id='cancel-component-delete-btn',
                    className='btn__blue dashboard__delete-popup--cancel',
                    children='Cancel'
                ),
            ]
        ),
    )


def rename_component_popup():
    return dbc.Modal(
        id='rename-component-popup',
        size='lg',
        centered=True,
        children=html.Div(
            className='dashboard__add-component',
            children=[
                # The popup title
                html.Span(
                    className='dashboard__add-component--title',
                    children='New Name'
                ),
                # The input for the component name
                dcc.Input(
                    id='rename-component-input',
                    className='dashboard__add-component--input',
                    type="text",
                    value='',
                    autoComplete='off'
                ),
                # If while trying to create a component there's an error this will show the error
                html.Span(
                    id='rename-component-not-available',
                    className='dashboard__add-component--warning hide',
                    children=''
                ),
                # Create the component
                html.Button(
                    id='rename-component-create-btn',
                    className='btn__green dashboard__add-component--create-btn',
                    children='Rename'
                ),
                # Cancel the component creation
                html.Button(
                    id='rename-component-cancel-btn',
                    className='btn__red dashboard__add-component--cancel-btn',
                    children='Cancel'
                )
            ]
        )
    )

def dashboard_components_section(session_maker):
    is_there_components = False
    first_components_dropdown_option = None
    with session_maker() as session:
        num_of_components = components_count(session)
        if num_of_components > 0: 
            is_there_components = True
    
    hide_elements_classname = ''
    add_component_btn_class = 'dashboard__components--add-component-btn'
    components_dropdown_options = []
    if not is_there_components:
        hide_elements_classname = 'hide'
        add_component_btn_class = 'dashboard__components--add-component-btn__while-none'
    else:
        with session_maker() as session:
            components_list = get_all_components(session)
            first_components_dropdown_option = components_list[0].id
            components_dropdown_options = [
                {'label': c.name, 'value': c.id} 
                for c in components_list
            ]
    return html.Div(
        className='dashboard__components',
        children=[
            # The Components dropdown
            dcc.Dropdown(
                options=components_dropdown_options,
                value=first_components_dropdown_option,
                className='dashboard__components--type ' + hide_elements_classname,
                id='components-dropdown',
                clearable=False,
            ),
            # Add component button
            html.Button(
                id='add-component',
                className='btn__blue center_items_vertical ' + add_component_btn_class,
                children='Add'
            ),
            # Delete component button
            html.Button(
                id='open-delete-component-popup',
                className='btn__red center_items_vertical ' + hide_elements_classname,
                children='Delete'
            ),
            # rename component button
            html.Button(
                id='rename-component',
                className='btn__green center_items_vertical ' + hide_elements_classname,
                children='Rename'
            ),
            # rename component button
            html.Button(
                id='export-component',
                className='btn__grey center_items_vertical ' + hide_elements_classname,
                children='Export'
            ),
            # rename component button
            html.Button(
                id='save-component',
                className='btn__grey center_items_vertical ' + hide_elements_classname,
                children='Save'
            ),
            # The add component popup
            add_component_popup(),
            # The confirm delete component popup
            delete_component_popup(),
            # rename component popup
            rename_component_popup()
        ]
    )