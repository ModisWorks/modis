# Setup module databse
import module_database.inspectors
event_handlers = inspectors.get_event_handlers()
required_perms = inspectors.get_required_perms()
