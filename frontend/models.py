from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils.text import slugify

from .enums import PLACEMENT_MODE, GRADES, STATUS


class Migration(models.Model):
    id = models.BigAutoField(primary_key = True)
    last_name = models.CharField(max_length = 60, verbose_name = "Last Name")
    first_name = models.CharField(max_length = 255, verbose_name = "First Name")
    username = models.CharField(max_length = 60, verbose_name = "Username")
    contact = models.CharField(max_length = 60, verbose_name = "Contact")
    email = models.CharField(max_length = 255, verbose_name = "Email")
    sponsor = models.CharField(max_length = 60, blank = True, verbose_name = "Sponsor")
    placement_name = models.CharField(max_length = 60, blank = True, verbose_name = "Placement Name")
    grade = models.CharField(max_length = 10, choices = GRADES, verbose_name = "Grade")
    placement_mode = models.CharField(max_length = 10, blank = True, choices = PLACEMENT_MODE, verbose_name = "Placement Mode")
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    updated_at = models.DateTimeField(auto_now = True, editable = False)

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Migration'
        verbose_name_plural = 'Migrations'

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class ProductCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 150, db_index = True)
    slug = models.SlugField(max_length = 75, unique = True, db_index = True)
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    updated_at = models.DateTimeField(auto_now = True, editable = False)

    class Meta:
        db_table = 'product_category'
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if self.slug != slug:
            self.slug = slug
        super(ProductCategory, self).save(*args, **kwargs)


class Product(models.Model):
    id = models.BigAutoField(primary_key = True)
    category = models.ForeignKey('ProductCategory', related_name = 'products', on_delete = models.SET_NULL, blank = True, null = True)
    name = models.CharField(max_length = 100, db_index = True)
    slug = models.SlugField(max_length = 75, db_index = True)
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    stock = models.PositiveIntegerField()
    code = models.CharField(max_length = 60, editable = False)
    reference = models.CharField(max_length = 60, editable = False)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    updated_at = models.DateTimeField(auto_now = True, editable = False)

    class Meta:
        db_table = 'product'
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if self.slug != slug:
            self.slug = slug
        super(Product, self).save(*args, **kwargs)


class FAQCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 150, db_index = True)
    slug = models.SlugField(max_length = 75, unique = True, db_index = True)
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    updated_at = models.DateTimeField(auto_now = True, editable = False)

    class Meta:
        db_table = 'faq_category'
        ordering = ('name',)
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if self.slug != slug:
            self.slug = slug
        super(FAQCategory, self).save(*args, **kwargs)


class FAQ(models.Model):
    id = models.AutoField(primary_key = True)
    category = models.ForeignKey('FAQCategory', related_name = 'faqs', on_delete = models.SET_NULL, blank = True, null = True)
    question = models.CharField(max_length = 500, db_index = True)
    slug = models.SlugField(max_length = 75, db_index = True)
    answer = RichTextUploadingField()
    status = models.SmallIntegerField(choices = STATUS, db_index = True, verbose_name = 'Displayed ?')
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    updated_at = models.DateTimeField(auto_now = True, editable = False)

    class Meta:
        db_table = 'faq'
        ordering = ('question',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        slug = slugify(self.question)
        if self.slug != slug:
            self.slug = slug
        super(FAQ, self).save(*args, **kwargs)
