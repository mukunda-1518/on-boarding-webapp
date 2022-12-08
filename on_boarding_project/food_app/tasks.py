from celery import shared_task
from .models import *
import structlog


log = structlog.getLogger(__name__)


@shared_task
def create_order(data):
    item_ids = data['item_ids']  # Assuming all the items are in db
    store_id = data['store_id']  # Assuming store is in db
    store_obj = Store.objects.get(id=store_id)
    merchant_obj = store_obj.merchant
    user_obj = CustomUser.objects.get(id=data['user_id'])
    order_obj = Order.objects.create(store=store_obj, merchant=merchant_obj, user=user_obj)
    orders_list = []
    for item_id in item_ids:
        order_item = OrderItem(order=order_obj, item_id=item_id)
        orders_list.append(order_item)
    OrderItem.objects.bulk_create(orders_list)
    log.info("New order is created by the user: {}".format(user_obj.username))
    return order_obj


@shared_task
def add_new_item(data, store_id):
    item_obj = Item(**data)
    item_obj.save()
    StoreItem.objects.create(store_id=store_id, item=item_obj)
    log.info("New item: {} is added to the store: {}".format(item_obj.name, store_id))
    return item_obj
    

@shared_task
def add_new_store(data, user_id):
    store = Store(merchant_id=user_id, **data)
    store.save()
    log.info("store with name: {} is created by {}".format(store.name, store.merchant.name))
    return store