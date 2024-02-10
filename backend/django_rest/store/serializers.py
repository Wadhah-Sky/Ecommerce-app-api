"""Define the serializers for you views"""

from rest_framework import serializers

from core.models import (Category, Attribute)

# Note: the calling of serializer inside another one called 'Nested
#       relationships'.


# class RecursiveField(serializers.Serializer):
#     """serialize recursive class to serialize self-referential models"""
#
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(
#             value,
#             context=self.context
#         )
#         return serializer.data


class CategoryChildSerializer(serializers.ModelSerializer):
    """Serialize class of Product model"""

    class Meta:
        """Serialize specific model fields"""

        model = Category
        fields = [
            'title',
            'slug'
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Serialize class of Category model"""

    # Note: this class's model has reverse self-referential, in order to use
    # this relationship (related_name) we need to include into this serializer
    # fields[].

    # Important: in Serializing Self Referential Model Recursively, you can't
    # use the following code:
    #
    # leaf_nodes = CategorySerializer(many=True, read_only=True)
    #
    # Because as this code line shown above of the class is reached, until then
    # CategorySerializer is not completely defined and this makes it as
    # compile time error.
    # To solve this issue choose one way from the listed ones below:
    # 1- define a function and call the class from it with the related instance
    #    to get serialize.
    # 2- create a recursive class (RecursiveField) as shown above in this file.
    # 3- create another class before this one to serialize the related
    #    instance.
    #
    # Take in consideration that method 1 and 2 can't control the depth of
    # serialization UNLESS you call to a child serializer class to serialize
    # your model instance/instances.

    class Meta:
        """Serialize specific model fields"""

        model = Category
        fields = [
            'title',
            'slug',
            'thumbnail',
            'icon',
            'leaf_nodes'
        ]
        # Define a list of read only fields.
        # read_only_fields = []

    # Define related/reverse model fields.
    # Note: if you use 'fields' list in Meta class rather than 'exclude' list,
    #       then you need to declare all related/reverse model fields in the
    #       'fields' list.
    # Note: 'StringRelatedField' will return the string representation for
    #       relational object/objects, if the object is null/blank will
    #       return null.
    # leaf_nodes = CategoryChildSerializer(many=True, read_only=True)
    leaf_nodes = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_leaf_nodes(self, instance):
        """Return all children of instance"""

        # Note: You have multiple ways to achieve what you need :
        #
        # 1- You can use get_children() method of MPTTModel:
        leaf_nodes = instance.get_children().filter(is_active=True)
        #
        # 2- You can use related_name of ForeignKey (it's 'leaf_nodes' in our
        #    Category model class of parent field) to serialize reverse
        #    relation of ForeignKey field, take in concern this way could cause
        #    error:
        #
        #    'ReverseManyToOneDescriptor' object has no attribute 'filter'
        #
        #    in case trying to use it to call the same serializer class (not
        #    a child serializer class).
        # leaf_nodes = Category.leaf_nodes.filter(is_active=True)
        #
        # 3- You can make direct queryset to related model class and fiter what
        #    you need:
        # leaf_nodes = Category.objects.filter(parent=instance, is_active=True)

        # Return only one level of children for current category instance, so
        # use a child serializer NOT the same serializer class because you
        # can't control the depth of children in this case.
        return CategoryChildSerializer(
            instance=leaf_nodes,
            many=True,
            read_only=True
        ).data

    def get_thumbnail(self, instance):
        """Return thumbnail url"""

        if instance.thumbnail:
            return instance.thumbnail.url


class CategoryDetailsSerializer(CategorySerializer):
    """Serialize class of Category model"""

    def ancestor_nodes(self, instance):
        """Return all ancestors of instance, including the instance itself"""

        # Get all the ancestor model instances including current instance.
        ancestor_nodes = instance.get_ancestors(include_self=True).filter(
            is_active=True
        )

        # Serialize the 'ancestor_nodes' list.
        return CategoryChildSerializer(
            instance=ancestor_nodes,
            many=True,
            read_only=True
        ).data

    def to_representation(self, instance):
        """Custom representation field to add to each returned instance"""

        # Note: this method DON'T require to declare the returned fields into
        # 'fields' list that defined in Meta class, and it's work similar to
        # SerializerMethodField() method.

        to_ret = super().to_representation(instance)

        to_ret['ancestor_nodes'] = self.ancestor_nodes(instance)

        return to_ret


class AttributeChildSerializer(serializers.ModelSerializer):
    """Serialize class of AttributeOption model"""

    class Meta:
        """Serialize specific model fields"""

        model = Attribute
        fields = [
            'title'
        ]


class AttributeSerializer(serializers.ModelSerializer):
    """Serialize class of Attribute model"""

    class Meta:
        """Serialize specific model fields"""

        model = Attribute
        fields = [
            'title',
            'input_class',
            'display_order',
            'options'
        ]

    # Define related/reverse model fields.
    options = serializers.SerializerMethodField()

    def get_options(self, instance):
        """Return list of attributes title that are connected to specific group
         of categories for filtering"""

        # Get category_slug from the view request.
        # kwarg_category_slug = self.context.get(
        #     'request'
        # ).parser_context['kwargs']['category_slug']

        # Get the context of 'category_ancestors' that we add to the serializer
        # context of the view.
        category_ancestors = self.context.get('category_ancestors')

        # Get conditional descendant instances of attributes for current
        # instance ordered alphabetically.
        # Info: it's important to not return attributes that not connected to
        #       product.
        # Note: get_descendants() doesn't include the current instance.
        attributes = instance.get_descendants().filter(
            category_attributes_attribute__category__in=category_ancestors,
            product_attributes_attribute__product__isnull=False
        ).distinct()

        # initialize an empty list.
        pk_list = []

        # Loop over returned attribute instances to get family of each one.
        for attribute in attributes:
            # Add the title of instance to the list as parent and child
            # title, in case its parent is a root node, otherwise use the
            # parent title.
            # if attribute.parent.is_root_node():
            #     options.append(
            #         {
            #             'child_title': attribute.title
            #         }
            #     )
            # elif attribute.parent.parent.is_root_node():
            #     options.append(
            #         {
            #             'child_title': attribute.parent.title,
            #             'grandchild_title': attribute.title
            #         }
            #     )
            # else:
            #     options.append(
            #         {
            #             'child_title': attribute.parent.parent.title,
            #             'grandchild_title': attribute.parent.title
            #         }
            #     )

            # Add the (level=1) in tree family instances for current attribute
            # ancestor.
            # Note: get_family() is iterable while get_root() is not.
            pk_list += [
                item.pk for item in attribute.get_family().filter(level=1)
            ]

        # Get attributes instances for non-duplicated pk and sort them.
        sorted_attributes = Attribute.objects.filter(
            pk__in=set(pk_list)
        ).order_by('display_order').only('title')

        # Loop over query of instances and get only title value.
        options = [item.title for item in sorted_attributes]

        # Return the sorted list of non-duplicated titles of attributes (level
        # 1) as options.
        return options
