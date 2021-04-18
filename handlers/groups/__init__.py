from .description import dispatcher
from .init import dispatcher
from .records import dispatcher
from .add_admins import dispatcher
from .add_users import dispatcher
from .remove_users import dispatcher
from .del_bot_messages import dispatcher
from .help import dispatcher
from .rec_messages import dispatcher

__all__ = ['dispatcher']
