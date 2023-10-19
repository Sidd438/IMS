from rest_framework import serializers


from .models import Department, DepartmentMember, Item, ItemDepartmentMember


class ItemSerializer(serializers.ModelSerializer):
    total_stock = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ("static_id",)

    def get_total_stock(self, instance):
        return instance.total_stock


class DepartmentMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepartmentMember
        fields = (
            "static_id",
            "name",
        )


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ("static_id", "name")


class ItemDepartmentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDepartmentMember
        read_only_fields = ("static_id",)
