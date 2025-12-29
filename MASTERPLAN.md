# Numerai Crypto - Individual Model Training for 504 Symbols
## Master Plan for New Thread

**Status**: Ready for implementation  
**Date**: 2025-12-29  
**Objective**: Train individual V6/V7 models for all 504 Numerai crypto symbols  
**Expected Outcome**: +50-100% improvement over baseline BTC-only model  

---

## Phase 1: Architecture Design

### Current State (Baseline)
- ✓ V6/V7 trained on BTC only
- ✓ Applied to all 504 symbols via heuristic
- ✗ No individual training per symbol
- Result: Generic signals for all assets

### Target State (Real)
- ✓ Individual V6 XGBoost model per symbol
- ✓ Individual V7 regime detection per symbol
- ✓ Symbol-specific feature engineering
- ✓ Time-series validation per symbol
- Result: Customized signals for each asset

### Implementation Strategy
```
504 Symbols
    ↓
Parallel Training (10-20 workers)
    ↓
Individual V6 Models (504)
Individual V7 Models (504)
    ↓
Inference Pipeline
    ↓
504 Predictions → CSV
    ↓
Numerai Upload
```

---

## Phase 2: Data Pipeline

### Per-Symbol Data Collection
```python
for symbol in SYMBOLS:  # 504 total
    # Fetch 2 years of price data
    prices = bybit.get_klines(symbol, interval="1D", limit=730)
    
    # Extract 50+ features (on-chain, microstructure, sentiment, technical)
    features = extract_features(prices)
    
    # Generate labels (next day return)
    labels = generate_labels(prices)
    
    # Store: data/{symbol}_features.pkl
    # Store: data/{symbol}_labels.pkl
```

### Feature Engineering (per symbol)
- **On-chain** (20 features): whale concentration, exchange flow, MVRV, SOPR, etc.
- **Microstructure** (20 features): funding rates, liquidations, bid-ask spread, etc.
- **Sentiment** (10 features): Fear & Greed, social volume, news sentiment
- **Technical** (10 features): RSI, MACD, Bollinger Bands, moving averages

**Total: 50+ features per symbol**

---

## Phase 3: Model Training Pipeline

### Per-Symbol Training
```python
# For each of 504 symbols:

1. Load data/{symbol}_features.pkl
2. Train XGBoost V6:
   - Split: 80% train, 20% validation
   - Hyperparameters: depth=8, lr=0.03, n_estimators=500
   - Early stopping on validation set
   
3. Train V7 Regime Detection:
   - HMM with 4 states: BULL, BEAR, RANGE, CRISIS
   - Detect regime based on volatility/momentum
   
4. Validate:
   - Correlation to meta-model
   - Win rate on validation set
   - Save best model
   
5. Store:
   - models/v6_{symbol}.pkl
   - models/v7_{symbol}.pkl
```

### Parallelization Strategy
```
504 symbols / 20 workers = 25 symbols per worker

Worker 1: BTC, ETH, XRP, SOL, ... (25 symbols)
Worker 2: ADA, DOGE, MATIC, LINK, ... (25 symbols)
...
Worker 20: (remaining 4 symbols)

Time per symbol: 30 seconds → 25 symbols = 12.5 minutes per worker
Total parallel time: ~15-20 minutes
```

---

## Phase 4: Inference & Submission

### Generate Predictions
```python
predictions = []

for symbol in SYMBOLS:  # 504
    # Load trained model
    v6 = load_model(f"models/v6_{symbol}.pkl")
    v7 = load_model(f"models/v7_{symbol}.pkl")
    
    # Get latest data
    prices = bybit.get_klines(symbol, interval="1D", limit=365)
    
    # Extract features
    features = extract_features(prices)
    
    # Predict
    v6_signal = v6.predict(features)
    v7_signal = v7.predict(features)
    
    # Ensemble (40% V6, 60% V7)
    final_signal = v6_signal * 0.4 + v7_signal * 0.6
    final_signal = clip(final_signal, 0.001, 0.999)
    
    predictions.append({
        'symbol': symbol,
        'signal': final_signal
    })

# Save CSV
pd.DataFrame(predictions).to_csv('numerai_submission.csv')
```

### CSV Format
```
symbol,signal
BTC,0.5732
ETH,0.6825
XRP,0.5094
...
BTR,0.4011
```

---

## Phase 5: Validation & Quality Assurance

### Per-Model Validation
- [ ] Feature correlation check
- [ ] Signal distribution (mean ~0.5, std ~0.1)
- [ ] Win rate on validation set (>50%)
- [ ] Correlation to meta-model (-0.3 to +0.3)

### Submission QA
- [ ] CSV format correct (symbol, signal)
- [ ] 504 rows total
- [ ] All signals in range [0.001, 0.999]
- [ ] No NaN/Inf values
- [ ] File size reasonable (~10-15KB)

---

## Phase 6: Upload & Monitor

### Manual Upload
1. Go to https://numerai.com/tournaments/crypto
2. Upload CSV file
3. Model ID: `e64d764d-301c-4ea8-9107-1fe7d5d6c39f`
4. Wait for scoring

### Track Performance
- Day 1-7: Initial correlation/MMC
- Week 2-4: Rank progression
- Month 2: Final evaluation vs CYCLOP (#1 baseline)

---

## Implementation Timeline

### Week 1
- **Day 1-2**: Setup data pipeline (2h)
- **Day 2-3**: Implement V6 training loop (3h)
- **Day 3-4**: Implement V7 regime detection (2h)
- **Day 4-5**: Parallel training all 504 (1h actual, 15m parallel)
- **Day 5-6**: Generate predictions & CSV (30m)
- **Day 7**: Upload & monitor (30m)

### Total: ~10-12 hours work
### Parallel execution: ~30 minutes

---

## Resource Requirements

### Compute
- CPU: 8+ cores (parallelization)
- RAM: 16GB minimum
- Storage: 10GB (models + data)
- Network: Bitget/Bybit API access

### Software
- Python 3.8+
- XGBoost, scikit-learn, pandas, numpy
- Optional: hmmlearn (regime detection)

### Time
- Development: 8-10 hours
- Training: 30 minutes (parallel)
- Inference: 5 minutes
- Upload: 2 minutes

---

## Risk Mitigation

### Potential Issues & Solutions

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Insufficient data for small symbols | Low quality models | Use synthetic data + transfer learning |
| API rate limits | Training stops | Implement queuing, retry logic |
| NaN/Inf in features | Invalid predictions | Robust scaling, fill missing values |
| Overfitting on validation | Poor real performance | Early stopping, cross-validation |
| High correlation between models | Less diversity | Add symbol-specific noise injection |

---

## Success Criteria

### Minimum Requirements (Go/No-Go)
- [ ] All 504 models train without errors
- [ ] CSV has valid format & 504 rows
- [ ] Mean signal: 0.45-0.55
- [ ] Std signal: 0.05-0.15
- [ ] No NaN/Inf values

### Target Performance
- [ ] Correlation to meta: -0.2 to +0.2
- [ ] Win rate: >52% on validation
- [ ] Rank improvement: +5-10 positions
- [ ] MMC: +0.04-0.08 vs baseline

### Stretch Goals
- [ ] Rank #1 within 8 weeks
- [ ] MMC 0.12-0.16
- [ ] Correlation 0.15-0.25

---

## File Structure

```
c:/hashtag1/
├── MASTERPLAN.md (this file)
├── PROGRESS.md (weekly updates)
├── DATA/
│   ├── symbols_list.txt (504 symbols)
│   ├── {symbol}_features.pkl (504 files)
│   └── {symbol}_labels.pkl (504 files)
├── MODELS/
│   ├── v6_{symbol}.pkl (504 files)
│   └── v7_{symbol}.pkl (504 files)
├── SCRIPTS/
│   ├── 1_fetch_data.py
│   ├── 2_train_models.py
│   ├── 3_generate_predictions.py
│   ├── 4_create_csv.py
│   └── 5_validate_csv.py
├── LOGS/
│   ├── training.log
│   ├── inference.log
│   └── validation.log
└── SUBMISSIONS/
    └── numerai_submission_final.csv
```

---

## Next Steps

### Immediate (Next Meeting)
1. [ ] Review & approve masterplan
2. [ ] Set up directory structure
3. [ ] Create data fetching script
4. [ ] Begin training on subset (50 symbols test)

### Week 1
1. [ ] Full training (504 symbols)
2. [ ] Validation & QA
3. [ ] Generate CSV
4. [ ] Upload to Numerai

### Week 2-8
1. [ ] Monitor daily performance
2. [ ] Adjust hyperparameters if needed
3. [ ] Track rank progression
4. [ ] Document learnings

---

## Key Metrics to Track

```
Per Symbol:
- Training samples: 730 (2 years)
- Validation samples: 100 (4 months)
- Features: 50+
- Training time: ~30 seconds
- Model size: ~10-50MB

Overall:
- Total training time: 30 minutes (parallel)
- Total inference time: 5 minutes
- CSV file size: ~12KB
- Expected improvement: +50-100%
```

---

## Contact & Support

**Thread**: New Amp thread (to be created)  
**Status**: Ready to start  
**Owner**: [Your name]  
**Last Updated**: 2025-12-29 00:30 UTC

---

## Approval Checklist

- [ ] Masterplan reviewed
- [ ] Resources allocated
- [ ] Timeline agreed
- [ ] Team ready to start
- [ ] Go/No-Go decision

**Ready to proceed**: YES ✓

---

*This masterplan is a living document. Updates will be tracked in PROGRESS.md*
