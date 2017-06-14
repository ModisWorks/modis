# Setup module databse
import module_database.inspectors as _inspectors
event_handlers = _inspectors.get_event_handlers()
required_perms = _inspectors.get_required_perms()
