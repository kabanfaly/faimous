import enum
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.audit_mixin import AuditMixin


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"


class User(AuditMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(
        db.Enum(GenderEnum, name="gender_enum", create_constraint=True),
        default=GenderEnum.male,
        nullable=False,
    )
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(10), default="fr")
    activated = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
