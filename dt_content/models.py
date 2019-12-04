from abc import abstractmethod

from ckeditor_uploader.fields import RichTextUploadingField
from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils.decorators import classproperty
from django.utils.text import camel_case_to_spaces
from model_utils.managers import InheritanceManager


class Menu(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    url_slug = models.SlugField(max_length=32, db_index=True)
    disabled = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, null=True, blank=True
    )
    content_section = models.OneToOneField(
        "ContentSection",
        related_name="menu",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # User will be redirected if redirect link is set
    redirect_to = models.URLField(null=True, blank=True)

    class Meta:
        order_with_respect_to = "parent"
        indexes = [models.Index(fields=["parent", "url_slug"])]
        unique_together = [["parent", "url_slug"]]

    def get_content_section(self):
        ContentSection = apps.get_model("dt_content", "ContentSection")
        if not self.content_section:
            content_section = ContentSection()
            content_section.save()
            self.content_section = content_section
            self.save()
        return self.content_section

    def save(self, *args, **kwargs):
        if self.parent and self.children.exists():
            raise RuntimeError(
                "Multi-level submenus are not supported (only menu and sub-menu)"
            )
        super().save(*args, **kwargs)

    @property
    def update_url(self):
        if self.parent:
            return reverse("dt-content:submenu-update", args=[self.id])
        else:
            return reverse("dt-content:menu-update", args=[self.id])

    @property
    def console_list_url(self):
        if self.parent:
            return reverse("dt-content:menu-update", args=[self.parent.id])
        else:
            return reverse("dt-content:menu-list")

    @property
    def url_path(self):
        if self.parent:  # is child
            return "{}/{}".format(self.parent.url_slug, self.url_slug)
        else:  # is parent
            return "{}".format(self.url_slug)

    def __str__(self):
        if self.parent:
            return "{} > {}".format(self.parent.title, self.title)
        else:
            return self.title


class StaticContentSectionManager(InheritanceManager):
    def get_queryset(self):
        return self._queryset_class(self.model).filter(menu=None)


class ContentSection(models.Model):
    # Key for static content sections (standlone content sections used in custom HTML)
    key = models.CharField(max_length=256, db_index=True)
    # Location of static ContentSection (if it is static)
    # Saves the url where the ContentSection was first initiated
    static_location = models.URLField(null=True)

    objects = models.Manager()
    static_objects = StaticContentSectionManager()

    def __str__(self):
        try:
            menu = self.menu
            if menu.parent:
                return "{} > {}".format(menu.parent.title, menu.title)
            else:
                return "{}".format(menu.title)
        except Menu.DoesNotExist as e:
            return "{}".format(self.key)

    @property
    def blocks(self):
        ContentBlock = apps.get_model("dt_content", "ContentBlock")
        return ContentBlock.objects.select_subclasses().filter(section=self)

    @property
    def empty(self):
        return not self.blocks.exists()

    @property
    def template_name(self):
        return "dt_content/content/content_section.html"


class StaticContentBlockManager(InheritanceManager):
    def get_queryset(self):
        return self._queryset_class(self.model).filter(section=None)


class ContentBlock(models.Model):
    section = models.ForeignKey(
        ContentSection,
        related_name="_blocks",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    # Whether this block is disabled within a ContentSection
    disabled = models.BooleanField(default=False)

    # Key for static content blocks (standlone content blocks used in custom HTML)
    key = models.CharField(max_length=256, null=True, blank=True, db_index=True)
    # Location of static ContentSection (if it is static)
    # Saves the url where the ContentSection was first initiated
    static_location = models.URLField(null=True)

    objects = InheritanceManager()
    static_objects = StaticContentBlockManager()

    class Meta:
        order_with_respect_to = "section"

    @classproperty
    def block_type(cls):
        return camel_case_to_spaces(cls.__name__).title()

    def get_block_type(self):
        return self.__class__.block_type

    @classproperty
    def block_type_key(cls):
        return camel_case_to_spaces(cls.__name__).replace(" ", "_")

    @property
    def console_list_url(self):
        if self.section:
            try:
                # menu-bound section
                menu = self.section.menu
                return menu.update_url
            except Menu.DoesNotExist as e:
                # static section
                return reverse(
                    "dt-content:content-section-update", args=[self.section.id]
                )
        else:
            # static block
            return reverse("dt-content:content-block-list")

    @property
    def template_name(self):
        return "dt_content/content/content_block.html"

    @property
    @abstractmethod
    def child_template_name(self):
        if type(self) is ContentBlock:
            raise RuntimeError(
                "The child_template_name property can only be retrieved from a subclass of ContentBlock. Consider looking into multi-table inheritance for Django models."
            )
        else:
            raise NotImplementedError(
                "The child_template_name property has not been set for {}".format(
                    type(self).__name__
                )
            )

    @classproperty
    @abstractmethod
    def create_url(cls):
        if cls is ContentBlock:
            raise RuntimeError(
                "The create_url property can only be retrieved from a subclass of ContentBlock. Consider looking into multi-table inheritance for Django models."
            )
        else:
            raise NotImplementedError(
                "The create_url property has not been set for {}".format(cls.__name__)
            )

    @property
    @abstractmethod
    def update_url(self):
        if type(self) is ContentBlock:
            raise RuntimeError(
                "The update_url property can only be retrieved from a child model of ContentBlock. Consider looking into multi-table inheritance for Django models."
            )
        else:
            raise NotImplementedError(
                "The update_url property has not been set for {}".format(
                    type(self).__name__
                )
            )

    def __str__(self):
        if self.section:
            return "{} in {}".format(self.block_type, str(self.section))
        else:
            # static block
            return "Static {} ({})".format(self.block_type, self.key)


class RichTextBlock(ContentBlock):
    base = models.OneToOneField(
        ContentBlock, on_delete=models.CASCADE, parent_link=True
    )
    content = RichTextUploadingField(default="", blank=True)

    @property
    def child_template_name(self):
        return "dt_content/content/rich_text_block.html"

    @classproperty
    def create_url(cls):
        return reverse("dt-content:rich-text-block-create")

    @property
    def update_url(self):
        return reverse("dt-content:rich-text-block-update", args=[self.id])


class CarouselBlock(ContentBlock):
    base = models.OneToOneField(
        ContentBlock, on_delete=models.CASCADE, parent_link=True
    )

    # NOT IMPLEMENTED

    @property
    def child_template_name(self):
        raise NotImplementedError()

    @classproperty
    def create_url(cls):
        return ""

    @property
    def update_url(self):
        raise NotImplementedError()


def update_content_block_subclasses():
    """
    Call this after you have defined additional ContentBlock subclasses
    to include them in `content_block_subclasses`
    """
    global content_block_classes
    content_block_classes = dict()
    for klass in ContentBlock.__subclasses__():
        content_block_classes[klass.block_type_key] = klass


content_block_classes = None
update_content_block_subclasses()
