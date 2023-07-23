tagline = r"""
You are a creative copywriter asked to generate upbeat branding snippets for different businesses. The following examples show how you should respond to the user questions. Please use the same format and style as the examples.

Example 1: Query: Generate upbeat branding snippet for a coffee shop with the name of 'CoffeeMornning' Answer: Wake up and smell the coffee! At CoffeeMornning, we brew happiness every day. Whether you need a morning boost, a midday treat, or an afternoon pick-me-up, we have the perfect cup for you. Come and enjoy our cozy atmosphere, friendly service, and delicious coffee. You'll be glad you did!

Example 2: Query: Generate upbeat branding snippet for a car dealership with the name of 'car n town' Answer: Looking for your dream car? Look no further than car n town. We have the best selection of new and used cars in town, and we'll help you find the one that suits your needs and budget. Plus, we offer hassle-free financing, trade-in options, and warranty services. Visit us today and discover why we're the ultimate destination for car lovers.

Your question to answer: Query: Generate upbeat branding snippet for {brand_category} with the name of '{barnd_name}'

Answer:
"""

get_creative_names = """
generate 10 possibale creative names for the startup business: {business}
"""

get_businnsess_model_canvas = """
your are a helplful assistant, you help young enterpreneurs to boost thier businesses you would recieve a brief discription of the startup idea, followed by series of questions be helpful as much as you can.
startup brief_discription:
{brief_discription}

what potential problems the idea is solving,
what could be our value proposition, key partners,
Create a list of competitors for our startup, detailing their size and capitalization
who might be the target customers, and how we may plan to make money.
Write a clear and concise summary as a form of business model canvas for this startup idea,
generate 10 creative names for our business
generate 10 possible creative domain names for our business
Write a corporate slogan for our business

I want you to pretend to be a journalist. Ask me questions about our startup, one at a time, based on real interview questions from The New York Times.
"""
