from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.db import models
from django.utils.safestring import mark_safe

from core.tools.mixins.models import NamedObjMixin, OnOffMixin, PriorityMixin


class EmailBackendSetting(models.Model):
    """Данные для бэкенда почтового клиента
    """
    use_tls = models.BooleanField('Use tls',default=True)
    host = models.CharField('Email host', max_length=1024)
    host_user = models.CharField('Email host user', max_length=255)
    host_password = models.CharField('Email host password', max_length=255)
    port = models.PositiveSmallIntegerField('Email port', default=587)

    email_admin = models.EmailField('Admin e-mail')

    is_active = models.BooleanField('Active')

    class Meta:
        verbose_name = 'Email backend setting'
        verbose_name_plural = 'Email backend settings'

    @staticmethod
    def _get_active_settings():
        return EmailBackendSetting.objects.get(is_active=True)

    @classmethod
    def _get_email_backend(cls):
        settings = cls._get_active_settings()
        backend = EmailBackend(host=settings.host, port=settings.port, username=settings.host_user,
                               password=settings.host_password, use_tls=settings.use_tls)
        return backend

    @classmethod
    def send_email(cls, subject, body, to=None):
        settings = cls._get_active_settings()

        if not to:
            to = settings.email_admin

        # TODO: шлет сырой html
        email = EmailMessage(subject=subject, body=mark_safe(body), from_email=settings.host_user, to=[to],
                             connection=cls._get_email_backend())
        email.send()

    def save(self, *args, **kwargs):
        if self.is_active:
            EmailBackendSetting.objects.update(is_active=False)
        super(EmailBackendSetting, self).save(*args, **kwargs)


class Contact(PriorityMixin, NamedObjMixin):
    details = models.TextField("Details")

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = 'priority',

    def __str__(self):
        return self.name


class Translation(PriorityMixin, NamedObjMixin):
    """Таблица, в которой хранятся все переводы
    Под name хранится название языка
    """
    default = models.BooleanField(default=False)
    image = models.ImageField('Image')

    class Meta:
        ordering = 'priority',

    def __str__(self):
        return self.name

    @staticmethod
    def get_translate_by(lang):
        translation = Translation.objects.filter(name=lang.upper()).first()
        return translation if translation else Translation.objects.get(default=True)

    def save(self, *args, **kwargs):

        # всегда должен оставаться дефолтный язык
        if self.default:
            Translation.objects.update(default=False)

        self.name = self.name.upper()

        super(Translation, self).save(*args, **kwargs)

    def delete(self, *args):
        if not Translation.objects.count() == 1:
            super(Translation, self).delete(*args)

    # общие
    site_name = models.TextField("Site name", default="MAXSender.com")
    buy = models.TextField("Buy", default="Buy")
    buy_title = models.TextField("Buy title", default="Buy")
    about = models.TextField("About", default="About")
    about_title = models.TextField("About title", default="About")
    sales = models.TextField("Sales", default="Sales")
    sales_title = models.TextField("Sales title", default="Sales")
    articles = models.TextField("Articles", default="Articles")
    articles_title = models.TextField("Articles title", default="Articles")
    faq = models.TextField("FAQ", default="FAQ")
    faq_title = models.TextField("FAQ title", default="FAQ")
    navigation = models.TextField("Navigation", default="Navigation")
    contacts = models.TextField("Contacts", default="Contacts")
    text_block = models.TextField("Text block", default="Text block")
    some_text_in_block = models.TextField("Some text in block", default="Some text in block")

    # данные для таблицы
    subscription = models.TextField("Subscription", default="Subscription")
    limits = models.TextField("Limits", default="Limits")
    package = models.TextField("Package", default="Package")
    tables_sizes = models.TextField("Tables sizes", default="Tables sizes")
    start_subscription = models.TextField("Start subscription", default="Start subscription")
    term = models.TextField("Term", default="Term")
    numbers_of_hands = models.TextField("Numbers of hands", default="Numbers of hands")
    next_limit = models.TextField("Next limit", default="next <br> limit")
    next_month = models.TextField("Next month", default="next <br> month")
    next_100k = models.TextField("Next 100k", default="next <br> 100k")
    cart_content = models.TextField("Cart content", default="Cart content")
    clear = models.TextField("Clear", default="clear")
    days_from = models.TextField("Days from", default="days from")
    price = models.TextField("Price", default="Price")
    cart_is_empty = models.TextField("Cart is empty", default="Cart is empty")
    total = models.TextField("Total", default="Total")
    make_order_in_cart = models.TextField("Make order (in cart)", default="Make order")
    add_to_cart = models.TextField("Add to cart (name block)", default="Add to cart")
    add_to_cart_btn = models.TextField("Add to cart (button)", default="Add to cart")
    order = models.TextField("Order", default="Order")
    game = models.TextField("Game", default="Game")
    limits = models.TextField("Limits", default="Limits")
    tables = models.TextField("Tables", default="Tables")
    count = models.TextField("Count", default="Count")
    start = models.TextField("Start", default="Start")
    past = models.TextField("Past", default="past")
    days = models.TextField("Days", default="days")

    # данные для страницы About
    text_in_about = models.TextField("Text in 'About'", default="Text in <b>'About'</b>")
    # данные для страницы Sales
    text_in_sales = models.TextField("Text in 'Sales'", default="Text in <b>'Sales'</b>")
    # данные для страницы Articles
    text_in_articles = models.TextField("Text in 'Articles'", default="Text in <b>'Articles'</b>")
    # данные для страницы FAQ
    text_in_faq = models.TextField("Text in 'FAQ'", default="Text in <b>'FAQ'</b>")

    # данные для страницы Order
    making_order = models.TextField("Making order", default="Making order")
    used_payment_system = models.TextField("Used payment system", default="Used payment system")
    our_details = models.TextField("Our details", default="Our details")
    your_email = models.TextField("Your e-mail", default="Your e-mail")
    your_name = models.TextField("Your name", default="Your name")
    instruction = models.TextField("Instruction", default="Instruction")
    text_in_instruction = models.TextField("Text in instruction", default="Text in <b>instruction</b>")
    back_to_table = models.TextField("Back to table", default="Back to table")
    make_order_in_order = models.TextField("Make order (in order page)", default="Make order")
    success = models.TextField("Success", default="Success! Pay your order and wait further directed on the your "
                                                  "e-mail. For any questions, please poker@test.ru")

    required_keys_for_client = ['{client_name}', '{type_payment}', '{details_payment}', '{total_price}', '{items}']
    email_letter_subject_for_client = models.TextField("Email letter subject for client", default="Subject")
    email_letter_body_for_client = models.TextField("Email letter body for client",
         default="Here must have keys: " + ', '.join(required_keys_for_client))

    required_keys_for_admin = ['{client_name}', '{type_payment}', '{details_payment}', '{total_price}', '{items}', '{notes}']
    email_letter_subject_for_admin = models.TextField("Email letter subject for admin", default="Subject")
    email_letter_body_for_admin = models.TextField("Email letter body for admin",
         default="Here must have keys: " + ', '.join(required_keys_for_admin))
