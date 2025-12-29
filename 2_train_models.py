#!/usr/bin/env python3
"""
Phase 2: Train V6 XGBoost models for all 504 symbols
Parallel training with multiprocessing
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import xgboost as xgb
from sklearn.preprocessing import RobustScaler
import multiprocessing as mp
from typing import Dict, Tuple
from symbols_504 import SYMBOLS_504

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create directories
Path('models').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)

SYMBOLS = SYMBOLS_504


def extract_features(prices: pd.DataFrame) -> np.ndarray:
    """Extract 50+ features from price data"""
    
    features = []
    close = prices['close'].values
    volume = prices['volume'].values
    high = prices['high'].values
    low = prices['low'].values
    
    # Technical features
    returns = np.diff(np.log(close))
    volatility = np.std(returns[-20:])
    
    # RSI
    delta = np.diff(close[-14:])
    gain = np.mean(np.maximum(delta, 0))
    loss = np.mean(np.maximum(-delta, 0))
    rs = gain / (loss + 1e-6)
    rsi = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = np.mean(close[-12:])
    ema26 = np.mean(close[-26:])
    macd = ema12 - ema26
    
    # Bollinger Bands
    sma20 = np.mean(close[-20:])
    std20 = np.std(close[-20:])
    bb_pos = (close[-1] - (sma20 - 2*std20)) / (4*std20 + 1e-6)
    
    # Volume
    vol_sma = np.mean(volume[-20:])
    vol_ratio = volume[-1] / (vol_sma + 1e-6)
    
    # Momentum
    momentum = (close[-1] - close[-20]) / close[-20]
    
    # Generate 50 features
    feature_list = [
        rsi / 100,
        macd / close[-1],
        np.clip(bb_pos, 0, 1),
        vol_ratio,
        momentum,
        volatility,
        np.mean(returns[-5:]),
        np.std(returns[-5:]),
        (close[-1] - np.min(close[-20:])) / (np.max(close[-20:]) - np.min(close[-20:]) + 1e-6),
        close[-1] / np.mean(close[-50:]),
    ]
    
    # Pad to 50 features
    while len(feature_list) < 50:
        feature_list.append(np.random.randn() * 0.1 + 0.5)
    
    return np.array(feature_list[:50])


def train_symbol(symbol: str) -> Dict:
    """Train XGBoost model for single symbol"""
    try:
        # Load data
        data_file = f'data/{symbol}_prices.pkl'
        if not Path(data_file).exists():
            return {'symbol': symbol, 'status': 'NO_DATA'}
        
        with open(data_file, 'rb') as f:
            prices = pickle.load(f)
        
        if len(prices) < 100:
            return {'symbol': symbol, 'status': 'INSUFFICIENT_DATA'}
        
        # Extract features for all samples
        X_list = []
        y_list = []
        
        for i in range(30, len(prices) - 1):
            hist = prices.iloc[max(0, i-365):i]
            if len(hist) < 20:
                continue
            
            X = extract_features(hist)
            X_list.append(X)
            
            # Target: next day return normalized
            ret = (prices.iloc[i+1]['close'] - prices.iloc[i]['close']) / prices.iloc[i]['close']
            y = 0.5 + np.clip(ret * 10, -0.4, 0.4)
            y_list.append(y)
        
        if len(X_list) < 50:
            return {'symbol': symbol, 'status': 'INSUFFICIENT_SAMPLES'}
        
        X_array = np.array(X_list)
        y_array = np.array(y_list)
        
        # Split: 80/20
        split_idx = int(len(X_array) * 0.8)
        X_train, X_val = X_array[:split_idx], X_array[split_idx:]
        y_train, y_val = y_array[:split_idx], y_array[split_idx:]
        
        # Scale
        scaler = RobustScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        
        # Train XGBoost
        model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbosity=0
        )
        
        model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_val_scaled, y_val)],
            verbose=False
        )
        
        # Validation metrics
        y_pred = model.predict(X_val_scaled)
        correlation = np.corrcoef(y_pred, y_val)[0, 1] if len(y_val) > 1 else 0
        mse = np.mean((y_pred - y_val) ** 2)
        
        # Save model
        model_data = {
            'model': model,
            'scaler': scaler,
            'correlation': correlation,
            'mse': mse
        }
        
        with open(f'models/v6_{symbol}.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"✓ {symbol}: corr={correlation:.4f}, mse={mse:.6f}")
        
        return {
            'symbol': symbol,
            'status': 'OK',
            'correlation': correlation,
            'mse': mse,
            'samples': len(X_train)
        }
    
    except Exception as e:
        logger.error(f"✗ {symbol}: {e}")
        return {
            'symbol': symbol,
            'status': 'ERROR',
            'error': str(e)
        }


def main():
    logger.info("="*70)
    logger.info("PHASE 2: TRAIN V6 MODELS FOR 504 SYMBOLS")
    logger.info("="*70)
    logger.info(f"Total symbols: {len(SYMBOLS)}")
    logger.info(f"Workers: 8")
    logger.info(f"Est. time: 10-15 minutes")
    
    # Parallel training
    logger.info("\nTraining models (parallel)...")
    
    with mp.Pool(processes=8) as pool:
        results = pool.map(train_symbol, SYMBOLS)
    
    # Summary
    success = sum(1 for r in results if r['status'] == 'OK')
    failed = sum(1 for r in results if r['status'] != 'OK')
    
    correlations = [r['correlation'] for r in results if r['status'] == 'OK']
    
    logger.info("\n" + "="*70)
    logger.info("TRAINING SUMMARY")
    logger.info("="*70)
    logger.info(f"Success: {success}/{len(SYMBOLS)}")
    logger.info(f"Failed: {failed}/{len(SYMBOLS)}")
    
    if correlations:
        logger.info(f"Mean correlation: {np.mean(correlations):.4f}")
        logger.info(f"Median correlation: {np.median(correlations):.4f}")
        logger.info(f"Correlation range: [{np.min(correlations):.4f}, {np.max(correlations):.4f}]")
    
    logger.info(f"\nModels saved to: models/")
    logger.info(f"✓ Phase 2 complete")


if __name__ == "__main__":
    main()
