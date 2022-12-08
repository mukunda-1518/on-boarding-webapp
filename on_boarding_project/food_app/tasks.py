from celery import shared_task
from .models import *
import structlog
from tastypie import http

log = structlog.getLogger(__name__)


@shared_task
def create_order(data):
    store_id = data['store_id'] 
    try:
       store_obj = Store.objects.get(id=store_id) 
    except Store.DoesNotExist:
        raise http.HttpNotFound()
    
    item_ids = data['item_ids']  
    item_objs = Item.objects.filter(id__in=item_ids)
    if len(item_ids) != len(item_objs):
        raise http.HttpNotFound()
    
    merchant_obj = store_obj.merchant
    user_obj = CustomUser.objects.get(id=data['user_id'])
    order_obj = Order.objects.create(store=store_obj, merchant=merchant_obj, user=user_obj)
    orders_list = []
    for item_id in item_ids:
        order_item = OrderItem(order=order_obj, item_id=item_id)
        orders_list.append(order_item)
    OrderItem.objects.bulk_create(orders_list)
    log.info("order_created", order_id=order_obj.pk, user=user_obj.name)


@shared_task
def add_new_item(data, store_id):
    item_obj = Item(**data)
    item_obj.save()
    StoreItem.objects.create(store_id=store_id, item=item_obj)
    log.info("item_created", item_id=item_obj.pk, store_id=store_id)
    

@shared_task
def add_new_store(data, user_id):
    store = Store(merchant_id=user_id, **data)
    store.save()
    log.info("store_created", store_id=store.pk)