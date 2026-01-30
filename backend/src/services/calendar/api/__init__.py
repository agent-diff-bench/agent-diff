# API endpoint handlers for Calendar API
from .methods import (
    # Routes (without batch)
    routes as _method_routes,
    calendar_routes,
    calendar_list_routes,
    event_routes,
    acl_routes,
    channels_routes,
    colors_routes,
    freebusy_routes,
    settings_routes,
    # Request utilities
    get_user_id,
    get_user_email,
    get_request_body,
    get_query_params,
    get_if_match,
    get_if_none_match,
    # Handler wrapper
    api_handler,
    # Calendar handlers
    calendars_get,
    calendars_insert,
    calendars_update,
    calendars_patch,
    calendars_delete,
    calendars_clear,
    # CalendarList handlers
    calendar_list_list,
    calendar_list_get,
    calendar_list_insert,
    calendar_list_update,
    calendar_list_patch,
    calendar_list_delete,
    calendar_list_watch,
    # Event handlers (basic CRUD)
    events_list,
    events_get,
    events_insert,
    events_update,
    events_patch,
    events_delete,
    # Event handlers (advanced)
    events_import,
    events_move,
    events_quick_add,
    events_instances,
    events_watch,
    # ACL handlers
    acl_list,
    acl_get,
    acl_insert,
    acl_update,
    acl_patch,
    acl_delete,
    acl_watch,
    # Channel handlers
    channels_stop,
    # Color handlers
    colors_get,
    # FreeBusy handlers
    freebusy_query,
    # Settings handlers
    settings_list,
    settings_get,
    settings_watch,
)

from .batch import (
    batch_handler,
    batch_routes,
)

# Combined routes including batch
routes = _method_routes + batch_routes

__all__ = [
    # Routes
    "routes",
    "calendar_routes",
    "calendar_list_routes",
    "event_routes",
    "acl_routes",
    "channels_routes",
    "colors_routes",
    "freebusy_routes",
    "settings_routes",
    # Request utilities
    "get_user_id",
    "get_user_email",
    "get_request_body",
    "get_query_params",
    "get_if_match",
    "get_if_none_match",
    # Handler wrapper
    "api_handler",
    # Calendar handlers
    "calendars_get",
    "calendars_insert",
    "calendars_update",
    "calendars_patch",
    "calendars_delete",
    "calendars_clear",
    # CalendarList handlers
    "calendar_list_list",
    "calendar_list_get",
    "calendar_list_insert",
    "calendar_list_update",
    "calendar_list_patch",
    "calendar_list_delete",
    "calendar_list_watch",
    # Event handlers (basic CRUD)
    "events_list",
    "events_get",
    "events_insert",
    "events_update",
    "events_patch",
    "events_delete",
    # Event handlers (advanced)
    "events_import",
    "events_move",
    "events_quick_add",
    "events_instances",
    "events_watch",
    # ACL handlers
    "acl_list",
    "acl_get",
    "acl_insert",
    "acl_update",
    "acl_patch",
    "acl_delete",
    "acl_watch",
    # Channel handlers
    "channels_stop",
    # Color handlers
    "colors_get",
    # FreeBusy handlers
    "freebusy_query",
    # Settings handlers
    "settings_list",
    "settings_get",
    "settings_watch",
    # Batch handlers
    "batch_handler",
    "batch_routes",
]
