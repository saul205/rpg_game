import DB as db
import DB.Entities.PlayerEntity
import DB.Entities.ItemEntity
import DB.Entities.ConsumableEntity


db.Base.metadata.create_all(db.engine)
