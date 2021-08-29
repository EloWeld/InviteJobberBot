# ======================= Authorize ======================= #
from yoomoney import Authorize

from src.data.config import YOOMONEY_CLIENT_ID, YOOMONEY_REDIR

Authorize(
    client_id=YOOMONEY_CLIENT_ID,
    redirect_uri=YOOMONEY_REDIR,
    scope=["account-info",
           "operation-history",
           "operation-details",
           "incoming-transfers",
           "payment-p2p",
           "payment-shop",
           ]
)