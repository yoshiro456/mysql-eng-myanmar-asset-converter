from objectbox.model import *

@Entity(id=1, uid=1)
class Dictionary:
    id = Id(id=1, uid=1001)
    word = Property(str, id=2, uid=1002)
    content = Property(str, id=3, uid=1003)

def get_objectbox_model():
    model = Model()
    model.entity(Dictionary, last_property_id=IdUid(3, 1003))
    model.last_entity_id = IdUid(1, 1)
    return model