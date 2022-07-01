setup(
    name="Candle Companion",
    version="1.0.0",
    description="An app to manage candle making recipes and inventories",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Paul McPhillips",
    author_email="paul@mcphillips.cc",
    packages=["CandleCompanion"],
    include_package_data=True,
    install_requires=["pillow", "fpdf"],
    entry_points={""},
)