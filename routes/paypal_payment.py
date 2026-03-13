from flask import Blueprint, redirect, url_for, request, session
import paypalrestsdk

paypal_bp = Blueprint("paypal", __name__)

paypalrestsdk.configure({
    "mode": "sandbox",  # change to live later
    "client_id": "AZ54IdovTCLMmdY8aJ7h3iRyBYeqSCdya5H2ARpHhB3-o9CHvFp43TIM-9u0qQa9pl06MXGVQksx9MQ4",
    "client_secret": "EK-44bRbJl0DCatTu6WFtizM0QqHg-_IxEIhvkhdWfGx3fDsTtSGg1nFlJ8AECxpBu7idmbN1T6ygQRD"
})


@paypal_bp.route("/paypal_pay")
def paypal_pay():

    cart = session.get("cart", {})

    total = sum(item["price"] * item["quantity"] for item in cart.values())

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for("paypal.payment_success", _external=True),
            "cancel_url": url_for("cart.checkout", _external=True)
        },
        "transactions": [{
            "amount": {
                "total": str(total),
                "currency": "USD"
            },
            "description": "Flask Store Order"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)

    return "Payment error"

@paypal_bp.route("/paypal_success")
def payment_success():

    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):

        session.pop("cart", None)

        return "Payment successful"

    return "Payment failed"