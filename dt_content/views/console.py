import json

from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect
from django.views.generic import *

from ..forms import *
from ..mixins import StaffMemberRequiredMixin
from ..models import *


class IndexView(StaffMemberRequiredMixin, TemplateView):
    template_name = "dt_content/console/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["static_section_count"] = ContentSection.static_objects.count()
        context["static_block_count"] = ContentBlock.static_objects.count()
        return context


class MenuListView(StaffMemberRequiredMixin, ListView):
    queryset = Menu.objects.filter(parent=None)
    context_object_name = "menu_list"
    template_name = "dt_content/console/menu_list.html"


class MenuCreateView(StaffMemberRequiredMixin, CreateView):
    form_class = MenuForm
    template_name = "dt_content/console/menu_create.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return (
            reverse("dt-content:menu-update", args=[self.object.id]) + "?success=true"
        )


class MenuUpdateView(StaffMemberRequiredMixin, UpdateView):
    model = Menu
    form_class = MenuForm
    slug_field = "id"
    context_object_name = "menu"
    template_name = "dt_content/console/menu_update.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        url = next_url or self.request.path
        return url + "?success=true"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.object.parent:  # if child menu, redirect to submenu update
            return redirect("dt-content:submenu-update", self.object.id)
        return response


class SubmenuCreateView(StaffMemberRequiredMixin, CreateView):
    form_class = SubmenuForm
    template_name = "dt_content/console/submenu_create.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        parent = request.GET.get("parent", None)
        if not parent:
            raise SuspiciousOperation
        try:
            self.parent = Menu.objects.get(id=parent)
        except Menu.DoesNotExist as e:
            raise SuspiciousOperation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent"] = self.parent
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["parent"] = self.parent.id
        return initial

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return (
            reverse("dt-content:menu-update", args=[self.parent.id]) + "?success=true"
        )


class SubmenuUpdateView(StaffMemberRequiredMixin, UpdateView):
    model = Menu
    form_class = SubmenuForm
    slug_field = "id"
    context_object_name = "menu"
    template_name = "dt_content/console/submenu_update.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        url = next_url or self.request.path
        return url + "?success=true"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.parent:  # if parent menu, redirect to menu update
            return redirect("dt-content:menu-update", self.object.id)
        return response


class MenuDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Menu.objects
    slug_field = "id"
    context_object_name = "menu"
    template_name = "dt_content/console/menu_delete.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next_url = self.request.GET.get("next", None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_url"] = self.next_url or self.object.console_list_url
        return context

    def get_success_url(self):
        return (self.next_url or self.object.console_list_url) + "?delete_success=True"


class ContentSectionListView(StaffMemberRequiredMixin, ListView):
    # Only lists static sections
    queryset = ContentSection.objects.filter(menu=None)
    context_object_name = "content_section_list"
    template_name = "dt_content/console/content_section_list.html"


class ContentSectionUpdateView(StaffMemberRequiredMixin, UpdateView):
    model = ContentSection
    fields = []
    slug_field = "id"
    context_object_name = "section"
    template_name = "dt_content/console/content_section_update.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        url = next_url or reverse("dt-content:content-section-list")
        return url + "?success=true"


class ContentSectionDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = ContentSection.objects
    slug_field = "id"
    context_object_name = "content_section"
    template_name = "dt_content/console/content_section_delete.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next_url = self.request.GET.get("next", None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_url"] = self.next_url or self.object.console_list_url
        return context

    def get_success_url(self):
        return (self.next_url or self.object.console_list_url) + "?delete_success=True"


class ContentBlockListView(StaffMemberRequiredMixin, ListView):
    queryset = ContentBlock.objects.select_subclasses().filter(section=None)
    context_object_name = "content_block_list"
    template_name = "dt_content/console/content_block_list.html"


class ContentBlockDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = ContentBlock.objects.select_subclasses()
    slug_field = "id"
    context_object_name = "content_block"
    template_name = "dt_content/console/content_block_delete.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next_url = self.request.GET.get("next", None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_url"] = self.next_url or self.object.console_list_url
        return context

    def get_success_url(self):
        return (self.next_url or self.object.console_list_url) + "?delete_success=True"


class ContentBlockUpdateView(StaffMemberRequiredMixin, UpdateView):  # Abstract class
    context_object_name = "object"  # can't use "block" due to collision
    slug_field = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list_url"] = self.object.console_list_url
        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        url = next_url or self.object.console_list_url
        return url + "?success=true"


class ContentBlockCreateView(StaffMemberRequiredMixin, CreateView):
    # Functionality limitied to creating blocks associated with sections
    # Static content blocks are not supported

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        section = self.request.GET.get("section", None)
        if not section:
            raise SuspiciousOperation("Missing GET parameter: `section`")
        try:
            self.section = ContentSection.objects.get(id=section)
        except ContentSection.DoesNotExist as e:
            raise SuspiciousOperation("Could not find section {}".format(section))

    def get_initial(self):
        initial = super().get_initial()
        initial["section"] = self.section.id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = self.section
        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url

        return self.object.console_list_url


class RichTextBlockUpdateView(ContentBlockUpdateView):
    model = RichTextBlock
    fields = ["content"]
    template_name = "dt_content/console/rich_text_block_update.html"


class RichTextBlockCreateView(ContentBlockCreateView):
    model = RichTextBlock
    form_class = RichTextBlockCreateForm
    template_name = "dt_content/console/rich_text_block_create.html"
