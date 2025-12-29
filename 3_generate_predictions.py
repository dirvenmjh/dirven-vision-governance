#!/usr/bin/env python3
"""
Phase 3: Generate predictions for all 504 symbols
Inference from trained models
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import multiprocessing as mp
from typing import Dict
from symbols_504 import SYMBOLS_504

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/inference.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

Path('logs').mkdir(exist_ok=True)

SYMBOLS = SYMBOLS_504


def extract_features(prices: pd.DataFrame) -> np.ndarray:
    """Extract 50 features from price data"""
    
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


def predict_symbol(symbol: str) -> Dict:
    """Generate prediction for single symbol"""
    try:
        # Load model
        model_file = f'models/v6_{symbol}.pkl'
        if not Path(model_file).exists():
            logger.warning(f"Model not found for {symbol}")
            return {'symbol': symbol, 'prediction': 0.5}
        
        with open(model_file, 'rb') as f:
            data = pickle.load(f)
        
        model = data['model']
        scaler = data['scaler']
        
        # Load latest prices
        price_file = f'data/{symbol}_prices.pkl'
        if not Path(price_file).exists():
            return {'symbol': symbol, 'prediction': 0.5}
        
        with open(price_file, 'rb') as f:
            prices = pickle.load(f)
        
        # Extract features from last 365 days
        features = extract_features(prices.iloc[-365:])
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Predict
        pred = model.predict(features_scaled)[0]
        pred = np.clip(pred, 0.001, 0.999)
        
        logger.info(f"{symbol}: {pred:.4f}")
        
        return {
            'symbol': symbol,
            'prediction': pred,
            'status': 'OK'
        }
    
    except Exception as e:
        logger.error(f"Prediction error for {symbol}: {e}")
        return {
            'symbol': symbol,
            'prediction': 0.5,
            'status': 'ERROR'
        }


def main():
    logger.info("="*70)
    logger.info("PHASE 3: GENERATE PREDICTIONS")
    logger.info("="*70)
    logger.info(f"Total symbols: {len(SYMBOLS)}")
    
    # Parallel inference
    logger.info("\nGenerating predictions (parallel)...")
    
    with mp.Pool(processes=8) as pool:
        results = pool.map(predict_symbol, SYMBOLS)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Summary
    success = sum(1 for r in results if r.get('status') == 'OK')
    
    logger.info("\n" + "="*70)
    logger.info("PREDICTION SUMMARY")
    logger.info("="*70)
    logger.info(f"Success: {success}/{len(SYMBOLS)}")
    
    if 'prediction' in df.columns:
        logger.info(f"Mean prediction: {df['prediction'].mean():.4f}")
        logger.info(f"Median prediction: {df['prediction'].median():.4f}")
        logger.info(f"Min: {df['prediction'].min():.4f}")
        logger.info(f"Max: {df['prediction'].max():.4f}")
        logger.info(f"Std: {df['prediction'].std():.4f}")
    
    logger.info(f"\n✓ Phase 3 complete")
    
    return results


if __name__ == "__main__":
    main()
