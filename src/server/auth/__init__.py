from .authenticator import Authenticator
from .authorizer import Authorizer


# Expose the methods as module-level functions for backward compatibility
verify_password = Authenticator.verify_password
get_user = Authenticator.get_user
authenticate_user = Authenticator.authenticate_user
create_user = Authenticator.create_user
create_access_token = Authorizer.create_access_token
get_current_user = Authorizer.get_current_user
