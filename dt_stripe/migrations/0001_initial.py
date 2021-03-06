# Generated by Django 2.2.4 on 2019-09-23 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(db_index=True, help_text='Id of Stripe Customer', max_length=128, verbose_name='id')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('description', models.TextField(blank=True, help_text='Description for admins', null=True, verbose_name='description')),
                ('source_status', models.CharField(choices=[('NA', 'None'), ('FA', 'Source payment failed'), ('AV', 'Source available')], default='NA', max_length=2, verbose_name='source status')),
                ('default_source_id', models.CharField(max_length=128, null=True, verbose_name='default source id')),
                ('default_source_brand', models.TextField(null=True, verbose_name='default source brand')),
                ('default_source_last4', models.CharField(max_length=4, null=True, verbose_name='default source last 4 digits')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(db_index=True, help_text='Id of Stripe Plan', max_length=128, verbose_name='id')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('currency', models.CharField(default='usd', max_length=3, verbose_name='currency')),
                ('interval', models.CharField(choices=[('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], max_length=16, verbose_name='interval')),
                ('interval_count', models.IntegerField(default=1, help_text='Number of intervals per billing cycle. I.e., interval=month and interval_count=3 for 3 months.', verbose_name='count')),
                ('name', models.CharField(help_text='Local name for use by admins', max_length=128, null=True, verbose_name='name')),
                ('description', models.TextField(blank=True, help_text='Local description for use by admins', null=True, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(db_index=True, help_text='Id of Stripe Product', max_length=128, verbose_name='id')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(blank=True, help_text="Description to be shown to the user. Only for products of type 'good'.", null=True, verbose_name='description')),
                ('product_type', models.CharField(choices=[('good', 'Good'), ('service', 'Service')], max_length=16, verbose_name='type')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(db_index=True, help_text='Id of Stripe Subscription', max_length=128, verbose_name='id')),
                ('status', models.CharField(choices=[('NA', 'No subscription'), ('AV', 'Active'), ('CE', 'Active until end of billing cycle)'), ('CX', 'Canceled due to expiry'), ('CP', 'Canceled due to payment issue')], default='NA', max_length=2, verbose_name='status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='dt_stripe.Customer')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='dt_stripe.Plan')),
            ],
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(db_index=True, help_text='Id of Stripe SKU', max_length=128, verbose_name='id')),
                ('price', models.IntegerField(verbose_name='price')),
                ('currency', models.CharField(default='usd', max_length=3, verbose_name='currency')),
                ('name', models.CharField(help_text='Local name for use by admins', max_length=128, null=True, verbose_name='name')),
                ('description', models.TextField(blank=True, help_text='Local description for use by admins', null=True, verbose_name='description')),
                ('product', models.ForeignKey(on_delete='CASCADE', related_name='skus', to='dt_stripe.Product')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='product',
            field=models.ForeignKey(on_delete='CASCADE', related_name='plans', to='dt_stripe.Product'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(db_index=True, help_text='Id of Stripe Order', max_length=128, verbose_name='id')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='dt_stripe.Customer')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='dt_stripe.SKU')),
            ],
        ),
    ]
