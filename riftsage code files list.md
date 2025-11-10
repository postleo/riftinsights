


## **Other Code Files Needed for Fully Functional Production-Ready Riftsage AI Agent**:

### **Lambda Function Code Files** (Python 3.11)

1. **`data_collection.py`**
   - Fetches match history from Riot API
   - Handles rate limiting and caching
   - Stores raw data in S3

2. **`feature_engineering.py`**
   - Transforms raw match data into ML features
   - Calculates derived metrics (KDA, CS/min, etc.)
   - Handles outliers and missing data

3. **`model_inference.py`**
   - Loads trained ML models from S3
   - Applies models to player data
   - Generates classifications and predictions

4. **`bedrock_generation.py`**
   - Constructs prompts from player data
   - Calls Amazon Bedrock API
   - Validates and stores generated insights

5. **`report_compilation.py`**
   - Assembles sections into complete report
   - Generates JSON, PDF, and social assets
   - Creates presigned S3 URLs

### **Model Training Scripts**

6. **`train_models.py`**
   - Annual batch training for 4 ML models
   - Validation and performance testing
   - Model artifact storage

### **Utility Modules**

7. **`riot_api_client.py`**
   - Wrapper for Riot API calls
   - Rate limit management
   - Error handling and retries

8. **`data_validators.py`**
   - Input validation functions
   - Data quality checks
   - Schema validation

9. **`prompt_builder.py`**
   - Constructs Bedrock prompts from templates
   - Injects player data
   - Version management

10. **`metrics_calculator.py`**
    - Calculates all 37 tracked metrics
    - Benchmark comparisons
    - Percentile rankings

### **Configuration Files**

11. **`config.yaml`**
    - Environment-specific settings
    - API endpoints and keys
    - Model parameters

12. **`champion_database.json`**
    - Initial champion metadata
    - Performance statistics
    - Fit explanations

13. **`prompt_templates/`** (Directory)
    - Separate template file for each section
    - Versioned templates for A/B testing

### **Deployment Scripts**

14. **`deploy.sh`**
    - Packages Lambda functions
    - Uploads to S3
    - Deploys CloudFormation stack

15. **`requirements.txt`**
    - Python dependencies for Lambda functions
    - Specific versions for reproducibility

### **Testing Files**

16. **`test_data_collection.py`**
17. **`test_feature_engineering.py`**
18. **`test_model_inference.py`**
19. **`test_bedrock_generation.py`**
20. **`test_integration.py`**
    - Unit and integration tests
    - Mock data fixtures
    - Performance benchmarks

### **Documentation Files**

21. **`README.md`** - Project overview and quick start
22. **`DEPLOYMENT.md`** - Detailed deployment guide
23. **`API_REFERENCE.md`** - Complete API documentation
24. **`ERROR_CODES.md`** - Error code catalog
25. **`DEVELOPMENT.md`** - Local development setup
26. **`AWS_STACK.md`** - list of all the aws resources created and used and their costs

### **Database Seed Data**

27. **`seed_champions.py`**
    - Populates ChampionRecommendationsTable
    - Updates with patch data

28. **`seed_benchmarks.py`**
    - Populates rank average data
    - Climb correlation coefficients

