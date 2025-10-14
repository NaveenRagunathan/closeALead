from io import BytesIO
from weasyprint import HTML, CSS
from models.offer import Offer

def get_currency_symbol(currency: str) -> str:
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "CAD": "$"}
    return symbols.get(currency, "$")

def generate_pdf(offer: Offer) -> bytes:
    """Generate PDF from offer data"""
    
    # Create HTML content based on template
    html_content = generate_html(offer)
    
    # Generate PDF
    pdf_file = BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    
    return pdf_file.read()

def generate_html(offer: Offer) -> str:
    """Generate HTML based on offer template"""
    
    currency_symbol = get_currency_symbol(offer.price_currency)
    features_html = "\n".join([
        f'<div class="feature"><span class="check">✓</span> {feature}</div>'
        for feature in (offer.features or [])
    ])
    
    # Add personalization if client name is provided
    personalization_html = ""
    if offer.client_name:
        personalization_html = f'<div class="personalization">Prepared for: <strong>{offer.client_name}</strong></div>'
    
    # Customize styles based on template
    if offer.template in {"modern", "bold", "elegant", "vibrant"}:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{ size: A4; margin: 0; }}
                body {{ margin: 0; font-family: 'Arial', sans-serif; }}
                .header {{ background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; padding: 60px 40px; }}
                .header h1 {{ font-size: 48px; margin: 0 0 20px 0; }}
                .header p {{ font-size: 20px; opacity: 0.9; }}
                .personalization {{ background: #f0f9ff; padding: 15px 40px; font-size: 14px; color: #1e40af; border-left: 4px solid #3b82f6; }}
                .content {{ padding: 40px; }}
                .description {{ font-size: 16px; line-height: 1.8; color: #374151; margin-bottom: 40px; }}
                .features {{ background: #f9fafb; padding: 40px; }}
                .features h2 {{ font-size: 32px; margin-bottom: 30px; }}
                .feature {{ display: flex; align-items: center; margin-bottom: 15px; font-size: 16px; }}
                .check {{ color: #10b981; font-size: 20px; margin-right: 15px; }}
                .pricing {{ text-align: center; padding: 60px 40px; }}
                .price-box {{ display: inline-block; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; padding: 40px 60px; border-radius: 20px; }}
                .price {{ font-size: 64px; font-weight: bold; }}
                .interval {{ font-size: 14px; opacity: 0.9; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{offer.title}</h1>
                <p>{offer.subtitle}</p>
            </div>
            {personalization_html}
            <div class="content">
                <div class="description">{offer.description}</div>
            </div>
            <div class="features">
                <h2>What You Get</h2>
                {features_html}
            </div>
            <div class="pricing">
                <div class="price-box">
                    <div class="price">{currency_symbol}{offer.price_amount}</div>
                    <div class="interval">
                        {offer.price_interval if offer.price_interval != 'one-time' else 'One-time payment'}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    # Default safely to the modern layout if template is unrecognized
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 0; }}
            body {{ margin: 0; font-family: 'Arial', sans-serif; }}
            .header {{ background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; padding: 60px 40px; }}
            .header h1 {{ font-size: 48px; margin: 0 0 20px 0; }}
            .header p {{ font-size: 20px; opacity: 0.9; }}
            .personalization {{ background: #f0f9ff; padding: 15px 40px; font-size: 14px; color: #1e40af; border-left: 4px solid #3b82f6; }}
            .content {{ padding: 40px; }}
            .description {{ font-size: 16px; line-height: 1.8; color: #374151; margin-bottom: 40px; }}
            .features {{ background: #f9fafb; padding: 40px; }}
            .features h2 {{ font-size: 32px; margin-bottom: 30px; }}
            .feature {{ display: flex; align-items: center; margin-bottom: 15px; font-size: 16px; }}
            .check {{ color: #10b981; font-size: 20px; margin-right: 15px; }}
            .pricing {{ text-align: center; padding: 60px 40px; }}
            .price-box {{ display: inline-block; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; padding: 40px 60px; border-radius: 20px; }}
            .price {{ font-size: 64px; font-weight: bold; }}
            .interval {{ font-size: 14px; opacity: 0.9; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{offer.title}</h1>
            <p>{offer.subtitle}</p>
        </div>
        {personalization_html}
        <div class="content">
            <div class="description">{offer.description}</div>
        </div>
        <div class="features">
            <h2>What You Get</h2>
            {features_html}
        </div>
        <div class="pricing">
            <div class="price-box">
                <div class="price">{currency_symbol}{offer.price_amount}</div>
                <div class="interval">
                    {offer.price_interval if offer.price_interval != 'one-time' else 'One-time payment'}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
