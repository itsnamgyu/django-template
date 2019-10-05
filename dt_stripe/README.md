## DT-STRIPE

Newer Stripe integration for the Django Template project, supporting token-based payments and subscriptions.

### Usage

- Copy Stripe API keys to `.env`.
- Enable webhooks to endpoint `<dt-stripe url base>/webhooks`, or `https://mysite.com/dt-stripe/webhooks` by default.
  - As of Oct 5th, 2019, we don't have any webhooks enabled.

### Products, Plans, SKUs

These can be created from dt_stripe. There is an option to fetch ALL objects from Stripe.

### Customers, Subscriptions, Orders

These will be created and stored in dt_stripe. Communication is mostly one-way (dt_stripe -> Stripe),
with the exception of Subscription cancellations.

Subscription cancellations will be handled via webhooks. Cancelled subscriptions are marked as
cancelled. To renew a subscription, the user must initialize a new subscription. When they do, the
old subscription is discarded from dt_stripe.