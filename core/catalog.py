"""Static content for the products, service-detail, markets and insights pages.

Specifications are indicative trade norms and are confirmed per order.
"""

P = "core/img/photos/"

PRODUCTS = [
    {
        "slug": "rice", "name": "Rice", "kicker": "Basmati & non-basmati", "icon": "bi-flower2",
        "category": "Grains",
        "img": P + "prod-rice.jpg", "bg": "bg-prod-rice",
        "summary": "Long-grain basmati and a range of non-basmati varieties, milled, sorted and packed for export.",
        "about": [
            "Rice is the staple that moves the most volume in agricultural trade. We source basmati and non-basmati rice from verified mills, matched to the grain length, ageing, broken percentage and polish your market expects.",
            "Every lot is sampled before dispatch, and packed in the bag size and material your port and buyer require.",
        ],
        "varieties": ["Basmati (1121, 1509, Pusa)", "Sella / parboiled", "Sona Masoori", "IR-64 & other non-basmati", "Broken rice"],
        "specs": [("Grain", "Extra-long / long, by variety"), ("Broken %", "Agreed per grade"), ("Moisture", "Within export norms"), ("Purity", "Sorted, stone and foreign-matter free")],
        "packing": ["PP / jute bags, 5-50 kg", "Retail packs on request", "20 ft / 40 ft containers, palletised"],
        "season": [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "uses": ["Retail & wholesale", "Food service", "Institutional supply"],
    },
    {
        "slug": "wheat-cereals", "name": "Wheat & Cereals", "kicker": "Milling and feed grades", "icon": "bi-flower1",
        "category": "Grains",
        "img": P + "prod-wheat.jpg", "bg": "bg-prod-wheat",
        "summary": "Milling wheat and coarse cereals, supplied in bulk or bagged, with inspection at loading.",
        "about": [
            "We supply milling wheat and other cereals for flour mills, feed manufacturers and traders, in bulk or bagged form, against agreed quality parameters.",
            "Independent inspection at the point of loading keeps quantity and quality transparent for both sides.",
        ],
        "varieties": ["Milling wheat", "Durum", "Maize / corn", "Millets (bajra, jowar)", "Barley"],
        "specs": [("Protein", "Per buyer specification"), ("Moisture", "Within export norms"), ("Test weight", "Agreed per lot"), ("Foreign matter", "Within agreed limits")],
        "packing": ["Bulk vessel / container liner", "PP bags, 25-50 kg", "Jumbo bags on request"],
        "season": [3, 4, 5, 6],
        "uses": ["Flour milling", "Animal feed", "Food processing"],
    },
    {
        "slug": "pulses", "name": "Pulses & Lentils", "kicker": "Protein-rich staples", "icon": "bi-record-circle",
        "category": "Pulses & Oilseeds",
        "img": P + "prod-pulses.jpg", "bg": "bg-prod-pulses",
        "summary": "Chickpeas, lentils, split peas and beans, cleaned, graded and bagged to specification.",
        "about": [
            "Pulses are in steady demand across retail, food processing and institutional buyers. We source cleaned and graded lots with consistent size, colour and moisture.",
            "Fumigation and phytosanitary paperwork are handled with the shipment where the destination requires them.",
        ],
        "varieties": ["Chickpeas (kabuli, desi)", "Lentils (masoor)", "Pigeon pea (toor)", "Green gram (moong)", "Black gram (urad)", "Yellow & green peas"],
        "specs": [("Size / grade", "Per variety and buyer"), ("Moisture", "Within export norms"), ("Admixture", "Cleaned and sorted"), ("Damage", "Within agreed tolerance")],
        "packing": ["PP bags, 25-50 kg", "Retail packs on request", "Fumigated container loads"],
        "season": [3, 4, 5, 10, 11, 12],
        "uses": ["Retail & wholesale", "Food processing", "Institutional supply"],
    },
    {
        "slug": "spices", "name": "Spices", "kicker": "Whole and ground", "icon": "bi-fire",
        "category": "Spices & Teas",
        "img": P + "prod-spices.jpg", "bg": "bg-prod-spices",
        "summary": "Turmeric, chilli, cumin, coriander and more, whole or ground, with aroma and colour you can specify.",
        "about": [
            "From turmeric and chilli to cumin, coriander and cardamom, we source spices whole or ground, to colour, pungency and volatile-oil expectations.",
            "Spices are especially sensitive to moisture and contamination, so lots are tested and sealed in food-grade packing before they travel.",
        ],
        "varieties": ["Turmeric", "Red chilli", "Cumin", "Coriander", "Cardamom", "Black pepper", "Fennel & fenugreek"],
        "specs": [("Form", "Whole, crushed or powder"), ("Colour / pungency", "Per buyer specification"), ("Moisture", "Within export norms"), ("Contaminants", "Tested to destination limits")],
        "packing": ["PP / HDPE bags, 25-50 kg", "Vacuum and retail packs", "Private label on request"],
        "season": [1, 2, 3, 4, 11, 12],
        "uses": ["Food manufacturing", "Retail brands", "Foodservice"],
    },
    {
        "slug": "oilseeds", "name": "Oilseeds", "kicker": "Sesame, groundnut and more", "icon": "bi-droplet-half",
        "category": "Pulses & Oilseeds",
        "img": P + "prod-oilseeds.jpg", "bg": "bg-prod-oilseeds",
        "summary": "Sesame, groundnut and other oilseeds, hulled or natural, machine-cleaned to high purity.",
        "about": [
            "Oilseeds supply both the edible-oil industry and the food and bakery trade. We source sesame, groundnut and similar seeds cleaned to high purity.",
            "Purity, oil content and moisture are the three numbers that matter, and we agree each of them before shipment.",
        ],
        "varieties": ["White sesame (hulled / natural)", "Black sesame", "Groundnut / peanut", "Sunflower seeds", "Mustard seed"],
        "specs": [("Purity", "Machine-cleaned, agreed %"), ("Oil content", "Per variety"), ("Moisture", "Within export norms"), ("Free fatty acid", "Where relevant")],
        "packing": ["PP bags, 25-50 kg", "Jumbo bags on request", "Container loads"],
        "season": [9, 10, 11, 12, 1, 2],
        "uses": ["Edible-oil crushing", "Bakery & confectionery", "Snack manufacturing"],
    },
    {
        "slug": "tea", "name": "Tea", "kicker": "Orthodox & CTC", "icon": "bi-cup-hot",
        "category": "Spices & Teas",
        "img": P + "prod-tea.jpg", "bg": "bg-prod-tea",
        "summary": "Black, green and speciality tea from established gardens, bulk or packed.",
        "about": [
            "We source tea in orthodox and CTC forms from established gardens, graded for leaf style, liquor and aroma, and supply it in bulk or in packed formats.",
            "Tea absorbs odours easily, so lots are packed and containerised in clean, dry conditions with the right liners.",
        ],
        "varieties": ["CTC black tea", "Orthodox black tea", "Green tea", "Speciality / garden teas"],
        "specs": [("Grade", "Per buyer sample"), ("Liquor / aroma", "Cup-tested against sample"), ("Moisture", "Within export norms"), ("Packing", "Food-grade, odour-free")],
        "packing": ["Paper sacks with liner", "Tea chests", "Retail and private label"],
        "season": [3, 4, 5, 6, 7, 8, 9, 10, 11],
        "uses": ["Blenders & packers", "Retail brands", "Hospitality"],
    },
    {
        "slug": "fruits", "name": "Fresh Fruits", "kicker": "Mango, banana and more", "icon": "bi-brightness-alt-high",
        "category": "Fresh Produce",
        "img": P + "prod-fruits.jpg", "bg": "bg-prod-fruits",
        "summary": "Seasonal fresh fruit, harvested at the right maturity and moved on a tight cold chain.",
        "about": [
            "Fresh fruit is a race against time. We coordinate harvest maturity, grading, pack-house handling and refrigerated freight so fruit arrives in the condition your buyers expect.",
            "Because quality windows are short, we plan these shipments around the season and confirm timelines before booking.",
        ],
        "varieties": ["Mango", "Banana", "Pomegranate", "Grapes", "Citrus"],
        "specs": [("Maturity", "Harvest-stage controlled"), ("Size / grade", "Per variety and market"), ("Temperature", "Cold chain maintained"), ("Shelf life", "Confirmed before booking")],
        "packing": ["Ventilated cartons", "Reefer containers", "Air freight for premium lines"],
        "season": [3, 4, 5, 6, 7, 10, 11, 12],
        "uses": ["Supermarkets", "Wholesale markets", "Processing"],
    },
    {
        "slug": "vegetables", "name": "Fresh Vegetables", "kicker": "Onion, potato and more", "icon": "bi-basket3",
        "category": "Fresh Produce",
        "img": P + "prod-veg.jpg", "bg": "bg-prod-veg",
        "summary": "Onion, potato and other vegetables, graded and packed for long-haul export.",
        "about": [
            "Hardy vegetables such as onion and potato travel well when graded, cured and packed correctly. We manage sourcing, grading and packing for sea and land freight.",
            "Quality inspection covers size, firmness, sprouting and damage so the lot clears at the destination.",
        ],
        "varieties": ["Onion", "Potato", "Garlic", "Ginger", "Green chilli", "Okra & others"],
        "specs": [("Size / grade", "Per variety and market"), ("Firmness", "Checked at loading"), ("Damage / sprouting", "Within agreed tolerance"), ("Temperature", "As required")],
        "packing": ["Mesh / PP bags", "Ventilated cartons", "Reefer or ventilated containers"],
        "season": [1, 2, 3, 4, 10, 11, 12],
        "uses": ["Wholesale markets", "Supermarkets", "Processing"],
    },
    {
        "slug": "cashew-dry-fruits", "name": "Cashew & Dry Fruits", "kicker": "Nuts and dried fruit", "icon": "bi-gem",
        "category": "Dry Fruits",
        "img": P + "prod-nuts.jpg", "bg": "bg-prod-nuts",
        "summary": "Cashew kernels, almonds, raisins and other dry fruit, graded and sealed for freshness.",
        "about": [
            "Nuts and dried fruit are high-value lines where grading and freshness carry the price. We source cashew kernels and other dry fruit graded by size and quality, sealed to keep oils and aroma intact.",
            "Packing is vacuum or tin where needed, with moisture control built into the shipment plan.",
        ],
        "varieties": ["Cashew kernels (W240, W320, W450)", "Almonds", "Raisins", "Walnuts", "Dates"],
        "specs": [("Grade / count", "Per buyer specification"), ("Colour", "Per grade"), ("Moisture", "Within export norms"), ("Packing", "Vacuum or tin")],
        "packing": ["Vacuum cartons", "Tins", "Retail and private label"],
        "season": [2, 3, 4, 5, 9, 10, 11],
        "uses": ["Retail brands", "Confectionery & bakery", "Gifting"],
    },
]

PRODUCT_CATEGORIES = ["Grains", "Pulses & Oilseeds", "Spices & Teas", "Fresh Produce", "Dry Fruits"]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def product_by_slug(slug):
    return next((p for p in PRODUCTS if p["slug"] == slug), None)


def season_cells(product):
    return [{"m": m, "on": (i + 1) in product["season"]} for i, m in enumerate(MONTHS)]


SERVICE_DETAILS = [
    {
        "slug": "product-sourcing", "name": "Product Sourcing", "icon": "bi-search",
        "img": P + "svc-sourcing.jpg", "bg": "bg-warehouse",
        "summary": "Finding and verifying reliable suppliers, matched to your specification and budget.",
        "lead": "The right supplier decides the quality, price and reliability of everything that follows. We find and verify them for you.",
        "body": [
            "We begin with your specification: product, grade, quantity, packaging, destination and target price. From there we shortlist suppliers from our network and beyond, and compare them on quality, capacity, track record and terms.",
            "Before you commit, we verify the supplier, request samples where needed and report back with a clear comparison, so you decide with facts.",
        ],
        "includes": ["Specification and budget review", "Supplier shortlisting and comparison", "Supplier verification", "Sample coordination", "Price and terms negotiation support"],
        "outcomes": [("Fewer surprises", "Verified suppliers, agreed specification"), ("Better pricing", "Several qualified quotes, compared"), ("Faster start", "A shortlist, not a search")],
    },
    {
        "slug": "quality-inspection", "name": "Quality Inspection", "icon": "bi-clipboard2-check",
        "img": P + "svc-inspection.jpg", "bg": "bg-quality",
        "summary": "Checks before dispatch, so what leaves the origin is what you ordered.",
        "lead": "A problem found at origin costs far less than one found at your port. We inspect before the goods ship.",
        "body": [
            "Inspections are planned against your specification: sampling, visual checks, measurements, packing and marking, and loading supervision. Where required we coordinate laboratory testing.",
            "You receive a clear report with findings, so you can approve the shipment, or ask for corrections, before it leaves.",
        ],
        "includes": ["Pre-shipment sampling and checks", "Quantity and packing verification", "Loading supervision", "Laboratory test coordination", "Inspection report"],
        "outcomes": [("Confidence", "Verified before it ships"), ("Fewer claims", "Issues caught at origin"), ("Record", "Report for every lot")],
    },
    {
        "slug": "documentation-support", "name": "Documentation Support", "icon": "bi-file-earmark-text",
        "img": P + "svc-docs.jpg", "bg": "bg-quality",
        "summary": "Invoices, packing lists, certificates of origin and customs paperwork.",
        "lead": "Cross-border trade runs on paperwork. We prepare it correctly the first time so shipments do not stall.",
        "body": [
            "We prepare and check the documents your shipment needs: commercial invoice, packing list, certificate of origin, bill of lading or airway bill, and product-specific certificates such as phytosanitary or fumigation where the destination requires them.",
            "Documents are checked against each other and against any letter of credit terms before they are released.",
        ],
        "includes": ["Commercial invoice & packing list", "Certificate of origin", "Phytosanitary / fumigation coordination", "Bill of lading / airway bill", "Letter of credit document checks"],
        "outcomes": [("Clean clearance", "Consistent, accurate documents"), ("Fewer delays", "Errors caught early"), ("Compliance", "In line with trade regulations")],
    },
    {
        "slug": "logistics-coordination", "name": "Logistics Coordination", "icon": "bi-truck",
        "img": P + "svc-logistics.jpg", "bg": "bg-sea",
        "summary": "Sea, air and land freight, planned end to end for timely shipments.",
        "lead": "Right mode, right route, right timing. We plan the move from the supplier's gate to your door.",
        "body": [
            "We choose the freight mode and route for your cargo: containers by sea, air freight for urgent or perishable lines, and road transport for domestic and cross-border legs. Temperature-controlled options are arranged for fresh produce.",
            "From booking to final delivery we track the shipment and keep you informed, so you always know where your goods are.",
        ],
        "includes": ["Mode and route planning", "Container and freight booking", "Cold chain arrangements for perishables", "Shipment tracking and updates", "Final-mile coordination"],
        "outcomes": [("On time", "Planned against your deadline"), ("Visibility", "Updates through the journey"), ("Cargo care", "Handling suited to the product")],
    },
    {
        "slug": "customs-compliance", "name": "Customs Compliance", "icon": "bi-shield-check",
        "img": P + "svc-customs.jpg", "bg": "bg-containers",
        "summary": "Smooth clearance and regulatory adherence on every border crossing.",
        "lead": "Every border has its own rules. We make sure your shipment meets them before it arrives.",
        "body": [
            "We review the import and export requirements for your product and route: classification, duties, permits, labelling and packaging rules. Then we coordinate clearance with customs agents at both ends.",
            "Knowing the requirements before the shipment is booked avoids the most expensive surprises.",
        ],
        "includes": ["Product classification guidance", "Permit and licence checks", "Duty and tax guidance", "Clearance coordination", "Labelling and packaging checks"],
        "outcomes": [("Predictable clearance", "Requirements known upfront"), ("Fewer penalties", "Rules followed at each border"), ("Peace of mind", "One partner owns the process")],
    },
    {
        "slug": "after-sales-support", "name": "After-Sales Support", "icon": "bi-headset",
        "img": P + "svc-support.jpg", "bg": "bg-meeting",
        "summary": "Continued assistance after delivery, from a dedicated point of contact.",
        "lead": "The shipment arriving is not the end. We stay with you for claims, repeat orders and the next plan.",
        "body": [
            "If anything is not right on arrival, you deal with one accountable person who works with the supplier and carrier to resolve it. For repeat business, we keep your specification and preferred suppliers on file.",
            "Many clients buy on a regular schedule, so we help plan recurring orders and forecast needs ahead of the season.",
        ],
        "includes": ["Dedicated point of contact", "Claims and issue resolution", "Repeat-order planning", "Supplier performance feedback", "Market and seasonal updates"],
        "outcomes": [("Accountability", "One person, start to finish"), ("Continuity", "Repeat orders made simple"), ("Long-term value", "Relationships, not one-off deals")],
    },
]


def service_by_slug(slug):
    return next((s for s in SERVICE_DETAILS if s["slug"] == slug), None)


REGIONS = [
    {"name": "Middle East & GCC", "note": "Large, steady demand for rice, spices, pulses, tea and fresh produce.", "icon": "bi-sun", "products": ["Rice", "Spices", "Tea", "Fresh produce"]},
    {"name": "Africa", "note": "Growing import demand for staples such as rice, wheat, pulses and sugar-based lines.", "icon": "bi-globe-europe-africa", "products": ["Rice", "Wheat", "Pulses"]},
    {"name": "South-East Asia", "note": "Regional trade in spices, pulses, oilseeds and processing ingredients.", "icon": "bi-geo-alt", "products": ["Spices", "Pulses", "Oilseeds"]},
    {"name": "Europe", "note": "Quality-driven buyers for spices, tea, speciality and certified lines.", "icon": "bi-building", "products": ["Spices", "Tea", "Dry fruits"]},
    {"name": "North America", "note": "Brands and importers sourcing spices, rice, tea and dry fruit.", "icon": "bi-globe-americas", "products": ["Rice", "Spices", "Dry fruits"]},
    {"name": "South Asia", "note": "Cross-border and domestic trade across neighbouring markets.", "icon": "bi-compass", "products": ["Grains", "Pulses", "Fresh produce"]},
]

INCOTERMS = [
    ("FOB", "Free On Board", "We deliver the goods on board the vessel at the origin port. You take over cost and risk from there."),
    ("CFR", "Cost & Freight", "We pay to bring the goods to your destination port. Risk transfers when they are loaded."),
    ("CIF", "Cost, Insurance & Freight", "As CFR, plus we arrange minimum cargo insurance to your destination port."),
    ("EXW", "Ex Works", "You collect from the supplier's premises and manage the journey from there."),
]

DOCS = [
    ("bi-receipt", "Commercial invoice"), ("bi-boxes", "Packing list"), ("bi-flag", "Certificate of origin"),
    ("bi-bug", "Phytosanitary certificate"), ("bi-wind", "Fumigation certificate"), ("bi-file-earmark-ruled", "Bill of lading / AWB"),
    ("bi-shield-plus", "Insurance certificate"), ("bi-clipboard2-data", "Quality / inspection report"),
]

QUALITY_STAGES = [
    ("Source", "Suppliers are verified and samples approved against your specification.", "bi-search"),
    ("Test", "Moisture, purity, grade and, where needed, laboratory tests on representative samples.", "bi-eyedropper"),
    ("Pack", "Food-grade, correctly marked packing, matched to your port and buyer.", "bi-box-seam"),
    ("Inspect", "Pre-shipment inspection and loading supervision before dispatch.", "bi-clipboard2-check"),
    ("Document", "Certificates and shipping documents checked against each other.", "bi-file-earmark-check"),
    ("Deliver", "Tracked to destination, with a contact for any follow-up.", "bi-truck"),
]

INSIGHTS = [
    {
        "slug": "agro-export-documents-checklist", "title": "The agro export documents checklist", "tag": "Documentation", "read": 4,
        "img": P + "svc-docs.jpg",
        "excerpt": "Eight documents most agricultural shipments need, and the mistakes that hold them up.",
        "body": [
            ("Why documents decide the shipment", "A container can be perfect and still sit at a port for days if the paperwork does not match. The most common causes are small: a quantity that differs between the invoice and the packing list, or a missing certificate."),
            ("The core set", "Most agricultural exports need a commercial invoice, packing list, certificate of origin, bill of lading or airway bill, and a quality or inspection report. Depending on product and destination you may also need a phytosanitary certificate, a fumigation certificate and an insurance certificate."),
            ("Check them against each other", "Descriptions, quantities, weights, marks and consignee names should read the same on every document. If a letter of credit is involved, documents must match its terms exactly, word for word."),
            ("Start early", "Ask for the destination's requirements before you book. Some certificates take days to obtain, and rules differ between countries, so confirm them for each shipment."),
        ],
    },
    {
        "slug": "basmati-vs-non-basmati", "title": "Basmati vs non-basmati: what buyers should check", "tag": "Products", "read": 4,
        "img": P + "prod-rice.jpg",
        "excerpt": "Grain length, ageing, broken percentage and packing: the specification points that drive rice price and quality.",
        "body": [
            ("Two families, many grades", "Basmati is known for extra-long grains that elongate on cooking and for its aroma. Non-basmati covers a wide group of varieties used for everyday staples. Within each, grades vary a great deal."),
            ("The numbers that matter", "Agree the grain length, the maximum broken percentage, moisture, and the level of foreign matter. For basmati, also agree whether the rice is aged and whether it is steam, raw or sella (parboiled)."),
            ("Sample first", "Approve a pre-shipment sample and keep a sealed counter-sample. If a quality claim arises later, both sides can refer to the same reference."),
            ("Packing and marking", "Bag size, material and printing differ by market, and some destinations are strict about labelling. Settle this before production, not after."),
        ],
    },
    {
        "slug": "incoterms-fob-cif-cfr", "title": "FOB, CFR or CIF: choosing your shipping terms", "tag": "Trade basics", "read": 3,
        "img": P + "bg-sea.jpg",
        "excerpt": "Incoterms decide who pays for what and who carries the risk. A short guide to the most used sea-freight terms.",
        "body": [
            ("Why it matters", "Incoterms are standard terms that say where costs and risk move from seller to buyer. A clear choice avoids disputes over damage, delay and charges."),
            ("The common three", "Under FOB the seller loads the goods on the vessel at the origin port. Under CFR the seller also pays freight to the destination port. Under CIF the seller adds minimum insurance to CFR."),
            ("Which to choose", "If you have strong freight rates or your own forwarder, FOB gives control. If you prefer a single landed quote, CFR or CIF is simpler. Check the rules in your destination country too."),
            ("Put it in writing", "State the Incoterm and its version, together with the named port, in the contract and on the invoice."),
        ],
    },
    {
        "slug": "pre-shipment-inspection-agro", "title": "What a pre-shipment inspection looks at", "tag": "Quality", "read": 4,
        "img": P + "quality.jpg",
        "excerpt": "Sampling, moisture, purity, packing and loading: how an inspection protects a bulk agro shipment.",
        "body": [
            ("Inspect before it leaves", "A pre-shipment inspection checks the goods at origin, when problems are still cheap to fix. It protects both buyer and supplier with an independent record."),
            ("What is checked", "Representative sampling, grade and size, moisture, foreign matter and visible damage, plus quantity, packing, marking and container condition."),
            ("Loading supervision", "Many problems arise at loading: the wrong lot, damaged bags, a dirty container. An inspector present at loading catches these and seals the container."),
            ("The report", "The result is a report with findings and photographs. You can approve the shipment, ask for corrections, or reject the lot before freight is paid."),
        ],
    },
]


def insight_by_slug(slug):
    return next((a for a in INSIGHTS if a["slug"] == slug), None)
