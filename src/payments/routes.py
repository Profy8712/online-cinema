from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from .schemas import PaymentSchema, PaymentCreateSchema
from .crud import create_payment
from .stripe_utils import create_stripe_checkout_session

router = APIRouter(prefix="/payments", tags=["payments"])

def get_current_user_id():
    # TODO: Replace with actual authentication
    return 1

@router.post("/checkout-session")
async def create_checkout_session(
    data: PaymentCreateSchema,
):
    # URLs для редиректа после оплаты
    success_url = "https://your-domain.com/payment-success"
    cancel_url = "https://your-domain.com/payment-cancel"
    session = create_stripe_checkout_session(
        amount=float(data.amount),
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"order_id": str(data.order_id)},
    )
    return {"checkout_url": session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request, session: AsyncSession = Depends(get_async_session)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    import stripe, os
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        session_obj = event["data"]["object"]
        metadata = session_obj.get("metadata", {})
        order_id = int(metadata["order_id"])
        user_id = 1  # В реальном проекте — получи по order
        amount = float(session_obj["amount_total"]) / 100
        external_payment_id = session_obj["id"]
        await create_payment(session, user_id, order_id, amount, external_payment_id)
    return {"status": "success"}
