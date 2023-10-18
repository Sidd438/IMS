import django_tables2 as tables
from django.utils.html import format_html


class OrderedColumn(tables.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, order_by=(kwargs["accessor"], "pk"))


class AlldepartmentMembersTable(tables.Table):
    name = tables.Column(
        empty_values={}, orderable=True, accessor="member"
    )

    status = tables.Column(
        empty_values={}, orderable=True, accessor="Item_department_member__status"
    )

    department = OrderedColumn(
        empty_values={}, orderable=True, accessor="department__name", verbose_name="department"
    )


    Item = tables.Column(
        empty_values={},
        orderable=True,
        accessor="Item_department_member__Item__name",
        verbose_name="Item",
    )

    dealloc = tables.TemplateColumn(
        empty_values={},
        orderable=False,
        template_name="department_view_dealloc_button.html",
        exclude_from_export=True,
    )

    checkout = tables.TemplateColumn(
        empty_values={},
        orderable=False,
        template_name="rec_checkout_department_checkbox.html",
        exclude_from_export=True,
    )

    class Meta:
        rowattrs = row_attrs = {"data-id": lambda record: record.static_id}
        template_name = "table_base.html"

    def render_status(self, value, record):
        color = "text-success"
        if value == None:
            value = "Unallocated"
            color = "text-warning"

        elif value == "Checked-out":
            color = "text-danger"

        return format_html(f"<div class='{color}'>{value}</div>")

    def value_status(self, value, record):
        return "Unallocated" if value is None else value

    def render_Item(self, value, record):
        return "-" if value == None else value


class departmentMembersTable(AlldepartmentMembersTable):
    leader = tables.Column(empty_values={}, orderable=True, accessor="is_leader")

    department = None

    class Meta:
        sequence = ("leader", "...")
        rowattrs = row_attrs = {"data-id": lambda record: record.static_id}
        template_name = "table_base.html"

    def render_leader(self, value, record):
        if record.is_leader:
            return format_html('<i class="fas fa-crown"></i>')
        else:
            return ""

    def value_leader(self, value, record):
        return "Yes" if record.is_leader else "No"


class ItemTable(tables.Table):
    name = tables.Column(empty_values={})
    occupied_space = tables.Column(empty_values={})
    available_space = tables.Column(empty_values={})
    total_capacity = tables.Column(empty_values={})
    view = tables.TemplateColumn(template_name="view_Item_button.html")

    class Meta:
        row_attrs = {"id": lambda record: str(record.static_id) + "_row"}
        template_name = "table_base.html"
        orderable = False

    def render_name(self, value, record):
        return record.name

    def render_occupied_space(self, value, record):
        return record.occupied_space

    def render_available_space(self, value, record):
        return record.available_space

    def render_total_capacity(self, value, record):
        return record.total_capacity


class MemberDetailsTable(tables.Table):
    name = tables.Column(empty_values={}, orderable=False)
    email = tables.Column(empty_values={}, orderable=False)
    college = tables.Column(empty_values={}, orderable=False)
    sports = tables.Column(empty_values={}, orderable=False)
    department = tables.Column(empty_values={}, orderable=False)

    class Meta:
        row_attrs = {"id": lambda record: str(record.static_id) + "_in_table"}
        template_name = "table_base.html"
        orderable = False

    def render_name(self, value, record):
        return record.member.profile.name

    def render_email(self, value, record):
        return record.member.profile.email

    def render_college(self, value, record):
        return record.member.profile.college.name

    def render_sports(self, value, record):
        member_sports = record.member.sports.all().values_list("name", flat=True)
        final_string = ", ".join(member_sports)
        return final_string

    def render_department(self, value, record):
        return record.department


class ItemdepartmentMemberDetailsTable(tables.Table):
    name = tables.Column(
        empty_values={}, accessor="department_member__member__profile__name", orderable=True
    )

    status = tables.Column(empty_values={}, orderable=True, accessor="status")

    email = tables.Column(
        empty_values={}, orderable=True, accessor="department_member__member__profile__email"
    )

    college = tables.Column(
        empty_values={},
        orderable=True,
        accessor="department_member__member__profile__college",
    )

    department = tables.Column(
        empty_values={}, orderable=True, accessor="department_member__department"
    )
    dealloc = tables.TemplateColumn(
        template_name="Item_department_dealloc_button.html", exclude_from_export=True
    )
    checkout = tables.TemplateColumn(
        template_name="rec_checkout_checkbox.html", exclude_from_export=True
    )

    class Meta:
        row_attrs = {"id": lambda record: str(record.static_id) + "_in_table"}
        template_name = "table_base.html"
        orderable = False

    def render_status(self, value, record):
        col = "success" if record.status == "Checked-in" else "danger"
        return format_html(f"<div class=text-{col}>{record.status}</div>")

    def value_status(self, value, record):
        return value


class AllocatedMembersTable(ItemdepartmentMemberDetailsTable):
    Item = tables.Column(empty_values={}, accessor="Item__name", orderable=True)

    class Meta:
        row_attrs = {"id": lambda record: str(record.static_id) + "_in_table"}
        template_name = "table_base.html"
        sequence = ("...", "dealloc", "checkout")
        orderable = False


class departmentListTable(tables.Table):
    department = tables.Column(empty_values={})
    total_members = tables.Column(empty_values={})
    leader = tables.Column(empty_values={})
    Items = tables.Column(empty_values={})
    view = tables.TemplateColumn(template_name="department_view_button.html")

    class Meta:
        row_attrs = {"id": lambda record: str(record.static_id) + "_row"}
        template_name = "table_base.html"
        orderable = False

    def render_total_members(self, value, record):
        return record.department_members.filter(member__verified_by_controllz=True).count()

    def render_leader(self, value, record):
        profile = record.department_members.filter(is_leader=True).first()
        if profile:
            return profile.member.profile.name
        return ""

    def render_Items(self, value, record):
        return format_html(
            "<br>".join(
                record.department_members.exclude(Item_department_member=None)
                .values_list("Item_department_member__Item__name", flat=True)
                .distinct()
            )
        )

    def render_department(self, value, record):
        return record.name


class ItemListTable(tables.Table):
    item_code = tables.Column(empty_values={}, orderable=False)
    item_name = tables.Column(empty_values={}, orderable=False)
    available_quantity = tables.Column(empty_values={}, orderable=False)

    class Meta:
        row_attrs = {"id": lambda record: str(record.static_id) + "_row"}
        template_name = "table_base.html"
        orderable = False

    def render_item_code(self, value, record):
        return record.item_code

    def render_item_name(self, value, record):
        return record.name

    def render_available_quantity(self, value, record):
        return record.present_quantity
