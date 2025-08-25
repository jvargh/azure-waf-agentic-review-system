# 🧪 **Sample Data for Azure Well-Architected Review System**

This directory contains comprehensive sample data for testing the Enhanced Azure Well-Architected Review System.

## 📁 **Directory Structure**

```
sample_data/
├── README.md                          # This file - Overview and usage guide
├── architecture_document.txt          # Sample architecture document for upload
├── azure_support_cases.csv           # Sample CSV for reactive case analysis
└── sample_architecture_images/        # Directory for architecture diagram samples
    └── README_IMAGES.md               # Guide for image samples and testing
```

## 📄 **Sample Files Overview**

### 1. **Architecture Document** (`architecture_document.txt`)
- **Type**: Text document for architecture analysis
- **Content**: Comprehensive e-commerce platform architecture on Azure
- **Services Covered**: 25+ Azure services across all Well-Architected pillars
- **Use Case**: Test document upload and enhanced multi-agent analysis
- **Size**: ~8KB comprehensive architecture documentation

**Key Features Tested**:
- Multi-tier architecture patterns
- Microservices design
- Security implementations
- High availability setup
- Cost optimization strategies
- Operational excellence practices

### 2. **Support Cases CSV** (`azure_support_cases.csv`)
- **Type**: CSV file for reactive case analysis
- **Content**: 21 realistic Azure support cases
- **Services Covered**: AKS, SQL Database, Storage, Functions, Key Vault, etc.
- **Use Case**: Test reactive case pattern analysis and Well-Architected violations
- **Patterns**: Authentication issues, performance problems, cost overruns, security incidents

**Key Patterns Identified**:
- Authentication failures (RBAC, certificates)
- Performance degradation (indexing, scaling)
- Cost optimization issues (wrong storage tiers)
- Security vulnerabilities (WAF, access policies)
- Operational challenges (monitoring, alerting)

### 3. **Architecture Images** (`sample_architecture_images/`)
- **Type**: Directory for architecture diagram images
- **Content**: Guidelines and descriptions for image samples
- **Formats**: PNG, JPG, SVG supported
- **Use Case**: Test image analysis and service detection capabilities

## 🚀 **How to Use These Samples**

### **Quick Start Testing**

1. **Upload Architecture Document**:
   ```bash
   # Via API
   curl -X POST "http://localhost:8000/api/assessments/{id}/documents" \
        -F "file=@sample_data/architecture_document.txt"
   
   # Via UI: Use the "Upload Documents" section
   ```

2. **Upload Reactive Cases CSV**:
   ```bash
   # Via API
   curl -X POST "http://localhost:8000/api/assessments/{id}/reactive-analysis" \
        -F "file=@sample_data/azure_support_cases.csv"
   
   # Via UI: Use the "Reactive Case Analysis" upload area
   ```

3. **Upload Architecture Images**:
   - Place your architecture diagrams in `sample_architecture_images/`
   - Upload via the image upload interface
   - System will detect Azure services and generate documentation

### **Complete Testing Workflow**

1. **Create New Assessment**:
   - Name: "Sample E-commerce Platform Review"
   - Description: "Testing enhanced analysis with sample data"

2. **Upload All Sample Data**:
   - Architecture document (required)
   - Support cases CSV (optional but recommended)
   - Architecture images (optional)

3. **Start Enhanced Analysis**:
   - Click "Start Analysis"
   - Monitor progress through all 5 pillars
   - Enhanced agents will analyze with sophisticated algorithms

4. **Review Enhanced Results**:
   - Overall score with 20+ sub-categories
   - Enhanced recommendations with business impact
   - Reactive insights from support case patterns
   - Service detection from images

## 📊 **Expected Results**

### **Analysis Quality**:
- **Overall Score**: ~65-70% (realistic scoring)
- **Sub-categories**: 20+ across 5 pillars (4-5 per pillar)
- **Recommendations**: 10+ with business impact and cost estimates
- **Detected Services**: 15-20 Azure services from combined inputs

### **Enhanced Features Demonstrated**:
- **Context-aware scoring** based on detected services
- **Cross-pillar collaboration** between agents
- **Reactive recommendations** from support case patterns
- **Professional recommendations** with implementation details

### **Sample Pillar Breakdown**:
- **Reliability**: 72.5% (High Availability, Disaster Recovery, Fault Tolerance, Backup Strategy, Reliability Monitoring)
- **Security**: 68.0% (Identity & Access, Data Protection, Network Security, Security Monitoring, Compliance)
- **Cost Optimization**: 55.5% (Resource Optimization, Cost Monitoring, Reserved Instances, Right-sizing)
- **Operational Excellence**: 78.0% (Monitoring, DevOps Practices, Automation, Documentation)
- **Performance Efficiency**: 64.5% (Scalability, Load Testing, Caching Strategy, Database Performance)

## 🔧 **Configuration for Testing**

Ensure your `.env` file is configured for enhanced testing:

```env
# Enhanced Emulated Mode (Current)
LLM_MODE="emulated"
ENHANCED_EMULATION="true"
RESPONSE_SOPHISTICATION="high"

# Real LLM Mode (When ready)
# LLM_MODE="real"
# OPENAI_API_KEY="your-openai-api-key-here"
```

## 🎯 **Testing Scenarios**

### **Scenario 1: Basic Enhanced Analysis**
- Upload only `architecture_document.txt`
- Verify 20+ sub-categories and enhanced recommendations

### **Scenario 2: Reactive Case Analysis**
- Upload both document and CSV
- Verify reactive recommendations based on support patterns
- Check risk assessment and violation detection

### **Scenario 3: Multi-Modal Analysis**
- Upload document, CSV, and architecture images
- Verify comprehensive analysis with all data sources
- Check service detection and cross-referencing

### **Scenario 4: Real LLM Comparison**
- Test with enhanced emulated mode first
- Switch to real LLM mode (with API key)
- Compare analysis quality and recommendations

## 📈 **Performance Expectations**

### **Enhanced Emulated Mode**:
- **Analysis Time**: ~10-15 seconds total
- **Progress Updates**: Real-time through 5 pillars
- **Consistency**: Same results for same inputs
- **Cost**: $0 (no API calls)

### **Real LLM Mode**:
- **Analysis Time**: ~30-60 seconds total
- **Progress Updates**: Real-time with actual AI processing
- **Variability**: Different insights on each run
- **Cost**: ~$0.50-2.00 per analysis (depending on content size)

## 🚀 **Next Steps**

1. **Test with Sample Data**: Use these files to verify system functionality
2. **Create Your Own**: Develop custom architecture documents and cases
3. **Real Integration**: Switch to real LLM mode when ready
4. **Production Use**: Deploy with confidence knowing the system works

## 📞 **Support**

If you encounter issues with the sample data:
1. Check file formats and sizes
2. Verify API endpoints are accessible
3. Review enhanced system configuration
4. Test with smaller samples first

These samples provide comprehensive testing coverage for all enhanced features of the Azure Well-Architected Review System!