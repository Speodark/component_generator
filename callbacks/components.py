import dash
from dash import Input, Output, ctx, no_update, ALL, State
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import name_exists, add_component, components_count, get_all_components, delete_component_by_id, rename_component

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))

@dash.callback(
    ############################################ Outputs for all situations
    # Components dropdown classname
    Output('components-dropdown', 'className'),
    # Components dropdown options
    Output('components-dropdown', 'options'),
    # Components dropdown options
    Output('components-dropdown', 'value'),
    ############################################ END
    ############################################ Outputs for Add components
    # Pop up
    Output('add-component-popup', 'is_open'),
    # Popup component warning
    Output('add-component-not-available', 'children'),
    Output('add-component-not-available', 'className'),
    # show the dropdown and delete button if they were hidden because there were no components
    Output('open-delete-component-popup', 'className'),
    # Add component button classname
    Output('add-component', 'className'),
    # Rename button classname
    Output('rename-component', 'className'),
    # Export button classname 
    Output('export-component', 'className'),
    # Save changes button
    Output('save-component', 'className'),
    ############################################ END
    ############################################ Outputs for delete components
    # Delete confirm popup
    Output('delete-component-popup', 'is_open'),
    ############################################ END
    ############################################ Outputs for rename components
    # Delete confirm popup
    Output('rename-component-popup', 'is_open'),
    # Popup component warning
    Output('rename-component-not-available', 'children'),
    Output('rename-component-not-available', 'className'),
    ############################################ END
    ############################################ Inputs for Add components
    # Button to open the popup
    Input('add-component', 'n_clicks'),
    # cancel the component creation and closes the popup
    Input('add-component-cancel-btn', 'n_clicks'),
    # try to create the component and close the popup
    Input('add-component-create-btn', 'n_clicks'),
    ############################################ END
    ############################################ Inputs for Delete components
    # Delete component button to open the delete confirm popup
    Input('open-delete-component-popup', 'n_clicks'),
    Input('delete-component-btn', 'n_clicks'),
    Input('cancel-component-delete-btn', 'n_clicks'),
    ############################################ END
    ############################################ Inputs for rename components
    # Button to open the popup
    Input('rename-component', 'n_clicks'),
    # cancel the component creation and closes the popup
    Input('rename-component-cancel-btn', 'n_clicks'),
    # try to create the component and close the popup
    Input('rename-component-create-btn', 'n_clicks'),
    ############################################ END
    # The name of the new component
    State('add-component-input', 'value'),
    # The current classname of the popup warning
    State('add-component-not-available', 'className'),
    # The value the user want to rename its component
    State('rename-component-input', 'value'),
    # The current classname of the popup warning for rename popup
    State('rename-component-not-available', 'className'),
    # The current classnames of thee dropdown and delete button and add component button
    State('open-delete-component-popup', 'className'),
    State('components-dropdown', 'className'),
    State('add-component', 'className'),
    # Rename button classname
    State('rename-component', 'className'),
    # Export button classname 
    State('export-component', 'className'),
    # Save changes button
    State('save-component', 'className'),
    State('components-dropdown', 'value'),
    prevent_initial_call=True
)
def open_add_component_popup(
    _, 
    __, 
    ___, 
    delete_,
    delete__,
    delete___,
    rename_,
    rename__,
    rename___,
    # From here is the states
    name, 
    not_available_classname, 
    rename_value, 
    not_available_rename_classname, 
    delete_component_classname, 
    components_dropdown_classname,
    add_component_btn_classname,
    rename_component_btn_classname,
    export_component_btn_classname,
    save_component_btn_classname,
    components_dropdown_value
):
    # All the outputs names, this is done to prevent from making mistakes when returning because the big amount of outputs

    # every button can change the dropdown
    components_dropdown_classname_output = no_update # components dropdown classname 
    components_dropdown_options_output = no_update # The components dropdown options
    components_dropdown_value_output = no_update # The components dropdown value
    # only for the add component button
    pop_up_open_output = no_update # Popup is open?
    warning_text_output = no_update # Warning text
    warning_class_output = no_update # Warning class name
    delete_component_btn_classname_output = no_update # delete component classname
    add_component_btn_classname_output = no_update # The add component btn classname
    rename_component_btn_classname_output = no_update # The rename component btn classname
    export_component_btn_classname_output = no_update # The export component btn classname
    save_component_btn_classname_output = no_update # The save component btn classname
    # only for the rename component button
    rename_popup_open_output = no_update # rename Popup is open?
    rename_warning_text_output = no_update # rename Warning text
    rename_warning_class_output = no_update # rename Warning class name

    # Only for the delete component button
    delete_popup_open_output = no_update # Delete confirm popup is open?

    # Which id triggered the callback
    triggered_id = ctx.triggered_id

    ###################################################################### Add component section
    # If we clicked the add component button
    if triggered_id == 'add-component':
        pop_up_open_output = True
    # If we clickeed the cancel on the popup of the create component
    elif triggered_id == 'add-component-cancel-btn':
        pop_up_open_output = False
        warning_text_output = ''
        warning_class_output = not_available_classname if 'hide' in not_available_classname else not_available_classname + ' hide'
    # If we click on the create button in the create component popup
    elif triggered_id == 'add-component-create-btn':
        # Name checks
        # is the name empty?
        if not name:
            warning_text_output = 'You must provide a name'
            warning_class_output = not_available_classname.replace('hide', '').strip()
        # Is the name longer than 3 characters?
        elif len(name) < 3:
            warning_text_output = 'The name must be 3 characters or more'
            warning_class_output = not_available_classname.replace('hide', '').strip()
        else:
            # Checks if the name already exists in the database
            name_already_exists = False
            with session_maker() as session:
                name_already_exists = name_exists(name, session)
            if name_already_exists:
                warning_text_output = 'This name is already taken'
                warning_class_output = not_available_classname.replace('hide', '').strip()
            else:
                # If all good with the name checks
                # add component
                with session_maker() as session:
                    add_component(name, session)
                new_value = None
                dropdown_options = []
                with session_maker() as session:
                    if components_count(session) > 0:
                        components_list = get_all_components(session)
                        new_value = components_list[0].id
                        dropdown_options = [
                            {'label': c.name, 'value': c.id} 
                            for c in components_list
                        ]
                
                pop_up_open_output = False 
                warning_text_output = '' 
                warning_class_output = not_available_classname if 'hide' in not_available_classname else not_available_classname + ' hide' 
                rename_component_btn_classname_output = rename_component_btn_classname.replace('hide', '').strip()
                export_component_btn_classname_output = export_component_btn_classname.replace('hide', '').strip()
                save_component_btn_classname_output = save_component_btn_classname.replace('hide', '').strip()
                delete_component_btn_classname_output = delete_component_classname.replace('hide', '').strip() 
                components_dropdown_classname_output = components_dropdown_classname.replace('hide', '').strip() 
                components_dropdown_options_output = dropdown_options 
                components_dropdown_value_output = new_value
                add_component_btn_classname_output = add_component_btn_classname.replace(
                    'dashboard__components--add-component-btn__while-none', 
                    'dashboard__components--add-component-btn'
                ).strip() 
    ###################################################################### END

    ###################################################################### DELETE COMPONENT SECTION
    if triggered_id == 'open-delete-component-popup':
        delete_popup_open_output = True
    elif triggered_id == 'cancel-component-delete-btn':
        delete_popup_open_output = False
    elif triggered_id == 'delete-component-btn':
        delete_popup_open_output = False
        with session_maker() as session:
            delete_component_by_id(components_dropdown_value, session)
        new_value = None
        dropdown_options = []
        with session_maker() as session:
            if components_count(session) > 0:
                components_list = get_all_components(session)
                new_value = components_list[0].id
                dropdown_options = [
                    {'label': c.name, 'value': c.id} 
                    for c in components_list
                ]
                delete_popup_open_output = False 
                components_dropdown_options_output = dropdown_options 
                components_dropdown_value_output = new_value
            else:
                components_dropdown_options_output = [] 
                components_dropdown_value_output = None
                rename_component_btn_classname_output = rename_component_btn_classname + ' hide'
                export_component_btn_classname_output = export_component_btn_classname + ' hide'
                save_component_btn_classname_output = save_component_btn_classname + ' hide'
                delete_component_btn_classname_output = delete_component_classname + ' hide'
                components_dropdown_classname_output = components_dropdown_classname + ' hide'
                add_component_btn_classname_output = add_component_btn_classname.replace(
                    'dashboard__components--add-component-btn',
                    'dashboard__components--add-component-btn__while-none'
                ).strip() 
    ###################################################################### END
    ###################################################################### Rename component section
    # If we clicked the add component button
    if triggered_id == 'rename-component':
        rename_popup_open_output = True
    # If we clickeed the cancel on the popup of the create component
    elif triggered_id == 'rename-component-cancel-btn':
        rename_popup_open_output = False
        rename_warning_text_output = ''
        rename_warning_class_output = not_available_rename_classname if 'hide' in not_available_rename_classname else not_available_rename_classname + ' hide'
    # If we click on the create button in the create component popup
    elif triggered_id == 'rename-component-create-btn':
        # Name checks
        # is the name empty?
        if not rename_value:
            rename_warning_text_output = 'You must provide a name'
            rename_warning_class_output = not_available_rename_classname.replace('hide', '').strip()
        # Is the name longer than 3 characters?
        elif len(rename_value) < 3:
            rename_warning_text_output = 'The name must be 3 characters or more'
            rename_warning_class_output = not_available_rename_classname.replace('hide', '').strip()
        else:
            # Checks if the name already exists in the database
            name_already_exists = False
            with session_maker() as session:
                name_already_exists = name_exists(rename_value, session)
            if name_already_exists:
                rename_warning_text_output = 'This name is already taken'
                rename_warning_class_output = not_available_rename_classname.replace('hide', '').strip()
            else:
                dropdown_options = []
                with session_maker() as session:
                    rename_component(components_dropdown_value, rename_value, session)
                    components_list = get_all_components(session)
                    dropdown_options = [
                        {'label': c.name, 'value': c.id} 
                        for c in components_list
                    ]
                
                rename_popup_open_output = False 
                rename_warning_text_output = '' 
                rename_warning_class_output = not_available_rename_classname if 'hide' in not_available_rename_classname else not_available_rename_classname + ' hide' 
                components_dropdown_options_output = dropdown_options 
    ###################################################################### END
    

    # The order is a must! do not switch around unless you are sure!
    return (
        components_dropdown_classname_output, # components dropdown classname 
        components_dropdown_options_output, # The components dropdown options
        components_dropdown_value_output, # The components dropdown value
        pop_up_open_output, # Popup is open?
        warning_text_output, # Warning text
        warning_class_output, # Warning class name
        delete_component_btn_classname_output, # delete component classname
        add_component_btn_classname_output, # The add component btn classname
        rename_component_btn_classname_output, # The rename component btn classname
        export_component_btn_classname_output, # The export component btn classname
        save_component_btn_classname_output, # The save component btn classname
        delete_popup_open_output, # is the delete popup open?
        rename_popup_open_output, # rename Popup is open?
        rename_warning_text_output, # rename Warning text
        rename_warning_class_output, # rename Warning class name
    )