"""Curated storefront descriptions for the RedCart catalogue, keyed by product name.

Used by the ``fill_descriptions`` management command. Exact specifications can
differ between model years, regions and configurations, so the copy sticks to
well-established features of each product line.
"""

DESCRIPTIONS = {
    # ── Phones ────────────────────────────────────────────────────────────────
    'iPhone 15 Pro Max': (
        "Apple's largest Pro iPhone pairs a lightweight titanium design with the A17 Pro chip "
        "for fast performance in apps, games and video editing.",
        [
            '6.7-inch Super Retina XDR display with ProMotion and Always-On',
            '48MP main camera plus a 5x optical-zoom telephoto camera',
            'Customisable Action button and USB-C connector',
            'Ceramic Shield front and all-day battery life',
        ],
    ),
    'Samsung Galaxy S24 Ultra': (
        "Samsung's flagship comes with a built-in S Pen, a titanium frame and Galaxy AI tools "
        "for live translation, note summaries and smarter photo editing.",
        [
            '6.8-inch QHD+ Dynamic AMOLED 2X display',
            '200MP main camera with long-range zoom',
            'Integrated S Pen for notes, sketches and precise control',
            'Snapdragon 8 Gen 3 for Galaxy processor',
        ],
    ),
    'Google Pixel 8 Pro': (
        "Google's Pixel 8 Pro is built around the Tensor G3 chip and Google's computational "
        "photography, with editing tools like Magic Editor and Best Take.",
        [
            '6.7-inch Super Actua display with a 120Hz refresh rate',
            'Triple rear camera with 5x optical telephoto',
            'Seven years of Android OS and security updates',
            'Built-in temperature sensor',
        ],
    ),
    'OnePlus 12': (
        "The OnePlus 12 is a flagship phone with Snapdragon 8 Gen 3 power, Hasselblad-tuned "
        "cameras and charging that gets you back to a full battery quickly.",
        [
            '6.82-inch 120Hz ProXDR display',
            'Large 5,400mAh battery with fast SUPERVOOC wired charging',
            'Wireless charging support',
            'Hasselblad camera system with a periscope telephoto',
        ],
    ),
    'Xiaomi Redmi Note 13 Pro': (
        "A mid-range phone with a 200MP main camera, a bright AMOLED screen and fast charging "
        "at a price that suits everyday buyers.",
        [
            '6.67-inch 120Hz AMOLED display',
            '200MP main camera with optical image stabilisation',
            '67W turbo charging',
            '5,000mAh-class battery for all-day use',
        ],
    ),
    'Infinix Zero 30': (
        "The Infinix Zero 30 is built for selfies and content creation, with a 50MP front camera "
        "that records 4K video and a curved AMOLED display.",
        [
            'Curved AMOLED display with a high refresh rate',
            '50MP front camera with 4K video recording',
            'High-resolution main rear camera',
            'Fast charging and a slim, light design',
        ],
    ),
    'Motorola Edge 50 Pro': (
        "Motorola's Edge 50 Pro combines a curved pOLED display, very fast TurboPower charging "
        "and Pantone-validated colour in a slim, premium body.",
        [
            '6.7-inch curved pOLED display with a 144Hz refresh rate',
            '125W TurboPower wired charging',
            '50MP main camera with AI-assisted photo tools',
            'Snapdragon 7 Gen 3 processor',
        ],
    ),
    'Nothing Phone 2a': (
        "The Nothing Phone (2a) brings the brand's see-through design and Glyph light interface "
        "to a more affordable phone with a clean, fast Nothing OS.",
        [
            '6.7-inch 120Hz AMOLED display',
            'Dual 50MP rear cameras',
            'Glyph Interface lights for notifications and timers',
            '5,000mAh battery',
        ],
    ),
    'Realme GT 6': (
        "The Realme GT 6 is a performance-focused phone with a Snapdragon 8s Gen 3 chip, a very "
        "bright display and 120W charging.",
        [
            '6.78-inch AMOLED display with very high peak brightness',
            '50MP main camera with optical image stabilisation',
            '5,500mAh battery with 120W fast charging',
            'Large cooling system for sustained gaming',
        ],
    ),

    # ── Laptops ───────────────────────────────────────────────────────────────
    'MacBook Pro 16 M3': (
        "The 16-inch MacBook Pro with Apple silicon is made for demanding work like video "
        "editing, music production and software development, with long battery life.",
        [
            '16.2-inch Liquid Retina XDR display',
            'Apple M3-series chip with unified memory',
            'Thunderbolt ports, HDMI, SDXC card slot and MagSafe 3 charging',
            '1080p FaceTime HD camera and six-speaker sound system',
        ],
    ),
    'Dell XPS 15': (
        "The Dell XPS 15 puts a large, nearly borderless display in a machined aluminium body, "
        "with enough power for creative work and everyday productivity.",
        [
            '15.6-inch InfinityEdge display (OLED options available)',
            'Intel Core processors with optional NVIDIA GeForce RTX graphics',
            'Aluminium chassis with a carbon-fibre palm rest',
            'Large precision touchpad and backlit keyboard',
        ],
    ),
    'HP spectre x360': (
        "The HP Spectre x360 is a premium 2-in-1 laptop with a 360-degree hinge, so you can use "
        "it as a laptop, tent, stand or tablet.",
        [
            'Convertible design with touchscreen and pen support',
            'Vivid display options including OLED',
            'Intel Core processors for smooth multitasking',
            'Premium metal design with a privacy camera shutter',
        ],
    ),
    'Lenovo ThinkPad X1 Carbon': (
        "Lenovo's flagship business ultrabook is known for its light carbon-fibre build, "
        "comfortable keyboard and business-grade security.",
        [
            'Lightweight carbon-fibre chassis',
            'Tested against MIL-STD-810H durability standards',
            'Classic ThinkPad keyboard with TrackPoint',
            'Thunderbolt 4 ports and fingerprint login',
        ],
    ),
    'ASUS ROG Zephyrus G14': (
        "The Zephyrus G14 is a compact 14-inch gaming laptop that fits strong graphics into a "
        "bag-friendly body for gaming and creative work on the go.",
        [
            'AMD Ryzen processor with NVIDIA GeForce RTX graphics',
            '14-inch high-refresh-rate display',
            'Portable design that is light for a gaming laptop',
            'Fast storage and memory for quick load times',
        ],
    ),
    'Microsoft Surface Pro 9': (
        "Surface Pro 9 is a tablet that turns into a laptop, with a built-in kickstand and "
        "support for Surface keyboards and pens.",
        [
            '13-inch PixelSense Flow touchscreen with up to 120Hz refresh rate',
            'Built-in adjustable kickstand',
            'Works with the Surface Pro Signature Keyboard and Slim Pen 2 (sold separately)',
            'Runs full Windows 11',
        ],
    ),
    'Razer Blade 15': (
        "The Razer Blade 15 puts desktop-class gaming performance into a slim CNC-milled "
        "aluminium body that also suits creative work.",
        [
            'NVIDIA GeForce RTX graphics',
            'High-refresh-rate 15.6-inch display',
            'Precision-machined aluminium unibody',
            'Per-key Razer Chroma RGB keyboard',
        ],
    ),
    'MSI Creator Z16': (
        "The MSI Creator Z16 is made for designers, editors and 3D artists, with a colour-accurate "
        "touch display and powerful graphics.",
        [
            '16-inch QHD+ 16:10 touch display with wide DCI-P3 colour coverage',
            'Intel Core processor with NVIDIA GeForce RTX graphics',
            'CNC-milled aluminium body',
            'Thunderbolt connectivity for fast external drives and displays',
        ],
    ),
    'Acer Swift 3': (
        "The Acer Swift 3 is a thin, light everyday laptop for studying, office work and "
        "streaming, with good battery life.",
        [
            'Slim, light aluminium design',
            'Full HD display',
            'Fingerprint reader for quick sign-in',
            'USB-C, USB-A and HDMI connectivity',
        ],
    ),

    # ── Gaming ────────────────────────────────────────────────────────────────
    'PlayStation 5 Slim': (
        "The PS5 Slim is a smaller, lighter PlayStation 5 with more built-in storage, playing "
        "the full PS5 library with fast load times.",
        [
            '1TB SSD for near-instant loading',
            'DualSense controller with haptic feedback and adaptive triggers',
            '4K gaming with ray tracing support',
            'Plays most PS4 games',
        ],
    ),
    'Xbox Series X': (
        "The Xbox Series X is Microsoft's most powerful console, built for 4K gaming, fast "
        "loading and thousands of games through backward compatibility.",
        [
            '4K gaming at up to 120 frames per second',
            '1TB custom NVMe SSD',
            'Quick Resume to switch between several games instantly',
            'Works with Xbox Game Pass (subscription sold separately)',
        ],
    ),
    'Nintendo Switch OLED': (
        "The Nintendo Switch OLED model has a larger, more vivid 7-inch OLED screen and plays "
        "on your TV, on a table or in your hands.",
        [
            '7-inch OLED screen with vivid colour and contrast',
            'Wide adjustable stand for tabletop play',
            '64GB internal storage, expandable with microSD',
            'Dock with a wired LAN port',
        ],
    ),
    'Razer DeathAdder V3': (
        "The DeathAdder V3 is a very light version of Razer's ergonomic esports mouse, shaped "
        "for comfort in long sessions.",
        [
            'Ultra-lightweight ergonomic right-handed shape',
            'Razer Focus Pro optical sensor',
            'Razer optical mouse switches for fast, consistent clicks',
            'Flexible Speedflex cable',
        ],
    ),
    'SteelSeries Apex Pro Keyboard': (
        "The Apex Pro lets you set how far each key travels before it registers, so you can "
        "tune it for fast gaming or relaxed typing.",
        [
            'OmniPoint adjustable-actuation switches',
            'OLED smart display for settings and notifications',
            'Aircraft-grade aluminium frame',
            'Per-key RGB lighting and magnetic wrist rest',
        ],
    ),
    'Elgato Stream Deck MK.2': (
        "Stream Deck MK.2 gives you 15 customisable LCD keys to control your stream, apps and "
        "smart home with one touch.",
        [
            '15 programmable LCD keys with custom icons',
            'Integrations for OBS, Twitch, YouTube, Spotify and more',
            'Detachable USB-C cable and adjustable stand',
            'Interchangeable faceplates',
        ],
    ),
    'Logitech G Pro X Superlight': (
        "A very light wireless esports mouse made with professional players, built for speed "
        "and precision without a cable.",
        [
            'Ultra-lightweight wireless design',
            'HERO 25K sensor for precise tracking',
            'LIGHTSPEED low-latency wireless',
            'Long battery life on a single charge',
        ],
    ),
    'Elgato 4K Capture Card': (
        "Record and stream console or PC gameplay in high quality with Elgato's 4K capture "
        "technology and passthrough so you can keep playing lag-free.",
        [
            'Capture and stream gameplay in up to 4K',
            'HDR passthrough to your TV or monitor',
            'Works with OBS Studio and Elgato 4K Capture Utility',
            'Supports PlayStation, Xbox, Nintendo Switch and PC',
        ],
    ),
    'Razer BlackShark V2 Headset': (
        "The BlackShark V2 is a wired esports headset with clear voice pickup and positional "
        "audio so you can hear where the action is.",
        [
            'Razer TriForce Titanium 50mm drivers',
            'THX Spatial Audio support',
            'Detachable HyperClear cardioid microphone',
            'Memory-foam ear cushions and a light frame',
        ],
    ),
    'Xbox Elite Controller Series 2': (
        "Microsoft's premium Xbox controller lets you adjust and swap parts to fit how you play, "
        "on Xbox and Windows PC.",
        [
            'Adjustable-tension thumbsticks and shorter hair-trigger locks',
            'Interchangeable thumbsticks, D-pad and paddles',
            'Rechargeable battery with charging case',
            'Up to three custom profiles stored on the controller',
        ],
    ),

    # ── Watches ───────────────────────────────────────────────────────────────
    'Rolex Submariner': (
        "Launched in 1953, the Rolex Submariner is the classic dive watch and one of the most "
        "recognisable luxury watches in the world.",
        [
            'Oyster case water resistant to 300 metres',
            'Unidirectional rotatable bezel with Cerachrom ceramic insert',
            'Self-winding Rolex movement, certified Superlative Chronometer',
            'Chromalight luminous display for low-light reading',
        ],
    ),
    'Apple Watch Series 9': (
        "Apple Watch Series 9 tracks your health and fitness and keeps you connected, with a "
        "brighter display and a hands-free double tap gesture.",
        [
            'S9 chip with double tap gesture',
            'Bright Always-On Retina display',
            'Heart rate, ECG and sleep tracking',
            'Crash Detection and Fall Detection',
        ],
    ),
    'Casio G-Shock GA-2100': (
        "The G-Shock GA-2100 has a slim octagonal case and the toughness G-Shock is known for, "
        "at an accessible price.",
        [
            'Carbon Core Guard structure for shock resistance',
            '200-metre water resistance',
            'Analogue-digital display with world time',
            'Stopwatch, countdown timer and LED light',
        ],
    ),
    'Garmin Fenix 7X': (
        "The Fenix 7X is Garmin's large-format multisport GPS watch for hiking, running, "
        "cycling and expeditions, with very long battery life.",
        [
            'Multi-band GPS with preloaded topographic maps',
            'Solar charging on Solar editions',
            'Built-in LED flashlight',
            'Advanced training, recovery and health metrics',
        ],
    ),
    'Samsung Galaxy Watch 6 Classic': (
        "The Galaxy Watch 6 Classic brings back Samsung's rotating bezel, with health "
        "tracking and Wear OS apps in a classic watch design.",
        [
            'Physical rotating bezel for easy navigation',
            'Sapphire crystal display',
            'Body composition, heart rate and sleep coaching',
            'Wear OS with Google apps',
        ],
    ),
    'Omega Seamaster Diver 300M': (
        "A dive watch with roots in 1993, the Seamaster Diver 300M is known for its wave-pattern "
        "dial and has appeared on James Bond's wrist.",
        [
            '300-metre water resistance with helium escape valve',
            'Omega Co-Axial Master Chronometer movement',
            'Ceramic dial and bezel with laser-engraved wave pattern',
            'Sapphire crystal',
        ],
    ),
    'Tag Heuer Carrera': (
        "Introduced in 1963 and inspired by motor racing, the TAG Heuer Carrera is a sporty, "
        "elegant watch that works for both work and weekends.",
        [
            'Motorsport-inspired design heritage',
            'Swiss-made automatic movement',
            'Scratch-resistant sapphire crystal',
            'Chronograph versions available',
        ],
    ),
    'Seiko Prospex Speedtimer': (
        "Part of Seiko's Prospex sports line, the Speedtimer is a chronograph that draws on "
        "Seiko's long history of timing sport.",
        [
            'Chronograph function for timing events',
            'Sporty dial inspired by Seiko racing chronographs',
            'Stainless steel case and bracelet',
            'Check the exact reference for movement and features',
        ],
    ),
    'Amazfit GTR 4': (
        "The Amazfit GTR 4 is a round smartwatch with long battery life, accurate GPS and "
        "health tracking at a mid-range price.",
        [
            '1.43-inch AMOLED display',
            'Dual-band GPS for accurate route tracking',
            'Up to 14 days of typical battery life',
            '150+ sports modes and 24/7 heart rate tracking',
        ],
    ),

    # ── Sneakers ──────────────────────────────────────────────────────────────
    'Nike Air Max 270': (
        "The Air Max 270 was Nike's first lifestyle Air Max, with a tall heel Air unit for soft "
        "cushioning all day.",
        [
            'Large visible Air unit in the heel',
            'Breathable mesh upper',
            'Foam midsole for lightweight comfort',
            'Rubber outsole for traction',
        ],
    ),
    'Adidas Ultraboost 23': (
        "The Ultraboost 23 is a cushioned running shoe that also works for everyday wear, with "
        "springy Boost cushioning and a sock-like upper.",
        [
            'Light BOOST midsole for energy return',
            'Primeknit+ upper for an adaptive fit',
            'Linear Energy Push system for a responsive ride',
            'Continental Rubber outsole for grip',
        ],
    ),
    'Jordan 1 Retro High OG': (
        "The shoe that started the Air Jordan line in 1985, the Jordan 1 High OG is a classic "
        "high-top that stays popular on and off the court.",
        [
            'Premium leather upper',
            'Air-Sole unit in the heel for cushioning',
            'Wings logo on the ankle collar',
            'Rubber cupsole with classic pivot-point traction',
        ],
    ),
    'New Balance 574': (
        "The New Balance 574 is a classic, easy-to-wear sneaker that has been a favourite since "
        "the late 1980s.",
        [
            'Suede and mesh upper',
            'ENCAP midsole for cushioning and support',
            'Rubber outsole for durability',
            'Retro running-inspired design',
        ],
    ),
    'Converse Chuck Taylor All Star': (
        "The Chuck Taylor All Star is one of the most recognisable sneakers ever made, with a "
        "simple canvas design that goes with almost anything.",
        [
            'Durable canvas upper',
            'Rubber toe cap and vulcanised sole',
            'Cushioned insole for comfort',
            'Iconic All Star ankle patch on high-tops',
        ],
    ),
    'Vans Old Skool': (
        "The Vans Old Skool is a classic skate shoe from 1977 and the first Vans shoe to feature "
        "the famous side stripe.",
        [
            'Suede and canvas upper',
            'Padded collar for support and comfort',
            'Signature rubber waffle outsole',
            'Reinforced toe cap',
        ],
    ),
    'ASICS Gel-Kayano 30': (
        "The Gel-Kayano 30 is ASICS's stability running shoe, giving extra support to runners "
        "whose feet roll inward.",
        [
            '4D GUIDANCE SYSTEM for adaptive stability',
            'FF BLAST PLUS ECO cushioning',
            'PureGEL technology in the heel for softer landings',
            'Engineered mesh upper',
        ],
    ),
    'Hoka Clifton 9': (
        "The Clifton 9 is Hoka's light, cushioned daily trainer, made for comfortable miles on "
        "the road and long days on your feet.",
        [
            'Lightweight, responsive foam midsole',
            'Early-stage Meta-Rocker for smooth heel-to-toe transitions',
            'Breathable knit upper',
            'Rubber outsole in high-wear areas',
        ],
    ),
    'Salomon Speedcross 6': (
        "The Speedcross 6 is Salomon's aggressive trail running shoe, built for grip on mud, "
        "loose ground and technical trails.",
        [
            'Deep chevron lugs with Mud Contagrip rubber',
            'Quicklace system for fast, secure lacing',
            'SensiFit construction for a locked-in fit',
            'Protective toe cap',
        ],
    ),
    'Puma RS-X': (
        "The Puma RS-X is a chunky, retro-inspired sneaker based on Puma's Running System "
        "shoes from the 1980s.",
        [
            'RS cushioning for everyday comfort',
            'Mixed mesh, leather and suede upper',
            'Bold chunky silhouette',
            'Rubber outsole',
        ],
    ),

    # ── Electronics ───────────────────────────────────────────────────────────
    'Sony WH-1000XM5': (
        "Sony's WH-1000XM5 are wireless over-ear headphones with excellent noise cancelling and "
        "clear calls, made for travel, work and focus.",
        [
            'Industry-leading noise cancelling with multiple microphones',
            'Up to 30 hours of battery life',
            'Quick charging and multipoint Bluetooth connection',
            'Speak-to-Chat and adaptive sound control',
        ],
    ),
    'Samsung 65-inch QLED TV': (
        "A 65-inch Samsung QLED smart TV with Quantum Dot colour and 4K resolution, for movies, "
        "sport and gaming.",
        [
            '65-inch 4K display with Quantum Dot technology',
            'HDR support for brighter, more detailed scenes',
            'Tizen smart TV platform with popular streaming apps',
            'Exact features depend on the model year and series',
        ],
    ),
    'Anker 737 Power Bank': (
        "The Anker 737 is a high-capacity power bank that can charge a laptop, tablet and phone, "
        "with a screen that shows charging information in real time.",
        [
            '24,000mAh capacity',
            'Up to 140W total output for laptops',
            'Smart digital display shows remaining power and wattage',
            'Two USB-C ports and one USB-A port',
        ],
    ),
    'Logitech MX Master 3S Mouse': (
        "The MX Master 3S is Logitech's advanced productivity mouse, with quiet clicks, a "
        "fast scroll wheel and tracking on almost any surface.",
        [
            '8,000 DPI sensor that tracks even on glass',
            'Quiet clicks',
            'MagSpeed electromagnetic scroll wheel',
            'Connects to up to three devices with Easy-Switch',
        ],
    ),
    'LG 27-inch 4K Monitor': (
        "A 27-inch LG 4K UHD monitor with sharp detail and accurate colour, ideal for office "
        "work, photo editing and entertainment.",
        [
            '27-inch 4K UHD (3840 x 2160) resolution',
            'IPS panel for wide viewing angles',
            'HDR10 support',
            'Exact ports and features depend on the model',
        ],
    ),
    'GoPro Hero 12 Black': (
        "The GoPro HERO12 Black is a rugged, waterproof action camera that records very smooth, "
        "high-resolution video for sports, travel and vlogging.",
        [
            '5.3K video and 27MP photos',
            'HyperSmooth 6.0 video stabilisation',
            'Waterproof to 10 metres without a housing',
            'HDR video and improved battery life',
        ],
    ),
    'DJI Mini 4 Pro': (
        "The DJI Mini 4 Pro is a compact, lightweight camera drone with obstacle sensing and "
        "pro-level video features in a foldable body.",
        [
            'Weighs under 249 grams',
            '4K HDR video and true vertical shooting',
            'Omnidirectional obstacle sensing',
            'ActiveTrack subject tracking',
        ],
    ),
    'Blue Yeti USB Microphone': (
        "The Blue Yeti is a popular plug-and-play USB microphone for podcasting, streaming, "
        "voice-overs and video calls.",
        [
            'Four pickup patterns: cardioid, omni, bidirectional and stereo',
            'Plug-and-play USB on Mac and Windows',
            'Zero-latency headphone output',
            'On-mic gain control and mute button',
        ],
    ),
    'Kindle Paperwhite 11th Gen': (
        "The Kindle Paperwhite is a waterproof e-reader with a glare-free screen that reads like "
        "paper, even in bright sunlight.",
        [
            '6.8-inch 300 ppi glare-free display',
            'Adjustable warm light',
            'IPX8 waterproof',
            'USB-C charging and battery that lasts weeks',
        ],
    ),

    # ── Home Appliances ───────────────────────────────────────────────────────
    'Dyson V15 Detect Vacuum': (
        "The Dyson V15 Detect is a powerful cordless vacuum that uses a laser to show hidden "
        "dust and a sensor to measure what it picks up.",
        [
            'Laser head reveals fine dust on hard floors',
            'Particle sensor shows dust counts on an LCD screen',
            'Up to 60 minutes of run time',
            'Advanced whole-machine filtration',
        ],
    ),
    'KitchenAid Stand Mixer': (
        "The KitchenAid tilt-head stand mixer is a kitchen classic for mixing, kneading and "
        "whipping, with a power hub for many optional attachments.",
        [
            '10 speeds for everything from stirring to whipping',
            'Planetary mixing action for thorough mixing',
            'Stainless steel bowl',
            'Power hub fits pasta, mincer and other attachments (sold separately)',
        ],
    ),
    'Nespresso Vertuo Pop': (
        "The Vertuo Pop is a compact Nespresso machine that brews espresso and larger coffees at "
        "the touch of a button.",
        [
            'Brews several cup sizes from espresso to mug',
            'Reads the barcode on each capsule for the right recipe',
            'Compact size suited to small kitchens',
            'Uses Nespresso Vertuo capsules',
        ],
    ),
    'Instant Pot Duo 7-in-1': (
        "The Instant Pot Duo replaces several kitchen appliances, so you can cook stews, rice, "
        "beans, soups and more quickly in one pot.",
        [
            'Pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yoghurt maker and warmer',
            'One-touch smart programmes',
            'Stainless steel inner pot',
            'Built-in safety features',
        ],
    ),
    'Ninja Air Fryer Pro': (
        "The Ninja Air Fryer Pro gives crispy results with little to no oil, and can also roast, "
        "reheat and dehydrate.",
        [
            'Air fry, roast, reheat and dehydrate functions',
            'High maximum temperature for extra crispiness',
            'Non-stick, dishwasher-safe basket and crisper plate',
            'Family-friendly basket size',
        ],
    ),
    'iRobot Roomba j7+': (
        "The Roomba j7+ is a smart robot vacuum that spots and avoids obstacles like cords and "
        "pet waste, then empties itself.",
        [
            'PrecisionVision Navigation to avoid common obstacles',
            'Clean Base automatic dirt disposal',
            'Smart mapping to clean specific rooms',
            'Control with the iRobot app or voice assistants',
        ],
    ),
    'Breville Barista Express': (
        "The Barista Express is an espresso machine with a built-in grinder, so you can go from "
        "beans to espresso in under a minute.",
        [
            'Integrated conical burr grinder with dose control',
            'Precise digital temperature control (PID)',
            'Low-pressure pre-infusion for balanced extraction',
            'Steam wand for hand-textured milk',
        ],
    ),
    'Samsung French Door Refrigerator': (
        "A spacious Samsung French door refrigerator with fresh food at eye level and a "
        "bottom freezer, made for busy family kitchens.",
        [
            'French door design with bottom-mount freezer',
            'Large capacity for family groceries',
            'Energy-efficient inverter compressor',
            'Exact capacity and dispenser features depend on the model',
        ],
    ),
    'Cuisinart Food Processor 14-Cup': (
        "This 14-cup Cuisinart food processor chops, slices, shreds and kneads large batches "
        "for family meals and meal prep.",
        [
            'Large 14-cup work bowl',
            'Stainless steel chopping, slicing and shredding blades',
            'Extra-large feed tube',
            'Simple on and pulse controls',
        ],
    ),
    'Weber Spirit II Gas Grill': (
        "The Weber Spirit II is a reliable gas grill for backyard cooking, with even heat and "
        "easy ignition.",
        [
            'GS4 grilling system for reliable ignition and even heat',
            'Porcelain-enamelled cast-iron cooking grates',
            'Flavorizer bars and grease management system',
            'Open cart design with tool hooks and side tables',
        ],
    ),

    # ── Fitness ───────────────────────────────────────────────────────────────
    'Peloton Bike+': (
        "The Peloton Bike+ is a premium indoor exercise bike with a large rotating touchscreen "
        "for live and on-demand classes at home.",
        [
            'Large rotating HD touchscreen for on- and off-bike workouts',
            'Auto-Follow resistance that adjusts with your instructor',
            'Apple GymKit integration',
            'Classes need a Peloton membership (sold separately)',
        ],
    ),
    'Theragun Pro Gen 6': (
        "Theragun Pro is Therabody's professional massage gun, used to ease muscle tension and "
        "support recovery after training.",
        [
            'Deep percussive therapy',
            'Ergonomic multi-grip handle and adjustable arm',
            'Interchangeable attachments for different muscle groups',
            'App-guided routines via Bluetooth',
        ],
    ),
    'Bowflex SelectTech 552 Dumbbells': (
        "Bowflex SelectTech 552 dumbbells replace a full rack of weights, letting you change "
        "the load with a simple turn of a dial.",
        [
            'Adjusts from 2 to 24 kg (5 to 52.5 lb) per dumbbell',
            'Replaces 15 pairs of dumbbells',
            'Quick dial-based weight selection',
            'Compact storage for home gyms',
        ],
    ),
    'TRX All-in-One Suspension Trainer': (
        "The TRX All-in-One uses your body weight for full-body strength, core and mobility "
        "workouts at home, outdoors or while travelling.",
        [
            'Adjustable suspension straps',
            'Door anchor and suspension anchor included',
            'Light and portable with a mesh carry bag',
            'Works for beginners through advanced athletes',
        ],
    ),
    'Garmin HRM-Pro Plus': (
        "The HRM-Pro Plus is Garmin's premium chest-strap heart rate monitor, giving accurate "
        "heart rate data and advanced running metrics.",
        [
            'Accurate chest-based heart rate monitoring',
            'ANT+ and Bluetooth for watches, bikes and apps',
            'Running dynamics such as ground contact time',
            'Stores heart rate data during swims',
        ],
    ),
    'Concept2 RowErg Rowing Machine': (
        "The Concept2 RowErg is the rowing machine used in gyms and by athletes worldwide, "
        "giving a low-impact, full-body workout.",
        [
            'Air-resistance flywheel with adjustable damper',
            'PM5 performance monitor with Bluetooth and ANT+',
            'Separates into two pieces for storage',
            'Durable build for heavy daily use',
        ],
    ),
    'Fitbit Charge 6': (
        "The Fitbit Charge 6 is a slim fitness tracker with built-in GPS, accurate heart rate "
        "tracking and handy Google apps on your wrist.",
        [
            'Built-in GPS for phone-free runs',
            'Heart rate, sleep and stress tracking',
            'Google Maps and Google Wallet on the wrist',
            'Up to 7 days of battery life',
        ],
    ),

    # ── Accessories ───────────────────────────────────────────────────────────
    'Peak Design Everyday Backpack': (
        "The Peak Design Everyday Backpack is a weatherproof camera and everyday bag with "
        "flexible organisation and quick side access.",
        [
            'Weatherproof shell fabric',
            'FlexFold dividers for cameras, laptops and daily gear',
            'Dual side access and MagLatch top closure',
            'Dedicated laptop and tablet sleeve',
        ],
    ),
    'Ray-Ban Aviator Classic': (
        "First designed in 1937, the Ray-Ban Aviator Classic is one of the most famous "
        "sunglasses ever made.",
        [
            'Lightweight metal frame',
            'Crystal glass lenses with 100% UV protection',
            'Adjustable nose pads for a comfortable fit',
            'Comes with a Ray-Ban case',
        ],
    ),
    'Louis Vuitton bag': (
        "A Louis Vuitton handbag from the French house famous for its fine leather goods and "
        "Monogram canvas since 1854.",
        [
            'Signature Louis Vuitton craftsmanship',
            'Durable materials made for everyday use',
            'Timeless design for day and evening',
            'See the product photos for the exact model, size and colour',
        ],
    ),
    'Apple AirTag 4-Pack': (
        "Attach an AirTag to keys, bags or luggage and find them in the Find My app using "
        "Apple's large network of devices.",
        [
            'Four AirTags in one pack',
            'Precision Finding on compatible iPhones',
            'Built-in speaker to help you locate items',
            'Water and dust resistant, with a replaceable battery',
        ],
    ),
    'PopSockets PopGrip': (
        "The PopGrip sticks to the back of your phone to give you a secure grip and a stand "
        "for videos and calls.",
        [
            'Expands to grip, collapses flat',
            'Works as a stand for landscape viewing',
            'Swappable top designs',
            'Repositionable adhesive base',
        ],
    ),
    'Moment Wide Lens for iPhone': (
        "Moment's Wide Lens is an add-on glass lens that captures a wider view on your phone "
        "camera without the distortion of cheaper clip-on lenses.",
        [
            'Premium glass optics',
            'Wider field of view for landscapes, architecture and groups',
            'Sharp edge-to-edge image quality',
            'Mounts with a Moment-compatible case (sold separately)',
        ],
    ),
    'Oakley Holbrook Sunglasses': (
        "The Oakley Holbrook has a classic square frame inspired by mid-century style, with "
        "Oakley's lens and frame technology.",
        [
            'Lightweight, durable O Matter frame',
            'Plutonite lens material that blocks 100% of UV',
            'Prizm lens options for better contrast',
            'Three-point fit for comfort',
        ],
    ),
    'Bellroy Card Holder Wallet': (
        "Bellroy's card holder is a slim leather wallet for people who carry only a few cards "
        "and want a flatter pocket.",
        [
            'Slim, minimal design',
            'Premium environmentally certified leather',
            'Quick-access card slots',
            'Fits easily in a front pocket',
        ],
    ),
    'Gucci Dionysus Mini Bag': (
        "The Gucci Dionysus is one of the house's best-known bags, recognisable by its "
        "textured tiger-head closure.",
        [
            'Signature tiger-head spur closure',
            'Sliding chain strap for shoulder or crossbody wear',
            'Compact mini size for daily essentials',
            'See the product photos for exact material and colour',
        ],
    ),

    # ── Fashion ───────────────────────────────────────────────────────────────
    "Levi's 501 Original Jeans": (
        "The Levi's 501 is the original blue jean, first made in 1873, with a straight leg and "
        "classic button fly.",
        [
            'Straight-leg fit that sits at the waist',
            'Signature button fly',
            'Durable cotton denim',
            'Classic five-pocket styling',
        ],
    ),
    'Nike Tech Fleece Hoodie': (
        "Nike Tech Fleece gives you warmth without bulk, with a smooth, structured look that "
        "works for training and everyday wear.",
        [
            'Lightweight Tech Fleece fabric',
            'Full-length zip',
            'Zipped pocket for small items',
            'Tailored, modern fit',
        ],
    ),
    'Ralph Lauren Polo Shirt': (
        "The Ralph Lauren polo is a timeless smart-casual shirt made from breathable cotton "
        "mesh, with the brand's embroidered pony.",
        [
            'Breathable cotton mesh fabric',
            'Signature embroidered Polo Pony',
            'Ribbed collar and armbands',
            'Two-button placket',
        ],
    ),
    'Zara Oversized Blazer': (
        "A relaxed, oversized blazer that dresses up jeans or completes a tailored outfit for "
        "the office or a night out.",
        [
            'Oversized, relaxed fit',
            'Lapel collar and long sleeves',
            'Button front fastening',
            'Easy to dress up or down',
        ],
    ),
    'H&M Linen Shirt': (
        "A lightweight linen shirt that stays cool and comfortable in warm weather, for "
        "casual days or smart-casual events.",
        [
            'Breathable linen fabric',
            'Relaxed fit',
            'Classic collar and button front',
            'Gets softer with every wash',
        ],
    ),
    'North Face Puffer Jacket': (
        "A warm, insulated puffer jacket from The North Face, made to handle cold weather and "
        "travel.",
        [
            'Insulated quilted design for warmth',
            'Water-repellent outer fabric',
            'Zip-up front and secure hand pockets',
            'Exact insulation and features depend on the model',
        ],
    ),
    'Acne Studios Biker Jacket': (
        "A leather biker jacket from Stockholm label Acne Studios, with a clean, modern take on "
        "the classic motorcycle style.",
        [
            'Leather construction',
            'Asymmetric zip front',
            'Notched lapels and zip pockets',
            'Gets better with age and wear',
        ],
    ),
    'Uniqlo Cashmere Turtleneck': (
        "A soft cashmere turtleneck from Uniqlo that adds warmth and polish to everyday "
        "outfits.",
        [
            '100% cashmere',
            'Classic turtleneck collar',
            'Soft, lightweight warmth',
            'Easy to layer under jackets and coats',
        ],
    ),
    'Burberry Trench Coat': (
        "The Burberry trench coat is the original, made in the cotton gabardine fabric that "
        "Thomas Burberry invented, and a lasting wardrobe classic.",
        [
            'Weather-resistant cotton gabardine',
            'Double-breasted front with belted waist',
            'Classic storm shield and epaulettes',
            'Signature Burberry check lining',
        ],
    ),

    # ── Home ──────────────────────────────────────────────────────────────────
    'Hydro Flask 32oz Water Bottle': (
        "The Hydro Flask 32 oz is an insulated stainless steel bottle that keeps drinks cold "
        "or hot for hours.",
        [
            'TempShield double-wall vacuum insulation',
            'Keeps drinks cold up to 24 hours or hot up to 12 hours',
            'Durable 18/8 pro-grade stainless steel',
            'BPA-free, leak-proof Flex Cap',
        ],
    ),
    'IKEA KALLAX Shelf Unit': (
        "The IKEA KALLAX is a simple cube shelving unit you can use for books, records, "
        "storage boxes or as a room divider.",
        [
            'Stand it upright or on its side',
            'Works with KALLAX inserts, drawers and boxes (sold separately)',
            'Finished on all sides, so it works as a room divider',
            'Simple, clean design for any room',
        ],
    ),
    'Yankee Candle Large Jar': (
        "A Yankee Candle large jar candle that fills your room with fragrance, in the brand's "
        "classic glass jar.",
        [
            'Large classic glass jar',
            'Long burn time',
            'Strong, room-filling fragrance',
            'Scent varies — see the product photos for details',
        ],
    ),
    'Lodge Cast Iron Frying Pan': (
        "Lodge cast iron skillets are pre-seasoned and ready to use, with excellent heat "
        "retention for searing, frying and baking.",
        [
            'Pre-seasoned with vegetable oil',
            'Works on gas, electric, induction, in the oven and over a campfire',
            'Excellent heat retention and even cooking',
            'Built to last for generations',
        ],
    ),
    'Cuisinart Cutting Board Set': (
        "A set of Cuisinart cutting boards in several sizes, so you can keep meat, vegetables "
        "and bread prep separate.",
        [
            'Multiple board sizes for different tasks',
            'Helps avoid cross-contamination between foods',
            'Easy to clean',
            'Practical everyday kitchen essential',
        ],
    ),
    'Brooklinen Luxury Sheet Set': (
        "Brooklinen's Luxe sheets are made from smooth, silky cotton sateen for a hotel-style "
        "bed at home.",
        [
            'Cotton sateen with a smooth, soft finish',
            'Includes flat sheet, fitted sheet and pillowcases',
            'Deep-pocket fitted sheet',
            'Gets softer with every wash',
        ],
    ),
    'Philips Hue Smart Bulb Starter Kit': (
        "The Philips Hue starter kit includes smart bulbs and the Hue Bridge, so you can "
        "control your lights from your phone or with your voice.",
        [
            'Millions of colours and shades of white light',
            'Hue Bridge for whole-home control and automations',
            'Works with Alexa, Google Assistant and Apple Home',
            'Schedules and routines in the Hue app',
        ],
    ),
    'Ring Video Doorbell 4': (
        "Ring Video Doorbell 4 lets you see, hear and speak to visitors from your phone, with "
        "colour video preview of what happened before motion was detected.",
        [
            '1080p HD video with two-way talk',
            'Colour Pre-Roll video preview',
            'Removable rechargeable battery or hardwired power',
            'Customisable motion zones',
        ],
    ),
    'Levoit Air Purifier Core 300': (
        "The Levoit Core 300 is a compact, quiet air purifier that helps remove dust, pollen, "
        "pet dander and smoke from bedrooms and offices.",
        [
            'Three-stage filtration with a True HEPA filter',
            'Quiet sleep mode',
            'Compact design for small to medium rooms',
            'Replaceable filters',
        ],
    ),
    'Dyson Airwrap Multi-Styler': (
        "The Dyson Airwrap uses airflow instead of extreme heat to curl, wave, smooth and dry "
        "hair with a set of attachments.",
        [
            'Curls and waves using air, without extreme heat',
            'Smoothing brushes and a pre-styling dryer',
            'Intelligent heat control to protect hair',
            'Several attachments for different styles',
        ],
    ),

    # ── Beauty (stored as Other) ──────────────────────────────────────────────
    'Charlotte Tilbury Flawless Filter': (
        "Charlotte Tilbury's Hollywood Flawless Filter is a complexion booster for a soft-focus, "
        "glowing finish.",
        [
            'Use as a primer, highlighter or mixed into foundation',
            'Gives skin a radiant, glowing look',
            'Available in a range of shades',
            'Lightweight, buildable formula',
        ],
    ),
    'The Ordinary Niacinamide Serum': (
        "The Ordinary Niacinamide 10% + Zinc 1% is a popular water-based serum for skin that "
        "looks oily or has blemishes and visible pores.",
        [
            'Niacinamide (vitamin B3) with zinc',
            'Helps the look of blemishes and enlarged pores',
            'Balances the look of oily skin',
            'Patch test before use and follow the directions',
        ],
    ),
}


def build_description(name):
    """Return the formatted description for ``name``, or ``None`` if it isn't in the catalogue."""
    entry = DESCRIPTIONS.get(name)
    if entry is None:
        return None
    overview, highlights = entry
    lines = '\n'.join(f'• {item}' for item in highlights)
    return f'{overview}\n\nHighlights\n{lines}'
