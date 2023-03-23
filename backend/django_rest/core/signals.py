"""Create api signals"""

# Important: Signals are implicit function calls which make debugging harder.
#            If the sender and receiver of your custom signal are both within
#            your project, you’re better off using an explicit function call.

from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify


from core.models import (User, Category, Attribute, PromotionCategory, Banner,
                         Card, PurchaseOrder, Product, ProductItem,
                         ProductAttribute, ProductItemAttribute,
                         ProductItemImage)
from core.tasks import (set_product_item_promotion)

import string
import random

# Import inspect module that provides several useful functions to help get
# information about live objects such as modules, classes, methods, functions,
# tracebacks, frame objects, and code objects.
import inspect


# Note: take in consideration the synchronizing issue of signal methods
#       since Django run its methods in synchronize.

# Note: Remember the use cases: We use post_save when we are interested more
#       in the creation of a model instance without modifying the values, while
#       we use pre_save when we are more into the monitoring the change in
#       model instance’s value, or if we are into modifying the instance’s
#       attribute’s values ourselves.

# Note: if you are trying to send foreign key (id) to a celery task, you can't
#       do it like:
#
#       <celery_task_name>.delay(instance.<foreign_key_name>)
#
#       This will raise an exception saying:
#
#       Object of type <foreign_key_name> is not JSON serializable
#
#       So you have to use the field (property) name of primary key like (id):
#
#       <celery_task_name>.delay(instance.<foreign_key_name>.id)


def create_slug(value):
    """Method to create a slug for model instance"""

    slug = slugify(value)
    random_string = get_random_string(length=8)
    return slug + '-' + random_string


def get_request_obj():
    """Function to return thread current request object from its stack"""

    # Info: there are two ways to get request object outside views.py methods:
    # 1- Thread-local storage (TLS): is a computer programming method that uses
    #    static or global memory local to a thread. We use it just for this
    #    purpose (storing subdomain model in the context global to the current
    #    request from middleware) and it works perfectly. But it came with
    #    consequences because it is global variables and as we know global
    #    variables can be hacked and changed through code injection attacks.
    #
    # 2- As far as I can tell, the 'post_save' and 'pre_save' signal handlers
    #    are called synchronously in the thread that calls save(). If we are in
    #    the normal request handling loop, then we can just walk up the stack
    #    to find the request object as a local variable somewhere as shown
    #    below:

    # Initialize an variable.
    request = None

    # We loop through frame records of the stack for the current thread and
    # search for get_response object and pick up the request object.
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break

    if request:
        return request

    else:
        return None


@receiver(pre_save, sender=User)
def set_slug_to_user(sender, instance, *args, **kwargs):
    """Create a slug for User object when pre_save signal is emit"""

    # if instance is exists (means instance object is created or trying to
    # create but not saved yet).
    if instance:
        instance.slug = create_slug(instance.username)


@receiver(pre_save, sender=Category)
def set_slug_to_category(sender, instance, *args, **kwargs):
    """Create a slug for category instance when pre_save signal is emit"""

    # if instance is exists (means instance object is created or trying to
    # create but not saved yet) and Not have 'slug' value (we  don't want to
    # re-create slug value for instance that already have one like when you are
    # trying to update the instance).
    if instance and not instance.slug:
        instance.slug = create_slug(instance.title)


@receiver(pre_save, sender=Attribute)
def set_slug_to_category(sender, instance, *args, **kwargs):
    """Create a slug for attribute instance when pre_save signal is emit"""

    if instance and not instance.slug:
        instance.slug = create_slug(instance.title)


@receiver(post_save, sender=PromotionCategory)
def set_promotion_to_product_item(sender, instance, created, **kwargs):
    """Set/Update PromotionItem instances those related to this instance
    Category using celery task"""

    if instance:

        # Add task to job queue.
        set_product_item_promotion.delay(
            instance.category.id,
            instance.promotion.id
        )


@receiver(pre_save, sender=Banner)
def set_slug_to_banner(sender, instance, *args, **kwargs):
    """Create a slug for Banner instance when pre_save signal is emit"""

    if instance:
        instance.slug = create_slug(instance.title)


@receiver(pre_save, sender=Card)
def set_slug_to_card(sender, instance, *args, **kwargs):
    """Set the slug for Card object when pre_save signal is emit"""

    if instance:
        instance.slug = create_slug(instance.title)


@receiver(pre_save, sender=Product)
def set_slug_to_product(sender, instance, *args, **kwargs):
    """Create a slug for product instance when pre_save signal is emit"""

    if instance:
        instance.slug = create_slug(instance.title)


@receiver(pre_save, sender=ProductItem)
def set_sku_to_product_item(sender, instance, *args, **kwargs):
    """Create (Stock Keeping Unit) value for product item instance when
    pre_save signal is emit"""

    if instance and not instance.sku:

        # Our formula for sku (Stock Keeping Unit) field:
        # sku (12) = category_title(3)-product_title(4)-random(3)

        # Get the first 3 characters of product.category.title (without spaces)
        category_t = instance.product.category.title
        category_title = category_t.replace(" ", "")[:3]

        # Get the first 4 characters of product.title (without spaces)
        product_t = instance.product.title
        product_title = product_t.replace(" ", "")[:4]

        # Format the first part
        first_part = "{}-{}".format(category_title, product_title)

        # Count the length of the random Characters.
        # Note: We minus 1 as space for the (-) dash character before random
        #       part.
        random_char_length = (12 - len(first_part)) - 1

        # Generate random string(characters and digits)
        random_part = "".join(
            random.choices(
                string.ascii_letters + string.digits, k=random_char_length
            )
        )

        # Format first part with random part
        char = "{}-{}".format(first_part, random_part)

        # Set the formula we made as sku field's value as uppercase.
        instance.sku = char.upper()


@receiver(pre_save, sender=ProductItem)
def set_slug_to_product_item(sender, instance, *args, **kwargs):
    """Create a slug for product's item instance when pre_save signal is
    emit"""

    if instance:
        instance.slug = create_slug(instance.sku)


@receiver(pre_save, sender=ProductItemImage)
def set_slug_to_product_item_image(sender, instance, *args, **kwargs):
    """Create a slug for product item image instance when pre_save signal is
    emit"""

    if instance and not instance.slug:
        instance.slug = create_slug(instance.product_item.sku)


@receiver(pre_save, sender=ProductAttribute)
def set_slug_to_product_attribute(sender, instance, *args, **kwargs):
    """Create slug for product attribute instance when pre_save signal is
    emit"""

    if instance:
        instance.slug = create_slug(instance.attribute.title)


@receiver(pre_save, sender=ProductItemAttribute)
def set_slug_to_product_item_attribute(sender, instance, *args, **kwargs):
    """Create a slug for product's item attribute instance when pre_save signal
     is emit"""

    if instance:
        instance.slug = create_slug(instance.product_attribute.attribute.title)


@receiver(pre_save, sender=PurchaseOrder)
def set_po_code_to_po(sender, instance, *args, **kwargs):
    """Generate the po_code for PO objects when pre_save signal is emit"""

    if instance and not instance.po_code:

        request = get_request_obj()

        if request:

            # the formula our system use to generate PO code:
            # Total characters = 24 :
            # Supplier.title(4)-User.last_name(4)-User.role(4)-
            # User.phone_number(last 4 char)-random number(up to 24)

            # Get the info you need from current user object of current thread.

            # Get the first 4 characters of supplier.title
            title = instance.supplier.title[:4]

            # Get the first 4 characters of user.last_name
            last_name = request.user.last_name[:4]

            # Get the first 4 characters of user.role
            role = request.user.role[:4]

            # Get the last 4 digit of user.phone_number
            phone_number = str(request.user.phone_number)[-4:]

            # Format the first part of formula.
            first_part = "{}-{}-{}-{}".format(
                title,
                last_name,
                role,
                phone_number
            )

            # Count the length of the random Characters.
            # Note: We minus 1 as space for the (-) dash character before
            #       random part.
            random_char_length = (24 - len(first_part)) - 1

            # Generate random string(characters and digits)
            random_part = "".join(
                random.choices(
                    string.ascii_letters + string.digits, k=random_char_length
                )
            )

            # Format first part with random part
            char = "{}-{}".format(first_part, random_part)

            # Set the formula we made as po_code field's value as uppercase.
            instance.po_code = char.upper()

        else:
            raise Exception(
                "There is no request object detected in thread stack!"
            )


# @receiver(m2m_changed, sender=models.Section.cards.through)
# def card_changed(sender, instance, action, pk_set, **kwargs):
#     """Raise django exception when a certain error happen"""
#
#     <Your code>
#
#
# @receiver(pre_save, sender=ColorGroup)
# def add_slug_to_color_group(sender, instance, *args, **kwargs):
#     """Create a slug for ColorGroup object when pre_save signal is emit"""
#
#     if instance:
#         instance.slug = create_slug(instance.color_group_name)
#
#
# @receiver(pre_save, sender=Color)
# def add_slug_to_color(sender, instance, *args, **kwargs):
#     """Create a slug for Color object when pre_save signal is emit"""
#
#     if instance:
#         instance.slug = create_slug(instance.color_name)
#
#
# @receiver(pre_save, sender=ProductStyleVariation)
# def add_slug_to_product_style_variation(sender, instance, *args, **kwargs):
#     """Create a slug for ProductStyleVariation object when pre_save signal is
#      emit"""
#
#     if instance:
#         instance.slug = create_slug(instance.style.style_name)
#
#
# @receiver(pre_save, sender=ProductStyleVariation)
# def add_headline_to_product_style_variation(sender, instance, *args, **kwargs):
#     """Create or update headline of ProductStyleVariation"""
#
#     if instance:
#         if instance.product_details.brand:
#             instance.product_headline = \
#                 f'{str(instance.product_details.brand)}, ' \
#                 f'{instance.product_details.product_name}, {str(instance)}'
#         else:
#             instance.product_headline = \
#                 f'{instance.product_details.product_name}, {str(instance)}'
#
#
# @receiver(pre_save, sender=Product)
# def add_slug_to_product(sender, instance, *args, **kwargs):
#     """Create a slug for Product object when pre_save signal is emit"""
#
#     if instance:
#         instance.slug = create_slug(str(instance))
#
#
# @receiver(pre_save, sender=Product)
# def add_deal_price_to_product(sender, instance, *args, **kwargs):
#     """Create or update deal_price of product"""
#
#     if instance:
#         if instance.offer:
#             # Set 'discount' variable to round to closet integer without
#             # decimal value using round()
#             discount = round(
#                 (instance.list_price * instance.offer.offer_discount)/100
#             )
#             # Set 'deal_price' after subtracting 'discount' from 'list_price'.
#             instance.deal_price = instance.list_price - discount
#         else:
#             instance.deal_price = None
#
#
# @receiver(post_save, sender=Offer)
# def update_offer_products(sender, instance, created, **kwargs):
#     """Update related all offer's products when the offer is updated using
#     celery task"""
#
#     # We need the celery task to execute only when update an existing offer.
#     if not created:
#         # Add task to job queue.
#         update_products_deal_price.delay(instance.id)
#
#
# @receiver(pre_save, sender=ProductImage)
# def add_slug_to_product_image(sender, instance, *args, **kwargs):
#     """Create a slug for ProductImage object when pre_save signal is emit"""
#
#     if instance:
#         instance.slug = create_slug(str(instance))
