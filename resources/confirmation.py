import traceback
from time import time

from flask import make_response, render_template
from flask_restful import Resource

from libs.mail_gun import MailGunException
from libs.strings import getText
from models.confirmation import ConfirmationModel
from models.user import UserModel

from schemas.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """Return confirmation HTML page."""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": getText("confirmation_not_found")}, 404

        if confirmation.expired:
            return {"message": getText("confirmation_link_expired")}, 400

        if confirmation.confirmed:
            return {"message": getText("confirmation_already_confirmed")}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=confirmation.user.email), 200, headers)
        # todo info in we intent to load a page from another location
        # return redirect("http://localhost:300", code=302)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """Returns confirmations for a given user. USe for testing."""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": getText("user_not_found")}, 404

        return {
                   "current_time": int(time()),
                   "confirmation": [
                       confirmation_schema.dump(each)
                       for each in user.confirmation.order_by(ConfirmationModel.expire_at).all()
                   ],
               }, 200

    @classmethod
    def post(cls, user_id: int):
        """Resend confirmation email"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": getText("user_not_found")}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": getText("confirmation_already_confirmed")}, 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            # lazy=dynamic comes in handy here, as we are saving after user has been created before
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": getText("confirmation_resend_successful")}, 201
        except MailGunException as err:
            return {"message": str(err)}, 500
        except:
            traceback.print_exc()
            return {"message": getText("confirmation_resend_fail")}, 500





