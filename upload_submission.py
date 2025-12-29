#!/usr/bin/env python3
"""
Upload Numerai Crypto submission
Uses Numerai API with credentials from .env
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

try:
    from numerapi import CryptoAPI
except ImportError:
    os.system("pip install numerapi -q")
    from numerapi import CryptoAPI

# Setup logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Model config
MODEL_ID = 'e64d764d-301c-4ea8-9107-1fe7d5d6c39f'
SUBMISSION_FILE = 'numerai_submission_final.csv'


def upload_to_numerai(filepath: str, model_id: str) -> bool:
    """Upload submission to Numerai"""
    try:
        if not Path(filepath).exists():
            logger.error(f"File not found: {filepath}")
            return False
        
        api = CryptoAPI()
        
        logger.info(f"Uploading {filepath}...")
        logger.info(f"Model ID: {model_id}")
        
        # Upload
        result = api.upload_predictions(
            file_path=filepath,
            model_id=model_id
        )
        
        logger.info(f"Success! Response: {result}")
        return True
    
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return False


def main():
    logger.info("="*70)
    logger.info("NUMERAI CRYPTO SUBMISSION UPLOAD")
    logger.info("="*70)
    
    try:
        success = upload_to_numerai(SUBMISSION_FILE, MODEL_ID)
        
        if success:
            logger.info("Upload complete!")
            return 0
        else:
            logger.error("Upload failed!")
            return 1
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
