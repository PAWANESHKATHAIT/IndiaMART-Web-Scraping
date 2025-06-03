# IndiaMART LED Lights Product Analysis

## Project Overview

This project involves scraping product data for LED lights from IndiaMART, a major B2B marketplace in India. The acquired data undergoes a rigorous cleaning and preprocessing phase, followed by in-depth Exploratory Data Analysis (EDA) to uncover key insights into the LED lighting market, product characteristics, supplier trends, and pricing.

The goal is to provide a structured overview of the scraped data, making it amenable for further analysis, business intelligence, or machine learning applications.

## Project Objective

The primary objective of this project is to:
* **Acquire a relevant dataset** of LED light products from IndiaMART.
* **Clean and preprocess the raw data** to handle inconsistencies, missing values, and prepare it for analysis.
* **Perform Exploratory Data Analysis (EDA)** to understand product distributions, common attributes (brands, materials, colors, usage), pricing trends, and supplier geographical presence.
* **Derive actionable insights** and formulate hypotheses about the LED lights market on IndiaMART.

## Dataset

The dataset was obtained by scraping product listings for "LED Lights" from IndiaMART.com.

* **Source:** IndiaMART.com (B2B Marketplace)
* **Initial Size:** Approximately 100 entries.
* **Key Features Collected:** Product Name, URL, Price, Unit, Supplier Name, Supplier Location, PDP Attributes (Wattage, Brand, Body Material, IP Rating, Usage/Application, Lighting Color, Color Temperature, Country of Origin, Description), Supplier Rating, Supplier Reviews Count, Supplier Member Since.

## Project Structure & Workflow

The analysis was performed in a Jupyter Notebook, following these key stages:

### 1. Data Acquisition (Scraping)

* **Method:** Web scraping (details of the scraping script are assumed to be outside this README's scope but would typically involve libraries like `requests` and `BeautifulSoup` or `Scrapy`).
* **Output:** `indiamart_led_lights.csv` containing the raw scraped data.

### 2. Data Cleaning & Preprocessing

This crucial phase addressed several data quality issues to ensure the dataset's readiness for analysis.

* **Handling Missing Values:**
    * **Dropping Columns:** Columns with extreme sparsity (almost entirely missing data) such as `pdp_supplier_member_since`, `pdp_ip_rating`, and `pdp_color_temperature` were removed as they provided little analytical value.
    * **Categorical Imputation:** Missing values in remaining categorical columns (e.g., `pdp_brand`, `pdp_body_material`, `pdp_usage/application`) were filled with `'N/A'` to treat missingness as a distinct category, preserving data integrity.
    * **Numerical Imputation (Median):** Missing numerical data, specifically in `pdp_wattage_numeric` (derived from `pdp_wattage`), were imputed using the **median** of their respective columns. This method was chosen for its robustness against outliers and skewed distributions, which are common in price and wattage data.
* **Data Type Conversion:**
    * `product_price` (initially string with currency symbols) was converted to `product_price_numeric` (integer/float).
    * `pdp_wattage` (string with units/ranges) was extracted and converted to `pdp_wattage_numeric` (float).
    * Supplier rating and review counts were ensured to be in appropriate numerical formats.
* **Duplicate Handling Strategy:**
    * Initially, `product_url` was used for deduplication. However, due to high redundancy (90 out of 100 entries being duplicates based on URL), the `product_url` column was dropped entirely, and the deduplication step was skipped. This ensured all 100 scraped entries were retained for analysis, acknowledging that some might represent conceptual duplicates.

### 3. Exploratory Data Analysis (EDA)

The cleaned data was then analyzed to extract insights:

* **Summary Statistics:** Basic statistical descriptions of numerical features (`product_price_numeric`, `pdp_wattage_numeric`, `pdp_supplier_rating_numeric`, `pdp_supplier_reviews_count_numeric`).
* **Distribution Analysis:** Visualizations (histograms) to understand the distribution of prices, wattages, ratings, and review counts.
* **Common Attributes:** Analysis of top categories for `pdp_brand`, `pdp_body_material`, `pdp_usage/application`, `pdp_lighting_color`, `pdp_country_of_origin` using bar plots.
* **Product Description Insights:** A Word Cloud generated from `pdp_description` to highlight frequently used keywords.
* **Regional Insights:** Identification of top supplier locations to understand geographical distribution.
* **Relationships:** Exploration of correlations between variables, such as:
    * Product Price vs. Wattage (scatter plot).
    * Product Price vs. Supplier Rating (box plot).
    * Average Product Price by Top Brands.

## Key Findings & Insights (General Examples - Based on likely outcomes)

* **Price Range & Distribution:** Identification of typical price points for LED lights, and whether prices are concentrated at lower ends or spread widely.
* **Wattage Trends:** Common wattage requirements and the relationship between wattage and price.
* **Supplier Landscape:** Dominant supplier ratings (e.g., mostly high ratings), and the distribution of reviews indicating supplier popularity/trust.
* **Market Leaders:** Identification of prominent brands and materials in the LED light segment.
* **Usage Patterns:** Most common applications or lighting colors for LED products.
* **Geographic Hubs:** Key cities or states that serve as major supply centers for LED lights in India.
* **Data Completeness:** Acknowledgment of persistent data gaps for certain attributes, suggesting challenges in data collection or seller information practices on IndiaMART.

## Technologies Used

* **Python 3.x**
* **Jupyter Notebook:** For interactive analysis and documentation.
* **Pandas:** For data manipulation and analysis.
* **NumPy:** For numerical operations.
* **Matplotlib:** For basic plotting and visualization.
* **Seaborn:** For enhanced statistical data visualization.
* **NLTK:** (Natural Language Toolkit) For text processing (stopwords for Word Cloud).
* **WordCloud:** For generating word clouds from text data.
* **`re` module:** For regular expressions in text cleaning.

## How to Run the Code

1.  **Prerequisites:**
    * Ensure you have Python 3.x installed.
    * Install necessary libraries:
        ```bash
        pip install pandas numpy matplotlib seaborn nltk wordcloud
        ```
    * Download NLTK stopwords (run this once in a Python environment or Jupyter cell):
        ```python
        import nltk
        nltk.download('stopwords')
        ```
2.  **Data File:** Place your scraped data file (`indiamart_led_lights.csv`) in the same directory as your Jupyter Notebook.
3.  **Jupyter Notebook:**
    * Open your Jupyter Notebook.
    * Run the cells sequentially, starting from data loading, through cleaning, and then the EDA steps.

## Future Enhancements

* **Advanced Text Analysis:** Deeper NLP on product descriptions (e.g., topic modeling, sentiment analysis).
* **More Sophisticated Imputation:** Explore machine learning-based imputation techniques (e.g., KNN Imputer) if retaining the original distribution of missing data is critical for predictive modeling.
* **Outlier Detection:** Implement formal outlier detection methods for numerical features.
* **Categorical Encoding:** Prepare categorical features for machine learning models (e.g., One-Hot Encoding, Label Encoding).
* **Predictive Modeling:** Build models to predict product prices based on features, or to classify product types.
* **Time Series Analysis:** If supplier 'member since' dates were consistently available, analyze supplier age trends.
* **Interactive Visualizations:** Use libraries like Plotly or Bokeh for dynamic dashboards.
