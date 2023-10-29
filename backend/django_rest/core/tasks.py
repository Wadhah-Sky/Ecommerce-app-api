"""Create your api tasks"""

from celery import shared_task

from django.db.models import Subquery
from django.core.exceptions import ObjectDoesNotExist

# from djmoney.money import Money

from core.models import (Category, ProductItem, Promotion, PromotionItem)

import logging


# Info: if you are trying to create/delete foreign key records from database
#       table, you need to select the foreign key field value using model
#       instance not an 'id' value.


@shared_task
def set_product_item_promotion(category_id, promotion_id):
    """Set/Update promotion to product_item in PromotionItem model class when
    post_save signal is emit"""

    try:
        # Get the wanted category model object depending on its primary key.
        category = Category.objects.get(pk=category_id)

        # Get a queryset of product items as model instances (only the 'id'
        # field value) those related to specific categories AND exclude the
        # ones those already connected to the provided promotion_id.

        # Note: Limiting a subquery to a single column (primary key, e.g. id)
        #       and search using (in) lookup expression, the subquery returns
        #       the leaf nodes of categories (including the current one in case
        #       itself is a leaf node).
        queryset = ProductItem.objects.filter(
            product__category__in=Subquery(
                category.get_leafnodes(include_self=True).values('pk')
            )
        ).exclude(
            promotion_items_product_item__promotion=promotion_id
        ).only('pk')

        # Get the model instance of promotion.
        promotion = Promotion.objects.get(pk=promotion_id)

    except ObjectDoesNotExist:
        return logging.exception(ObjectDoesNotExist)
    except Exception as e:
        return logging.exception(e)
    else:
        # Loop over every single product item of queryset.
        for instance in queryset:

            # Create a single record in PromotionItem model class using save()
            # or create() method:
            # 1- save() method, first needs to create model instance and then
            #    save it.
            # 2- create() method will create a model instance and save it
            #    automatically through model manager.
            try:
                PromotionItem.objects.create(
                    promotion=promotion,
                    product_item=instance
                )
            except Exception as e:
                logging.exception(e)


# @shared_task
# def set_product_list_and_deal_price(prod_item_id, currency, list_price,
#                                     deal_price):
#     """Update the related Product instance list and deal price values when
#     post_save signal is emit"""
#
#     # Note: update() doesn't run any save() methods on your models, or emit
#     # the pre_save or post_save signals (which are a consequence of calling
#     # save()), or honor the auto_now field option.
#
#     queryset = Product.objects.filter(product_items_product__id=prod_item_id)
#
#     # Check whether deal_price is None or not.
#     if deal_price:
#         # Convert the value of deal_price to be MoneyField (to store two
#         # values, the value itself and the currency).
#         deal_price = Money(deal_price, currency)
#
#     # Now update related instance in the database using update() method,
#     # and remember that update() method will not emit any signal.
#     queryset.update(
#         list_price=Money(list_price, currency),
#         deal_price=deal_price
#     )


# @shared_task
# def update_products_deal_price(offer_id):
#     """Update all products that have a specific offer by emit save() signal
#     for each Product model instance"""
#
#     # Note: update() doesn't run any save() methods on your models, or emit
#     # the pre_save or post_save signals (which are a consequence of calling
#     # save()), or honor the auto_now field option.
#
#     # Retrieve all Product instances that have sent offer id.
#     queryset = Product.objects.filter(offer=offer_id)
#
#     # Trigger save() signals for each instance of queryset.
#     for instance in queryset:
#         instance.save()
