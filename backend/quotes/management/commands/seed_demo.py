from django.core.management.base import BaseCommand
from quotes.models import Part, Quote, QuoteLineItem
from decimal import Decimal


class Command(BaseCommand):
    help = "Seed demo Parts, Quotes, and QuoteLineItems"

    def handle(self, *args, **options):
        QuoteLineItem.objects.all().delete()
        Quote.objects.all().delete()
        Part.objects.all().delete()

        parts = [
            Part(stock_code="ABC123", description="Widget Alpha"),
            Part(stock_code="DEF456", description="Widget Delta"),
            Part(stock_code="XYZ999", description="Widget Xtreme"),
        ]
        Part.objects.bulk_create(parts)
        parts = {p.stock_code: p for p in Part.objects.all()}

        q1 = Quote.objects.create(name="AxiomR_250915_085017", status="approved")
        q2 = Quote.objects.create(name="AxiomR_250916_105501", status="pending")

        QuoteLineItem.objects.create(quote=q1, part=parts["ABC123"], quantity=2, price=Decimal("12.50"))
        QuoteLineItem.objects.create(quote=q1, part=parts["ABC123"], quantity=1, price=Decimal("3.50"))
        QuoteLineItem.objects.create(quote=q1, part=parts["DEF456"], quantity=5, price=Decimal("2.00"))
        QuoteLineItem.objects.create(quote=q2, part=parts["XYZ999"], quantity=1, price=Decimal("99.99"))

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
